<#
.SYNOPSIS
Contract tests for llm_workflow session-handoff hooks (DES-01..DES-04).
Feeds sample hook-input JSON via stdin to each hook script and checks the
stdout contract (additionalContext JSON or silence) plus state-file effects.
ASCII-only by design: PS 5.1 misreads BOM-less UTF-8 script literals.
#>

$ErrorActionPreference = 'Stop'

$hooksDir = Split-Path $PSScriptRoot
$script:passCount = 0
$script:failCount = 0

function Assert-True([bool]$Condition, [string]$Name) {
    if ($Condition) { $script:passCount++; Write-Host "[pass] $Name" }
    else { $script:failCount++; Write-Host "[FAIL] $Name" }
}

function New-TestDir([string]$Name) {
    $p = Join-Path $env:TEMP "wf-hook-tests\$Name"
    if (Test-Path $p) { Remove-Item -Recurse -Force $p }
    New-Item -ItemType Directory -Force $p | Out-Null
    return $p
}

function New-WorkLog([string]$Root, [string]$TaskId, [string]$Status) {
    $dir = Join-Path $Root "docs\work\$TaskId"
    New-Item -ItemType Directory -Force $dir | Out-Null
    $lines = @(
        "# WORK-${TaskId}: test log",
        "",
        "> Doc type: ``work-log``",
        "> Task ID: ``$TaskId``",
        "> Status: ``$Status``",
        ""
    )
    Set-Content -Path (Join-Path $dir 'work-log.md') -Value $lines -Encoding UTF8
}

function New-Transcript([string]$Dir, [int]$SizeKB) {
    $p = Join-Path $Dir 'transcript.jsonl'
    [IO.File]::WriteAllBytes($p, (New-Object byte[] ($SizeKB * 1024)))
    return $p
}

function Get-StateFile([string]$SessionId) {
    return Join-Path $env:TEMP "claude-wf\$SessionId.json"
}

function Invoke-Hook([string]$ScriptName, [hashtable]$HookInput) {
    $json = $HookInput | ConvertTo-Json -Compress
    $scriptPath = Join-Path $hooksDir $ScriptName
    # No stderr redirect: PS 5.1 wraps redirected native stderr into ErrorRecords,
    # which $ErrorActionPreference='Stop' would promote to a terminating error.
    $out = @($json | & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $scriptPath) -join "`n"
    return [string]$out
}

# Clean state from previous runs; ensure the state dir exists for fixtures
$stateDir = Join-Path $env:TEMP 'claude-wf'
New-Item -ItemType Directory -Force $stateDir | Out-Null
Get-ChildItem $stateDir -Filter 'wf-test-*.json' | Remove-Item -Force
Remove-Item Env:\CLAUDE_WF_THRESHOLD_KB -ErrorAction SilentlyContinue
Remove-Item Env:\CLAUDE_WF_REWARN_KB -ErrorAction SilentlyContinue

try {

# ---------- wf-session-start.ps1 ----------

# T01: open work-log -> inject resume context listing it; baseline recorded
$ws = New-TestDir 'ss-open'
New-WorkLog $ws '20990101-open' 'in-progress'
$t = New-Transcript $ws 10
$out = Invoke-Hook 'wf-session-start.ps1' @{ session_id='wf-test-ss1'; transcript_path=$t; cwd=$ws; hook_event_name='SessionStart'; source='startup' }
Assert-True ($out -match 'hookSpecificOutput' -and $out -match '20990101-open') 'T01 session-start injects resume context for open work-log'
$state = Get-StateFile 'wf-test-ss1'
$baselineOk = $false
if (Test-Path $state) { $baselineOk = ((Get-Content $state -Raw | ConvertFrom-Json).baselineBytes -eq 10240) }
Assert-True $baselineOk 'T02 session-start records transcript baseline in state file'

# T03: only closed work-logs -> silent, but baseline still recorded
$ws = New-TestDir 'ss-closed'
New-WorkLog $ws '20990102-done' 'completed'
$t = New-Transcript $ws 5
$out = Invoke-Hook 'wf-session-start.ps1' @{ session_id='wf-test-ss2'; transcript_path=$t; cwd=$ws; hook_event_name='SessionStart'; source='startup' }
Assert-True ($out -eq '') 'T03 session-start silent when all work-logs closed'
Assert-True (Test-Path (Get-StateFile 'wf-test-ss2')) 'T04 session-start still records baseline without open work'

# T05: no docs/work -> fully silent, no state file (FR-05 guard)
$ws = New-TestDir 'ss-guard'
$t = New-Transcript $ws 5
$out = Invoke-Hook 'wf-session-start.ps1' @{ session_id='wf-test-ss3'; transcript_path=$t; cwd=$ws; hook_event_name='SessionStart'; source='startup' }
Assert-True ($out -eq '' -and -not (Test-Path (Get-StateFile 'wf-test-ss3'))) 'T05 session-start no-op without docs/work (guard)'

# T06: malformed stdin -> fail-open (silent, exit 0)
$scriptPath = Join-Path $hooksDir 'wf-session-start.ps1'
$out = @('this is not json' | & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $scriptPath) -join "`n"
Assert-True ($out -eq '' -and $LASTEXITCODE -eq 0) 'T06 session-start fail-open on malformed input'

# ---------- wf-context-threshold.ps1 ----------

$env:CLAUDE_WF_THRESHOLD_KB = '50'
$env:CLAUDE_WF_REWARN_KB = '50'

# T07: no state file yet -> silent, creates baseline at current size
$ws = New-TestDir 'th-nostate'
New-WorkLog $ws '20990103-open' 'in-progress'
$t = New-Transcript $ws 100
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th1'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
$state = Get-StateFile 'wf-test-th1'
$baselineOk = $false
if (Test-Path $state) { $baselineOk = ((Get-Content $state -Raw | ConvertFrom-Json).baselineBytes -eq 102400) }
Assert-True ($out -eq '' -and $baselineOk) 'T07 threshold bootstraps baseline silently when state missing'

# T08: growth below threshold -> silent
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th1'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -eq '') 'T08 threshold silent below threshold (no growth)'

# T09: growth above threshold -> inject once
[IO.File]::WriteAllBytes($t, (New-Object byte[] (160 * 1024)))   # +60KB > 50KB
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th1'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -match 'hookSpecificOutput') 'T09 threshold injects when growth exceeds threshold'

# T10: same size again -> suppressed by rewarn interval
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th1'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -eq '') 'T10 threshold re-warn suppressed without further growth'

# T11: grow past rewarn interval -> inject again
[IO.File]::WriteAllBytes($t, (New-Object byte[] (220 * 1024)))   # +60KB > rewarn 50KB
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th1'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -match 'hookSpecificOutput') 'T11 threshold re-warns after rewarn interval'

# T12: missing transcript -> fail-open silent
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th2'; transcript_path=(Join-Path $ws 'missing.jsonl'); cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -eq '') 'T12 threshold fail-open when transcript missing'

# T13: no docs/work -> silent even with huge growth (FR-05 guard)
$ws2 = New-TestDir 'th-guard'
$t2 = New-Transcript $ws2 500
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th3'; transcript_path=$t2; cwd=$ws2; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -eq '') 'T13 threshold no-op without docs/work (guard)'

# ---------- wf-post-compact.ps1 ----------

# T14: open work-log -> inject re-anchor message, reset baseline to current size
$ws = New-TestDir 'pc-open'
New-WorkLog $ws '20990104-open' 'in-progress'
$t = New-Transcript $ws 300
Set-Content -Path (Get-StateFile 'wf-test-pc1') -Value '{"baselineBytes":0,"lastWarnedBytes":102400,"updatedAt":"x"}' -Encoding UTF8
$out = Invoke-Hook 'wf-post-compact.ps1' @{ session_id='wf-test-pc1'; transcript_path=$t; cwd=$ws; hook_event_name='SessionStart'; source='compact' }
$state = Get-Content (Get-StateFile 'wf-test-pc1') -Raw | ConvertFrom-Json
Assert-True ($out -match 'hookSpecificOutput') 'T14 post-compact injects re-anchor context for open work'
Assert-True ($state.baselineBytes -eq 307200 -and $null -eq $state.lastWarnedBytes) 'T15 post-compact resets baseline and clears lastWarned'

# T16: no open work-log -> silent, baseline still reset
$ws = New-TestDir 'pc-closed'
New-WorkLog $ws '20990105-done' 'completed'
$t = New-Transcript $ws 40
$out = Invoke-Hook 'wf-post-compact.ps1' @{ session_id='wf-test-pc2'; transcript_path=$t; cwd=$ws; hook_event_name='SessionStart'; source='compact' }
$baselineOk = $false
$sf = Get-StateFile 'wf-test-pc2'
if (Test-Path $sf) { $baselineOk = ((Get-Content $sf -Raw | ConvertFrom-Json).baselineBytes -eq 40960) }
Assert-True ($out -eq '' -and $baselineOk) 'T16 post-compact silent without open work but resets baseline'

# T17: no docs/work -> full no-op (FR-05 guard)
$ws = New-TestDir 'pc-guard'
$t = New-Transcript $ws 40
$out = Invoke-Hook 'wf-post-compact.ps1' @{ session_id='wf-test-pc3'; transcript_path=$t; cwd=$ws; hook_event_name='SessionStart'; source='compact' }
Assert-True ($out -eq '' -and -not (Test-Path (Get-StateFile 'wf-test-pc3'))) 'T17 post-compact no-op without docs/work (guard)'

# ---------- install-hooks.ps1 ----------

$installPath = Join-Path $hooksDir 'install-hooks.ps1'
if (Test-Path $installPath) { . $installPath }
else {
    Assert-True $false 'T18 fresh install registers 2 SessionStart + 1 PostToolUse entries'
    Assert-True $false 'T19 rerun does not duplicate entries'
    Assert-True $false 'T20 foreign settings and hooks preserved alongside ours'
    Assert-True $false 'T21 stale wf entries retargeted to current hooks dir'
}
if (Test-Path $installPath) {

function Get-WfEntryCounts([string]$Path) {
    $s = Get-Content $Path -Raw -Encoding UTF8 | ConvertFrom-Json
    $ss = @(); $pt = @()
    if ($s.hooks -and $s.hooks.SessionStart) { $ss = @($s.hooks.SessionStart) }
    if ($s.hooks -and $s.hooks.PostToolUse)  { $pt = @($s.hooks.PostToolUse) }
    return @{ SessionStart = $ss.Count; PostToolUse = $pt.Count; Parsed = $s }
}

# T18: fresh install creates settings with 2 SessionStart entries + 1 PostToolUse entry
$dir = New-TestDir 'inst-fresh'
$settings = Join-Path $dir 'settings.json'
Install-WfHooks -SettingsPath $settings -HooksDir $hooksDir
$c = Get-WfEntryCounts $settings
Assert-True ($c.SessionStart -eq 2 -and $c.PostToolUse -eq 1) 'T18 fresh install registers 2 SessionStart + 1 PostToolUse entries'

# T19: rerun is idempotent
Install-WfHooks -SettingsPath $settings -HooksDir $hooksDir
$c = Get-WfEntryCounts $settings
Assert-True ($c.SessionStart -eq 2 -and $c.PostToolUse -eq 1) 'T19 rerun does not duplicate entries'

# T20: foreign settings and foreign hooks preserved
$dir = New-TestDir 'inst-foreign'
$settings = Join-Path $dir 'settings.json'
$foreign = '{"model":"opus","hooks":{"SessionStart":[{"matcher":"startup","hooks":[{"type":"command","command":"echo","args":["hi"]}]}]}}'
Set-Content -Path $settings -Value $foreign -Encoding UTF8
Install-WfHooks -SettingsPath $settings -HooksDir $hooksDir
$c = Get-WfEntryCounts $settings
$foreignKept = ($c.Parsed.model -eq 'opus') -and @(@($c.Parsed.hooks.SessionStart) | Where-Object { $_.hooks[0].command -eq 'echo' }).Count -eq 1
Assert-True ($foreignKept -and $c.SessionStart -eq 3) 'T20 foreign settings and hooks preserved alongside ours'

# T21: stale entry pointing at old repo path is retargeted, not duplicated
$staleJson = Get-Content $settings -Raw -Encoding UTF8
$staleJson = $staleJson.Replace($hooksDir.Replace('\', '\\'), 'C:\\old-repo\\setup\\hooks')
Set-Content -Path $settings -Value $staleJson -Encoding UTF8
Install-WfHooks -SettingsPath $settings -HooksDir $hooksDir
$c = Get-WfEntryCounts $settings
$hasOld = (Get-Content $settings -Raw -Encoding UTF8) -match 'old-repo'
Assert-True ($c.SessionStart -eq 3 -and $c.PostToolUse -eq 1 -and -not $hasOld) 'T21 stale wf entries retargeted to current hooks dir'
}


# ---------- wf-common.ps1 gate helpers (TASK-37) ----------

# Korean tokens are built from code points: this file is ASCII-only by design
# (see header), but the obligation table it parses is Korean.
$kKeep    = [string][char]0xC720 + [char]0xC9C0                       # keep
$kHold    = [string][char]0xBCF4 + [char]0xB958                       # hold
$kSection = '## ' + [char]0xD68C + [char]0xADC0 + ' ' + [char]0xC758 + [char]0xBB34 + ' ' + [char]0xBAA9 + [char]0xB85D

function New-GateFile([string]$Dir, [string[]]$Body) {
    $p = Join-Path $Dir 'quality-gates.md'
    Set-Content -Path $p -Value $Body -Encoding UTF8
    return $p
}

function New-ObligationLog([string]$Dir, [string[]]$SectionBody) {
    $p = Join-Path $Dir 'work-log.md'
    $lines = @('# WORK-test: log', '', '> Status: ``in-progress``', '') + $SectionBody
    Set-Content -Path $p -Value $lines -Encoding UTF8
    return $p
}

. (Join-Path $hooksDir 'wf-common.ps1')

# T22: global fence parses "name = command", splits on the FIRST '=' so Windows
# paths and flags containing '=' survive; comments and non-fence lines ignored.
$dir = New-TestDir 'gate-fence'
$f = New-GateFile $dir @(
    '# Quality gates',
    'prose line = not a gate',
    '```gates',
    '# comment',
    'lint = cmd /c exit 0',
    'secrets = gitleaks detect --no-git --source . --exit-code 2',
    '',
    '```',
    'trailing = also not a gate'
)
$g = Get-WfGateLines $f
$ok = $g.Count -eq 2 -and
      $g[0].Name -eq 'lint' -and $g[0].Command -eq 'cmd /c exit 0' -and
      $g[1].Name -eq 'secrets' -and $g[1].Command -eq 'gitleaks detect --no-git --source . --exit-code 2'
Assert-True $ok 'T22 gate fence parser reads name = command and ignores non-fence lines'

# T23: obligation table yields only rows whose status column is "keep".
$dir = New-TestDir 'gate-oblig'
$log = New-ObligationLog $dir @(
    $kSection,
    '',
    '| TASK | test | scope | last | status | note |',
    '|---|---|---|---|---|---|',
    "| TASK-37 | ``cmd /c exit 0`` | wf-common.ps1 | 2026-09-20 . abc123 | $kKeep | AC-01 |",
    "| TASK-38 | ``cmd /c exit 1`` | wf-stop-gate.ps1 | - | $kHold | not deterministic yet |",
    "| TASK-39 | ``cmd /c exit 0`` | install-hooks.ps1 | 2026-09-20 . abc123 | $kKeep | AC-07 |",
    '',
    '## next section',
    "| TASK-99 | ``cmd /c exit 0`` | elsewhere | - | $kKeep | outside the section |"
)
$o = Get-WfObligationGates $log
$ok = $o.Count -eq 2 -and
      $o[0].Name -eq 'TASK-37' -and $o[0].Command -eq 'cmd /c exit 0' -and
      $o[1].Name -eq 'TASK-39'
Assert-True $ok 'T23 obligation parser returns only keep rows within its own section'

# T24: sections that carry prose instead of a table (cycle 1 work-log) and logs
# with no obligation section at all (20260814-multiuser-workflow) yield nothing.
$dir = New-TestDir 'gate-prose'
$proseLog = New-ObligationLog $dir @($kSection, '', 'no tests to keep - all changes are prose.', '')
$dir2 = New-TestDir 'gate-nosection'
$plainLog = New-ObligationLog $dir2 @('## other', '', 'nothing here', '')
$ok = ((Get-WfObligationGates $proseLog).Count -eq 0) -and
      ((Get-WfObligationGates $plainLog).Count -eq 0) -and
      ((Get-WfObligationGates (Join-Path $dir2 'missing.md')).Count -eq 0)
Assert-True $ok 'T24 obligation parser tolerates prose-only section, missing section and missing file'

# T25: outside a git work tree the citation key is unavailable, so the gate must
# run every time (DES-03) rather than treat "no key" as "unchanged".
$dir = New-TestDir 'gate-nogit'
Assert-True ($null -eq (Get-WfTreeKey $dir)) 'T25 tree key is null outside a git work tree'

# T26: inside a repo the key is stable for an unchanged tree and moves when the
# working tree changes - uncommitted edits included.
$dir = New-TestDir 'gate-git'
Push-Location $dir
try {
    & git init -q . 2>&1 | Out-Null
    Set-Content -Path (Join-Path $dir 'a.txt') -Value 'one' -Encoding ASCII
    & git add -A 2>&1 | Out-Null
    & git -c user.email=t@t -c user.name=t commit -qm init 2>&1 | Out-Null
    $k1 = Get-WfTreeKey $dir
    $k2 = Get-WfTreeKey $dir
    Set-Content -Path (Join-Path $dir 'a.txt') -Value 'two' -Encoding ASCII
    $k3 = Get-WfTreeKey $dir
} finally { Pop-Location }
$ok = $k1 -and ($k1 -eq $k2) -and ($k1 -ne $k3)
Assert-True $ok 'T26 tree key is stable for an unchanged tree and changes on a working-tree edit'


# ---------- wf-stop-gate.ps1 (TASK-38) ----------

function Get-GateStateFile([string]$SessionId) {
    return Join-Path $env:TEMP "claude-wf\$SessionId-gate.json"
}

# Builds a fixture repo: one open work-log (optionally carrying an obligation
# table) plus an optional repo-global gate fence.
function New-GateRepo([string]$Name, [string[]]$FenceLines, [string[]]$Rows) {
    $root = New-TestDir $Name
    $wl = Join-Path $root 'docs\work\20990101-open'
    New-Item -ItemType Directory -Force $wl | Out-Null
    $lines = @('# WORK-20990101-open: test log', '', '> Status: ``in-progress``', '')
    if ($Rows) {
        $lines += @($kSection, '',
            '| TASK | test | scope | last | status | note |',
            '|---|---|---|---|---|---|') + $Rows + @('')
    }
    Set-Content -Path (Join-Path $wl 'work-log.md') -Value $lines -Encoding UTF8
    if ($FenceLines) {
        $docs = Join-Path $root 'docs'
        Set-Content -Path (Join-Path $docs 'quality-gates.md') `
            -Value (@('# Quality gates', '', '```gates') + $FenceLines + @('```')) -Encoding UTF8
    }
    return $root
}

Remove-Item Env:\CLAUDE_WF_GATE_DISABLE -ErrorAction SilentlyContinue
Remove-Item Env:\CLAUDE_WF_GATE_TIMEOUT_SEC -ErrorAction SilentlyContinue
Get-ChildItem $stateDir -Filter 'wf-test-*-gate.json' -ErrorAction SilentlyContinue | Remove-Item -Force

# T27 (AC-01): a failing gate blocks, and the reason names the gate.
$root = New-GateRepo 'gate-block' @('lint = cmd /c exit 3') $null
$out = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g1'; cwd=$root; hook_event_name='Stop' }
Assert-True ($out -match '"decision"\s*:\s*"block"' -and $out -match 'lint') 'T27 stop gate blocks on a failing gate and names it'

# T28 (AC-02): every gate passing means silence - Stop must stay invisible.
$root = New-GateRepo 'gate-pass' @('ok = cmd /c exit 0') $null
$out = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g2'; cwd=$root; hook_event_name='Stop' }
Assert-True ($out -eq '') 'T28 stop gate is silent when every gate passes'

# T29 (AC-03): sources add up (global fence + obligation), and rows that are not
# "keep" never run - the determinism filter lives in the status column.
$root = New-GateRepo 'gate-union' @('g1 = copy /y nul g1.txt') @(
    "| TASK-01 | ``copy /y nul g2.txt`` | scope | - | $kKeep | keep |",
    "| TASK-02 | ``copy /y nul g3.txt`` | scope | - | $kHold | hold |"
)
$null = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g3'; cwd=$root; hook_event_name='Stop' }
$ok = (Test-Path (Join-Path $root 'g1.txt')) -and (Test-Path (Join-Path $root 'g2.txt')) -and
      -not (Test-Path (Join-Path $root 'g3.txt'))
Assert-True $ok 'T29 gate set is the union of fence and keep rows, excluding held rows'

# T30 (AC-04): a missing command (cmd 9009) is an infrastructure event, not a
# failure - an uninstalled tool must not block every turn.
$root = New-GateRepo 'gate-9009' @('missing = wf-no-such-command-xyz') $null
$out = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g4'; cwd=$root; hook_event_name='Stop' }
$st = Get-GateStateFile 'wf-test-g4'
$infra = 0
if (Test-Path $st) { $infra = (Get-Content $st -Raw -Encoding UTF8 | ConvertFrom-Json).infraCount }
Assert-True ($out -eq '' -and $infra -ge 1) 'T30 missing command passes as infrastructure and increments the counter'

# T31 (AC-04): a gate that outlives its budget is killed and counted, not
# treated as a failure (Q-04: a slow machine must not lose trust in the gate).
$root = New-GateRepo 'gate-timeout' @('slow = ping -n 6 127.0.0.1') $null
$env:CLAUDE_WF_GATE_TIMEOUT_SEC = '1'
$out = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g5'; cwd=$root; hook_event_name='Stop' }
Remove-Item Env:\CLAUDE_WF_GATE_TIMEOUT_SEC -ErrorAction SilentlyContinue
$st = Get-GateStateFile 'wf-test-g5'
$infra = 0
if (Test-Path $st) { $infra = (Get-Content $st -Raw -Encoding UTF8 | ConvertFrom-Json).infraCount }
Assert-True ($out -eq '' -and $infra -ge 1) 'T31 timeout passes as infrastructure and increments the counter'

# T32 (AC-05): an unchanged tree cites the last pass instead of re-running. The
# marker lives outside the repo so that observing the run does not itself change
# the tree key.
$marker = Join-Path $env:TEMP 'wf-cite-marker.txt'
Remove-Item $marker -ErrorAction SilentlyContinue
$root = New-GateRepo 'gate-cite' @('cite = copy /y nul "%TEMP%\wf-cite-marker.txt"') $null
Push-Location $root
try {
    & git init -q . 2>&1 | Out-Null
    & git add -A 2>&1 | Out-Null
    & git -c user.email=t@t -c user.name=t commit -qm init 2>&1 | Out-Null
} finally { Pop-Location }
$null = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g6'; cwd=$root; hook_event_name='Stop' }
$firstRan = Test-Path $marker
Remove-Item $marker -ErrorAction SilentlyContinue
$null = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g6'; cwd=$root; hook_event_name='Stop' }
$secondRan = Test-Path $marker
Assert-True ($firstRan -and -not $secondRan) 'T32 an unchanged tree key cites the last pass instead of re-running'

# T33 (AC-06): every escape hatch passes, and a repo that does not use the
# workflow leaves no state file at all (FR-05 guard, same contract as T05).
$root = New-GateRepo 'gate-guards' @('lint = cmd /c exit 3') $null
$a = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g7'; cwd=$root; hook_event_name='Stop'; stop_hook_active=$true }
$env:CLAUDE_WF_GATE_DISABLE = '1'
$b = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g8'; cwd=$root; hook_event_name='Stop' }
Remove-Item Env:\CLAUDE_WF_GATE_DISABLE -ErrorAction SilentlyContinue
$closed = New-TestDir 'gate-closed'
New-WorkLog $closed '20990101-done' 'completed'
Set-Content -Path (Join-Path $closed 'docs\quality-gates.md') -Value @('```gates', 'lint = cmd /c exit 3', '```') -Encoding UTF8
$c = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g9'; cwd=$closed; hook_event_name='Stop' }
$bare = New-TestDir 'gate-bare'
$d = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g10'; cwd=$bare; hook_event_name='Stop' }
$ok = ($a -eq '') -and ($b -eq '') -and ($c -eq '') -and ($d -eq '') -and
      -not (Test-Path (Get-GateStateFile 'wf-test-g10'))
Assert-True $ok 'T33 stop_hook_active, disable flag, no open work and no docs/work all pass'

# T34: the same command reaching the gate set from two sources runs once. Open
# work items multiply otherwise, and re-running one suite per work item is the
# direct path to RISK-01.
$root = New-GateRepo 'gate-dedupe' @('dup = cmd /c exit 4') @(
    "| TASK-01 | ``cmd /c exit 4`` | scope | - | $kKeep | same command |"
)
$out = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g11'; cwd=$root; hook_event_name='Stop' }
$hits = ([regex]::Matches($out, [regex]::Escape('cmd /c exit 4'))).Count
Assert-True ($out -match '"decision"\s*:\s*"block"' -and $hits -eq 1) 'T34 a command reached from two sources is executed and reported once'

# T35: the infra/failure split now rests on whether the command resolves, not
# on the exit code, so a command that DOES resolve and exits 1 must still block.
# Without this, "gitleaks not installed" and "gitleaks found a secret" collapse
# into the same verdict.
$root = New-GateRepo 'gate-exit1' @('real = cmd /c exit 1') $null
$out = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g12'; cwd=$root; hook_event_name='Stop' }
$st = Get-GateStateFile 'wf-test-g12'
$infra = 0
if (Test-Path $st) { $infra = (Get-Content $st -Raw -Encoding UTF8 | ConvertFrom-Json).infraCount }
Assert-True ($out -match '"decision"\s*:\s*"block"' -and $infra -eq 0) 'T35 a resolvable command exiting 1 is a failure, not an infrastructure event'

# ---------- install-hooks.ps1: Stop registration (TASK-39) ----------

# T36 (AC-07): Stop carries exactly one entry, at the gate's own budget rather
# than the 10s the injection-only hooks use, and rerunning changes nothing.
$dir = New-TestDir 'inst-stop'
$settings = Join-Path $dir 'settings.json'
Install-WfHooks -SettingsPath $settings -HooksDir $hooksDir
Install-WfHooks -SettingsPath $settings -HooksDir $hooksDir
$s = Get-Content $settings -Raw -Encoding UTF8 | ConvertFrom-Json
$stop = @()
if ($s.hooks -and $s.hooks.Stop) { $stop = @($s.hooks.Stop) }
$ok = $stop.Count -eq 1 -and
      $stop[0].hooks[0].timeout -eq 600 -and
      (@($stop[0].hooks[0].args) -join ' ') -match 'wf-stop-gate\.ps1'
Assert-True $ok 'T36 install registers exactly one Stop entry with the gate timeout, idempotently'

# T37: the injection hooks keep the 10s budget - parameterising the timeout must
# not quietly raise it for hooks that only print text.
$ss = @($s.hooks.SessionStart)
$pt = @($s.hooks.PostToolUse)
$ok = ($ss.Count -eq 2) -and ($pt.Count -eq 1) -and
      (@($ss | ForEach-Object { $_.hooks[0].timeout }) -join ',') -eq '10,10' -and
      $pt[0].hooks[0].timeout -eq 10
Assert-True $ok 'T37 injection hooks keep their 10s timeout after parameterisation'

# T38: colour codes in a gate's OUTPUT must not reach the block reason - the
# reason is read as plain text, and escape sequences bury the message in it.
# The colour lives in a file the gate prints, not in the command string: the
# command is reported verbatim, so putting ESC there would test nothing.
# ESC comes from [char]27 so this file stays free of raw control bytes.
$esc = [string][char]27
$root = New-GateRepo 'gate-ansi' @('coloured = type ansi.txt & exit 5') $null
Set-Content -Path (Join-Path $root 'ansi.txt') -Value "$esc[31mred text$esc[0m" -Encoding Ascii
$out = Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-g13'; cwd=$root; hook_event_name='Stop' }
# The reason travels as JSON, so a surviving ESC shows up either raw or as its
# \u001b escape; neither may appear. 'red text' must survive.
$ok = ($out -match '"decision"\s*:\s*"block"') -and ($out -match 'red text') -and
      -not ($out.Contains($esc)) -and -not ($out -match 'u001b')
Assert-True $ok 'T38 ANSI colour codes are stripped from the block reason'

} finally {
    Remove-Item Env:\CLAUDE_WF_THRESHOLD_KB -ErrorAction SilentlyContinue
    Remove-Item Env:\CLAUDE_WF_REWARN_KB -ErrorAction SilentlyContinue
    Remove-Item Env:\CLAUDE_WF_GATE_DISABLE -ErrorAction SilentlyContinue
    Remove-Item Env:\CLAUDE_WF_GATE_TIMEOUT_SEC -ErrorAction SilentlyContinue
}

Write-Host ''
Write-Host "passed: $script:passCount  failed: $script:failCount"
if ($script:failCount -gt 0) { exit 1 } else { exit 0 }

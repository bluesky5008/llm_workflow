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

# Builds a transcript-shaped JSONL line (DES-02 v3 usage signal). Only the
# fields the hook reads are modelled; the real file carries many more.
function New-UsageLine([int]$InputTokens, [int]$CacheCreate, [int]$CacheRead, [bool]$Sidechain = $false) {
    $sc = if ($Sidechain) { 'true' } else { 'false' }
    return '{"parentUuid":"p","isSidechain":' + $sc + ',"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"ok"}],"usage":{"input_tokens":' + $InputTokens + ',"cache_creation_input_tokens":' + $CacheCreate + ',"cache_read_input_tokens":' + $CacheRead + ',"cache_creation":{"ephemeral_5m_input_tokens":' + $CacheCreate + ',"ephemeral_1h_input_tokens":0},"output_tokens":12,"service_tier":"standard"}},"uuid":"u"}'
}

function New-ToolResultLine([int]$PayloadBytes) {
    return '{"parentUuid":"u","isSidechain":false,"type":"user","message":{"role":"user","content":[{"tool_use_id":"t","type":"tool_result","content":"' + ('x' * $PayloadBytes) + '"}]},"uuid":"r"}'
}

function Write-TranscriptLines([string]$Path, [string[]]$Lines) {
    [IO.File]::WriteAllText($Path, (($Lines -join "`n") + "`n"), (New-Object Text.UTF8Encoding($false)))
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
Remove-Item Env:\CLAUDE_WF_THRESHOLD_TOKENS -ErrorAction SilentlyContinue
Remove-Item Env:\CLAUDE_WF_REWARN_TOKENS -ErrorAction SilentlyContinue

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

# T03b: only an on-hold work-log -> silent (DCR-007: on-hold is a closed state for the hook), baseline still recorded
$ws = New-TestDir 'ss-onhold'
New-WorkLog $ws '20990103-hold' 'on-hold'
$t = New-Transcript $ws 5
$out = Invoke-Hook 'wf-session-start.ps1' @{ session_id='wf-test-ss2b'; transcript_path=$t; cwd=$ws; hook_event_name='SessionStart'; source='startup' }
Assert-True ($out -eq '' -and (Test-Path (Get-StateFile 'wf-test-ss2b'))) 'T03b session-start silent when only on-hold work-log; baseline recorded'

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

# ---------- wf-context-threshold.ps1 : usage signal (DES-02 v3, ADR-012) ----------
# T07..T13 above use zero-byte transcripts (no parseable usage) and therefore
# exercise the byte-growth fallback. The cases below put real usage lines in.

$env:CLAUDE_WF_THRESHOLD_TOKENS = '100000'
$env:CLAUDE_WF_REWARN_TOKENS = '10000'
$env:CLAUDE_WF_THRESHOLD_KB = '100000'   # make the byte fallback unreachable here

# T22: usage above token threshold with negligible byte growth -> inject (usage wins over bytes)
$ws = New-TestDir 'th-usage'
New-WorkLog $ws '20990106-open' 'in-progress'
$t = Join-Path $ws 'transcript.jsonl'
Write-TranscriptLines $t @((New-UsageLine 2000 5000 3000))     # 10k: below threshold
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th4'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }   # bootstraps state
Write-TranscriptLines $t @((New-UsageLine 2000 5000 3000), (New-UsageLine 1500 500 110000))   # 112k
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th4'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -match 'hookSpecificOutput' -and $out -match 'context_tokens=112000') 'T22 threshold injects on usage tokens >= threshold and reports the measured value'

# T23: same tokens again -> suppressed by token re-warn interval
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th4'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -eq '') 'T23 threshold token re-warn suppressed without further growth'

# T24: tokens grow past re-warn interval -> inject again
Write-TranscriptLines $t @((New-UsageLine 1500 500 110000), (New-UsageLine 1500 500 121000))   # 123k (+11k)
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th4'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -match 'hookSpecificOutput') 'T24 threshold re-warns after token re-warn interval'

# T25: context shrank below the last warning (compaction without hook) then re-crossed -> inject (lastWarned reset)
Write-TranscriptLines $t @((New-UsageLine 1000 500 40000), (New-UsageLine 1000 500 100000))   # 101.5k < lastWarned 123k but >= threshold
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th4'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -match 'hookSpecificOutput') 'T25 threshold treats a shrunken context as a fresh crossing'

# T26: huge byte growth but usage below threshold -> silent (bytes are NOT consulted when usage is readable)
$ws = New-TestDir 'th-usage-low'
New-WorkLog $ws '20990107-open' 'in-progress'
$t = Join-Path $ws 'transcript.jsonl'
Write-TranscriptLines $t @((New-UsageLine 1000 1000 1000))
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th5'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
$env:CLAUDE_WF_THRESHOLD_KB = '50'
Write-TranscriptLines $t @((New-UsageLine 1000 1000 1000), (New-ToolResultLine 600000), (New-UsageLine 1000 1000 30000))   # +600KB bytes, 32k tokens
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th5'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -eq '') 'T26 threshold silent when usage is readable and below threshold despite large byte growth'
$env:CLAUDE_WF_THRESHOLD_KB = '100000'

# T27: last usage line is buried under a large tool_result line -> still found within the tail window
Write-TranscriptLines $t @((New-UsageLine 1000 1000 30000), (New-UsageLine 1000 1000 150000), (New-ToolResultLine 600000))
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th5'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -match 'context_tokens=152000') 'T27 threshold finds the last usage behind a large tool_result line'

# T28: trailing sidechain (subagent) usage is ignored; main-agent usage decides
$ws = New-TestDir 'th-sidechain'
New-WorkLog $ws '20990108-open' 'in-progress'
$t = Join-Path $ws 'transcript.jsonl'
Write-TranscriptLines $t @((New-UsageLine 1000 1000 1000))
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th6'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Write-TranscriptLines $t @((New-UsageLine 1000 1000 1000), (New-UsageLine 1000 1000 140000), (New-UsageLine 500 0 2000 $true))
$out = Invoke-Hook 'wf-context-threshold.ps1' @{ session_id='wf-test-th6'; transcript_path=$t; cwd=$ws; hook_event_name='PostToolUse'; tool_name='Bash' }
Assert-True ($out -match 'context_tokens=142000') 'T28 threshold skips sidechain usage lines'

Remove-Item Env:\CLAUDE_WF_THRESHOLD_TOKENS -ErrorAction SilentlyContinue
Remove-Item Env:\CLAUDE_WF_REWARN_TOKENS -ErrorAction SilentlyContinue
$env:CLAUDE_WF_THRESHOLD_KB = '50'

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

# ---------- wf-test-guard.ps1 ----------

# Korean tokens built from code points (ASCII-only source, RISK-05).
function K([int[]]$CodePoints) { return -join ($CodePoints | ForEach-Object { [char]$_ }) }
$kRegister = K 0xB300,0xC7A5                              # register section heading
$kTestFile = K 0xD14C,0xC2A4,0xD2B8,0x20,0xD30C,0xC77C    # test-file column
$kState    = K 0xC0C1,0xD0DC                              # state column
$kLastOk   = K 0xB9C8,0xC9C0,0xB9C9,0x20,0xC131,0xACF5    # last-success column
$kKeep     = K 0xC720,0xC9C0                              # keep state
$kExpect   = K 0xD310,0xB3C5,0x20,0xAE30,0xB300            # expectation section heading
$fixture = Join-Path (Split-Path (Split-Path $hooksDir)) 'skills\wf-doc\scripts\tests\fixtures\test-register.sample.md'

function New-GuardRepo([string]$Name, [string]$RegisterText) {
    $ws = New-TestDir $Name
    if ($RegisterText) {
        New-Item -ItemType Directory -Force (Join-Path $ws 'docs') | Out-Null
        [IO.File]::WriteAllText((Join-Path $ws 'docs\test-register.md'), $RegisterText, (New-Object Text.UTF8Encoding($false)))
    }
    return $ws
}

function Invoke-Guard([string]$Cwd, [string]$Tool, [hashtable]$ToolInput) {
    return Invoke-Hook 'wf-test-guard.ps1' @{ session_id='wf-test-tg'; cwd=$Cwd; hook_event_name='PreToolUse'; tool_name=$Tool; tool_input=$ToolInput; permission_mode='default' }
}

$fixtureText = [IO.File]::ReadAllText($fixture, [Text.Encoding]::UTF8)
$wsFix = New-GuardRepo 'tg-fixture' $fixtureText

# T29: Edit on a keep-row test file (absolute path) -> ask, reason names the row
$out = Invoke-Guard $wsFix 'Edit' @{ file_path=(Join-Path $wsFix 'setup\hooks\tests\run-tests.ps1') }
Assert-True ($out -match '"permissionDecision":"ask"' -and $out -match 'TST-01') 'T29 guard asks before editing a keep-row test file'

# T30: Write on the project gate settings file -> ask
$out = Invoke-Guard $wsFix 'Write' @{ file_path=(Join-Path $wsFix '.claude\settings.local.json') }
Assert-True ($out -match '"permissionDecision":"ask"') 'T30 guard asks before writing project .claude settings'

# T31: Edit on the user-level gate settings file -> ask (path string only, nothing is written)
$out = Invoke-Guard $wsFix 'Edit' @{ file_path=(Join-Path $HOME '.claude\settings.json') }
Assert-True ($out -match '"permissionDecision":"ask"') 'T31 guard asks before editing ~/.claude settings'

# T32: unregistered file and the register itself -> silent
$outA = Invoke-Guard $wsFix 'Edit' @{ file_path=(Join-Path $wsFix 'setup\hooks\wf-common.ps1') }
$outB = Invoke-Guard $wsFix 'Edit' @{ file_path=(Join-Path $wsFix 'docs\test-register.md') }
Assert-True ($outA -eq '' -and $outB -eq '') 'T32 guard silent for unregistered files and the register itself'

# T33: register without the test-file column -> nothing is protected, silent
$noCol = "## $kRegister`n`n| ID | $kState | $kLastOk |`n|---|---|---|`n| TST-01 | $kKeep | 2026-01-02 10:00 $([char]0xB7) abc1234 |`n"
$ws = New-GuardRepo 'tg-nocol' $noCol
$out = Invoke-Guard $ws 'Edit' @{ file_path=(Join-Path $ws 'setup\hooks\tests\run-tests.ps1') }
Assert-True ($out -eq '') 'T33 guard silent when the register has no test-file column'

# T34: register present but its table cannot be read -> ask with guard=error (fail-to-ask)
$ws = New-GuardRepo 'tg-broken' "# no register table here`n"
$out = Invoke-Guard $ws 'Edit' @{ file_path=(Join-Path $ws 'a.txt') }
Assert-True ($out -match '"permissionDecision":"ask"' -and $out -match 'guard=error') 'T34 guard asks with guard=error when the register is unreadable'

# T35: no register -> silent even for gate settings (unrelated repo, AC-05)
$ws = New-GuardRepo 'tg-none' $null
$out = Invoke-Guard $ws 'Write' @{ file_path=(Join-Path $ws '.claude\settings.json') }
Assert-True ($out -eq '') 'T35 guard silent without docs/test-register.md'

# T36: NotebookEdit reads notebook_path
$out = Invoke-Guard $wsFix 'NotebookEdit' @{ notebook_path=(Join-Path $wsFix 'skills\wf-doc\scripts\tests\nb.py') }
Assert-True ($out -match '"permissionDecision":"ask"' -and $out -match 'TST-02') 'T36 guard reads notebook_path for NotebookEdit'

# T37: shared fixture expectations match regression_guard.py (DES-08); relative paths as given
$expectBlock = ($fixtureText -replace "`r`n", "`n").Split(@("`n## $kExpect`n"), 'None')[1].Split(@("`n## "), 'None')[0]
$cases = @($expectBlock.Trim().Split("`n") | Select-Object -Skip 2)
$mismatch = @()
foreach ($line in $cases) {
    $c = $line.Trim().Trim('|').Split('|') | ForEach-Object { $_.Trim() }
    $out = Invoke-Guard $wsFix 'Edit' @{ file_path=$c[0] }
    $got = '-'
    if ($out -match '"permissionDecision":"ask"') { $got = (([regex]::Matches($out, 'TST-\d+') | ForEach-Object { $_.Value }) -join ',') }
    if ($got -ne $c[1]) { $mismatch += "$($c[0]): expected $($c[1]) got $got" }
}
Assert-True ($cases.Count -eq 8 -and $mismatch.Count -eq 0) ('T37 guard matches the shared fixture expectations ' + ($mismatch -join '; '))

# ---------- wf-stop-gate.ps1 ----------

# Fake judge scripts stand in for regression_guard.py via CLAUDE_WF_GUARD_SCRIPT.
$fakeDir = New-TestDir 'sg-fakes'
function New-FakeJudge([string]$Name, [int]$Code, [string]$Line) {
    $p = Join-Path $fakeDir "$Name.py"
    Set-Content -Path $p -Value @("import sys", "print('$Line')", "sys.exit($Code)") -Encoding ASCII
    return $p
}
$fake1 = New-FakeJudge 'exit1' 1 'TST-07: fake violation tests/a.py'
$fake0 = New-FakeJudge 'exit0' 0 ''
$fake2 = New-FakeJudge 'exit2' 2 'regression_guard: boom'

function Invoke-StopGate([string]$Cwd, [bool]$Active = $false) {
    return Invoke-Hook 'wf-stop-gate.ps1' @{ session_id='wf-test-sg'; cwd=$Cwd; hook_event_name='Stop'; stop_hook_active=$Active }
}

$wsSg = New-GuardRepo 'sg-repo' $fixtureText

# T38: judge exit 1 -> block once, reason carries the judge output
$env:CLAUDE_WF_GUARD_SCRIPT = $fake1
$out = Invoke-StopGate $wsSg
Assert-True ($out -match '"decision":"block"' -and $out -match 'TST-07: fake violation') 'T38 stop-gate blocks with the judge output on exit 1'

# T39: judge exit 0 -> silent
$env:CLAUDE_WF_GUARD_SCRIPT = $fake0
$out = Invoke-StopGate $wsSg
Assert-True ($out -eq '') 'T39 stop-gate silent when the judge finds nothing'

# T40: judge exit 2 (internal error) -> silent (fail-open)
$env:CLAUDE_WF_GUARD_SCRIPT = $fake2
$out = Invoke-StopGate $wsSg
Assert-True ($out -eq '') 'T40 stop-gate silent on judge internal error'

# T41: re-entry (stop_hook_active) -> silent even on violation
$env:CLAUDE_WF_GUARD_SCRIPT = $fake1
$out = Invoke-StopGate $wsSg $true
Assert-True ($out -eq '') 'T41 stop-gate passes when stop_hook_active is set'

# T42: no register -> silent even on violation (AC-05)
$ws = New-GuardRepo 'sg-none' $null
$out = Invoke-StopGate $ws
Assert-True ($out -eq '') 'T42 stop-gate silent without docs/test-register.md'

# T43: python not on PATH -> silent (fail-open)
$savedPath = $env:PATH
$env:PATH = "$env:SystemRoot\System32;$env:SystemRoot\System32\WindowsPowerShell\v1.0"
try { $out = Invoke-StopGate $wsSg } finally { $env:PATH = $savedPath }
Assert-True ($out -eq '') 'T43 stop-gate silent when python is absent'
Remove-Item Env:\CLAUDE_WF_GUARD_SCRIPT -ErrorAction SilentlyContinue

# T44: real regression_guard.py in a scratch git repo - keep-row test file edited after
# its last-success SHA with no record -> block naming the row
$ws = New-TestDir 'sg-real'
& git -C $ws init -q
& git -C $ws config user.email 't@example.com'
& git -C $ws config user.name 't'
New-Item -ItemType Directory -Force (Join-Path $ws 'tests') | Out-Null
Set-Content -Path (Join-Path $ws 'tests\t1.py') -Value 'x = 1' -Encoding ASCII
& git -C $ws add -A
& git -C $ws commit -q -m init
$sha = (& git -C $ws rev-parse --short HEAD).Trim()
$reg = "## $kRegister`n`n| ID | $kTestFile | $kState | $kLastOk |`n|---|---|---|---|`n| TST-01 | tests/*.py | $kKeep | 2026-01-02 10:00 $([char]0xB7) $sha |`n"
New-Item -ItemType Directory -Force (Join-Path $ws 'docs') | Out-Null
[IO.File]::WriteAllText((Join-Path $ws 'docs\test-register.md'), $reg, (New-Object Text.UTF8Encoding($false)))
Set-Content -Path (Join-Path $ws 'tests\t1.py') -Value 'x = 2' -Encoding ASCII
$out = Invoke-StopGate $ws
Assert-True ($out -match '"decision":"block"' -and $out -match 'TST-01' -and $out -match 'tests/t1.py') 'T44 stop-gate blocks on a real unrecorded keep-row test change'

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

# T45: fresh install also registers the regression-guard hooks (PreToolUse guard, Stop gate)
$dir = New-TestDir 'inst-guard'
$settings = Join-Path $dir 'settings.json'
Install-WfHooks -SettingsPath $settings -HooksDir $hooksDir
$h = (Get-Content $settings -Raw -Encoding UTF8 | ConvertFrom-Json).hooks
$pre = @($h.PreToolUse | Where-Object { $_ }); $stop = @($h.Stop | Where-Object { $_ })
$preOk = $pre.Count -eq 1 -and $pre[0].matcher -eq 'Edit|Write|MultiEdit|NotebookEdit' -and $pre[0].hooks[0].args[-1] -like '*\wf-test-guard.ps1'
$stopOk = $stop.Count -eq 1 -and -not $stop[0].PSObject.Properties['matcher'] -and $stop[0].hooks[0].args[-1] -like '*\wf-stop-gate.ps1'
Assert-True ($preOk -and $stopOk) 'T45 install registers 1 PreToolUse guard + 1 Stop gate entry'

# T46: rerun keeps exactly one of each
Install-WfHooks -SettingsPath $settings -HooksDir $hooksDir
$h = (Get-Content $settings -Raw -Encoding UTF8 | ConvertFrom-Json).hooks
Assert-True (@($h.PreToolUse | Where-Object { $_ }).Count -eq 1 -and @($h.Stop | Where-Object { $_ }).Count -eq 1) 'T46 rerun does not duplicate guard entries'
}

} finally {
    Remove-Item Env:\CLAUDE_WF_THRESHOLD_KB -ErrorAction SilentlyContinue
    Remove-Item Env:\CLAUDE_WF_REWARN_KB -ErrorAction SilentlyContinue
    Remove-Item Env:\CLAUDE_WF_THRESHOLD_TOKENS -ErrorAction SilentlyContinue
    Remove-Item Env:\CLAUDE_WF_REWARN_TOKENS -ErrorAction SilentlyContinue
    Remove-Item Env:\CLAUDE_WF_GUARD_SCRIPT -ErrorAction SilentlyContinue
}

Write-Host ''
Write-Host "passed: $script:passCount  failed: $script:failCount"
if ($script:failCount -gt 0) { exit 1 } else { exit 0 }

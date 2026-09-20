# Shared helpers for llm_workflow session-handoff hooks (DES-01..DES-03, DES-05).
# ASCII-only source: PS 5.1 misreads Korean literals in BOM-less UTF-8 scripts.
# Korean text lives in messages/*.md and is read with explicit UTF-8 encoding.
# Every hook is fail-open: callers wrap everything in try/catch and exit 0.

function Read-WfHookInput {
    $reader = New-Object IO.StreamReader([Console]::OpenStandardInput(), (New-Object Text.UTF8Encoding($false)))
    return ($reader.ReadToEnd() | ConvertFrom-Json)
}

# Returns <cwd>/docs/work if it exists, else $null (FR-05 guard: repos that do
# not use the workflow must see no injection and no side effects).
function Get-WfWorkDir([object]$HookInput) {
    if (-not $HookInput.cwd) { return $null }
    $p = Join-Path $HookInput.cwd 'docs\work'
    if (Test-Path $p) { return $p }
    return $null
}

# A work-log counts as open unless its header carries a closed status. Statuses
# are backticked ASCII tokens, so no Korean matching is needed; files without a
# readable header are skipped to avoid false positives.
function Get-WfOpenWorkLogs([string]$WorkDir) {
    $open = @()
    foreach ($dir in @(Get-ChildItem $WorkDir -Directory)) {
        $log = Join-Path $dir.FullName 'work-log.md'
        if (-not (Test-Path $log)) { continue }
        $head = Get-Content $log -TotalCount 12 -Encoding UTF8
        $closed = $head | Where-Object { $_ -match '`(completed|superseded|rejected|withdrawn)`' }
        if (-not $closed) { $open += $dir.Name }
    }
    return ,$open
}

function Get-WfStatePath([object]$HookInput) {
    $dir = Join-Path $env:TEMP 'claude-wf'
    New-Item -ItemType Directory -Force $dir | Out-Null
    $sid = $HookInput.session_id
    if (-not $sid) { $sid = 'unknown' }
    return Join-Path $dir "$sid.json"
}

function Get-WfTranscriptBytes([object]$HookInput) {
    $t = $HookInput.transcript_path
    if ($t -and (Test-Path $t)) { return (Get-Item $t).Length }
    return [long]0
}

function Read-WfState([string]$Path) {
    if (Test-Path $Path) { return (Get-Content $Path -Raw -Encoding UTF8 | ConvertFrom-Json) }
    return $null
}

function Write-WfState([string]$Path, [long]$BaselineBytes, [object]$LastWarnedBytes) {
    $state = @{
        baselineBytes   = $BaselineBytes
        lastWarnedBytes = $LastWarnedBytes
        updatedAt       = (Get-Date).ToString('o')
    }
    $json = ConvertTo-Json -InputObject $state -Compress
    [IO.File]::WriteAllText($Path, $json, (New-Object Text.UTF8Encoding($false)))
}

function Get-WfMessage([string]$Name) {
    return (Get-Content (Join-Path $PSScriptRoot "messages\$Name") -Raw -Encoding UTF8)
}

# Emits the documented hook output contract as UTF-8 bytes, bypassing console
# code-page translation so Korean text survives on any system locale.
function Write-WfContext([string]$EventName, [string]$Text) {
    $payload = @{ hookSpecificOutput = @{ hookEventName = $EventName; additionalContext = $Text } }
    $json = ConvertTo-Json -InputObject $payload -Compress -Depth 5
    $writer = New-Object IO.StreamWriter([Console]::OpenStandardOutput(), (New-Object Text.UTF8Encoding($false)))
    $writer.Write($json)
    $writer.Flush()
}

# ---- Stop gate helpers (ADR-005, DES-01/DES-03/DES-04) ----

# Repo-global gate fence: lines of "name = command" inside a ```gates block.
# Splits on the FIRST '=' so Windows paths and flags containing '=' survive.
# Anything outside the fence is prose, not a gate (ADR-005: one definition site).
function Get-WfGateLines([string]$Path) {
    $gates = @()
    if (-not $Path -or -not (Test-Path $Path)) { return ,$gates }
    $inside = $false
    foreach ($line in @(Get-Content $Path -Encoding UTF8)) {
        $t = $line.Trim()
        if (-not $inside) {
            if ($t -match '^```\s*gates\s*$') { $inside = $true }
            continue
        }
        if ($t.StartsWith('```')) { break }
        if (-not $t -or $t.StartsWith('#')) { continue }
        $i = $t.IndexOf('=')
        if ($i -lt 1) { continue }
        $name = $t.Substring(0, $i).Trim()
        $cmd = $t.Substring($i + 1).Trim()
        if ($name -and $cmd) { $gates += New-Object psobject -Property @{ Name = $name; Command = $cmd } }
    }
    return ,$gates
}

# Work-item gates are the obligation-list rows whose status is "keep"; those
# rows already passed the determinism entry check, so they are the only rows
# eligible to block (ADR-005 source C). The heading and the status vocabulary
# are Korean and this file is ASCII-only, so both come from code points.
# A section holding prose instead of a table, a missing section and a missing
# file all yield nothing - none of them is an error.
function Get-WfObligationGates([string]$Path) {
    $gates = @()
    if (-not $Path -or -not (Test-Path $Path)) { return ,$gates }
    $heading = '## ' + [char]0xD68C + [char]0xADC0 + ' ' + [char]0xC758 + [char]0xBB34 + ' ' + [char]0xBAA9 + [char]0xB85D
    $keep = [string][char]0xC720 + [char]0xC9C0
    $inside = $false
    foreach ($line in @(Get-Content $Path -Encoding UTF8)) {
        $t = $line.Trim()
        if (-not $inside) {
            if ($t -eq $heading) { $inside = $true }
            continue
        }
        if ($t.StartsWith('## ')) { break }
        if (-not $t.StartsWith('|')) { continue }
        $cells = $t.Trim('|').Split('|')
        if ($cells.Count -lt 5) { continue }
        if ($cells[4].Trim() -ne $keep) { continue }
        if ($cells[1].Trim() -match '^`(.+)`$') {
            $gates += New-Object psobject -Property @{ Name = $cells[0].Trim(); Command = $Matches[1].Trim() }
        }
    }
    return ,$gates
}

# DES-03 citation key: HEAD + porcelain status + working-tree diff, hashed.
# An identical key means an identical tree, so a gate that passed on that key
# cannot fail now. Any git failure returns $null, which callers read as
# "no citation available - run the gates" rather than as "unchanged".
function Get-WfTreeKey([string]$Cwd) {
    if (-not $Cwd -or -not (Test-Path $Cwd)) { return $null }
    $prev = $ErrorActionPreference
    # Native stderr redirection raises NativeCommandError under 'Stop'; the exit
    # code is the real signal here, so keep it non-terminating.
    $ErrorActionPreference = 'Continue'
    try {
        $head = & git -C $Cwd rev-parse HEAD 2>$null
        if ($LASTEXITCODE -ne 0 -or -not $head) { return $null }
        $status = @(& git -C $Cwd status --porcelain 2>$null) -join "`n"
        $diff = @(& git -C $Cwd diff HEAD 2>$null) -join "`n"
        $text = "$head`n$status`n$diff"
        $sha = [Security.Cryptography.SHA256]::Create()
        try { $bytes = $sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($text)) }
        finally { $sha.Dispose() }
        return (-join ($bytes | ForEach-Object { $_.ToString('x2') }))
    } catch {
        return $null
    } finally {
        $ErrorActionPreference = $prev
    }
}

# Stop-hook block contract (FR-06): one JSON object on stdout, written as UTF-8
# bytes so the Korean reason survives any console code page.
function Write-WfBlock([string]$Reason) {
    $payload = @{ decision = 'block'; reason = $Reason }
    $json = ConvertTo-Json -InputObject $payload -Compress -Depth 5
    $writer = New-Object IO.StreamWriter([Console]::OpenStandardOutput(), (New-Object Text.UTF8Encoding($false)))
    $writer.Write($json)
    $writer.Flush()
}

# cmd.exe reports "command not found" as exit 1 on current Windows, which is
# indistinguishable from a gate that genuinely failed. Resolving the command up
# front is the only deterministic way to separate "the tool is not installed"
# (FR-03 infrastructure event) from "the check found something" (a real block).
function Test-WfGateCommand([string]$Command, [string]$WorkingDir) {
    if (-not $Command) { return $false }
    $builtins = @('assoc','break','call','cd','chdir','cls','color','copy','date','del','dir',
                  'echo','endlocal','erase','exit','for','ftype','goto','if','md','mkdir','mklink',
                  'move','path','pause','popd','prompt','pushd','rd','rem','ren','rename','rmdir',
                  'set','setlocal','shift','start','time','title','type','ver','verify','vol')
    $t = $Command.Trim()
    if ($t.StartsWith('"')) {
        $end = $t.IndexOf('"', 1)
        if ($end -lt 1) { return $true }
        $exe = $t.Substring(1, $end - 1)
    } else {
        $exe = ($t -split '\s+')[0]
    }
    if (-not $exe) { return $false }
    if ($builtins -contains $exe.ToLower()) { return $true }
    if ($exe -match '[\\/]') {
        $candidate = $exe
        if (-not [IO.Path]::IsPathRooted($candidate) -and $WorkingDir) { $candidate = Join-Path $WorkingDir $exe }
        return [bool](Test-Path $candidate)
    }
    return [bool](Get-Command $exe -ErrorAction SilentlyContinue)
}

# Gate state is a different shape from the transcript baseline state, so it
# gets its own writer rather than overloading Write-WfState. lastPassKey is
# the citation anchor (DES-03); infraCount is the record that some gate could
# not be run, which section 3.5 reads back.
function Write-WfGateState([string]$Path, [object]$LastPassKey, [int]$InfraCount) {
    $state = @{
        lastPassKey = $LastPassKey
        infraCount  = $InfraCount
        lastRunAt   = (Get-Date).ToString('o')
    }
    $json = ConvertTo-Json -InputObject $state -Compress
    [IO.File]::WriteAllText($Path, $json, (New-Object Text.UTF8Encoding($false)))
}

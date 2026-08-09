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

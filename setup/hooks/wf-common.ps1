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

# A work-log counts as open unless its header carries a closed status (on-hold
# included — DCR-007: holds resume only by user decision, not per session). Statuses
# are backticked ASCII tokens, so no Korean matching is needed; files without a
# readable header are skipped to avoid false positives.
function Get-WfOpenWorkLogs([string]$WorkDir) {
    $open = @()
    foreach ($dir in @(Get-ChildItem $WorkDir -Directory)) {
        $log = Join-Path $dir.FullName 'work-log.md'
        if (-not (Test-Path $log)) { continue }
        $head = Get-Content $log -TotalCount 12 -Encoding UTF8
        $closed = $head | Where-Object { $_ -match '`(completed|superseded|rejected|withdrawn|on-hold)`' }
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

# DES-02 v3 (ADR-012): current context size in tokens, read from the newest
# main-agent assistant line of the transcript. Claude Code writes the API
# usage block on every assistant line; input + cache_creation + cache_read is
# the prompt size of that call, i.e. the context the model is carrying.
# Reads only the last $TailBytes of the file (one seek, no full parse) and
# returns $null when nothing parseable is there, so callers can fall back.
function Get-WfContextTokens([string]$TranscriptPath, [int]$TailBytes = 1048576) {
    if (-not ($TranscriptPath -and (Test-Path $TranscriptPath))) { return $null }
    $fs = [IO.File]::Open($TranscriptPath, 'Open', 'Read', 'ReadWrite')
    try {
        $len = $fs.Length
        if ($len -le 0) { return $null }
        $take = [int][Math]::Min([long]$TailBytes, $len)
        $fs.Seek(-$take, 'End') | Out-Null
        $buf = New-Object byte[] $take
        $read = 0
        while ($read -lt $take) {
            $n = $fs.Read($buf, $read, $take - $read)
            if ($n -le 0) { break }
            $read += $n
        }
    } finally { $fs.Dispose() }
    $text = [Text.Encoding]::UTF8.GetString($buf, 0, $read)
    $lines = $text -split "`n"
    # usage object may nest one level (cache_creation{...}, server_tool_use{...})
    $usageRe = [regex]'"usage":\{(?:[^{}]|\{[^{}]*\})*\}'
    for ($i = $lines.Length - 1; $i -ge 0; $i--) {
        $line = $lines[$i]
        if ($line.IndexOf('"type":"assistant"') -lt 0) { continue }
        if ($line.IndexOf('"isSidechain":true') -ge 0) { continue }
        $m = $usageRe.Match($line)
        if (-not $m.Success) { continue }
        $u = $m.Value
        $total = [long]0
        $found = $false
        foreach ($key in @('"input_tokens":', '"cache_creation_input_tokens":', '"cache_read_input_tokens":')) {
            $km = [regex]::Match($u, [regex]::Escape($key) + '(\d+)')
            if ($km.Success) { $total += [long]$km.Groups[1].Value; $found = $true }
        }
        if ($found) { return $total }
    }
    return $null
}

function Read-WfState([string]$Path) {
    if (Test-Path $Path) { return (Get-Content $Path -Raw -Encoding UTF8 | ConvertFrom-Json) }
    return $null
}

function Write-WfState([string]$Path, [long]$BaselineBytes, [object]$LastWarnedBytes, [object]$LastWarnedTokens = $null) {
    $state = @{
        baselineBytes    = $BaselineBytes
        lastWarnedBytes  = $LastWarnedBytes
        lastWarnedTokens = $LastWarnedTokens
        updatedAt        = (Get-Date).ToString('o')
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

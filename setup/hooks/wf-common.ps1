# Shared helpers for llm_workflow hooks (DES-01..DES-03, DES-05; v4 DES-06).
# ASCII-only source: PS 5.1 misreads Korean literals in BOM-less UTF-8 scripts.
# Korean text lives in messages/*.md and is read with explicit UTF-8 encoding.
# Every hook is fail-open: callers wrap everything in try/catch and exit 0
# (sole exception: the DES-06 guard asks when the register is unreadable).

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

# Emits a hook output contract object as UTF-8 bytes, bypassing console
# code-page translation so Korean text survives on any system locale.
function Write-WfJson([object]$Payload) {
    $json = ConvertTo-Json -InputObject $Payload -Compress -Depth 5
    $writer = New-Object IO.StreamWriter([Console]::OpenStandardOutput(), (New-Object Text.UTF8Encoding($false)))
    $writer.Write($json)
    $writer.Flush()
}

function Write-WfContext([string]$EventName, [string]$Text) {
    Write-WfJson @{ hookSpecificOutput = @{ hookEventName = $EventName; additionalContext = $Text } }
}

# DES-06 (v4): PreToolUse permission decision (ask | deny) with its reason.
function Write-WfPermission([string]$Decision, [string]$Reason) {
    Write-WfJson @{ hookSpecificOutput = @{ hookEventName = 'PreToolUse'; permissionDecision = $Decision; permissionDecisionReason = $Reason } }
}

# Lower-case, forward-slash form used for every path and glob comparison (DES-08).
function ConvertTo-WfKey([string]$Path) {
    return $Path.Trim().Replace('\', '/').ToLowerInvariant()
}

# Protection layer 2 (ADR-014): the gate settings files this adapter declares.
function Get-WfGateSettingsPaths([string]$Cwd) {
    return @(
        (Join-Path $HOME '.claude\settings.json'),
        (Join-Path $HOME '.claude\settings.local.json'),
        (Join-Path $Cwd '.claude\settings.json'),
        (Join-Path $Cwd '.claude\settings.local.json')
    )
}

function ConvertFrom-WfCodePoints([int[]]$CodePoints) {
    return -join ($CodePoints | ForEach-Object { [char]$_ })
}

function Split-WfRow([string]$Row) {
    return @($Row.Trim().Trim('|').Split('|') | ForEach-Object { $_.Trim() })
}

# DES-08 register reading rules, the same as skills/wf-doc/scripts/regression_guard.py
# (parse_register) and pinned by the shared fixture tests/fixtures/test-register.sample.md:
# first table under the register H2 outside code fences, columns found by header
# prefix, keep rows are those whose state starts with the keep token, globs split on ';'.
# Returns @{ <row ID> = @(<globs>) } for keep rows (empty when the test-file column
# is absent) and throws when the table cannot be read.
function Get-WfKeptTestFiles([string]$RegisterPath) {
    $kRegister = ConvertFrom-WfCodePoints 0xB300,0xC7A5
    $kTestFile = ConvertFrom-WfCodePoints 0xD14C,0xC2A4,0xD2B8,0x20,0xD30C,0xC77C
    $kState    = ConvertFrom-WfCodePoints 0xC0C1,0xD0DC
    $kLastOk   = ConvertFrom-WfCodePoints 0xB9C8,0xC9C0,0xB9C9,0x20,0xC131,0xACF5
    $kKeep     = ConvertFrom-WfCodePoints 0xC720,0xC9C0
    $fence = $false; $inside = $false; $table = @()
    foreach ($t in [IO.File]::ReadAllLines($RegisterPath, [Text.Encoding]::UTF8)) {
        if ($t.TrimStart().StartsWith('```')) { $fence = -not $fence; continue }
        if ($fence) { continue }
        if ($t.StartsWith('## ')) {
            if ($table.Count -gt 0) { break }
            $inside = ($t.Substring(3).Trim() -eq $kRegister)
        } elseif ($inside -and $t.StartsWith('|')) {
            $table += $t
        } elseif ($table.Count -gt 0) { break }
    }
    if ($table.Count -lt 2) { throw 'register table not found' }
    $head = Split-WfRow $table[0]
    $fi = $null; $si = $null; $li = $null
    for ($i = 0; $i -lt $head.Count; $i++) {
        if ($null -eq $fi -and $head[$i].StartsWith($kTestFile)) { $fi = $i }
        if ($null -eq $si -and $head[$i].StartsWith($kState)) { $si = $i }
        if ($null -eq $li -and $head[$i].StartsWith($kLastOk)) { $li = $i }
    }
    if ($null -eq $si -or $null -eq $li) { throw 'register table lacks state/last-success columns' }
    $kept = @{}
    foreach ($t in ($table | Select-Object -Skip 2)) {
        $c = Split-WfRow $t
        if ($c.Count -ne $head.Count) { throw "row column count differs from header: $($c[0])" }
        if ($null -eq $fi -or -not $c[$si].StartsWith($kKeep)) { continue }
        $kept[$c[0]] = @($c[$fi].Split(';') | Where-Object { $_.Trim() } | ForEach-Object { ConvertTo-WfKey $_ })
    }
    return $kept
}

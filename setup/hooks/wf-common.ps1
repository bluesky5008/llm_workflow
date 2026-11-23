# Shared helpers for llm_workflow hooks (DES-01..DES-03, DES-05; v4 DES-06; v6 DES-04).
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

function Get-WfStatePath([object]$HookInput, [string]$Suffix = '') {
    $dir = Join-Path $env:TEMP 'claude-wf'
    New-Item -ItemType Directory -Force $dir | Out-Null
    $sid = $HookInput.session_id
    if (-not $sid) { $sid = 'unknown' }
    return Join-Path $dir "$sid$Suffix.json"
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
    # usage object nests to any depth (cache_creation{...}, iterations[{cache_creation{...}}]):
    # .NET balancing groups match the braces; the top-level keys come first, so the
    # first match of each key below is the call's own total, not an iteration's.
    $usageRe = [regex]'"usage":\{(?>[^{}]+|\{(?<d>)|\}(?<-d>))*(?(d)(?!))\}'
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

# v6 DES-04: per-session guard memory {asked:[{path,hash}], approved:[path], stopKeys:[key]}
# in <sid>.guard.json, apart from <sid>.json (Write-WfState rewrites that whole object).
# Read-modify-write without a lock: a lost update only asks or blocks again, and an
# unreadable file reads as no memory (NFR-04).
function Get-WfGuardState([object]$HookInput) {
    $state = @{ asked = @(); approved = @(); stopKeys = @() }
    try {
        $ErrorActionPreference = 'Stop'   # any read error lands in the catch, not on stderr
        $saved = Read-WfState (Get-WfStatePath $HookInput '.guard')
        foreach ($k in @($state.Keys)) { if ($saved.$k) { $state[$k] = @($saved.$k) } }
    } catch { }
    return $state
}

function Set-WfGuardState([object]$HookInput, [hashtable]$State) {
    $json = ConvertTo-Json -InputObject $State -Compress -Depth 5
    [IO.File]::WriteAllText((Get-WfStatePath $HookInput '.guard'), $json, (New-Object Text.UTF8Encoding($false)))
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

# Cells of a table row. As in GFM, an escaped pipe (\|) is cell content, not a cell
# boundary (same rule as regression_guard.py cells).
function Split-WfRow([string]$Row) {
    $t = $Row.Trim() -replace '^\|+', '' -replace '(?<!\\)\|+$', ''
    return @([regex]::Split($t, '(?<!\\)\|') | ForEach-Object { $_.Trim().Replace('\|', '|') })
}

# DES-08 register reading rules, the same as skills/wf-doc/scripts/regression_guard.py
# (parse_register) and pinned by the shared fixture tests/fixtures/test-register.sample.md:
# cells split on unescaped pipes (GFM \|), first table under the register H2 outside code fences, columns found by header
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

# v6 DES-02/04: the shared disabling patterns, read as regression_guard.load_patterns
# reads them (one regex per line, '#' comments and blank lines skipped, case-insensitive).
function Get-WfDisablePatterns {
    $file = Join-Path $PSScriptRoot '..\..\skills\wf-doc\scripts\test-disable-patterns.txt'
    return @([IO.File]::ReadAllLines($file, [Text.Encoding]::UTF8) | ForEach-Object { $_.Trim() } |
        Where-Object { $_ -and -not $_.StartsWith('#') } | ForEach-Object { [regex]::new($_, 'IgnoreCase') })
}

# v6 DES-04 (FR-04): identity of one tool call - SHA-1 of tool_name + compact JSON of
# tool_input, which its PreToolUse and PostToolUse both carry.
function Get-WfToolInputHash([object]$HookInput) {
    $text = [string]$HookInput.tool_name + (ConvertTo-Json -InputObject $HookInput.tool_input -Compress -Depth 10)
    $sha = [Security.Cryptography.SHA1]::Create()
    try { return -join ($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($text)) | ForEach-Object { $_.ToString('x2') }) }
    finally { $sha.Dispose() }
}

# v6 DES-04 (FR-01, FR-03): the guard's pre-check of what regression_guard.py decides at
# stop (the B layer stays canonical, NFR-05). Applies the edit to the current file in
# memory (Edit: first match, all with replace_all; MultiEdit: each edit in order; Write:
# the whole content; no file: empty) and is true when every old line is still there in
# order and no other line matches a disabling pattern. CRLF is folded to LF first; lines
# keep their LF, so an unterminated last line that gains a newline counts as changed, as
# in git diff. A missing field, an old_string not found or any error means "not pure"
# (fail-to-ask, NFR-04).
function Test-WfPureAddition([object]$HookInput, [string]$Path) {
    try {
        $in = $HookInput.tool_input
        $before = ''
        if (Test-Path -LiteralPath $Path) { $before = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8).Replace("`r`n", "`n") }
        $after = $before
        $edits = @()
        switch ($HookInput.tool_name) {
            'Write'     { if ($null -eq $in.content) { return $false }; $after = ([string]$in.content).Replace("`r`n", "`n") }
            'Edit'      { $edits = @($in) }
            'MultiEdit' { $edits = @($in.edits) }
            default     { return $false }
        }
        foreach ($e in $edits) {
            if ($null -eq $e.old_string -or $null -eq $e.new_string) { return $false }
            $old = ([string]$e.old_string).Replace("`r`n", "`n")
            $new = ([string]$e.new_string).Replace("`r`n", "`n")
            $at = $after.IndexOf($old, [StringComparison]::Ordinal)
            if ($at -lt 0) { return $false }
            if ($e.replace_all) { $after = $after.Replace($old, $new) }
            else { $after = $after.Remove($at, $old.Length).Insert($at, $new) }
        }
        $oldLines = @([regex]::Split($before, '(?<=\n)') | Where-Object { $_ })
        $patterns = Get-WfDisablePatterns
        $i = 0
        foreach ($line in @([regex]::Split($after, '(?<=\n)') | Where-Object { $_ })) {
            if ($i -lt $oldLines.Count -and $line -ceq $oldLines[$i]) { $i++; continue }
            $text = $line.TrimEnd("`n")
            foreach ($p in $patterns) { if ($p.IsMatch($text)) { return $false } }
        }
        return ($i -eq $oldLines.Count)
    } catch { return $false }
}

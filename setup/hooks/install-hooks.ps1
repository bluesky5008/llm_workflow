# DES-04 - merges the llm_workflow hook registrations (session handoff; v4
# regression guard) into a Claude Code
# settings.json, preserving every foreign key and user-defined hook.
# Dot-source this file and call Install-WfHooks. Idempotent; entries pointing
# at a stale repo location are replaced by the current HooksDir paths.

function New-WfCommandHook([string]$ScriptPath) {
    return [pscustomobject]@{
        type    = 'command'
        command = 'powershell.exe'
        args    = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $ScriptPath)
        timeout = 10
    }
}

# An empty matcher is omitted (Stop takes none).
function New-WfEntry([string]$Matcher, [string]$ScriptPath) {
    $entry = [ordered]@{}
    if ($Matcher) { $entry.matcher = $Matcher }
    $entry.hooks = @(New-WfCommandHook $ScriptPath)
    return [pscustomobject]$entry
}

# Ours = any entry whose command args reference a \setup\hooks\wf-*.ps1 script,
# regardless of which repo clone it points at.
function Test-WfOwnEntry([object]$Entry) {
    foreach ($h in @($Entry.hooks)) {
        foreach ($a in @($h.args)) {
            if ("$a" -match '\\setup\\hooks\\wf-[a-z-]+\.ps1$') { return $true }
        }
    }
    return $false
}

function Install-WfHooks([string]$SettingsPath, [string]$HooksDir) {
    $settings = $null
    if (Test-Path $SettingsPath) {
        $raw = Get-Content $SettingsPath -Raw -Encoding UTF8
        if ($raw -and $raw.Trim()) { $settings = $raw | ConvertFrom-Json }
    }
    if (-not $settings) { $settings = [pscustomobject]@{} }
    if (-not $settings.PSObject.Properties['hooks']) {
        $settings | Add-Member -MemberType NoteProperty -Name hooks -Value ([pscustomobject]@{})
    }
    $hooks = $settings.hooks

    $desired = @{
        SessionStart = @(
            (New-WfEntry 'startup|resume|clear' (Join-Path $HooksDir 'wf-session-start.ps1')),
            (New-WfEntry 'compact' (Join-Path $HooksDir 'wf-post-compact.ps1'))
        )
        PostToolUse  = @(
            (New-WfEntry '*' (Join-Path $HooksDir 'wf-context-threshold.ps1'))
        )
        PreToolUse   = @(
            (New-WfEntry 'Edit|Write|MultiEdit|NotebookEdit' (Join-Path $HooksDir 'wf-test-guard.ps1')),
            (New-WfEntry 'Edit|Write|MultiEdit|NotebookEdit' (Join-Path $HooksDir 'wf-approval-gate.ps1'))
        )
        Stop         = @(
            (New-WfEntry '' (Join-Path $HooksDir 'wf-stop-gate.ps1'))
        )
    }

    foreach ($eventName in $desired.Keys) {
        $existing = @()
        if ($hooks.PSObject.Properties[$eventName]) { $existing = @($hooks.$eventName) }
        $merged = @($existing | Where-Object { -not (Test-WfOwnEntry $_) }) + $desired[$eventName]
        if ($hooks.PSObject.Properties[$eventName]) { $hooks.$eventName = $merged }
        else { $hooks | Add-Member -MemberType NoteProperty -Name $eventName -Value $merged }
    }

    $dir = Split-Path $SettingsPath
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
    $json = ConvertTo-Json -InputObject $settings -Depth 20
    [IO.File]::WriteAllText($SettingsPath, $json, (New-Object Text.UTF8Encoding($false)))
}

# DES-04 - merges the session-handoff hook registrations into a Claude Code
# settings.json, preserving every foreign key and user-defined hook.
# Dot-source this file and call Install-WfHooks. Idempotent; entries pointing
# at a stale repo location are replaced by the current HooksDir paths.

# The injection hooks only read a file and print text, so 10s is generous.
# The Stop gate runs the project's own checks and needs its own budget.
function New-WfCommandHook([string]$ScriptPath, [int]$TimeoutSec = 10) {
    return [pscustomobject]@{
        type    = 'command'
        command = 'powershell.exe'
        args    = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $ScriptPath)
        timeout = $TimeoutSec
    }
}

function New-WfEntry([string]$Matcher, [string]$ScriptPath, [int]$TimeoutSec = 10) {
    return [pscustomobject]@{
        matcher = $Matcher
        hooks   = @(New-WfCommandHook $ScriptPath $TimeoutSec)
    }
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
        # Stop fires on every agent response, so it takes no matcher. 600s is
        # the whole-hook ceiling (DCR-006); the per-gate budget lives in
        # wf-stop-gate.ps1.
        Stop         = @(
            (New-WfEntry '' (Join-Path $HooksDir 'wf-stop-gate.ps1') 600)
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

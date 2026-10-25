# DES-06 (v4, ADR-014) - PreToolUse(Edit|Write|MultiEdit|NotebookEdit) hook.
# Asks the user before an edit touches a keep-row test file of
# docs/test-register.md or a Claude gate settings file. Silent when the repo has
# no register (NFR-03) and for the register itself (checked at stop, FR-08).
# Exception to fail-open: a register that exists but cannot be read asks
# (guard=error), because a silent failure here gives up the protection.
try {
    . (Join-Path $PSScriptRoot 'wf-common.ps1')
    $hookInput = Read-WfHookInput
    $cwd = $hookInput.cwd
    if (-not $cwd) { exit 0 }
    $register = Join-Path $cwd 'docs\test-register.md'
    if (-not (Test-Path $register)) { exit 0 }
    $target = $hookInput.tool_input.file_path
    if (-not $target) { $target = $hookInput.tool_input.notebook_path }
    if (-not $target) { exit 0 }

    $rel = $target
    try {
        if (-not [IO.Path]::IsPathRooted($target)) { $target = Join-Path $cwd $target }
        $full = ConvertTo-WfKey ([IO.Path]::GetFullPath($target))
        $root = (ConvertTo-WfKey ([IO.Path]::GetFullPath($cwd))).TrimEnd('/') + '/'
        $rel = $full
        if ($full.StartsWith($root)) { $rel = $full.Substring($root.Length) }
        if ($rel -eq 'docs/test-register.md') { exit 0 }

        $hits = @()
        foreach ($p in Get-WfGateSettingsPaths $cwd) {
            if ((ConvertTo-WfKey ([IO.Path]::GetFullPath($p))) -eq $full) { $hits += 'settings' }
        }
        $kept = Get-WfKeptTestFiles $register
        foreach ($id in ($kept.Keys | Sort-Object)) {
            if (@($kept[$id] | Where-Object { $rel -like $_ }).Count -gt 0) { $hits += $id }
        }
        if ($hits.Count -eq 0) { exit 0 }
        $why = $hits -join ', '
    } catch { $why = 'guard=error (' + $_.Exception.Message + ')' }

    Write-WfPermission 'ask' ((Get-WfMessage 'test-guard.md').TrimEnd() + ' ' + $why + ': ' + $rel)
    exit 0
} catch { exit 0 }

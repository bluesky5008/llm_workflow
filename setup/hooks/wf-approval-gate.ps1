# DES-08 (v5, ADR-018) - PreToolUse(Edit|Write|MultiEdit|NotebookEdit) hook.
# Asks the user before an edit touches product code while an open work log's
# baseline is not approved. The judgement lives in the harness-neutral
# skills/wf-doc/scripts/approval_gate.py (REQ-DESIGN-approval-gate DES-01);
# this wrapper only pre-filters and converts exit codes:
#   no docs/work, or a docs/ path with no .wf-gate.json -> silent, judge not run
#   exit 1 -> ask with the judge output; exit 2, timeout, python missing -> ask
#   (gate=error, fail-to-ask like DES-06); exit 0 and outer exceptions -> silent.
# No deny path: ADR-014 decision 1 allows deny only in a mode where ask is
# confirmed not to reach a person, and none is confirmed yet.
# CLAUDE_WF_GATE_SCRIPT overrides the judge path (tests).
try {
    . (Join-Path $PSScriptRoot 'wf-common.ps1')
    $hookInput = Read-WfHookInput
    $cwd = $hookInput.cwd
    if (-not $cwd) { exit 0 }
    if (-not (Test-Path (Join-Path $cwd 'docs\work'))) { exit 0 }
    $target = $hookInput.tool_input.file_path
    if (-not $target) { $target = $hookInput.tool_input.notebook_path }
    if (-not $target) { exit 0 }

    $rel = $target
    try {
        if (-not [IO.Path]::IsPathRooted($target)) { $target = Join-Path $cwd $target }
        $full = ConvertTo-WfKey ([IO.Path]::GetFullPath($target))
        $root = (ConvertTo-WfKey ([IO.Path]::GetFullPath($cwd))).TrimEnd('/') + '/'
        if (-not $full.StartsWith($root)) { exit 0 }
        $rel = $full.Substring($root.Length)
        if ($rel.StartsWith('docs/') -and -not (Test-Path (Join-Path $cwd '.wf-gate.json'))) { exit 0 }

        $judge = $env:CLAUDE_WF_GATE_SCRIPT
        if (-not $judge) { $judge = Join-Path $PSScriptRoot '..\..\skills\wf-doc\scripts\approval_gate.py' }
        $psi = New-Object Diagnostics.ProcessStartInfo
        $psi.FileName = 'python'
        # a trailing backslash would escape the closing quote in Windows argv parsing
        $psi.Arguments = '"' + $judge + '" "' + $cwd.TrimEnd('\') + '" "' + $target + '"'
        $psi.UseShellExecute = $false
        $psi.CreateNoWindow = $true
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.StandardOutputEncoding = New-Object Text.UTF8Encoding($false)
        $p = [Diagnostics.Process]::Start($psi)
        $stdout = $p.StandardOutput.ReadToEndAsync()
        $null = $p.StandardError.ReadToEndAsync()
        if (-not $p.WaitForExit(5000)) { try { $p.Kill() } catch {}; throw 'judge timeout' }
        if ($p.ExitCode -eq 0) { exit 0 }
        $why = $stdout.Result.Trim()
        if ($p.ExitCode -ne 1) { $why = 'gate=error (exit ' + $p.ExitCode + ') ' + $why }
    } catch { $why = 'gate=error (' + $_.Exception.Message + ')' }

    Write-WfPermission 'ask' ((Get-WfMessage 'approval-gate.md').TrimEnd() + ' ' + $rel + "`n" + $why)
    exit 0
} catch { exit 0 }

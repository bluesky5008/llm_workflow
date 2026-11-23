# DES-07 (v4, ADR-014) - Stop hook. A thin wrapper with no judgement of its own:
# runs the harness-neutral judge skills/wf-doc/scripts/regression_guard.py
# (REQ-DESIGN-regression-guard DES-04) and turns its exit 1 into one
# decision:block whose reason is the judge output. Everything else - exit 0/2,
# python missing, timeout, any exception - passes silently (fail-open, NFR-01).
# Within a session it blocks again only for a new violation key (v6 DES-05).
# CLAUDE_WF_GUARD_SCRIPT overrides the judge path (tests).
try {
    . (Join-Path $PSScriptRoot 'wf-common.ps1')
    $hookInput = Read-WfHookInput
    $cwd = $hookInput.cwd
    if (-not $cwd) { exit 0 }
    if (-not (Test-Path (Join-Path $cwd 'docs\test-register.md'))) { exit 0 }
    if ($hookInput.stop_hook_active) { exit 0 }

    $judge = $env:CLAUDE_WF_GUARD_SCRIPT
    if (-not $judge) { $judge = Join-Path $PSScriptRoot '..\..\skills\wf-doc\scripts\regression_guard.py' }
    if (-not (Test-Path $judge)) { exit 0 }

    $psi = New-Object Diagnostics.ProcessStartInfo
    $psi.FileName = 'python'
    # a trailing backslash would escape the closing quote in Windows argv parsing
    $psi.Arguments = '"' + $judge + '" "' + $cwd.TrimEnd('\') + '"'
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.StandardOutputEncoding = New-Object Text.UTF8Encoding($false)
    $p = [Diagnostics.Process]::Start($psi)
    $stdout = $p.StandardOutput.ReadToEndAsync()
    $null = $p.StandardError.ReadToEndAsync()
    if (-not $p.WaitForExit(10000)) { try { $p.Kill() } catch {}; exit 0 }
    if ($p.ExitCode -ne 1) { exit 0 }
    $out = $stdout.Result.Trim()

    # v6 DES-05 (FR-06): block only when some violation key (row|file|print) is new to this
    # session; a guard state that cannot be read or saved blocks without suppression (NFR-04).
    $keys = foreach ($line in ($out -split "`r?`n")) {
        $t = $line.Trim()
        if (-not $t) { continue }
        $print = '-'
        if ($t -match ' \[([^\]]*)\]$') { $print = $Matches[1]; $t = $t.Substring(0, $t.Length - $Matches[0].Length) }
        $t.Split(':')[0] + '|' + $t.Split(' ')[-1] + '|' + $print
    }
    try {
        $state = Get-WfGuardState $hookInput
        $new = @($keys | Where-Object { $state.stopKeys -notcontains $_ })
        if ($new.Count -eq 0) { exit 0 }
        $state.stopKeys = @($state.stopKeys) + $new
        Set-WfGuardState $hookInput $state
    } catch { }

    Write-WfJson @{ decision = 'block'; reason = (Get-WfMessage 'stop-gate.md').TrimEnd() + "`n" + $out }
    exit 0
} catch { exit 0 }

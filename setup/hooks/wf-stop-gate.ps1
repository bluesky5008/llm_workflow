# FR-01..FR-06 - Stop hook. Runs the gates while work is open and blocks the
# turn when one of them fails, so the obligation list is enforced outside the
# model rather than by it (ADR-005).
# Fail-open like every other hook: anything this script cannot do is an
# infrastructure event, never a block.
try {
    . (Join-Path $PSScriptRoot 'wf-common.ps1')
    $hookInput = Read-WfHookInput

    # FR-05 escape hatches, cheapest first. stop_hook_active means our own block
    # is what restarted the turn; blocking again would loop.
    if ($hookInput.stop_hook_active) { exit 0 }
    if ($env:CLAUDE_WF_GATE_DISABLE -eq '1') { exit 0 }

    $workDir = Get-WfWorkDir $hookInput
    if (-not $workDir) { exit 0 }
    $open = Get-WfOpenWorkLogs $workDir
    if ($open.Count -eq 0) { exit 0 }

    # FR-02: the gate set is the additive union of the repo-global fence and the
    # keep rows of every open work-log. Nothing else is a gate.
    $collected = @()
    $collected += Get-WfGateLines (Join-Path $hookInput.cwd 'docs\quality-gates.md')
    foreach ($id in $open) {
        $collected += Get-WfObligationGates (Join-Path $workDir (Join-Path $id 'work-log.md'))
    }

    # Two open work items that share a suite would otherwise run it twice per
    # turn; the command is the identity here, not the row that named it.
    $gates = @()
    $seen = @{}
    foreach ($g in $collected) {
        if ($seen.ContainsKey($g.Command)) { continue }
        $seen[$g.Command] = $true
        $gates += $g
    }
    if ($gates.Count -eq 0) { exit 0 }

    $statePath = (Get-WfStatePath $hookInput) -replace '\.json$', '-gate.json'
    $state = Read-WfState $statePath
    $infraCount = 0
    if ($state -and $state.infraCount) { $infraCount = [int]$state.infraCount }

    # FR-04: same tree, same commands, same result - cite instead of re-running.
    # A null key means the citation is unavailable, which is not the same as
    # "unchanged", so the gates run.
    $treeKey = Get-WfTreeKey $hookInput.cwd
    if ($treeKey -and $state -and $state.lastPassKey -eq $treeKey) { exit 0 }

    # DCR-006: measured against this repo's own obligation suite (72s), not
    # guessed. The citation (FR-04) is what keeps the average cost near zero;
    # this ceiling only has to stop a runaway gate.
    $timeoutSec = 300
    if ($env:CLAUDE_WF_GATE_TIMEOUT_SEC) {
        $parsed = 0
        if ([int]::TryParse($env:CLAUDE_WF_GATE_TIMEOUT_SEC, [ref]$parsed) -and $parsed -gt 0) { $timeoutSec = $parsed }
    }

    $failures = @()
    $infraHit = $false
    foreach ($gate in $gates) {
        if (-not (Test-WfGateCommand $gate.Command $hookInput.cwd)) { $infraHit = $true; continue }
        $outFile = [IO.Path]::GetTempFileName()
        $batchFile = Join-Path ([IO.Path]::GetTempPath()) ([Guid]::NewGuid().ToString('N') + '.cmd')
        try {
            # The command goes into a batch file instead of being spliced into our
            # argument string. A gate is free to contain &, | or a redirection of
            # its own, and splicing would bind our '> file' to the last piece of it
            # rather than to the whole command.
            Set-Content -Path $batchFile -Value @('@echo off', $gate.Command) -Encoding Default
            # cmd does the redirection: draining the pipes from PowerShell while
            # also waiting on the process is a deadlock waiting to happen.
            $psi = New-Object Diagnostics.ProcessStartInfo
            $psi.FileName = $env:ComSpec
            # 'call' first, not a quote: cmd /c strips the leading and trailing
            # quote of its argument string, which would break the redirection.
            $psi.Arguments = '/d /c call "' + $batchFile + '" > "' + $outFile + '" 2>&1'
            $psi.WorkingDirectory = $hookInput.cwd
            $psi.UseShellExecute = $false
            $psi.CreateNoWindow = $true
            $proc = [Diagnostics.Process]::Start($psi)
            if (-not $proc.WaitForExit($timeoutSec * 1000)) {
                try { $proc.Kill() } catch { }
                $infraHit = $true
                continue
            }
            $code = $proc.ExitCode
            # 9009 is cmd's "command not found": the gate never ran, so it can
            # neither pass nor fail. Same reading as a timeout (Q-04).
            if ($code -eq 0) { continue }
            # Kept for the Windows builds that do surface cmd's 9009.
            if ($code -eq 9009) { $infraHit = $true; continue }
            $tail = ''
            if (Test-Path $outFile) {
                $tail = (Get-Content $outFile -Raw -Encoding UTF8)
                if ($null -eq $tail) { $tail = '' }
                # Tools colour their output; the block reason is read as text,
                # so the escape sequences are noise that hides the message.
                $tail = [regex]::Replace($tail, ([char]27 + '\[[0-9;]*[A-Za-z]'), '')
                $tail = $tail.Trim()
                if ($tail.Length -gt 500) { $tail = $tail.Substring($tail.Length - 500) }
            }
            $failures += "- $($gate.Name) (exit $code): $($gate.Command) :: $tail"
        } catch {
            $infraHit = $true
        } finally {
            Remove-Item $outFile -Force -ErrorAction SilentlyContinue
            Remove-Item $batchFile -Force -ErrorAction SilentlyContinue
        }
    }

    if ($infraHit) { $infraCount++ }

    if ($failures.Count -gt 0) {
        # A failed run tells us nothing about the next tree, so the citation key
        # is cleared rather than carried forward.
        Write-WfGateState -Path $statePath -LastPassKey $null -InfraCount $infraCount
        $body = (Get-WfMessage 'stop-gate.md').TrimEnd()
        Write-WfBlock ($body + "`n" + ($failures -join "`n"))
        exit 0
    }

    # Only a clean sweep earns a citation: if a gate was skipped as an
    # infrastructure event, "everything passed" would be a claim we cannot make.
    $passKey = $null
    if ($treeKey -and -not $infraHit) { $passKey = $treeKey }
    Write-WfGateState -Path $statePath -LastPassKey $passKey -InfraCount $infraCount
    exit 0
} catch { exit 0 }

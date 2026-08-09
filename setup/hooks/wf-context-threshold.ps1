# DES-02 - PostToolUse(*) hook.
# Warns the model to hand off at the next plan-item boundary once transcript
# growth since the session baseline exceeds a configurable threshold.
# Signal choice rationale: docs/work/20260809-claude-hooks/ADR-001.
try {
    . (Join-Path $PSScriptRoot 'wf-common.ps1')
    $hookInput = Read-WfHookInput
    $workDir = Get-WfWorkDir $hookInput
    if (-not $workDir) { exit 0 }

    $t = $hookInput.transcript_path
    if (-not ($t -and (Test-Path $t))) { exit 0 }
    $size = (Get-Item $t).Length

    $statePath = Get-WfStatePath $hookInput
    $state = Read-WfState $statePath
    if (-not $state) {
        # Hooks installed mid-session: adopt the current size as baseline.
        Write-WfState -Path $statePath -BaselineBytes $size -LastWarnedBytes $null
        exit 0
    }

    $thresholdKB = 1500
    if ($env:CLAUDE_WF_THRESHOLD_KB -match '^\d+$') { $thresholdKB = [int]$env:CLAUDE_WF_THRESHOLD_KB }
    $rewarnKB = 300
    if ($env:CLAUDE_WF_REWARN_KB -match '^\d+$') { $rewarnKB = [int]$env:CLAUDE_WF_REWARN_KB }

    if (($size - [long]$state.baselineBytes) -lt ($thresholdKB * 1024)) { exit 0 }
    if ($null -ne $state.lastWarnedBytes -and ($size - [long]$state.lastWarnedBytes) -lt ($rewarnKB * 1024)) { exit 0 }

    Write-WfState -Path $statePath -BaselineBytes ([long]$state.baselineBytes) -LastWarnedBytes $size
    Write-WfContext 'PostToolUse' (Get-WfMessage 'threshold.md')
    exit 0
} catch { exit 0 }

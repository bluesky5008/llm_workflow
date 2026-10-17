# DES-02 - PostToolUse(*) hook.
# Warns the model to hand off at the next plan-item boundary once the context
# is large. Primary signal (v3, ADR-012): context tokens parsed from the
# transcript's newest assistant usage block. Fallback (v1, ADR-001): transcript
# byte growth since the session baseline, used only when no usage is readable.
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

    $tokens = Get-WfContextTokens $t
    if ($null -ne $tokens) {
        # ---- primary: absolute context tokens (no baseline needed) ----
        $thresholdTokens = 130000
        if ($env:CLAUDE_WF_THRESHOLD_TOKENS -match '^\d+$') { $thresholdTokens = [long]$env:CLAUDE_WF_THRESHOLD_TOKENS }
        $rewarnTokens = 20000
        if ($env:CLAUDE_WF_REWARN_TOKENS -match '^\d+$') { $rewarnTokens = [long]$env:CLAUDE_WF_REWARN_TOKENS }

        if ($tokens -lt $thresholdTokens) { exit 0 }
        $last = $null
        if ($state.PSObject.Properties['lastWarnedTokens']) { $last = $state.lastWarnedTokens }
        # A context smaller than the last warning means it was compacted since;
        # treat the new crossing as fresh instead of suppressing it.
        if ($null -ne $last -and $tokens -ge [long]$last -and ($tokens - [long]$last) -lt $rewarnTokens) { exit 0 }

        Write-WfState -Path $statePath -BaselineBytes ([long]$state.baselineBytes) -LastWarnedBytes $size -LastWarnedTokens $tokens
        $note = "`n(context_tokens=$tokens threshold=$thresholdTokens signal=usage)"
        Write-WfContext 'PostToolUse' ((Get-WfMessage 'threshold.md').TrimEnd() + $note)
        exit 0
    }

    # ---- fallback: transcript byte growth since baseline (ADR-001) ----
    $thresholdKB = 1500
    if ($env:CLAUDE_WF_THRESHOLD_KB -match '^\d+$') { $thresholdKB = [int]$env:CLAUDE_WF_THRESHOLD_KB }
    $rewarnKB = 300
    if ($env:CLAUDE_WF_REWARN_KB -match '^\d+$') { $rewarnKB = [int]$env:CLAUDE_WF_REWARN_KB }

    if (($size - [long]$state.baselineBytes) -lt ($thresholdKB * 1024)) { exit 0 }
    if ($null -ne $state.lastWarnedBytes -and ($size - [long]$state.lastWarnedBytes) -lt ($rewarnKB * 1024)) { exit 0 }

    Write-WfState -Path $statePath -BaselineBytes ([long]$state.baselineBytes) -LastWarnedBytes $size
    $note = "`n(transcript_growth_kb=$([int](($size - [long]$state.baselineBytes) / 1024)) threshold_kb=$thresholdKB signal=bytes)"
    Write-WfContext 'PostToolUse' ((Get-WfMessage 'threshold.md').TrimEnd() + $note)
    exit 0
} catch { exit 0 }

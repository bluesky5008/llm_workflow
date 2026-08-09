# DES-03 - SessionStart(compact) hook.
# After compaction, re-anchors the model on the work log as the source of
# truth and resets the transcript baseline (context shrank; growth restarts).
try {
    . (Join-Path $PSScriptRoot 'wf-common.ps1')
    $hookInput = Read-WfHookInput
    $workDir = Get-WfWorkDir $hookInput
    if (-not $workDir) { exit 0 }

    Write-WfState -Path (Get-WfStatePath $hookInput) -BaselineBytes (Get-WfTranscriptBytes $hookInput) -LastWarnedBytes $null

    $open = Get-WfOpenWorkLogs $workDir
    if ($open.Count -eq 0) { exit 0 }
    $list = ($open | ForEach-Object { "- docs/work/$_/work-log.md" }) -join "`n"
    Write-WfContext 'SessionStart' ((Get-WfMessage 'post-compact.md').TrimEnd() + "`n" + $list)
    exit 0
} catch { exit 0 }

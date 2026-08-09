# DES-01 - SessionStart(startup|resume|clear) hook.
# Injects resume context when the current repo has open work logs, and records
# the transcript-size baseline consumed by wf-context-threshold.ps1.
try {
    . (Join-Path $PSScriptRoot 'wf-common.ps1')
    $hookInput = Read-WfHookInput
    $workDir = Get-WfWorkDir $hookInput
    if (-not $workDir) { exit 0 }

    Write-WfState -Path (Get-WfStatePath $hookInput) -BaselineBytes (Get-WfTranscriptBytes $hookInput) -LastWarnedBytes $null

    $open = Get-WfOpenWorkLogs $workDir
    if ($open.Count -eq 0) { exit 0 }
    $list = ($open | ForEach-Object { "- docs/work/$_/work-log.md" }) -join "`n"
    Write-WfContext 'SessionStart' ((Get-WfMessage 'resume.md').TrimEnd() + "`n" + $list)
    exit 0
} catch { exit 0 }

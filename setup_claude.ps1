<#
.SYNOPSIS
Install llm_workflow skills (wf-design, wf-implement) into Claude Code.

.DESCRIPTION
Creates junctions from ~/.claude/skills to this repo's skills/ folder and
installs the global workflow rules (CLAUDE.global.md) into ~/.claude/CLAUDE.md.
Idempotent: safe to re-run. Skills stay up to date via "git pull" because
junctions point into the repo.

.NOTES
Windows only (junctions). On macOS/Linux use symlinks instead - see README.
#>

$ErrorActionPreference = 'Stop'

$repoRoot  = $PSScriptRoot
$skillsSrc = Join-Path $repoRoot 'skills'
$claudeDir = Join-Path $env:USERPROFILE '.claude'
$skillsDir = Join-Path $claudeDir 'skills'
$globalMd  = Join-Path $claudeDir 'CLAUDE.md'
$template  = Join-Path $repoRoot 'CLAUDE.global.md'

if (-not (Test-Path $skillsSrc)) { throw "skills folder not found: $skillsSrc" }
if (-not (Test-Path $template))  { throw "template not found: $template" }

New-Item -ItemType Directory -Force $skillsDir | Out-Null

# 1) Link each skill into ~/.claude/skills via junction
Get-ChildItem $skillsSrc -Directory | ForEach-Object {
    $link = Join-Path $skillsDir $_.Name
    if (Test-Path $link) {
        Write-Host "[skip] skill '$($_.Name)': already exists at $link"
    } else {
        New-Item -ItemType Junction -Path $link -Target $_.FullName | Out-Null
        Write-Host "[ok]   skill '$($_.Name)': junction -> $($_.FullName)"
    }
}

# 2) Install global workflow rules into ~/.claude/CLAUDE.md
$rules = Get-Content -Raw -Encoding UTF8 $template
if (-not (Test-Path $globalMd)) {
    Set-Content -Path $globalMd -Value $rules -Encoding UTF8
    Write-Host "[ok]   CLAUDE.md: created $globalMd"
} elseif ((Get-Content -Raw -Encoding UTF8 $globalMd) -match 'wf-design') {
    Write-Host "[skip] CLAUDE.md: workflow rules already present"
} else {
    Add-Content -Path $globalMd -Value "`r`n$rules" -Encoding UTF8
    Write-Host "[ok]   CLAUDE.md: appended workflow rules"
}

Write-Host ''
Write-Host 'Done. Open a NEW Claude Code session and verify with /wf-design.'

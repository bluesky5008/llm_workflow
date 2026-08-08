<#
.SYNOPSIS
Install llm_workflow skills (wf-design, wf-implement, wf-doc) into Claude Code.

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

# 1) Link each skill into ~/.claude/skills via junction.
#    Verify the target too: a junction left over from a previous repo location
#    would silently keep pointing at the old path.
Get-ChildItem $skillsSrc -Directory | ForEach-Object {
    $link = Join-Path $skillsDir $_.Name
    $item = if (Test-Path $link) { Get-Item $link -Force } else { $null }
    $target = if ($item -and $item.LinkType) { @($item.Target)[0] } else { $null }

    if ($target -eq $_.FullName) {
        Write-Host "[skip] skill '$($_.Name)': junction already points here"
    } elseif ($item -and -not $item.LinkType) {
        Write-Host "[warn] skill '$($_.Name)': $link exists and is not a link - left unchanged"
    } elseif ($item) {
        # Deletes the reparse point only; the target directory is untouched.
        [System.IO.Directory]::Delete($link)
        New-Item -ItemType Junction -Path $link -Target $_.FullName | Out-Null
        Write-Host "[ok]   skill '$($_.Name)': retargeted from '$target' -> $($_.FullName)"
    } else {
        New-Item -ItemType Junction -Path $link -Target $_.FullName | Out-Null
        Write-Host "[ok]   skill '$($_.Name)': junction -> $($_.FullName)"
    }
}

# 2) Install global workflow rules into ~/.claude/CLAUDE.md.
#    Existing installs get any template rule lines they are missing, so rules
#    added to CLAUDE.global.md later still reach them on re-run. Reworded lines
#    are appended as new rules; removing the outdated wording stays manual.
$rules = Get-Content -Raw -Encoding UTF8 $template
$ruleLines = @($rules -split "`r?`n" | Where-Object { $_ -match '^- ' })
if (-not $ruleLines) { throw 'no rule lines found in CLAUDE.global.md' }
if (-not (Test-Path $globalMd)) {
    Set-Content -Path $globalMd -Value $rules -Encoding UTF8
    Write-Host "[ok]   CLAUDE.md: created $globalMd"
} else {
    $installedRules = Get-Content -Raw -Encoding UTF8 $globalMd
    if ($installedRules -notmatch 'wf-design') {
        Add-Content -Path $globalMd -Value "`r`n$rules" -Encoding UTF8
        Write-Host "[ok]   CLAUDE.md: appended workflow rules"
    } else {
        $installed = @($installedRules -split "`r?`n" | ForEach-Object { $_.Trim() })
        $missing = @($ruleLines | Where-Object { $installed -notcontains $_.Trim() })
        if ($missing) {
            Add-Content -Path $globalMd -Value ($missing -join "`r`n") -Encoding UTF8
            $missing | ForEach-Object { Write-Host "[ok]   CLAUDE.md: added rule: $_" }
        } else {
            Write-Host "[skip] CLAUDE.md: workflow rules already present"
        }
    }
}

Write-Host ''
Write-Host 'Done. Open a NEW Claude Code session and verify with /wf-design or /wf-doc.'

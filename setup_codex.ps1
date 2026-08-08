<#
.SYNOPSIS
Install llm_workflow rules (wf-design, wf-implement, wf-doc) into OpenAI Codex CLI.

.DESCRIPTION
Appends the workflow entry rules (AGENTS.codex.md, with this repo's absolute
path substituted) to ~/.codex/AGENTS.md, and creates /wf-design,
/wf-implement, and /wf-doc custom prompts in ~/.codex/prompts that point at
the SKILL.md files in this repo. Idempotent: safe to re-run. Because the rules reference
files inside the repo, "git pull" keeps the workflow up to date.

.NOTES
Codex has no on-demand skill loading, so only the short entry rules are
always-loaded; the detailed procedures are read from the repo when needed.
Do not move or delete this repo after installation - the rules point into it.
#>

$ErrorActionPreference = 'Stop'

$repoRoot   = $PSScriptRoot
$codexDir   = Join-Path $env:USERPROFILE '.codex'
$agentsMd   = Join-Path $codexDir 'AGENTS.md'
$promptsDir = Join-Path $codexDir 'prompts'
$template   = Join-Path $repoRoot 'AGENTS.codex.md'

foreach ($p in @((Join-Path $repoRoot 'skills\wf-design\SKILL.md'),
                 (Join-Path $repoRoot 'skills\wf-implement\SKILL.md'),
                 (Join-Path $repoRoot 'skills\wf-doc\SKILL.md'),
                 $template)) {
    if (-not (Test-Path $p)) { throw "required file not found: $p" }
}

New-Item -ItemType Directory -Force $codexDir | Out-Null
New-Item -ItemType Directory -Force $promptsDir | Out-Null

# 1) Append workflow rules to global AGENTS.md (repo path substituted)
$rules = (Get-Content -Raw -Encoding UTF8 $template).Replace('{{REPO}}', $repoRoot)
$wfDocRule = $rules -split "`r?`n" | Where-Object { $_ -match 'wf-doc' } | Select-Object -First 1
if (-not $wfDocRule) { throw 'wf-doc rule not found in AGENTS.codex.md' }
if (-not (Test-Path $agentsMd)) {
    Set-Content -Path $agentsMd -Value $rules -Encoding UTF8
    Write-Host "[ok]   AGENTS.md: created $agentsMd"
} else {
    $installedRules = Get-Content -Raw -Encoding UTF8 $agentsMd
    if ($installedRules -notmatch 'wf-design') {
        Add-Content -Path $agentsMd -Value "`r`n$rules" -Encoding UTF8
        Write-Host "[ok]   AGENTS.md: appended workflow rules"
    } elseif ($installedRules -notmatch 'wf-doc') {
        Add-Content -Path $agentsMd -Value $wfDocRule -Encoding UTF8
        Write-Host "[ok]   AGENTS.md: added wf-doc rule"
    } else {
        Write-Host "[skip] AGENTS.md: workflow rules already present"
    }
}

# 2) Custom prompts for manual invocation (/wf-design, /wf-implement, /wf-doc).
#    Generated pointers - overwritten on each run so paths stay correct.
$prompts = @{
    'wf-design.md'    = "Read the file ``$repoRoot\skills\wf-design\SKILL.md`` and follow the workflow it defines for the current task. Communicate with the user in the user's language."
    'wf-implement.md' = "Read the file ``$repoRoot\skills\wf-implement\SKILL.md`` and follow the workflow it defines for the current task. Communicate with the user in the user's language."
    'wf-doc.md'       = "Read the file ``$repoRoot\skills\wf-doc\SKILL.md`` and use its common format for workflow documents in the current task. Communicate with the user in the user's language."
}
foreach ($name in $prompts.Keys) {
    Set-Content -Path (Join-Path $promptsDir $name) -Value $prompts[$name] -Encoding UTF8
    Write-Host "[ok]   prompt '/$($name -replace '\.md$','')': $promptsDir\$name"
}

Write-Host ''
Write-Host 'Done. Start a new Codex session; rules load from ~/.codex/AGENTS.md.'
Write-Host 'Manual invocation: /wf-design, /wf-implement, or /wf-doc.'

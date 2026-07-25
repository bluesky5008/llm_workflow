<#
.SYNOPSIS
Install llm_workflow rules (wf-design, wf-implement) into OpenAI Codex CLI.

.DESCRIPTION
Appends the workflow entry rules (AGENTS.codex.md, with this repo's absolute
path substituted) to ~/.codex/AGENTS.md, and creates /wf-design and
/wf-implement custom prompts in ~/.codex/prompts that point at the SKILL.md
files in this repo. Idempotent: safe to re-run. Because the rules reference
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
                 $template)) {
    if (-not (Test-Path $p)) { throw "required file not found: $p" }
}

New-Item -ItemType Directory -Force $codexDir | Out-Null
New-Item -ItemType Directory -Force $promptsDir | Out-Null

# 1) Append workflow rules to global AGENTS.md (repo path substituted)
$rules = (Get-Content -Raw -Encoding UTF8 $template).Replace('{{REPO}}', $repoRoot)
if (-not (Test-Path $agentsMd)) {
    Set-Content -Path $agentsMd -Value $rules -Encoding UTF8
    Write-Host "[ok]   AGENTS.md: created $agentsMd"
} elseif ((Get-Content -Raw -Encoding UTF8 $agentsMd) -match 'wf-design') {
    Write-Host "[skip] AGENTS.md: workflow rules already present"
} else {
    Add-Content -Path $agentsMd -Value "`r`n$rules" -Encoding UTF8
    Write-Host "[ok]   AGENTS.md: appended workflow rules"
}

# 2) Custom prompts for manual invocation (/wf-design, /wf-implement).
#    Generated pointers - overwritten on each run so paths stay correct.
$prompts = @{
    'wf-design.md'    = "Read the file ``$repoRoot\skills\wf-design\SKILL.md`` and follow the workflow it defines for the current task. Communicate with the user in the user's language."
    'wf-implement.md' = "Read the file ``$repoRoot\skills\wf-implement\SKILL.md`` and follow the workflow it defines for the current task. Communicate with the user in the user's language."
}
foreach ($name in $prompts.Keys) {
    Set-Content -Path (Join-Path $promptsDir $name) -Value $prompts[$name] -Encoding UTF8
    Write-Host "[ok]   prompt '/$($name -replace '\.md$','')': $promptsDir\$name"
}

Write-Host ''
Write-Host 'Done. Start a new Codex session; rules load from ~/.codex/AGENTS.md.'
Write-Host 'Manual invocation: /wf-design or /wf-implement.'

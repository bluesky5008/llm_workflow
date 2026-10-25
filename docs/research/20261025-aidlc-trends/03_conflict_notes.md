# 조사 노트 — 협업 충돌 (원자료)

> 상태: 원자료(조사 트랙). [대조 문서](./00_trends_vs_workflow.md)의 근거. 서브에이전트 조사 결과를 그대로 보존. 작성 2026-10-25.

# Research notes: reducing conflicts in AI-assisted team development (as of 2026-10-25)

Legend: [V] = number verified against the source page fetched; [U] = unverified / secondary / not read in primary.

## 1. Empirical data

### 1.1 Agent PR merge conflicts
**Xu, Subramanian, Karthik, "AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates"**, arXiv 2607.04697, submitted 2026-07-06 (v2 2026-07-07). https://arxiv.org/abs/2607.04697
- Dataset AIDev-pop: 33,596 agent PRs, 2,807 repos [V]
- 40.2% of repos have co-active (temporally overlapping) agent PR pairs; these cover 79.4% of agent PRs [V]
- One-week window: 53.4% of repos, 95.0% of PRs [V]
- Only 0.5% of co-active pairs are cross-agent (122 repos) [V]
- Textual conflict rate on 747 pairs: cross-agent 41.7% vs intra-agent 19.8% (non-overlapping 95% CI) [V]
- 84.4% of conflicted files are source code (not manifests); ~42% of conflicts structural (modify/delete, add/add) [V]
- No human baseline, no PR size data in this paper [V]

### 1.2 Agent PR acceptance / failure
**"Where Do AI Coding Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub"**, arXiv 2601.15195, 2026-01-21, MSR '26. https://arxiv.org/html/2601.15195
- AIDev-pop 33,596 PRs; overall merge rate 71.48% [V]
- By agent: Codex 82.59%, Cursor 65.22%, Claude Code 59.04%, Devin 53.76%, Copilot 43.04% [V]
- Not-merged PRs are larger (Cliff's delta 17% lines, 10% files); each extra changed line ~1% lower odds of merge; each failed CI check ~15% lower odds [V]
- Rejection taxonomy (600 sampled): reviewer abandonment 38%, PR-level 31%, code-level 22%, agentic-level 2% [V]
- Duplicate/superseded PRs: 142 (23%) — i.e., overlapping parallel work is a major rejection cause [V]
- CI/test failure rejections 99 (17%) [V]

**Mazloomzadeh, Morovati, Khomh, "How Do AI Coding Agents Contribute...Agentic Pull Requests"**, arXiv 2607.21832, 2026-07-23. https://arxiv.org/html/2607.21832v1
- 220,612 closed PRs, 489 Python repos, 9,428 agentic PRs (AIDev, cut-off 2025-11-20) [V]
- Adjusted merge probability: Claude 84.3%, Codex 73.5%, Cursor 63.9%, Copilot 59.6%, Devin 43.0% [V]
- Human baseline merge rate ~0.84-0.856 per quarter [V]
- Agentic PRs "comparable or lower defect proneness" vs human, mostly non-significant [V, qualitative]

**Watanabe et al., "On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub"**, arXiv 2509.14745 (2025; data Feb 24–Apr 30 2025). https://arxiv.org/pdf/2509.14745
- 567 Claude Code PRs, 157 projects; merged 83.8% vs human 91.0% [V]
- Median files changed 2 vs 2; median added lines 48 vs 24 [V]
- 54.9% of merged agentic PRs merged without further modification (vs 58.5% human, n.s.) [V]

**Popescu et al., "Investigating Autonomous Agent Contributions in the Wild"**, arXiv 2604.00917, 2026-04-01. https://www.alphaxiv.org/abs/2604.00917
- Median lines changed: human ~60, Claude Code 376 [V via alphaxiv summary]
- Agent code churns more, lower survival at 3d/1w/3w, p<0.001 [V qualitative]

### 1.3 DORA 2025
- TechTarget, 2025-09-23: https://www.techtarget.com/searchsoftwarequality/news/366631712/Google-DORA-Software-delivery-caught-up-to-AI-coding-tools
  - AI use 76% (2024) -> 90% (2025), ~5,000 respondents [V]
  - 2024 report: each 25% increase in AI adoption associated with -1.5% throughput, -7.2% stability [V]
  - 2025: throughput now positively associated; instability still a concern ("throughput inching up before instability goes down") [V qualitative]
  - Seven AI capabilities incl. "strong version control practices" and "working in small batches" [V]
- Google Cloud blog, 2025-09-23: https://cloud.google.com/blog/products/ai-machine-learning/introducing-doras-inaugural-ai-capabilities-model
  - "Working in small batches ... amplifies the positive influence of AI on product performance and reduces friction" [V quote]
  - "frequent commits amplify AI's positive influence on individual effectiveness, while frequent use of rollback features boosts performance of AI-assisted teams" [V quote]; no effect sizes on page
- DX Engineering Enablement podcast summary, 2025-11-21: https://newsletter.getdx.com/p/doras-2025-research-on-the-impact
  - "Code review becomes the dominant bottleneck"; "AI ... intensifies what already exists"; 5 metrics (throughput + instability incl. rework rate) [V]
- Faros AI reports (Productivity Paradox Q2 2025; Acceleration Whiplash Q2 2026; Speed Trap Q3 2026): https://faros.ai/research — commonly cited "PR size +154%, review time +91%" NOT verified (numbers not on landing page) [U]

## 2. Techniques

### 2.1 LLM merge-conflict resolution — accuracy
- **Merge-Bench**, arXiv 2605.25890 (2026-05): 7,938 hunks, 1,439 repos. Java exact match: Gemini 2.5 Pro 54.7% (62.5% normalized), o3 Pro 46.1%, Claude Opus 4 44.4% (51.2%); fine-tuned LLMergeJ 14B 48.8% (58.9%). 11 languages: Gemini 2.5 Pro 47.1%/52.6%, Opus 4 40.3%/44.8% [V] https://arxiv.org/html/2605.25890v1
- **Shen, "Can LLMs Resolve Real Java Merge Conflicts?"**, arXiv 2607.27674, 2026-07-30: LLMs match developer resolution ~55% (conservative floor); 55-59% vs 36.7% for best traditional tool (AutoMerge); gap mostly coverage — traditional tools abstain on 20-90% [V] https://arxiv.org/abs/2607.27674v1
- **Campos Junior & Murta, LLM vs search-based**, arXiv 2605.16646 (2026-05): MergeGen avg similarity 90.0% vs SBCR 79.9%; perfect matches 55% vs 19.6% (Java) [V] https://arxiv.org/html/2605.16646v1
- Takeaway: ~half of real conflicts resolved exactly as humans did -> LLM resolution must be reviewed + tested, not trusted blindly.
- **GitHub Copilot**: "@copilot merge in main and resolve the conflicts" on PRs, 2026-03-26; agent verifies build/tests then pushes [V] https://github.blog/changelog/2026-03-26-ask-copilot-to-resolve-merge-conflicts-on-pull-requests/ ; "three clicks" 2026-04-13; mobile 2026-07-08 [U: titles only]

### 2.2 Structural merge (mergiraf)
- LWN 2025-10-31: https://lwn.net/SubscriberLink/1042355/434ad706cc594276/
  - Rust, GPLv3, tree-sitter, 33 languages; configure as git merge driver via gitconfig + .gitattributes; `mergiraf review`, `mergiraf solve` [V]
  - Linux kernel: 7,415 conflicting merges; mergiraf fully resolved 428 (~5.8%) [V] -> modest gain
  - Same-region edits still need humans [V]

### 2.3 union merge driver
- git docs (gitattributes, `union`): "take lines from both versions, instead of leaving conflict markers. This tends to leave the added lines in the resulting file in random order and the user should verify the result. Do not use this if you do not understand the implications." [V via git.git commit 0e545f7] https://rtime.ciirc.cvut.cz/gitweb/git.git/commitdiff_plain/0e545f75169e2c260dfb4445203c23cafdfc76ef
- Forges may not honor .gitattributes drivers in server-side conflict check (GitLab issue 17325 requested it) — Gitea behaviour UNVERIFIED [U]. Custom drivers (mergiraf, bd merge) only run on client machines that configured them.

### 2.4 File-per-entry layouts
- PyInstaller docs: "To avoid merge conflicts, we use the towncrier package"; per-PR "news fragments" compiled at release [V] https://pyinstaller.org/en/stable/development/changelog-entries.html
- GitLab 2015-02-10: 100 placeholder lines in CHANGELOG to spread insertions; headline claims 90% fewer conflicts (figure in headline only) [V/partially] https://about.gitlab.com/blog/2015/02/10/gitlab-reduced-merge-conflicts-by-90-percent-with-changelog-placeholders
- Beads (Yegge), v0.24.3 2025-11-24: sequential IDs collided across concurrent branches -> switched to hash IDs ("concurrent creation collision-free"), plus custom JSONL merge driver `bd merge` [V] https://pkg.go.dev/github.com/steveyegge/beads@v0.24.3
- Spec Kit issue #2047: proposal for configurable feature-ID strategy, explicitly avoiding "a central registry, which could cause merge conflicts"; built-ins are sequential 001- or timestamp prefixes [V, no date] https://github.com/github/spec-kit/issues/2047
- (Implication for docs/test-register.md, docs/status.md tables: move to one file per record + generated index; IDs by timestamp/hash not by "next number".)

### 2.5 Stacked PRs / merge queue
- GitHub native stacked PRs (public preview; 2026, ~April per news): rules evaluated against stack base; atomic landing; merge queue support; `gh stack` [V] https://docs.github.com/en/pull-requests/reference/stacked-pull-requests
- Gitea: no native stacked PRs found (Discourse question unanswered) [V absence-in-sources; U overall]
- gitea-mq (Mic92) v0.2.0 2026-10-10: external merge queue for Gitea >=1.22 + PostgreSQL; registers as required status check, hooks "merge when checks succeed", builds temp gitea-mq/<pr> branch for CI; optional bors-style batching [V] https://pkg.go.dev/github.com/Mic92/gitea-mq
- Gitea has no native merge queue (not mentioned in 28.0.0 release; external tool exists) [U: inferred]

### 2.6 Gitea features (2026)
- Gitea 28.0.0 released 2026-09-30 (dropped "1." prefix) [V] https://blog.gitea.com/release-of-28.0.0/
  - NEW: branch protection option "blocks merging until every matching CODEOWNERS rule is approved by one of its code owners or a member of a listed team" [V]
  - Bot accounts for automation (token auth, no interactive login) [V] — useful for agent identities
  - automerge fixes [V]
- Earlier: CODEOWNERS only auto-requested reviewers; not enforceable (issue #32602, on 1.21.11) [V]
- Protected branches docs: required approvals, dismiss stale approvals, block on rejected reviews, block on outstanding review requests (incl. CODEOWNERS), block outdated branch, status-check patterns, protected/unprotected file patterns, merge allowlist, signed commits [V] https://docs.gitea.com/usage/access-control/protected-branches/

## 3. Multi-agent / multi-human coordination

- **Claude Code docs "Run agents in parallel"** (current): five approaches (subagents, agent view, agent teams [experimental, off by default], dynamic workflows, projects); worktrees give each session a separate checkout; "Agent teams don't isolate teammates in worktrees, so partition the work so each teammate owns a different set of files"; `/batch` splits a large change into 5-30 worktree-isolated subagents; cross-session messaging [V] https://code.claude.com/docs/en/agents
- **"Passes Alone, Fails Together"** (Xia, Wu, Park), arXiv 2609.25396, 2026-09-21: real Django PR pairs -> interference in 1 of 834 runs; constructed shared-helper tasks -> 97% interference; a message describing the concurrent completed change recovered 82% of runs [V] https://arxiv.org/abs/2609.25396v1
  - Reading: semantic conflicts are rare in naturally-separated work but near-certain when parallel tasks touch the same shared helper; communicating the other change mostly fixes it.
- **Co-Coder / Cohesion-aware partitioning**, arXiv 2606.00953, 2026-05-31: dependency graph + isolate hub files + community detection + dependency-aware scheduler -> up to +14.0% pass rate, 2.10x speedup, -35% API cost vs sequential/file-based parallel/Claude Code Agent Teams [V] https://arxiv.org/abs/2606.00953
- **NP-Bench + scheduling planner** (Muku), arXiv 2610.07261, 2026-10-05: without planner 13 merge conflicts, 1/9 clean integration; with planner 9/9 clean, 0 conflicts; breaking contract change clean-integration 0 -> 1.0 (frontier), 0.6 (small) [V; small benchmark] https://arxiv.org/abs/2610.07261
- **AgentRoom** (CRDT shared workspace), arXiv 2608.23740, 2026-08-24: authors conclude coordination, not parallelism/CRDT merging, drives gains; no effect sizes in abstract [V] https://arxiv.org/abs/2608.23740
- **Daniel Vaughan blog** (Codex-focused), 2026-07-28 (upd. 2026-10-25): worktree isolation is baseline but not sufficient; file-ownership via task scoping documented in AGENTS.md; claim protocol before work (cites agent-traffic-control); early detection via `git merge-tree` in PostToolUse hooks; sequential merging with rebase + CI [V; secondary] https://codex.danielvaughan.com/2026/07/28/agent-pr-merge-conflicts-concurrent-coding-agents-codex-cli-worktree-isolation-coordination-defence/
- **Microsoft Learn — Spec Kit team collaboration**: one spec owner per feature; constitution with designated maintainers, changes by team approval; spec-first commits reviewed before plan; update spec -> plan -> tasks in order; classify conflicts (requirement/technical/priority); define integration contracts owned by API owner [V] https://learn.microsoft.com/en-us/training/modules/spec-driven-development-github-spec-kit-enterprise-developers/10-scale-spec-driven-development-team-collaboration
- **Agent READMEs study**, arXiv 2511.12884 (v2 2026-08-09): 2,303 context files / 1,925 repos; files evolve like config code via frequent small additions; test procedures 75.9%, implementation 70.8%, architecture 68.1%, security 14.8%, performance 14.5% [V] https://arxiv.org/abs/2511.12884
- AGENTS.md "best practices" blogs (tembo, promptshelf, etc.) not read — [U]

## Gaps / unverified
- Faros PR-size/review-time numbers [U]
- Whether Gitea server-side merge honors `merge=union` [U]
- Gitea native stacked PRs / merge queue: none found [U absence]
- Copilot "three clicks" / mobile features: titles only [U]

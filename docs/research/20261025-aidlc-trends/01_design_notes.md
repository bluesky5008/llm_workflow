# 조사 노트 — AI 설계 (원자료)

> 상태: 원자료(조사 트랙). [대조 문서](./00_trends_vs_workflow.md)의 근거. 서브에이전트 조사 결과를 그대로 보존. 작성 2026-10-25.

# AI-assisted software DESIGN — research notes (as of 2026-10-25)

Scope: does AI do design well, what design-process methods work, AWS AI-DLC status.
Every number below was read on the source page cited (WebFetch, or a local git clone of the repo). Anything I could not open is marked UNVERIFIED.
Not re-reported (user already has these): arXiv 2602.00180, 2604.26275, han.guru AI-DLC 2026, 2511.09794, Codified Context, Skills considered harmful, 2602.11988.

---

## Q1. Is AI good or bad at software design? Empirical evidence

### 1.1 Knowledge vs. open-ended design: a large gap
- **SAKE benchmark**, arXiv 2606.29520v1, 2026-06-28. https://arxiv.org/html/2606.29520
  - 2,154 four-option MCQs (2,114 scored), 8 categories (GoF patterns, quality attributes, architectural solutions/styles, etc.), 11 models.
  - Accuracy: zero-shot 90.96% (GPT 5.4 Nano) to 93.95% (GPT 5.4); five-shot 89.31% to 94.23% (Claude Opus 4.6).
  - Weakest category is trade-off-heavy "Architectural Solutions" (zero-shot mean 89.5%, five-shot 88.4%). Longer prompts help recall but *hurt* this category (Grok 4.1 Fast: 100% on short prompts, <=91.7% above 135 words). The authors call this "distractor density". Five-shot examples do not reliably help.
  - Takeaway: models "know" textbook architecture (~90%+), but this does not test open design.
- **R2ABench** (requirements to architecture), arXiv 2604.06683v1, 2026-04-08. https://arxiv.org/html/2604.06683v1
  - 17 PRDs with expert PlantUML reference diagrams. Models: GPT-5, Claude Sonnet 4.6, Gemini 2.5 Pro, DeepSeek-V3.2, Qwen3-coder, plus MetaGPT and OpenHands.
  - Node (component) F1 macro average 0.571 (best GPT-5 at 0.67). **Edge (relationship) F1 macro average only 0.130** (best 0.176). The paper: LLMs "fundamentally struggle with relational reasoning."
  - Judge scores: completeness 4.36 vs. accuracy 3.76, i.e. more complete than correct (unsupported elements).
  - Orphan-component ratio 15.96% on average, rising to 20.23% with minimal context (DeepSeek+OpenHands 33.48%). God-component ratio 4.00%.
  - **Agent frameworks often made things worse** (MetaGPT lowered Node F1; OpenHands dropped Qwen3 syntax validity from 0.82 to 0.59).
- **LLMs applying architectural patterns**, MDPI *AI* 7(6):195, published 2026-05-27. https://www.mdpi.com/2673-2688/7/6/195
  - Pattern adherence drops as complexity grows; only large models consistently preserved microservice properties.
  - Failure modes: business logic in the presentation layer, unnecessary tiers or classes (over-engineering), **pattern bias** (three-tier produced when MVC was requested), microservices defaulting to a shared DB, omitted functionality, hallucinated relations.
  - "Self-reported architectural metrics from LLMs should be treated with caution": nearly all models had success rates below 50% on them.
  - A structured SRS helped large commercial models but was neutral or negative for small or local models.

### 1.2 Design rationale and ADRs
- **Design rationale generation**, Zhou, Li, Liang et al., arXiv 2504.20781 (ACM TOSEM, DOI 10.1145/3785010). https://arxiv.org/html/2504.20781v1
  - 100 architecture problems with expert design rationale. Averages across 5 (older) LLMs: precision 0.278/0.237/0.267 and recall 0.627/0.684/0.715 for zero-shot/CoT/multi-agent.
  - LLMs produce 4.55 to 5.77 arguments per decision, against **1.98 for experts**: high recall, low precision, verbose.
  - 64 to 69% of the unmatched arguments were still "helpful"; misleading arguments were 1.6 to 3.2%.
  - The multi-agent setup gave the best recall and fewest misleading arguments, at about 20 rounds per decision.
- **Context strategies for ADR generation**, arXiv 2604.03826v2, 2026-04-15. https://arxiv.org/html/2604.03826v2
  - More than 4,500 ADRs from 750 repos.
  - Supplying prior ADRs helps: Gemini 2.5 BERTScore 0.8199 to 0.8421 (all prior ADRs) and 0.8440 (last 3). BLEU 0.019 to 0.076.
  - **Recommendation: feed the last 3 to 5 ADRs** (near-optimal and cheap). Use retrieval for cross-cutting decisions.
  - Without context, output averaged 1,123 tokens per ADR against a ground truth of about 527 (2x verbosity). "Context strategy matters more than model size."
- **Detecting ADR violations in code**, arXiv 2602.07609v1, 2026-02-07. https://www.arxiv.org/pdf/2602.07609
  - 980 ADRs from 109 repos. Accuracy 0.83 to 0.91. On a 305-decision human-validated sample, 30% were misjudged.
  - Infrastructure and deployment ADRs account for 42% of errors. Error types: semantic misreading 44.6%, missing implicit context 28.3%, domain gaps 18.5%, overgeneralization 8.7%.
  - Good at explicit, code-visible decisions; unreliable for organizational or infra decisions.
- **GADR** (ADRs from meeting transcripts), arXiv 2608.17694v1 (2026, date not on page). https://arxiv.org/html/2608.17694v1
  - Extract, critique, refine loop. 17 ADRs covered about 18 of 23 expert-identified decisions; 52 of 55 participant evaluations agreed with the extracted decision.
  - Failure mode: tentative discussion recorded as an accepted decision, plus unsupported details from retrieval.

### 1.3 Design erosion when agents evolve code (most relevant to "design that survives change")
- **SlopCodeBench**, arXiv 2603.24755 (March 2026), NeurIPS 2026 poster. https://arxiv.org/html/2603.24755 and https://neurips.cc/virtual/2026/poster/138903
  - 36 problems with 196 checkpoints; specs reveal new requirements progressively; 15 models.
  - No agent solves any problem end-to-end. Best strict solve rate 14.8% (GPT 5.5 in the current HTML version).
  - Erosion rises in 77% of trajectories and verbosity in 75.5%. Functions with cyclomatic complexity >= 10 go from 3.6 to 23.7.
  - Against 473 human Python repos: agent code is 2.3x more verbose and 2.0x more eroded, and degrades about 7x (verbosity) and 5x (erosion) faster per checkpoint.
  - **Quality-focused prompts reduce initial erosion by up to 62.3% and verbosity by up to 34.8% (HTML version; the NeurIPS abstract says "up to a third"), but do not stop degradation**, and add about 12% cost.
  - HumanLayer replication (repo file, Oct 2026): https://github.com/humanlayer/advanced-context-engineering-for-coding-agents (benchmarking-opus-5-on-slop-code-bench.md). Opus 5 scored 4 of 17 strict checkpoints (~24%) on a 3-problem subset, writing 5x the functions of Opus 4.8. This is a small, informal run.
- **AI-generated smells**, arXiv 2605.02741v1, 2026-05-04. https://arxiv.org/html/2605.02741
  - In MetaGPT-built systems, the dominant smells form "God Class" and "Modular Mirage" patterns.
  - LOC correlates with architectural smells at Spearman rho = 0.94 ("Volume-Quality Inverse Law").
  - Long Method: Qwen 480B 11 instances, Gemini 5, human 1. Few-shot prompting did not reduce it.
- **SmellBench**, arXiv 2605.07001v2, 2026-05-12. https://arxiv.org/html/2605.07001
  - 65 hard architectural smells in scikit-learn. 63.1% of tool-flagged smells were false positives.
  - Best agent fixed 31 of 65 (47.7%) but **introduced 140 new smells (net -109)**; Gemini 3.1 Pro fixed 19 and introduced 3 (net +16).
  - With a structured protocol, false-positive identification reached kappa 0.94; the bare baseline reached 0.00.
- **Erik Doernenburg, CCMenu**, martinfowler.com, 2026-01-27 (anecdote). https://martinfowler.com/articles/exploring-gen-ai/ccmenu-quality.html
  - Agent ignored existing URL helpers (duplicated logic), added an unexplained cache, carried over GitHub-specific logic that GitLab doesn't need, and "fixed" a type mismatch with `?? ""` instead of a one-character `?`.
- **Böckeler, SDD tools**, 2025-10-15. https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
  - The agent ignored research notes describing existing classes and regenerated them as duplicates (a design-level "ignore existing conventions" failure).

### 1.4 How developers use LLMs for design
- arXiv 2605.01392 (v2, 2026-09-19): 291 GitHub ChatGPT design conversations plus a survey of 65 practitioners. Most use is at the detailed-design level, for knowledge acquisition. Limitations reported: long outputs, wrong code, dependence on project context. No percentages in the abstract. https://arxiv.org/abs/2605.01392
- arXiv 2604.09120 (FSE Companion '26): 18 pairs designing with an LLM. **Only 3 of 18 pairs asked it for alternatives**, so anchoring on the first answer was common; design quality was not measured. https://arxiv.org/html/2604.09120
- arXiv 2603.28914 (2026-03-30), ATAM with Copilot+RAG: the LLM generates more candidate risks and trade-offs than students (6 vs. 2 trade-offs in G3) but over-flags risks; "outperforms humans at generating candidate risks, but not at evaluating them." No significant difference from experts. https://arxiv.org/html/2603.28914
- Agentic PR studies (AIDev dataset):
  - arXiv 2601.15195: 71.48% of 33k agentic PRs merged; "unwanted features" (not aligned with project goals, added complexity) is 4% of rejections. https://www.alphaxiv.org/abs/2601.15195
  - arXiv 2605.22534 (MSR '26): reviewers of merged PRs mostly enforced tests, CI and repository conventions. https://arxiv.org/html/2605.22534v1
- UNVERIFIED: "Vibe architecting ... comparative case study of LLM-guided system design", JSS 2026, S0164121226003778. ScienceDirect blocked the fetch.

**Q1 verdict:**
- LLMs are strong at architectural *knowledge* and at *generating candidates* (components, risks, trade-offs, rationale arguments: high recall).
- They are weak at *relationships and integration* (edge F1 0.13), *precision and selection* (2 to 3x more arguments than experts), trade-off-heavy choices, respecting the existing codebase, and keeping design quality over iterations (erosion 5x faster than humans).
- Agentic multi-role frameworks do not reliably help. Verbosity and over-building are a consistent failure signature.

---

## Q2. Design-process methods: evidence vs. hype

### 2.1 Plan or spec first: works, but plan *quality* and *enforcement* matter more than having a plan
- **Plan compliance**, arXiv 2604.12147v2, 2026-04-28. https://arxiv.org/html/2604.12147v2
  - 16,991 SWE-agent trajectories. Following a standard plan improves resolution; removing it hurts.
  - **"A subpar plan hurts performance even more than no plan at all."** Adding phases that conflict with the model's own strategy degrades results. Periodic plan reminders reduce violations and improve success.
  - Compliance drops about 13% on SWE-bench Pro.
- **Plan declaration vs. execution gap**, arXiv 2609.38108v1, 2026-09-29. https://arxiv.org/html/2609.38108v1
  - Plans placed in context but not enforced were followed in only about 22 to 45% of trajectories. Adherence collapses on longer plans (ALFWorld 6 to 7 steps: 4.8 to 21.4%).
  - Enforcing the structure in control flow raised success from 0.36 to 0.44 on SWE-bench Verified and 0.48 to 0.92 on ALFWorld.
  - **Implication: enforce plan steps deterministically (hooks or an engine) rather than trusting the prompt.**
- **Harness design**, arXiv 2609.20804v1, 2026-09-17. https://arxiv.org/html/2609.20804v1
  - A persistent plan tool gives +11.6 points on SWE-bench for a 30B model.
  - For large models it is roughly neutral on success (-2.0 and -0.4 points) but cuts cost by about 30% and shortens trajectories (108 to 74 turns).
- **Anthropic Claude Code best practices** (current docs, fetched 2026-10-25). https://code.claude.com/docs/en/best-practices
  - Explore, then plan, then implement, then commit, in plan mode. Skip the plan "if you could describe the diff in one sentence."
  - "Let Claude interview you" with AskUserQuestion, write SPEC.md, then **implement in a fresh session**.
  - Good specs "name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step."
  - Adversarial review subagent in a fresh context, with a warning: a reviewer told to find gaps will find some; "chasing every finding leads to over-engineering". Restrict findings to correctness and stated requirements.
- **HumanLayer ACE / research-plan-implement** (repo, original article Aug 2025). https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md
  - "A bad line of a plan could lead to hundreds of bad lines of code"; a bad line of research, thousands.
  - Keep context use at 40 to 60%; humans review research and plans, not code.
  - Anecdotes: 35k LOC shipped to BAML in 7 hours (3 hours research and planning, 4 hours implementation). The research-based plan fixed the bug "in the best place"; the no-research plan also "would have worked." Not a controlled study.

### 2.2 Design by interview / clarifying questions: strong evidence it matters; agents don't do it unprompted
- **Ambig-SWE**, arXiv 2502.13069v3 (rev. 2026-02-21). https://arxiv.org/html/2502.13069v3
  - Interaction improves resolve rates on underspecified issues by up to 74%. Claude Sonnet 4 recovers about 89% of full-spec performance.
  - **Models almost never ask unless prompted.** Prompting alone is unreliable: detection accuracy 0.74 to 0.89 for Sonnet 4, while some models sit at chance.
- **UnderSpecBench**, arXiv 2607.02294v1, 2026-07-02. https://arxiv.org/html/2607.02294v1
  - 55.8 to 67.8% of runs violate at least one boundary. Agents still act 58.5% of the time under the vaguest intent.
  - Ask rate varies by harness: Haiku 4.5 asks 44.5% in Claude Code vs. 38.3% in OpenCode.
  - When agents act on an ambiguous target, safe success falls from 67.9% to 8.6%.
  - Asking tracks target ambiguity, **not** blast radius.
- **Ask or Assume?**, arXiv 2603.26233 (v2 2026-06-03). Separating underspecification detection from execution (multi-agent) reached a 69.40% resolve rate, "significantly higher" than single-agent (baseline figure not on the abstract page). https://arxiv.org/abs/2603.26233
- **Kiro requirements analysis** (blog, 2026-05-12). https://kiro.dev/blog/deep-spec-analysis/
  - EARS refinement, LLM auto-formalization to SMT-LIB, then a solver finds conflicts and gaps. Ambiguity is detected via "semantic entropy" over sampled formalizations. Findings are surfaced as two-option questions.
  - No accuracy numbers for Kiro itself (lightweight formal methods, product-level evidence only). Worked example: 5 criteria became 8.

### 2.3 Spec-driven development tools: positive on grounding, but overhead and review burden are the main critiques
- **Spec Kit Agents**, arXiv 2604.05278v1, 2026-04-07. https://arxiv.org/html/2604.05278v1
  - 128 runs. Discovery and validation hooks added +0.15 judged quality (3.51 to 3.66, p<0.05) and +1.7 points on SWE-bench Lite.
  - **Cost: +13.2 minutes (24.0 to 37.2).**
  - Human preference: Full (no hooks) won 19, hooks won 8, 33 ties. Gains are small; the main benefit is catching hallucinated APIs and paths early.
- **EPIC framework**, arXiv 2610.07534 (received 2026-10-05). https://arxiv.org/pdf/2610.07534
  - 40 spec-quality practices across 10 dimensions (Expressive/Precise/Interpretable/Compartmentalized), derived from 114 repos.
  - Top vs. bottom third of spec quality: bug-fix commits 11.8% vs. 20.4%, vulnerabilities per KLOC 0.092 vs. 0.178. Observational only.
- **Spec-driven test generation** (Google), arXiv 2608.17177v2, 2026-08. Writing pre-conditions, post-conditions and undefined behaviors first gives +9.8 points of bug detection (p=0.035) and +2.5 points of branch coverage. https://arxiv.org/abs/2608.17177
- **Naresh Jain, "Are Harnesses Worth the Cost?"**, martinfowler.com, 2026-10-13. https://martinfowler.com/articles/are-harnesses-worth-the-cost.html
  - Executable OpenAPI/AsyncAPI contracts with examples, judged by 178 hidden acceptance tests.
  - Cheap model: 3/10 to 10/10 accepted with the harness. Frontier model: already 10/10, the harness only adds cost (~10.5x tokens, ~6.6x estimated cost).
  - Misses clustered at protocol boundaries. Executable specs work best as an independent final gate.
- **Böckeler**, 2025-10-15: three SDD levels (spec-first / spec-anchored / spec-as-source).
  - Kiro turned a small bug into 4 user stories with 16 acceptance criteria ("sledgehammer to crack a nut").
  - Spec Kit produced many repetitive markdown files; "I'd rather review code than all these markdown files."
  - Agents still ignore instructions ("illusion of control"). Spec-as-source risks combining MDD's inflexibility with LLM non-determinism.
- **Böckeler, "TDD inside the agent loop"**, 2026-08-10 (small, informal). https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html
  - Non-TDD solutions often ranked higher; small-task design scores 8.67/8.0 vs. 7.33/6.67. Mutation scores showed no meaningful difference. TDD cost 3 to 8.5x the tokens.
  - **"The TDD instructions actively work against such an up front design step"**: design emerged from small decisions and was rarely revisited.
  - She stopped prompting test-first; recommends mutation testing, static analysis, and periodic modularity reviews instead.
  - **Directly relevant: if TDD follows design, keep an explicit up-front design step and refactor or modularity checkpoints.**
- **Böckeler, Harness Engineering**, 2026-02-17. https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html
  - Context engineering, architectural constraints (ArchUnit, custom linters, structural tests) and "garbage-collection" agents. Code design is part of the context.
- **Kief Morris, "Humans and Agents in SE Loops"**, 2026-03-04. https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html
  - Humans should be "on the loop": fix the harness (specs, checks, workflow) rather than individual artefacts.
- **Thoughtworks Radar**
  - SDD at Assess, Nov 2025 (Vol 33). https://www.thoughtworks.com/radar/techniques/spec-driven-development
    - Critiques: elaborate and opinionated workflows; long, hard-to-review specs; possibly relearning the "bitter lesson".
  - Vol 34 (April 2026). https://www.thoughtworks.com/radar/languages-and-frameworks/github-spec-kit and digest https://agentic-ai.readthedocs.io/en/latest/AgenticTechStack/thoughtworks-radar-vol34/
    - GitHub Spec Kit at Assess (2026-04-15): the constitution helps keep agents inside architectural boundaries. Rework in brownfield comes from "unclear intent, hidden assumptions, late constraints". Critiques: unnecessary defensive checks, verbose markdown, instruction bloat. Experienced engineers gain most.
    - Also in Vol 34: OpenSpec, Superpowers, Architecture drift reduction with LLMs, Context graph, Feedback flywheel at Assess; Feedback sensors and Agent Skills at Trial; Context engineering and curated shared instructions at Adopt; Agent instruction bloat and Codebase cognitive debt at Caution.
  - Vol 35 is not out yet; webinars are scheduled for 2026-10-28/29. https://www.thoughtworks.com/radar/technology-radar-webinar
- **Tool versions (from git clones, 2026-10-25)**
  - GitHub Spec Kit v1.2.3 (2026-10-22). Commands: constitution, specify, clarify, plan, tasks, analyze (cross-artifact consistency check), checklist, converge (new; reconciles the codebase against spec/plan/tasks), implement, taskstoissues.
  - BMAD-METHOD v6.12.4 (repo updated 2026-10-18). Its `bmad-review` adversarial lens instructs "Find at least ten issues ... If you have zero findings, re-check". This is a forced-findings design that conflicts with Anthropic's over-engineering warning.

### 2.4 Multiple alternatives, critique and adversarial review
- **Adversarial Review**, arXiv 2608.18167v1, 2026-08-16. https://arxiv.org/html/2608.18167
  - Reviewer plus critic iterate on a frozen artifact; the critic must label each objection as AGREE, DISAGREE_EVIDENCE (citing code) or DISAGREE_CONCERN.
  - SWE-PRBench F1 0.533 vs. 0.495 for a single reviewer. Naive adversarial review scored 0.457 (false consensus; 3 of 5 comments fabricated in one case).
  - SWE-bench Verified 75.2% vs. 71.6%, at about 4.5x the tokens.
  - **Evidence-tagging of objections is what made it work.**
- Alternatives generation: no rigorous study found showing that "generate N designs then select" improves outcomes.
  - Indirect evidence: anchoring in human-LLM pairs (only 3 of 18 asked for alternatives); LLMs generate more trade-offs and risks than students but over-flag.
  - AI-DLC's domain-design stage enforces options with pros/cons/reversibility only "when more than one viable decomposition" exists. Treat this as practice, not evidence.

---

## Q3. AWS AI-DLC: status as of Oct 2026 (primary source: git clone of awslabs/aidlc-workflows, HEAD 2026-10-24)

- **Origin.** AWS blog by Raja SP, 2025-07-31. https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle
  - Inception (Mob Elaboration), Construction (Mob Construction), Operations. Bolts replace sprints; Units of Work replace epics.
  - Plan, then ask, then implement; AI "defers critical decisions to humans".
- **Current release.** Stable **v2.11.1 (2026-10-20)**. Preview builds are daily (latest tag v2.11.2-preview.20261024.1).
  - Timeline: 2.11.0 (2026-10-08), 2.10.0 (2026-09-24), 2.9.0 (2026-09-15), 2.8.0 (2026-09-08), 2.7.0 (2026-09-01).
  - A builder.aws.com post from 2026-07-21 described v2.3.0 "GA PREVIEW" (32 stages, 9 scopes); this is now outdated. https://builder.aws.com/content/3GnQs6zaYp4mAx9FWBulDkhWnBo/ai-dlc-v2-core-concepts
- **Structure (README and docs/guide/04-phases-and-stages.md)**
  - 5 phases and 33 stages: Initialization 0.1 to 0.3 (automatic, no gate), Ideation 1.1 to 1.7 (new in v2), Inception 2.1 to 2.9, Construction 3.1 to 3.7, Operation 4.1 to 4.7 (all conditional).
  - 14 agents (11 domain, 2 reviewers, 1 composer). 11 workflow profiles. 124-event audit trail.
  - Supported harnesses: Claude Code, Kiro CLI/IDE, Codex CLI, Cursor, opencode, Copilot. Recommended model is Claude Opus 4.8.
- **Inception stages and artifacts**
  - 2.1 Reverse Engineering (brownfield only): developer scan, then architect synthesis; 9 RE artifacts.
  - 2.2 Practices Discovery: hub-and-spoke with mutually blind inspectors, then a human interview. Produces team-practices.md and discovered-rules.md, promoted to memory.
  - 2.3 Requirements Analysis: requirements.md.
  - 2.4 User Stories: a "mob" of design, developer and quality agents in parallel.
  - 2.5 Refined Mockups.
  - 2.6 Domain Design: components.md (YAML catalogue plus mermaid diagram) and decisions.md (ADRs).
  - 2.7 Units Generation: unit-of-work.md and a dependency DAG.
  - 2.8 Contract Design.
  - 2.9 Delivery Planning: bolt-plan.md and risk rationale.
- **Domain Design stage (core/aidlc-common/stages/inception/domain-design.md)**: a concrete model for a design phase.
  - Step 2: write a questions file using `[Answer]:` tags.
  - Step 3: MANDATORY ambiguity analysis, with follow-up questions until resolved.
  - Step 4: machine-readable YAML component catalogue with well-formedness rules (unique names, symmetric depends_on/dependents, single entity owner, acyclic graph). When more than one decomposition is viable, list Option A/B with pros, cons and reversibility, plus a recommendation; "the team chooses at the gate."
  - Step 5: ADRs with Context, Decision, Consequences and Alternatives Rejected.
  - Step 6: traceability.json mapping each story or FR to a component, with GAP rows.
  - Sensors: required-sections, upstream-coverage, traceability. Reviewer: architecture-reviewer, advisory, max 2 iterations.
  - The stage explicitly separates concerns: it does NOT decide deployment topology (Units Generation does) or tech stack and NFRs (later stages).
- **Architecture reviewer agent**
  - Adversarial posture ("REFUTE this design"), but "a finding backed only by architectural taste is a suggestion, not grounds for NOT-READY".
  - In advisory mode it drops the refute loop and ranks findings for the human.
  - READY means "a developer could build this system without architectural guidance."
- **Human-in-the-loop**
  - Every stage outside Initialization ends with an approval gate that needs a real human message (AIDLC_SKIP_HUMAN_PRESENCE_GUARD is the only bypass).
  - Automated verification gates at phase boundaries check traceability and orphaned artifacts.
  - Construction default (new solo work): unit-major, serial, with a verified Unit checkpoint. Approval requires a tool-written verification receipt from a human-authorized verification command.
  - Optional walking skeleton, human-approved. "Continue automatically" waives ordinary checkpoints, but plan approval, verification-command choice, and failures always stop.
- **2026 changes**
  - v2 deterministic engine replaces trust-the-model rules (code picks the next stage; the LLM works within it).
  - Ideation phase and Practices Discovery added. Profiles (Classic = v1-style ceremony, 18 stages; Express 10; Bugfix 9). Learning loop (human-kept corrections become rules for the next workflow).
  - 2.9 added commit provenance. 2.10 added stronger human authority in Construction. 2.11 added Plan Approval asked by the engine and leaner scope defaults.
  - Sources: https://felipefontoura.com/articles/ai-dlc-v2/ (2026-09-02, updated 10-01) and the repo CHANGELOG.
- **Field lessons** (orchestrator.dev, 2026-10-03). https://orchestrator.dev/blog/2026-10-03-ai-dlc-in-practice/
  - Gate fatigue after about an hour of review; separation of duties (the intent author shouldn't approve the plan); a small bugfix triggered 6 approvals; senior reviewers are slower at gates because they catch more.
  - AWS's 10 to 15x claim is treated as an upper bound; no independent outcome data.

---

## Unverified / not opened
- JSS "Vibe architecting" (ScienceDirect robots-blocked).
- HumanLayer original ACE blog page (read from the repo markdown instead).
- github.com HTML pages (not allowlisted); repos were read via git clone.
- Exact Ask-or-Assume baseline numbers (not on the abstract page).
- Plan-compliance exact success-rate numbers (in figures only).

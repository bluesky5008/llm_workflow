# AI-DLC / 에이전트 기반 SDLC 논문 리딩 리스트 (2026-08-27 기준)

관심사: AI 에이전트의 효율적 사용, 에이전트 코딩 워크플로우(최소구현·TDD·회귀검증·형상관리),
기존 스킬 영역(요구공학·설계·역공학·검증)의 보완 + 미고려 영역 발굴.

---

## A. AI-DLC 자체 (방법론 원전)

| 제목 | 출처 | 핵심 |
|---|---|---|
| AI-Driven Development Lifecycle (AI-DLC): Reimagining Software Engineering for the AI Era | IJAIDSML (저널), [링크](https://ijaidsml.org/index.php/ijaidsml/article/view/469) / [PDF](https://ijaidsml.org/index.php/ijaidsml/article/download/469/431) | AWS AI-DLC(Raja SP, 2025.7)의 학술 정리. Intent → Unit → Bolt, Mob Elaboration 개념 |
| AI-DLC 2026 (Waldrip, Driscol 외) | [han.guru](https://han.guru/papers/ai-dlc-2026/) · [GitHub](https://github.com/thebushidocollective/ai-dlc) | 세 가지 운영 모드(HITL / OHOTL / AHOTL), "처방 대신 역압(backpressure)" — 테스트·타입체크·린트·보안스캔이 자동 거부하는 품질 게이트, 파일·git 기반 메모리, Ralph Wiggum 루프 |
| AI-DLC 개요 | [IBM Think](https://www.ibm.com/think/topics/ai-dlc) | 입문용 개념 정리 |
| Agentic AI in the SDLC: Architecture, Empirical Evidence, and the Reshaping of SE (Bhati, 2026.4) | [arXiv 2604.26275](https://arxiv.org/abs/2604.26275) | L0~L5 6계층 참조 아키텍처(모델·추론/메모리·ACI·도구·오케스트레이션·거버넌스). 전통 SDLC 단계별 → 에이전틱 SDLC 매핑. SWE-bench Verified 1.96%(2023.10)→78.4%(2026.4) |
| LLM-Based Agentic Systems for SE: Challenges and Opportunities (2026.1) | [arXiv 2601.09822](https://arxiv.org/abs/2601.09822) | 서베이 |
| SDLC Perspective: A Survey of Benchmarks for Code LLMs and Agents | [arXiv 2505.05283](https://arxiv.org/abs/2505.05283) | SDLC 단계별 벤치마크 지도. "내 워크플로우의 어떤 단계가 측정 가능한가"를 볼 때 유용 |

---

## B. 기존 스킬 영역 보완

### B1. 요구공학 / 스펙 주도 개발
| 제목 | 출처 | 핵심 |
|---|---|---|
| Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants (Piskala, 2026.1, AIWare 2026) | [arXiv 2602.00180](https://arxiv.org/abs/2602.00180) | spec-first / spec-anchored / spec-as-source 3단계 엄격도 + 언제 SDD가 이득인지 판단 프레임워크 |
| Spec Kit Agents: Context-Grounded Agentic Workflows (2026.4) | [arXiv 2604.05278](https://arxiv.org/html/2604.05278v1) | GitHub Spec Kit 기반 에이전트 워크플로우 |
| LLMs for Requirements Engineering: A Cross-Task Empirical Evaluation (2026.8) | [arXiv 2608.21531](https://arxiv.org/html/2608.21531) | RE 태스크별 LLM 성능 비교 |
| Towards an Agentic LLM-based Approach to Requirement Formalization (2026.4) | [arXiv 2604.18228](https://arxiv.org/html/2604.18228) | 비정형 스펙 → 형식 요구사항 |
| Collaborative and AI-Supported Requirements Elicitation: An Empirical Study (2026.6) | [arXiv 2606.24060](https://arxiv.org/html/2606.24060) | 도출 단계 실증 |

### B2. 설계 / 아키텍처
| 제목 | 출처 | 핵심 |
|---|---|---|
| Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory (2026.6) | [arXiv 2606.01385](https://arxiv.org/html/2606.01385v1) | 요구→아키텍처 연결에 계층 메모리 사용 |
| Designing LLM-based Multi-Agent Systems for SE Tasks: Quality Attributes, Design Patterns and Rationale | [arXiv 2511.08475](https://arxiv.org/html/2511.08475v1) | 멀티에이전트 설계 패턴 카탈로그 |
| Developing LLM-based Multi-Agent Systems in SE: A Mixed-Method Experience Report (2026.8) | [arXiv 2608.11965](https://arxiv.org/html/2608.11965v1) | 실무 경험 보고 |

### B3. 역공학 / 레거시 이해
| 제목 | 출처 | 핵심 |
|---|---|---|
| Reversa: Reverse Documentation Engineering Framework — 레거시 → AI 에이전트용 운영 스펙 (2026.5) | [arXiv 2605.18684](https://arxiv.org/html/2605.18684v1) | Scout→Archaeologist→Detective→Architect→Writer→Reviewer 6역할. 산출물에 **confirmed / inferred / gap 신뢰도 태깅** + 코드 추적성 + Gherkin 패리티 시나리오. COBOL→Go 사례(517 claims, 97.1% 신뢰) |
| Environment-in-the-Loop: Rethinking Code Migration with LLM-based Agents (2026.2) | [arXiv 2602.09944](https://arxiv.org/html/2602.09944v1) | 마이그레이션에 실행환경 피드백 |
| LLM Agents Can See Code Repositories (2026.6) | [arXiv 2606.14061](https://arxiv.org/html/2606.14061v4) | 리포 수준 이해 |

### B4. 검증 / TDD / 회귀
| 제목 | 출처 | 핵심 |
|---|---|---|
| **TDAD: Test-Driven Agentic Development — 그래프 기반 영향분석으로 회귀 감소** (Alonso, Yovine, Braberman, 2026.3) | [arXiv 2603.17973](https://arxiv.org/abs/2603.17973) | 코드↔테스트 의존 그래프를 **스킬(정적 텍스트)로 제공**. 회귀율 6.08%→1.82%(−70%). **주의: "TDD 하라"는 절차 지시만 주면 오히려 회귀 9.94%로 악화.** 컨텍스트 제공 > 절차 처방 |
| TDD-Agent: Test-Driven Reasoning for Code Generation (2026.8) | [arXiv 2608.16742](https://arxiv.org/abs/2608.16742v1) | 테스트를 "고정 검증기"가 아니라 "진화하는 추론 산출물"로 취급, 코드와 테스트 동시 정제 |
| Scaling TDD Code Generation from Functions to Classes (2026.2) | [arXiv 2602.03557](https://arxiv.org/abs/2602.03557) | 클래스 단위로 확장 시 TDD 효과 실증 |
| TDD Governance for Multi-Agent Code Generation via Prompt Engineering (2026.4) | [arXiv 2604.26615](https://arxiv.org/abs/2604.26615) | 멀티에이전트 TDD 거버넌스 |
| Rethinking Verification for LLM Code Generation: From Generation to Testing | [arXiv 2507.06920](https://arxiv.org/html/2507.06920v2) | 검증용 테스트 품질 자체를 문제화 |
| LLM-as-a-Verifier: A General-Purpose Verification Framework (2026.7) | [arXiv 2607.05391](https://arxiv.org/html/2607.05391) | LLM 검증기 프레임워크 |
| Code Review Agent Benchmark (2026.3) | [arXiv 2603.23448](https://arxiv.org/html/2603.23448v1) | 리뷰 에이전트 벤치마크 |

---

## C. 고려하지 못했을 가능성이 높은 영역 (추천)

### C1. 컨텍스트 파일(CLAUDE.md/AGENTS.md)의 실효성 — 반직관적 결과
| 제목 | 출처 | 핵심 |
|---|---|---|
| **Evaluating AGENTS.md: Are Repository-Level Context Files Helpful?** (Gloaguen, Vechev 외 ETH, 2026.2/6) | [arXiv 2602.11988](https://arxiv.org/abs/2602.11988) | 컨텍스트 파일이 **성공률을 일반적으로 높이지 않고 비용은 평균 20%+ 증가**. 유용한 건 "비표준 관행 문서화"뿐 |
| Do Context Files Help Coding Agents? Two-Agent Ablation on Real Repos (Khatri, 2026.7) | [arXiv 2607.27250](https://arxiv.org/html/2607.27250v1) | Claude Code·Codex 288회 실행. 정확도 변화 없음(≤10–15pp 바운드). 실패 원인은 지식 부족이 아니라 설계·패턴 선택·배선 |
| Agent READMEs: An Empirical Study of Context Files (2025.11) | [arXiv 2511.12884](https://arxiv.org/abs/2511.12884) | 현장 컨텍스트 파일 실태 |
| Codified Context: Infrastructure for AI Agents in a Complex Codebase (Vasilopoulos, 2026.2) | [arXiv 2602.20478](https://arxiv.org/html/2602.20478v1) | 108K LoC C# 시스템 283세션. **단일 파일은 확장 안 됨** → 3계층(핫 메모리 660줄 헌법 / 19개 도메인 전문 에이전트 / MCP로 온디맨드 검색되는 콜드 스펙 34개). 인프라가 코드베이스의 24.2% |
| Context Engineering for AI Agents in OSS | [arXiv 2510.21413](https://arxiv.org/abs/2510.21413) | OSS 컨텍스트 엔지니어링 실태 |
| Agentic Context Engineering (ICLR 2026) | [arXiv 2510.04618](https://arxiv.org/abs/2510.04618) | 컨텍스트 자체를 자기개선 |

### C2. 하네스 엔지니어링 → 루프 엔지니어링
| 제목 | 출처 | 핵심 |
|---|---|---|
| **Agentic Harness Engineering: Observability-Driven Automatic Evolution** (Fudan 외, 2026.4) | [arXiv 2604.25850](https://arxiv.org/abs/2604.25850) | 트래젝토리 증류 + 결정 검증으로 하네스 자동 진화. Terminal-Bench 69.7→77.0%. **성능 향상은 시스템 프롬프트가 아니라 도구·미들웨어·장기 메모리에서 나옴** |
| **LoopsBench: From Harness Engineering to Loop Engineering** (Microsoft 외, 2026.7) | [arXiv 2608.00267](https://arxiv.org/html/2608.00267v1) | 장기 개발(의존 DAG 5,300 유닛). 최고 조합(Opus 4.7+Claude Code)도 25%. 병목은 코드 생성이 아니라 **계획·코드·테스트 상태 유지 규율**, 회귀는 모든 루프에서 발생 |
| Building Effective AI Coding Agents for the Terminal (OpenDev, Bui, 2026.3) | [arXiv 2603.05344](https://arxiv.org/abs/2603.05344) | 계획/실행 이중 에이전트, 적응형 컨텍스트 압축, 지연 도구 발견, **이벤트 기반 시스템 리마인더로 지시 소실 방지**, 세션 간 자동 메모리 |
| Code as Agent Harness (2026.5) | [arXiv 2605.18747](https://arxiv.org/abs/2605.18747) | 코드 자체를 하네스로 |
| Natural-Language Agent Harnesses (2026.3) | [arXiv 2603.25723](https://arxiv.org/abs/2603.25723) | 자연어 하네스 |
| From QA to Task Completion: Survey on Agent System and Harness Design (2026.6) | [arXiv 2606.20683](https://arxiv.org/html/2606.20683v1) | 하네스 설계 서베이 |
| awesome-agent-harness | [GitHub](https://github.com/RUCAIBox/awesome-agent-harness) | 논문 모음 |

### C3. 세션 간 메모리 (형상관리와 맞닿음)
| 제목 | 출처 | 핵심 |
|---|---|---|
| **PROJECTMEM: Local-First, Event-Sourced Memory and Judgment Layer** (Utah, 2026.6) | [arXiv 2606.12329](https://arxiv.org/html/2606.12329v1) | 벡터DB 없이 append-only 이벤트 로그(issue/attempt/fix/decision/note, JSONL+MD, git 친화). **"Memory-as-Governance": 이전에 실패한 수정 반복·취약 파일 편집 전에 경고하는 사전 게이트.** 세션당 토큰 50%+ 절감 |

### C4. 스킬 자체의 품질과 위험 (스킬로 워크플로우를 만드는 사람에게 직결)
| 제목 | 출처 | 핵심 |
|---|---|---|
| **From Anatomy to Smells: An Empirical Study of SKILL.md** (Hong, Imani, Ahmed, 2026.7) | [arXiv 2607.01456](https://arxiv.org/abs/2607.01456) | 238개 SKILL.md, **26종 스킬 냄새 카탈로그**. 99%가 냄새 보유, 평균 10.5개. 최다: Rationalization Loophole(94%). 그 외 No Validation Step, Execute Without a Plan, Never Asks Human, No Progress Tracking, Undelegated Detail, Buried Gotchas, Missing Template 등 |
| **Agent Skills Can Be Harmful: Skill-Induced Failures** (HUST/MSR/UIUC, 2026.8) | [arXiv 2608.11888](https://arxiv.org/html/2608.11888v1) | 스킬이 오히려 실패 유발. 기능 실패의 68.8%는 "관련 있어 보이는 스킬"이 필드 누락/오구현 유도. 효율 저하의 62.6%는 과잉 절차(특히 **과잉 검증 36.8%**). 권고: 필수 요구와 재사용 템플릿 분리, 스킬-태스크 호환성 점검, **검증 범위를 불확실성/예산에 조건화**, 선택 자료는 지연 로드 |
| Agent Skills for LLMs: Architecture, Acquisition, Security (2026.2) | [arXiv 2602.12430](https://arxiv.org/html/2602.12430v4) | 스킬 서베이 |
| Agent Skills in the Wild / Malicious Agent Skills / Risk Assessment of Malicious Skill Files | [2601.10338](https://arxiv.org/pdf/2601.10338) · [2602.06547](https://arxiv.org/html/2602.06547v1) · [2608.05223](https://arxiv.org/html/2608.05223) | 외부 스킬 도입 시 보안 |

### C5. 산출물의 보안 부채·유지보수·리뷰 (회귀검증 뒤 단계)
| 제목 | 출처 | 핵심 |
|---|---|---|
| **Trust but Verify? Security Debt of Autonomous Coding Agents** (KDD 2026 WS, 2026.7) | [arXiv 2607.12428](https://arxiv.org/html/2607.12428v1) | 4,022 PR 분석. **39% PR에 보안 취약**, 82%가 공급망 무결성, 치명 등급의 99.6%는 하드코딩 자격증명, 리뷰가 81.1%를 놓침. 인간이 실제 유출 비밀의 68% 도입 |
| To What Extent Does Agent-generated Code Require Maintenance? (NAIST, 2026.5) | [arXiv 2605.06464](https://arxiv.org/html/2605.06464) | AI 코드는 이후 손질이 적고, 변경 유형이 기능확장 위주(인간은 버그픽스 위주) |
| Debt Behind the AI Boom: Large-Scale Study of AI-Generated Code (2026.3) | [arXiv 2603.28592](https://arxiv.org/html/2603.28592) | 대규모 기술부채 실증 |
| AI-Generated Smells: Code and Architecture in LLM/Agent-Driven Development (2026.5) | [arXiv 2605.02741](https://arxiv.org/html/2605.02741v1) | 아키텍처 냄새 |
| More Code, Less Reuse: AI-generated PR 품질과 리뷰어 감정 (2026.1) | [arXiv 2601.21276](https://arxiv.org/abs/2601.21276) | 재사용 감소 경향 |
| How AI Coding Agents Modify Code: Large-Scale PR Study (2026.1) | [arXiv 2601.17581](https://arxiv.org/html/2601.17581) | 에이전트 수정 패턴 |
| From Human-Centric to Agentic Code Review (2026.7) | [arXiv 2607.13196](https://arxiv.org/html/2607.13196v1) | 리뷰 품질 세대 비교 |
| 3100 Opinions on Code Review in an AI World (2026.7) | [arXiv 2607.07980](https://arxiv.org/abs/2607.07980v1) | 실무자 담론 인과이론 |

### C6. 검증기 게이밍 (테스트를 통과시키기 위한 편법)
| 제목 | 출처 | 핵심 |
|---|---|---|
| LLMs Gaming Verifiers: RLVR Can Lead to Reward Hacking (ICLR 2026 WS, 2026.4) | [arXiv 2604.15149](https://arxiv.org/pdf/2604.15149) | RLVR 학습 모델은 검증기 약점을 공략. 난이도·추론 예산이 커질수록 편법 증가. Isomorphic Perturbation Testing 제안 → 테스트를 "동형 변형"해서 진짜 이해 여부 확인 |
| EvilGenie: A Reward Hacking Benchmark (MIT) | [링크](https://futuretech.mit.edu/publication/evilgenie-a-reward-hacking-benchmark) | 코딩 에이전트의 테스트 조작 벤치마크 |

---

## D. 계속 추적용 큐레이션
- [VoltAgent/awesome-ai-agent-papers (2026)](https://github.com/VoltAgent/awesome-ai-agent-papers)
- [YerbaPage/Awesome-Repo-Level-Code-Generation](https://github.com/YerbaPage/Awesome-Repo-Level-Code-Generation)
- [Anthropic 2026 agentic coding trends report](https://resources.anthropic.com/2026-agentic-coding-trends-report)
- [Context Engineering Research: Papers & Benchmarks (2026)](https://www.iwoszapar.com/p/context-engineering-research-2026)

---

## F. [2차 추가] 사내 에이전트·LLM 게이트웨이 개발/운영 관점

### F1. 모델 라우팅 / 캐스케이딩 (게이트웨이 핵심 기능)
| 제목 | 출처 | 핵심 |
|---|---|---|
| Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey (Moslem, Kelleher, TCD) | [arXiv 2603.04445](https://arxiv.org/html/2603.04445v1) | 6분류: 난이도 인식 / 인간선호 정렬(RouteLLM, Arch-Router) / 클러스터링 / RL·밴딧 / 불확실성 기반 / 캐스케이딩(FrugalGPT, AutoMix). 설계 축 = 언제(생성 전·후)·무엇으로(질의/응답 신호)·어떻게(규칙/분류기/정책) |
| **Agent-as-a-Router: Agentic Model Routing for Coding Tasks** (Zhou, You 외, 2026.6) | [arXiv 2606.22902](https://arxiv.org/abs/2606.22902) | 라우팅을 정적 분류가 아닌 Context→Action→Feedback 루프로. Orchestrator+Verifier+Memory. CodeRouterBench(~10K 태스크, 8개 프론티어 모델) 공개. 태스크 차원 성능 통계 추가만으로 +15.3% |
| Beyond Accuracy and Cost: Latency-Aware LLM Query Routing for Dynamic Workloads (2026.7) | [arXiv 2607.18253](https://arxiv.org/abs/2607.18253) | 동적 부하에서 지연 고려 라우팅 |
| Latency-Quality Routing for Functionally Equivalent Tools in LLM Agents (2026.5) | [arXiv 2605.14241](https://arxiv.org/abs/2605.14241) | 모델이 아닌 **동등 기능 도구** 간 라우팅 |
| Toward Reliable Design of LLM-Enabled Agentic Workflows: Latency-Reliability-Cost (NYU, 2026.4) | [arXiv 2605.23929](https://arxiv.org/html/2605.23929v1) | 순차/병렬/피드백 구성별 토큰 예산 최적 배분(water-filling). 워크플로우 구조 자체가 성능 변수 |
| Awesome-Routing-LLMs | [GitHub](https://github.com/MilkThink-Lab/Awesome-Routing-LLMs) | 추적용 |

### F2. 캐시 / 컨텍스트 압축 (게이트웨이 비용·지연)
| 제목 | 출처 | 핵심 |
|---|---|---|
| **Don't Break the Cache: Prompt Caching for Long-Horizon Agentic Tasks** (Lumer 외, 2026.1) | [arXiv 2601.06007](https://arxiv.org/abs/2601.06007) | OpenAI/Anthropic/Google 500+ 세션 실증. 비용 41–80% 절감, TTFT 13–31% 개선. **나이브 전체 컨텍스트 캐싱은 오히려 지연 증가**. 동적 내용은 시스템 프롬프트 끝으로, 동적 도구 결과는 캐시 제외 |
| TokenPilot: Cache-Efficient Context Management for LLM Agents (2026.6) | [arXiv 2606.17016](https://arxiv.org/html/2606.17016v1) | 캐시 친화 컨텍스트 관리 |
| Practical Online KV Cache Compaction for LLM Agents: An Empirical Study (2026.8) | [arXiv 2608.00902](https://arxiv.org/html/2608.00902) | 자체 호스팅 모델 운용 시 참고 |
| Parallel Context Compaction for Long-Horizon LLM Agent Serving (2026.5) | [arXiv 2605.23296](https://arxiv.org/html/2605.23296v1) | 서빙 측 압축 |

### F3. 사내 에이전트 구축 경험 보고 (가장 직접적 비교군)
| 제목 | 출처 | 핵심 |
|---|---|---|
| **Building an Internal Coding Agent at Zup: Lessons and Open Questions** (Pinto 외, Zup Innovation) | [arXiv 2604.09805](https://arxiv.org/abs/2604.09805) | Node CLI + FastAPI 백엔드 + Maestro 오케스트레이터, Postgres/Redis/WebSocket. 교훈: **프레임워크보다 직접 구현한 루프가 통제·반복 속도 우위**, 도구 설계 품질 > 프롬프트 엔지니어링, 편집 도구는 전체 파일 재작성 대신 문자열 치환, 클라이언트 측 도구 실행, 승인→자율 점진 감독 모드. 미해결: 도구 매니페스트 설계법, 모델/오케스트레이터 추론 경계, 교차 도구 안전정책, 장기 메모리, 생성 코드 QA |
| **Shared Organizational Memory for Enterprise Coding Agents** (2026.7) | [arXiv 2608.00122](https://arxiv.org/abs/2608.00122) | 팀 확장 시 핵심. 작업 중 경험을 기여자 승인 하에 Q&A 메모리로 큐레이션, 보안/프라이버시 필터, 이후 에이전트에 검색 제공. "지식 캡처를 플랫폼 수준 기능으로" (효과는 평가 중) |
| Building Effective AI Coding Agents for the Terminal (OpenDev) | [arXiv 2603.05344](https://arxiv.org/abs/2603.05344) | (C2 참고) 계획/실행 분리, 압축, 지연 도구 발견 |

### F4. 관측성 / 실패 진단 (AgentOps)
| 제목 | 출처 | 핵심 |
|---|---|---|
| **AgentDebugX: Failure Observability, Attribution, Recovery** (Toronto/Google/Stanford/UIUC, 2026.7) | [arXiv 2607.18754](https://arxiv.org/html/2607.18754v1) | Detect→Attribute→Recover→Rerun 폐루프. 프레임워크 독립 트레이스 포맷, 19+ 실패 모드 분류, 팀 간 공유용 Error Hub. Python 라이브러리/CLI/웹/스킬 제공. GAIA 실패 73건 중 13건 1회 재실행으로 복구 |
| AgentFixer: From Failure Detection to Fix Recommendations (2026.3) | [arXiv 2603.29848](https://arxiv.org/html/2603.29848) | 실패 → 수정 추천 |
| From Agent Traces to Trust: Evidence Tracing and Execution Provenance — Survey (2026.6) | [arXiv 2606.04990](https://arxiv.org/html/2606.04990) | 트레이스 기반 신뢰·출처 서베이 |
| AI Observability for LLM Systems: Multi-Layer Analysis (2026.4) | [arXiv 2604.26152](https://arxiv.org/html/2604.26152v1) | 신뢰도 보정부터 인프라 트레이싱까지 계층별 |
| Agent-as-a-Judge: Evaluate Agents with Agents | [arXiv 2410.10934](https://arxiv.org/abs/2410.10934) | 에이전트 평가의 표준 참조 |
| Evaluation and Benchmarking of LLM Agents: A Survey | [arXiv 2507.21504](https://arxiv.org/html/2507.21504v1) | 평가 서베이 |

### F5. MCP / 도구 생태계 보안 (게이트웨이가 막아야 할 것)
| 제목 | 출처 | 핵심 |
|---|---|---|
| **A First Look at the Security Issues in the MCP Ecosystem** (Li, Gao, Delaware, DSN 2026) | [arXiv 2510.16558](https://arxiv.org/abs/2510.16558) | 호스트 4종·서버 67,057개·레지스트리 6곳. 도구 이름 충돌 혼동, 서버 제거 후 남는 dangling 도구, **도구 포이즈닝 성공률 20–100%**, 도구 섀도잉, 자동 업데이트 통한 메타데이터 주입. 레지스트리에 유효 GitHub 토큰 5개 노출, 하이재킹 가능 계정 212개. MCPInspect 사전 스크리닝 도구. 권고: 도구 호출 전 독립 검증, 네이밍 표준화, 소유권 지속 검증 |
| MCP at First Glance: Security and Maintainability of MCP Servers | [arXiv 2506.13538](https://arxiv.org/abs/2506.13538) | 서버 코드 품질·보안 실태 |

## G. [2차 추가] 팀 단위 확장 근거
| 제목 | 출처 | 핵심 |
|---|---|---|
| **A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption** (Stanford/CMU 외, ASE '26, 2026.8) | [arXiv 2608.25241](https://arxiv.org/html/2608.25241) | RAMP 4단계 성숙도 모델(기업 리포 441개로 구축) → OSS 509개에 DiD 적용. **AI 설정 파일을 커밋하지 않은 리포는 복잡도 증가가 2.0배(+52.7% vs +26.7%)**, 정적분석 경고 1.7배. 속도 이득(28–38% 커밋 증가)은 성숙도 무관. 73.8%의 설정은 한 번 커밋 후 수정 없음. → C1의 "컨텍스트 파일은 정확도에 무효"와 **양립**: 태스크 성공률이 아니라 **팀 수준 품질 부채 억제**에 효과 |
| Early Adoption of Agentic Coding Tools by GitHub Projects (RIT, 2026.7) | [arXiv 2607.14037](https://arxiv.org/abs/2607.14037) | 25,264 PR. 중앙값 리포는 1–2건뿐. 소규모 팀이 더 활발. 79%가 **1인 검토** — 다인 협업 리뷰는 드묾 |
| Agentic Much? Adoption of Coding Agents on GitHub (2026.1) | [arXiv 2601.18341](https://arxiv.org/html/2601.18341v2) | 도입 실태 |
| Toward Agentic SE Beyond Code: Vision, Values, Vocabulary | [arXiv 2510.19692](https://arxiv.org/html/2510.19692v2) | 팀·조직 관점 프레이밍 |
| A Comprehensive Empirical Evaluation of Agent Frameworks on Code-centric SE Tasks | [arXiv 2511.00872](https://arxiv.org/html/2511.00872v1) | 사내 에이전트 프레임워크 선택 시 비교 근거 |

---

## E. 우선 읽기 순서 제안 (실무 적용 관점)

### 게이트웨이/사내 에이전트 트랙 (2차)
1. Zup 경험 보고 (2604.09805) — 같은 일을 먼저 한 팀의 결정과 미해결 문제
2. Don't Break the Cache (2601.06007) — 게이트웨이 프롬프트 레이아웃 규칙 (즉시 적용 가능)
3. MCP 생태계 보안 (2510.16558) — 게이트웨이에 넣을 도구 검증 게이트
4. Agent-as-a-Router (2606.22902) + 라우팅 서베이 (2603.04445) — 코딩 태스크 라우팅 설계
5. AgentDebugX (2607.18754) — 트레이스 포맷·실패 분류를 팀 공유 자산으로
6. A Few Pages of Markdown (2608.25241) + Shared Org Memory (2608.00122) — 팀 확장 시 "무엇을 리포에 커밋할지"의 근거

### 워크플로우/스킬 트랙 (1차)
1. TDAD (2603.17973) — 회귀검증 스킬을 "절차"에서 "의존 컨텍스트"로 바꿀 근거
2. Agent Skills Can Be Harmful (2608.11888) + SKILL.md Smells (2607.01456) — 현재 스킬 4종 점검 체크리스트
3. Evaluating AGENTS.md (2602.11988) + Codified Context (2602.20478) — 컨텍스트 파일 다이어트 vs 계층화
4. AI-DLC 2026 — HITL/OHOTL/AHOTL 모드를 워크플로우에 태깅
5. LoopsBench (2608.00267) + Agentic Harness Engineering (2604.25850) — 장기 작업의 상태 규율
6. PROJECTMEM (2606.12329) — 실패 이력을 git 친화 로그로 남겨 재발 방지 게이트
7. Reversa (2605.18684) — 역공학 스킬에 confirmed/inferred/gap 태깅 도입
8. Security Debt (2607.12428) — 회귀검증 뒤 시크릿/공급망 스캔 게이트

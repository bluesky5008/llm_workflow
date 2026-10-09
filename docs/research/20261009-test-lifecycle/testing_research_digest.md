# 테스트 방법론·수명주기 조사 정리 — llm_workflow의 테스트 관련 근거 통합

> 목적: 워크플로우의 테스트 규정(작성 기준·회귀 관리·수명주기·결과 기록)을 보강하는 후속 논문의 자료. 2026-10-09 세션에서 (1) 선행 조사 `docs/research/20260919-aidlc-research/` 14편 중 테스트 관련 내용을 발췌하고, (2) 같은 날 외부 검색으로 보강한 신규 근거를 합쳤다.
> 출발점: 사용자의 사용 경험에서 나온 요구 7번("회귀테스트는 증가 방향만 있고 정리·최적화 방안이 없다")과 8번(테스트 결과·커버리지 기록). 요구 전문은 2026-10-09 세션 대화에 있고, 본 문서 §0에 요약했다.
> 기준 커밋: 현행 규정은 `c4cde3f`(2026-08-17, main). 9월 사이클 2건은 `archive/202609-cycles` 브랜치에 보존되어 있으며 §1.3에서 input으로 참조한다.
> 검증 수준 표기: **[본문]** = 논문 본문·원문 페이지를 직접 읽음, **[초록]** = 초록·요약 페이지만 확인, **[2차]** = 다른 자료가 인용한 수치로 원문 미확인. 선행 조사에서 가져온 수치는 그 문서의 검증 수준을 그대로 따른다(해당 문서는 "본문에서 확인 못함"을 명시하는 관행을 썼다).

---

## 0. 결론 먼저

1. **현행 워크플로우의 테스트 규정은 "언제 무엇을 만드는가"만 있고, 만든 테스트의 품질 기준과 그 이후의 수명(갱신·병합·격리·폐기)에 대한 규정이 없다.** 설계 당시 "TDD를 지시하고 테스트를 수행하라"는 지침으로 에이전트의 자율에 맡긴 결과다(§1).
2. **그 자율은 신뢰할 수 없다는 직접 증거가 2026년에 나왔다.** TEBench(§3.1)에서 Claude Code·Codex CLI·OpenCode 7개 구성은 코드 변경 후 "깨진 테스트"는 잘 고치지만, "통과하지만 더 이상 검증하지 않는 테스트(stale)"는 F1 약 36%에 그쳤다. 실행 실패 신호가 없으면 정리는 일어나지 않는다.
3. **선행 조사(§2)는 회귀 압력의 구조를 밝혔지만 정리 쪽은 다루지 않았다.** TDAD는 "어떤 테스트를 돌릴지"(맵), LoopsBench는 "무엇을 지켜야 하는지"(의무 목록), Skills Harmful은 "얼마나 자주 돌릴지"(조건화)를 주었다. 세 편 모두 테스트 집합이 커지기만 하는 문제를 전제로 삼지 않았다.
4. **정리의 원칙은 "입증 책임을 삭제 쪽에"다.** 실무 삭제 기준(§3.3)은 삭제 분류 5종과 전부 성립해야 하는 관문 조건을 두고, "한 번도 실패한 적 없는 테스트는 무가치가 아니라 하중을 받고 있을 가능성"으로 취급한다. 이는 에이전트가 통과를 위해 테스트를 지운다는 보고(§3.6)와 양립하는 유일한 형태다.
5. **품질 판정에는 커버리지가 아니라 뮤테이션 점수가 필요하다.** LLM 생성 테스트는 테스트 냄새(Assertion Roulette, Magic Number, Lazy Test)와 동어반복 단언이 반복되며(§3.2), 커버리지는 이를 구분하지 못한다. 다만 뮤테이션은 비용이 커서 관문 옵션으로 둔다.
6. **규정의 분량에는 상한이 있다.** Skills Harmful의 과잉 검증 36.8%, TDAD의 "절차보다 컨텍스트", AGENTS.md 실무 가이드의 "일반 소프트웨어 공학을 가르치지 말라"는 같은 방향이다. 본문에는 판단 규칙만, 세부는 references, 집행은 기계적 검사로 간다(§4.4).
7. **설계 제안은 세 겹이다(§4).** 작성 기준(행위 검증·결정성·크기 라벨), 수명주기(상태 5종과 전이 트리거), 기계적 검사(냄새 린트·뮤테이션·커버리지 중복). 이 중 수명주기가 요구 7번의 본체다.

---

## 1. 현행 워크플로우의 테스트 규정 실태

### 1.1 규정 위치와 내용 (`c4cde3f`)

| 위치 | 규정 | 성격 |
|---|---|---|
| wf-implement §2.4 | 사소하지 않은 로직에 "깨지면 실패하는 가장 작은 실행 가능한 검증 하나". 자명한 한 줄 변경은 테스트 불요. 저장소 기존 테스트 체계 안에서 작성. 테스트 우선은 양을 늘리는 규칙이 아님 | 무엇을 만드는가 |
| wf-implement §3.3 | Red→Green→Refactor. 버그 수정은 재현 테스트 선행(경량 경로 포함). 테스트 없는 기존 코드 변경 시 특성화 테스트. 사이클 부적용 시 이유 기록 후 후행 검증 | 언제·어떤 순서로 만드는가 |
| wf-implement §3.4 | 6단계 검증(정적 분석→변경 영역 단위→통합→인수 시나리오→비기능→빌드). 실패 4분류(이번 변경/기존/환경/미확인). "실패한 검증을 제외하여 전체 성공으로 보고하지 않는다" | 어떻게 검증하는가 |
| wf-implement §3.5 | 리뷰 18문항 중 테스트 관련 3개: "의도하지 않은 회귀가 없는가", "테스트가 구현 방식이 아니라 요구 동작을 검증하는가", "TDD 미적용 이유가 기록되었는가" | 사후 점검 |
| wf-implement §3.6·§5 | 통합 시 최종 빌드·테스트. 완료 조건 "관련 자동화 테스트와 빌드가 성공했다" | 완료 판정 |
| wf-doc verification 템플릿 | `검증 ID / 인수 조건 / 방법·명령 / 결과(성공·실패·미수행) / 증거` 표. "명령은 실제 실행한 형태로" | 기록 형식 |

### 1.2 공백 (이 문서가 다루는 범위)

| 공백 | 근거 |
|---|---|
| 테스트의 **품질 기준** 없음 — 결정성, 행위 지향, 크기, 단언의 변별력 | §2.4·§3.3에 해당 어휘 없음. 선행 조사 `01_solution_plan.md` §2.0 원인 G: "§2.4 테스트 기준에 결정성 요건 없음" |
| 테스트의 **수명주기** 없음 — 코드 변경 후 기존 테스트의 갱신·병합·격리·폐기 | §3.5의 "회귀가 없는가"는 질문일 뿐 확인 수단이 없음(`llm_workflow_vs_papers_round1.md` §2.1 대조표) |
| **회귀 목록** 없음 — 무엇을 지켜야 하는지가 기록되지 않음 | `02_baseline_llm_workflow.md`: 후속 사이클 4개 중 앞 사이클 테스트 재실행 0건 |
| 검증 결과의 **귀속** 없음 — SHA·명령이 기록되지 않음 | 같은 문서: 검증 행 35개 중 SHA 기록 실질 0건, 명령 기록 2건, 실패 분류 어휘 사용 0건 |
| 테스트 **결과의 정량 기록**(건수·시간·커버리지) 없음 | verification 템플릿에 해당 열 없음. 사이클 총 검증 시간 "측정 불가" |

### 1.3 보관 브랜치 사이클 1(`20260920-regression-tier`)이 메운 것과 남긴 것

`archive/202609-cycles` 브랜치의 `docs/work/20260920-regression-tier/`는 선행 조사의 S1·S2·S3을 구현했다. 3튜플 앵커(ADR-004), `test-map` 유형, work-log `## 회귀 의무 목록` 절, `references/verification-depth.md`, verification 표의 `분류` 열. 의무 목록 행의 상태값은 `유지 | 대체(→DCR/TASK) | 폐기(이유)`였다.

남긴 결함은 **상태값은 있으나 그 전이를 일으키는 관문이 없다**는 점이다. 등록(TASK 완료 시)만 규정되고, 대체·폐기로 넘어가는 시점·기준·증거가 없다. 사용자가 실사용에서 관찰한 "증가 방향만 있다"는 이 설계의 결함을 정확히 짚은 것이며, 선행 조사 S2의 "삭제 금지" 원칙이 관문 없이 이식된 결과다.

---

## 2. 선행 조사(2026-08/09) 발췌 — 테스트 관련

원문: `docs/research/20260919-aidlc-research/`. 아래는 테스트 규정에 직접 닿는 부분만 추렸고, 각 항목의 원문 위치를 적었다.

### 2.1 TDAD — "어떤 테스트를 돌릴지"라는 컨텍스트가 회귀를 줄인다

출처: Alonso, Yovine, Braberman, *TDAD: Test-Driven Agentic Development*, arXiv 2603.17973 (2026.3). 원문 발췌: `s1-s3_papers_deep_dive.md` §3, `llm_workflow_vs_papers_round1.md` §2.1.

| 지표 (Phase 1, SWE-bench Verified 100건, Qwen3-Coder 30B 4-bit) | Vanilla | TDD 절차 프롬프트 | 의존 맵 + TDD |
|---|---|---|---|
| 테스트 단위 회귀율(P2P 실패/총) | 6.08% (562/9,245) | 9.94% | **1.82%** (155/8,536) |
| 인스턴스 단위 회귀율 | 30.2% | 33.3% | 33.3% |
| 파국적 회귀(P2P 전부 실패) | 3 | 5 | 1 |
| 해결률 | 31% | 31% | 29% |

- 제공물은 `test_map.txt`(소스 파일→테스트 파일, 한 줄 한 매핑)와 약 20줄 SKILL.md. 런타임에 MCP·DB 없이 grep만.
- 자동 개선 루프에서 가장 큰 효과는 SKILL.md를 107줄 9단계 TDD 절차에서 20줄로 줄인 것(해결률 12%→50%). 단 맵 없이 프롬프트만 줄이면 30%→20%로 악화. 저자 해석: "context (which tests to check) outperforms procedure (how to do TDD)".
- 테스트↔코드 연결 우선순위: 명명 규칙 `test_foo.py→foo.py` → 접두 매칭 → 디렉터리 근접. 영향 분석 가중치 Direct 0.95 / Coverage 0.80 / Transitive 0.70 / Imports 0.50.
- **한계**: 통계 검정 없음, 단일 실행. 인스턴스 단위 회귀율은 개선 없음(테스트 단위 70% 감소는 파국 회귀 3→1이 분모를 지배했을 가능성). Phase 2는 회귀 0%/0%로 회귀 감소 효과를 검증하지 못함. Python·pytest·소형 모델 조건이며 프론티어 모델 재현 미확인. 동적 디스패치·fixture·parametrize 맹점.
- **워크플로우 교훈**: §3.3의 TDD를 버릴 근거는 아니다(test-first vs test-after 비교가 아님). 옮길 것은 §3.4-2 "변경 영역의 단위 테스트"에 대상 목록을 공급하는 입력이다. F2P(새 동작) 지시는 두껍고 P2P(회귀) 지시는 얇다는 불균형이 지적됐다.

### 2.2 LoopsBench — 완료된 의무는 명시적 상태로 추적해야 한다

출처: Microsoft·Nanjing·UCL·SJTU, *LoopsBench: From Harness Engineering to Loop Engineering*, arXiv 2608.00267 (2026.7). 원문 발췌: `s1-s3_papers_deep_dive.md` §1.

- 112 task, 8언어, 5,300+ 개발 단위, 의존 깊이 중앙값 6. 개발 단위 u = (요구사항, 파일/심볼 스코프, 전제 집합, 참조 패치, 표준 테스트).
- 게이트의 두 문장: "The gate affects scoring rather than editing permission." / "Once a unit clears the gate, its tests and the tests of its predecessors are kept enforced as regression tests on every later layer." 루프는 무엇을 유지해야 하는지 **통보받지 않는다**.
- 회귀율 정의: 이전에 통과한 테스트 의무 중 이후 편집에서 실패한 비율.

| 루프 | Edge F1 | PatchLen | 작성 테스트 수 | 회귀율 |
|---|---|---|---|---|
| Claude Code | 0.71 | 1.58 | 28 | 7.11% |
| Codex | 0.67 | 1.71 | 24 | 4.83% |
| GitHub Copilot | 0.58 | 1.83 | 22 | 6.91% |
| OpenHands | 0.39 | 2.31 | 16 | 2.46% |
| mini-swe-agent | 0.27 | 2.54 | 11 | 0.24% |

- "Context-budget renewal does not remove regression pressure." dynamic workflows는 좁은 워커 컨텍스트에도 run당 0.36 회귀 사건. → "completed obligations still require explicit state tracking when workers return."
- 5,300 단위에서 루프가 남긴 테스트 11~28개: "sparse test authoring"이 선행 의무의 회귀 보호를 약하게 한다.
- **주의**: 회귀율과 작성 테스트 수가 같은 방향인 것은 진행이 많을수록 지킬 의무가 많아서이지, 테스트를 많이 쓰면 회귀가 는다는 뜻이 아니다. Table 4의 루프 간 RR은 분모가 달라 비교 금지. 논문은 "explicit state tracking"을 권고하면서 그 처방을 실험하지 않았다.
- **워크플로우 번역**(`s1-s3` §1.5): TASK = 단위, `completed` 전이 = 게이트 통과, 회귀 의무 목록 = active obligation state, work-log = 새 라운드에 대한 통보. 목록 행: 발행 TASK / 테스트 식별자 / 실행 명령 / 보호 스코프 / 마지막 성공(일시·커밋) / 상태 / 비고. Edge F1 ≤ 0.71이므로 의존성 필드로 재실행 대상을 고르면 30% 이상 놓친다 → 기본은 전량 재실행, 선별은 시간이 문제일 때만.
- **금지 규칙**: 의무 테스트를 통과시키려고 수정·삭제·제외하지 않는다. 회귀를 "기존 실패"로 재분류하려면 마지막 성공 증거보다 앞선 실패 증거가 있어야 한다.

### 2.3 Agent Skills Can Be Harmful — 과잉 검증은 조건화로 푼다

출처: HUST/MSR/UIUC, arXiv 2608.11888 (2026.8). 원문 발췌: `s1-s3_papers_deep_dive.md` §2, `llm_workflow_vs_papers_round1.md` §2.2.

- 확정 실패 307건 = 기능 125 + 효율 182. 효율 회귀 중 **EV(과잉 검증) 67건, 36.8%** — "excessive or repeated tests, rebuilds, debugging attempts, or checklist verification after the main artifact has been produced". SBCB(스킬 본문 자체 비용) 43건 23.6%.
- 기능 실패 중 ESM(환경 불일치) 8건 6.4%: 스킬이 패키지 해석·작업 디렉터리를 바꿔 "에이전트의 자체 점검 환경 ≠ 검증기 환경".
- Finding 4: "skill authors should condition verification scope and pipeline depth on task uncertainty, change size, and budget rather than prescribing exhaustive workflows by default."
- **중요한 단서**: EV 67건은 전부 PASS/PASS 쌍이다. 논문은 EV가 기능 실패를 늘린다고 주장하지 않는다. 편집 목표는 검증을 줄이는 것이 아니라 "동일 검증의 무조건 반복"을 조건부로 바꾸는 것이다.
- 현행 워크플로우 판정: 과잉 검증 "해당(부분)" — TASK마다 §3.3 근접 검증 → §3.4 6단계 → §3.5 18문항 → §3.6 최종 빌드·테스트 → wf-doc 13문항 → wf-tree 10문항. 산출물 이후 체크리스트 41문항.
- **한계**: 반복 실행 없음(비결정성 통제는 T=2.0 임계와 쌍 통제에만 의존), 주석자 수·카파 미기재, 후보→확정에서 절반 이상 탈락했으나 사유별 건수 없음.

### 2.4 솔루션 플랜의 회귀 진단과 설계 (`01_solution_plan.md` §2.0~2.1)

관찰된 증상: 반복 사용할수록 회귀검사 시간 증가, 간헐적 결과 부정합. 원인 7개를 현행 규정에서 도출했다.

| # | 원인 | 유형 |
|---|---|---|
| A | 중복 실행 — TASK당 최대 7~8회, 생략 조건 없음 | 시간 |
| B | 전량 실행 — "변경 영역" 판단이 에이전트 재량이라 전체 스위트로 기움. A×B = 이차 증가 | 시간 |
| C | 결과에 커밋 앵커 없음 | 부정합 |
| D | 실행 집합 비결정 | 부정합 |
| E | 실행 환경·명령 미고정 | 부정합 |
| F | 세션 경계의 기억 소실 | 부정합 |
| G | flaky·순서 의존 테스트 누적 — §2.4에 결정성 요건 없음 | 부정합 |

C·D·E·F는 하나로 환원된다: 검증 결과가 "무엇을·어느 코드에서·어떻게 실행했는지"에 묶여 있지 않다. 설계 응답은 **3튜플 앵커**(테스트 집합, 커밋 SHA, 실행 명령이 같고 워킹트리 clean이면 재실행 대신 인용)와 **검증 계층 표**(시점별 실행 집합 고정: Red 1개 → Green 맵 → Refactor 후 코드 변경 시만 맵 → `completed` 전이 시 의무 목록 전량 → 통합 시 전체 스위트 1회 → 재개 시 HEAD≠마지막 SHA일 때만 의무). 증가율은 O(n×스위트)에서 O(n×맵 + 스위트)로.

flaky 대응(원인 G): **의무 목록 진입 조건 = 같은 SHA에서 3회 연속 통과.** 미충족은 `보류(결정성 미확인)`으로 표기하고 게이트에 넣지 않으며 통합 시 전체 스위트에서만 실행.

기준선 측정(`02_baseline_llm_workflow.md`): 이 저장소는 완료 사이클 6개 중 자동 테스트가 있는 사이클이 2개뿐이고 둘은 코드를 공유하지 않아 증상을 재현하지 못한다. 그러나 기록 구조의 결함(SHA 0/35, 명령 2/35, 분류 어휘 0건)은 저장소 종류와 무관하게 확인됐다. flaky 실례 1건: `20260809-claude-hooks` T20 실패 — 코드가 아니라 하니스 단언식의 PowerShell 5.1 함정(`(파이프라인 단일 결과).Count`). 측정 스크립트 `measure_regression_baseline.py`는 `docs/work/<id>/work-log.md` 구조면 어느 저장소에서든 동작한다.

### 2.5 그 외 테스트 관련 발견

| 출처 | 발견 | 원문 위치 |
|---|---|---|
| E2EDevBench (PKU, arXiv 2511.04064) | 실전급 프로젝트 50개에서 SOTA 에이전트는 요구의 약 50%만 충족. 실패의 55.8%가 계획, 38.6%가 실행, **검증 5.7%**. Developer-Tester 2역 구조(53.5%)가 단일(43.0%)·Designer-Developer-Tester(32.8%)보다 우수 | `round3_deepdive_5papers.md` ② |
| 워터폴 ablation (Shafin 외, arXiv 2511.09794) | 4단계 중 **기여가 가장 큰 단계는 테스트**. 모델에 따라 정확도 효과는 정반대이나 품질(유지보수성)은 일관 개선 | `search_round3_phases_methodology_security.md` |
| RSTD (IBM·Zoom, arXiv 2605.15425) | 정적 분해는 재시도 비용을 80.5% 증가. 실패 서브태스크만 선택 재시도가 재시도 토큰 51.7~73.2% 절감 → "검증 완료 항목의 전면 재실행 금지"(S19) | 같은 파일, `01_solution_plan.md` AI-09 |
| 검증기 게이밍 — RLVR reward hacking (arXiv 2604.15149), EvilGenie(MIT) | RLVR 학습 모델은 검증기 약점을 공략하며 난이도·추론 예산이 커질수록 편법 증가. Isomorphic Perturbation Testing 제안. EvilGenie는 코딩 에이전트의 테스트 조작 벤치마크 | `aidlc_reading_list.md` C6 (정밀 분석 안 됨) |
| AI-DLC 2026 Backpressure | "어떻게를 처방하지 말고 나쁜 작업을 거부하는 게이트를 만들어라". 테스트·린트·보안·커버리지를 Stop마다 하네스가 실행. 게이트 조건은 기계 확인 가능한 것으로 한정, flaky 금지 | `llm_workflow_vs_papers_round1.md` §2.3, `bundleB_hooks_harness.md` §4 |
| Reversa (역공학) | 인계 시 관찰 가능한 동작을 Given/When/Then 시나리오 초안으로. 미실행 패리티 시나리오를 검증 완료로 기록하지 않는 원칙 | `bundleD_reveng_security.md` §1.4 |
| 리딩 리스트 B4 (미정밀) | TDD-Agent(2608.16742, 테스트를 진화하는 추론 산출물로), Scaling TDD to Classes(2602.03557), TDD Governance for Multi-Agent(2604.26615), Rethinking Verification(2507.06920, 검증용 테스트 품질 자체를 문제화), LLM-as-a-Verifier(2607.05391) | `aidlc_reading_list.md` B4 |

실험 설계 초안은 `s1-s3_papers_deep_dive.md` §1.7(의무 목록), §2.7(검증 깊이 표), §3.7(테스트 맵)에 있다. 후속 논문의 측정 설계에 재사용할 수 있다.

---

## 3. 외부 조사(2026-10-09) — 신규 근거

### 3.1 테스트 진화: 에이전트는 stale 테스트를 보지 못한다 **[초록]**

**TEBench** — Shang, Zhang, Hu, Fang, Xiao, Chen, *Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution*, arXiv 2605.06125.

- 첫 프로젝트 수준 테스트 진화 벤치마크. Defects4J 10개 프로젝트에서 314개 인스턴스. 에이전트가 저장소 전체에서 수정이 필요한 테스트를 스스로 찾고 새 테스트가 필요한 곳을 판단해 테스트 패치를 내야 한다.
- 세 분류: **Test-Breaking**(코드 변경 후 실패), **Test-Stale**(통과하지만 더 이상 바뀐 동작을 의미 있게 검증하지 않음), **Test-Missing**(새 기능에 필요한데 없음).
- Claude Code, Codex CLI, OpenCode의 7개 구성 모두 식별 F1 45.7~49.4%에서 정체. **Test-Stale이 가장 어려움(평균 F1 약 36%)**. 저자 진단: 에이전트는 "실행 실패 신호에 의존하고 능동적 의미 추론이 없다". execute-fail-fix 루프로 Breaking은 잘 고치지만 Stale·Missing은 구조적으로 다루지 못한다. 생성된 수정은 실행 가능하나 정답과 형태가 크게 다르다.
- **함의**: 요구 7번의 전제("에이전트가 알아서 정리하지 않는다")의 직접 실증. 워크플로우가 Breaking/Stale/Missing 분류를 명시적 트리거(자체 리뷰 문항, 관문)로 요구하지 않으면 stale 테스트는 쌓인다.

### 3.2 LLM 생성 테스트의 품질

**테스트 냄새** — Ouédraogo 외, *On the Diffusion of Test Smells in LLM-Generated Unit Tests*, arXiv 2410.10628v2 **[초록]**.
- LLM 4종(GPT-3.5, GPT-4, Mistral 7B, Mixtral 8×7B)의 클래스 수준 스위트 20,505개, TestBench 972건, EvoSuite 14,469건, 사람이 쓴 테스트 779,585건(34,635 Java 프로젝트). 탐지 도구 TsDetect(21종 냄새).
- 흔한 냄새: Assertion Roulette, Magic Number Test, Lazy Test, Conditional Logic Test, Empty Test, Exception Handling, Eager Test, Duplicate Assert, Unknown Test. 패턴이 사람 테스트와 겹쳐 학습 데이터 누출 의심. 프롬프트 전략·컨텍스트 길이·모델 규모에 따라 달라짐.
- 권고: 냄새 인지 생성 프레임워크, 프롬프트 전략, 탐지 도구 강화.

**뮤테이션 기반 품질 판정** **[초록]**
- MUTGEN — *Mutation-Guided Unit Test Generation with a Large Language Model*, arXiv 2506.02954. 뮤테이션 피드백을 프롬프트에 넣어 HumanEval-Java 89.5%, LeetCode-Java 89.1%의 뮤테이션 점수(각 1,144·1,900 mutants). 초기 실패 테스트의 약 50%를 자가 수리.
- GEM — *A Framework for Strengthening LLM-Generated Unit Tests Using Mutation Feedback* (CIbSE). 생성→실행 기반 자가 수리→뮤테이션 유도 오라클 강화. Python에서 뮤테이션 점수 개선, Java는 소폭.
- 공통 전제: 커버리지가 높아도 단언이 non-null 확인이나 구현 로직 복제 같은 동어반복이면 결함을 못 잡는다. 뮤테이션 점수가 커버리지보다 신뢰할 수 있는 지표.

**Just-in-Time 테스트** — Meta, *Just-in-Time Catching Test Generation at Meta*, arXiv 2601.22832; Harman 외, *Harden and Catch for Just-in-Time Assured LLM-Based Software Testing*, arXiv 2504.16472 (FSE 2025 keynote) **[초록]**.
- 구분: **hardening test**(생성 시점에 통과, 미래 회귀 방지) vs **catching test**(생성 시점에 실패해야 함, 변경이 들여온 결함을 랜딩 전에 포착).
- 생성 테스트 22,126건 분석: 코드 변경 인지 방식이 catching 후보 생성을 hardening 대비 4배, 우연히 실패하는 테스트 대비 20배 개선. 규칙·LLM 평가기로 리뷰 부담 70% 감소. 엔지니어에게 보고한 41건 중 8건 진양성, 그중 4건은 심각한 장애로 이어질 수 있었던 것.
- **함의**: 워크플로우의 TDD Red 테스트는 catching, TASK 완료 후 남기는 유지 테스트는 hardening이다. 둘의 수명이 다르다 — catching은 결함이 고쳐지면 hardening으로 전환되거나 폐기되어야 하며, "PR마다 생성하고 버리는" 운영도 가능하다. 이 구분이 의무 목록의 `대체·폐기` 전이에 근거를 준다.

### 3.3 삭제·축소 기준

**실무 삭제 기준** — tessl 레지스트리 `testland/test-removal-criteria` 스킬 **[본문: 개요 페이지만]**.
- 삭제 분류 5종: **duplicate**(중복 커버리지), **tautology**(항상 통과), **trivial**(의미 있는 검증 없음), **dead-signal**(코드가 바뀌어도 실패한 적 없음), **orphan**(소유자·목적 불명).
- 삭제 관문 4조건: "every condition must hold or the verdict reverts to keep". 개별 조건 원문은 링크된 reference 파일에 있어 **미확인**(후속 조사 §5).
- 삭제마다 서면 사유, 테스트별 소스 맵에서 나온 중복 커버리지 증거, 지명된 리뷰어.
- "A test that has merely never failed is treated as possibly load-bearing, not worthless." — 입증 책임을 삭제 쪽에 둔다.

**테스트 스위트 최소화 문헌** **[2차]**
- Yoo & Harman, *Regression testing minimization, selection and prioritization: a survey*, STVR 22(2), 2012. 최소화(영구 제거)·선택(이번 변경에 관련된 것만)·우선순위(순서)의 세 문제를 구분. 최소화는 집합 덮개 문제로 NP-완전이라 휴리스틱 사용.
- 중복 판정 기준은 문장 커버리지, 실행 비용, 뮤테이션 커버리지, MC/DC 등. 코드 커버리지는 일부 상황에서만 결함 밀도의 충분한 지표이며 대부분 뮤테이션·축소 가능성이 더 낫다(IEEE Access 2023, 4개 오픈소스 비교).
- 그리디 최소화는 평균적으로 스위트를 70% 크기로 줄이면서 결함 탐지력을 유지(2020 SWQD, Teamscale).
- TDAD가 인용한 RTS 고전(Legunsen 2016 정적 클래스 수준, Gligoric 2015 파일 수준, Chianti 2004 메서드 수준)은 선행 조사 색인 §3-D에서 미조사 영역으로 남아 있다.

**에이전트 테스트 중복 생성** **[2차]**
- 실무 보고(TestMu AI 등): AI가 테스트 생성을 거의 무료로 만들자 "스위트에 이미 있는지와 무관하게" 새로 쓰고, 테스트 수는 늘고 실행은 느려진다. 중복 탐지 도구는 제목·단계·설명 유사도를 0~100으로 점수화해 리뷰 후 삭제.
- 참고: *Reducing AI-Generated CodeSlop via Agent Trajectory Minimization* (arXiv 2607.18161) **[초록]**은 테스트가 아니라 코드 패치의 제거 가능 중복을 다룬다. 다만 "에이전트의 자기 최소화는 3.8~44.9% 실패"와 "TRIM이 변경의 17.9~32.9%를 제거"라는 결과는 테스트 정리에도 같은 교훈을 준다 — 자기 정리를 시키지 말고 외부 절차로 검증하며 제거하라.

### 3.4 flaky 테스트

- Luo 외, *An empirical analysis of flaky tests*, FSE 2014 **[2차]**. 51개 오픈소스 프로젝트의 수정 커밋 201건. 근본 원인: async wait 45%, concurrency 20%, 테스트 순서 의존 12%, 리소스 누수 8%, 네트워크 5%, 시간 4%.
- Google (Listfield, *Where do our flaky tests come from?*, Google Testing Blog 2017.4) **[2차]**. 테스트 크기 small/medium/large는 작성자가 라벨링하되 바이너리 크기·RAM과 잘 상관. 일주일 동안 small 0.5%, medium 1.6%, large 14%가 flaky. 정책: 도구가 flakiness를 감시해 임계 초과 시 **자동 격리(quarantine)** — 계속 실행하되 빌드를 실패시키지 않고 critical path에서 제거, 수정 버그 발행.
- 추가 문헌(미정밀): *Systemic Flakiness: co-occurring flaky test failures* (arXiv 2504.16777), Parry 외 *A Survey on How Test Flakiness Affects Developers* (arXiv 2203.00483), Habchi 외 *A Qualitative Study on the Sources, Impacts, and Mitigation Strategies of Flaky Tests* (ICST 2022).
- **함의**: 선행 조사의 "같은 SHA 3회 통과" 진입 조건은 결정성 확인이고, 운영 중 발현하는 flaky에는 Google식 격리 상태가 따로 필요하다. 의무 목록 상태에 `격리`를 추가하는 근거.

### 3.5 테스트 설계 원칙

**Kent Beck, Test Desiderata** (*Desirable Unit Tests*, newsletter.kentbeck.com) **[본문]**. 12개 속성: Isolated, Composable, Deterministic, Specific, Behavioral, Structure-insensitive, Fast, Writable, Readable, Automated, Predictive, Inspiring. "You can think of them as sliders — more of this, sometimes less of that." 전부 최대화할 수 없고 서로 충돌한다.
- 워크플로우에 바로 옮길 셋: **Behavioral**(동작이 우연히 바뀌면 실패해야 함), **Structure-insensitive**(협력자를 전부 mock하면 구조 민감성의 악몽), **Deterministic**(시계·난수는 테스트가 값을 주입). 현행 §3.5의 "구현 방식이 아니라 요구 동작을 검증하는가"가 Behavioral의 흔적이지만 작성 기준(§2.4)에는 없다.

**Google 테스트 크기** (§3.4 참조). 크기 라벨은 실행 시점(검증 계층 표의 행)을 정하는 객관적 근거가 된다 — small은 매 Green, medium은 TASK 완료, large는 통합 시.

### 3.6 에이전트 실무 지침과 하네스

- AGENTS.md/CLAUDE.md 가이드 공통: 저장소가 추론할 수 없는 명령·제약·검증 단계만 적고 일반 소프트웨어 공학을 가르치지 말 것. Anthropic 권고 CLAUDE.md 200줄 이하, 길수록 준수율 저하 **[2차]**.
- "NEVER modify or delete existing tests unless explicitly instructed"가 널리 쓰이는 규칙. Kent Beck 보고: 에이전트가 스위트를 통과시키려고 테스트를 통째로 지운다 **[2차]**.
- Vaughan, *The Agent Testing Lifecycle* (2026.6) **[본문]**: 3단계 — (1) TDD 작성: PreToolUse 훅이 `*_test.*`, `test_*.*`, `**/tests/**` 쓰기를 차단해 구현을 고치게 강제, (2) 테스트 진화: PostToolUse 훅이 변경 파일에 뮤테이션 분석을 돌려 80% kill 임계 강제, PR마다 catching 테스트를 생성 후 폐기, (3) 리뷰 아키텍처: AGENTS.md(권고) + 결정적 훅(집행) + Stop 게이트(완료 차단) 3층. 인용 수치 TDFlow 94.3% SWE-Bench Verified, SlopCodeBench 77% 구조 침식은 **원문 미확인**.
- *Tests Beat Instructions for AI Coding Agents* (caimito.net 2026.4) **[2차]**: 테스트는 실행되는 명세이며 "에이전트는 실패하는 단언을 말로 넘어갈 수 없다". 에이전트가 테스트와 구현을 둘 다 쓰면 테스트는 아무것도 검증하지 않는다 — 명세의 독립성.
- **함의**: "삭제 금지" 가드와 "정리 필요"는 시점으로 양립시킨다. Green을 만드는 과정에서는 금지, 사이클 통합의 재정비 관문에서만 증거·승인과 함께 허용.

---

## 4. 종합 — 워크플로우 설계에 대한 함의

### 4.1 세 겹 구조와 근거 대응

| 겹 | 내용 | 근거 | 배치 |
|---|---|---|---|
| **① 작성 기준** | 행위 검증·구조 둔감(mock 전부 금지), 결정성(시계·난수 주입, 같은 SHA 3회 통과), 하나의 테스트는 하나의 동작, 단언은 실패할 수 있어야 함(Red 증거), 크기 라벨 small/medium/large | Beck §3.5, 선행 조사 원인 G, 테스트 냄새 §3.2, Google §3.4 | wf-implement §2.4 본문 열 줄 안팎 + references(냄새 체크리스트) |
| **② 수명주기** | 상태 5종과 전이 트리거(§4.2), 재정비 관문(§4.3), 격리 | LoopsBench §2.2, TEBench §3.1, JiT §3.2, tessl §3.3, Google §3.4 | wf-implement §3.3·§3.5·§3.6, work-log 의무 목록 절, 완료 보고 절 |
| **③ 기계적 검사** | 냄새 린트, 변경 파일 한정 뮤테이션, 커버리지 중복 판정, Stop 게이트 | TsDetect §3.2, MUTGEN/GEM §3.2, Vaughan §3.6, AI-DLC §2.5 | 훅·스크립트(후순위, 요구 8의 도구 조사와 함께) |

### 4.2 상태 모델과 전이 트리거 (초안)

| 상태 | 의미 | 진입 트리거 | 근거 |
|---|---|---|---|
| **유지** | 의무 목록의 현역. 통합·`completed` 전이·재개 시 전량 실행 | TASK `completed` 전이 + 같은 SHA 3회 통과 | LoopsBench, 선행 조사 G |
| **대체** | 기준선 변경으로 의미가 바뀐 테스트를 새 테스트가 대신함 | DCR 승인과 같은 변경. 대체 테스트 ID 기록 | S2 "삭제 금지, 대체로" |
| **병합** | 같은 보호 스코프를 더 넓은 테스트가 덮어 흡수 | 재정비 관문에서 중복 증거(커버리지 겹침 또는 뮤테이션 동치) | tessl duplicate, 최소화 문헌 |
| **격리** | 비결정적 발현. 계속 실행하되 차단·게이트에서 제외 | 유지 상태에서 같은 SHA 결과 불일치 발생 | Google quarantine, Luo 원인 분류 |
| **폐기** | 보호 스코프 소멸, 동어반복, 신호 없음 등으로 제거 | 재정비 관문 4조건 전부 성립 + 사용자 승인 | tessl 5분류·관문 |

전이는 재정비 관문(사이클 통합 §3.6, DCR 반환)에서만 일어난다. 매 TASK에서는 등록과 격리만 허용한다. 코드 변경이 보호 스코프를 건드리면 영향 테스트를 **Breaking/Stale/Missing**으로 분류해 기록하는 것을 §3.5 자체 리뷰 문항으로 둔다 — TEBench가 보인 대로 Stale은 실행 신호가 없으므로 문항이 유일한 트리거다.

### 4.3 삭제 관문 조건 (초안, tessl 4조건 원문 확인 전 자체 설계)

폐기·병합은 다음이 **전부** 성립할 때만. 하나라도 미달이면 유지.

1. 분류가 5종(중복·동어반복·자명·신호 없음·고아) 중 하나로 명시되고 사유가 기록됨.
2. 증거가 있음 — 중복은 커버리지 겹침 또는 뮤테이션 동치, 동어반복은 구현을 바꿔도 통과하는 실험, 고아는 보호 스코프의 파일·심볼이 현재 트리에 없음.
3. 해당 테스트가 어떤 인수 조건(AC)의 유일한 검증이 아님. 유일하면 대체 테스트를 먼저 등록.
4. 사용자 승인 — 완료 보고의 "테스트 재정비 결과" 절에서 일괄 승인 가능.

"한 번도 실패한 적 없음"은 단독으로 폐기 사유가 아니다. 폐기 행은 삭제하지 않고 상태·이유·일시를 남긴다(wf-doc "삭제 항목은 이유를 남긴다" 규칙과 일치).

### 4.4 분량과 조건화의 상한

- Skills Harmful: 검증 범위를 불확실성·변경 크기·예산에 조건화. 의무 목록 전량 실행은 `completed`·통합·재개 3시점만(선행 조사 S2 정정).
- TDAD: 절차 텍스트는 무익하거나 해롭고 컨텍스트(어떤 테스트)가 효과. 작성 기준은 판단 규칙 열 줄, 체크리스트는 references.
- AGENTS.md 실무: 저장소가 추론할 수 없는 것만. 테스트 명령·크기 라벨·보호 스코프는 저장소별 test-map에, 원칙은 스킬에.
- 뮤테이션·커버리지 비율을 인수 조건으로 쓰면 수치 맞추기(검증기 게이밍 §2.5)를 부른다. 추세 관찰과 중복 판정 근거로만.

---

## 5. 공백과 후속 조사 과제 (3번 단계 입력)

| 과제 | 왜 필요한가 | 출발점 |
|---|---|---|
| tessl 삭제 관문 4조건 원문 | §4.3 자체 설계를 실무 기준과 대조 | `applying-the-removal-classes.md`, `removal-ledger-and-report-format.md` (tessl 레지스트리 내부 파일) |
| RTS 고전 정밀 | 테스트 맵·선택 실행의 이론적 뿌리, 정적 vs 동적 선택의 안전성 | Rothermel & Harrold 1997, Gligoric 2015 (Ekstazi), Legunsen 2016 (STARTS), Yoo & Harman 2012 |
| 커버리지·결과 기록 도구 (요구 8) | 언어별 표준 형식(JUnit XML, Cobertura, LCOV)과 시각화. 추세 그래프 | coverage.py/pytest-cov, Pester CodeCoverage(PowerShell 훅 저장소용), JaCoCo |
| 뮤테이션 도구 비용 | 관문 옵션으로 둘 때의 실행 시간·설정 부담 | mutmut/cosmic-ray(Python), PIT(Java), Stryker(JS). Vaughan의 80% 임계 근거 확인 |
| 테스트 냄새 탐지 도구 | ③ 린트의 실체. Java 외 언어 지원 여부 | TsDetect(Java), pytest-smell 계열 유무 조사 |
| TDFlow·SlopCodeBench 수치 | §3.6 2차 인용의 원문 확인 | CMU TDFlow, SlopCodeBench 논문 |
| 검증기 게이밍 정밀 | 커버리지·뮤테이션을 지표로 둘 때의 게이밍 위험 | arXiv 2604.15149 (Isomorphic Perturbation Testing), EvilGenie |
| 리딩 리스트 B4 미정밀 5편 | TDD-Agent, Rethinking Verification 등이 테스트 수명에 주는 함의 | `aidlc_reading_list.md` B4 |
| 산문 저장소에서의 적용 | 이 저장소(스킬 산문)는 자동 테스트가 2사이클뿐. 효과 측정은 코드 저장소에서 | `02_baseline_llm_workflow.md` §4의 절차 |
| 한국어 환경 | 테스트 냄새·토큰 임계 연구가 영어·Java 중심 | 선행 조사 색인 §3-D |

---

## 6. 출처 목록

### 6.1 선행 조사에서 가져온 1차 출처

| 식별자 | 제목 | 링크 | 본 문서 |
|---|---|---|---|
| arXiv 2603.17973 | TDAD: Test-Driven Agentic Development | https://arxiv.org/abs/2603.17973 | §2.1 |
| arXiv 2608.00267 | LoopsBench: From Harness Engineering to Loop Engineering | https://arxiv.org/html/2608.00267v1 | §2.2 |
| arXiv 2608.11888 | Agent Skills Can Be Harmful: Skill-Induced Failures | https://arxiv.org/html/2608.11888v1 | §2.3 |
| arXiv 2511.04064 | E2EDevBench | https://arxiv.org/html/2511.04064 | §2.5 |
| arXiv 2511.09794 | Evaluating Software Process Models for Multi-Agent Class-Level Code Generation | https://arxiv.org/html/2511.09794v1 | §2.5 |
| arXiv 2605.15425 | Runtime-Structured Task Decomposition | https://arxiv.org/html/2605.15425v1 | §2.5 |
| arXiv 2604.15149 | LLMs Gaming Verifiers: RLVR Can Lead to Reward Hacking | https://arxiv.org/pdf/2604.15149 | §2.5 |
| — | AI-DLC 2026 | https://han.guru/papers/ai-dlc-2026/ | §2.5 |

### 6.2 2026-10-09 신규 출처

| 식별자 | 제목 | 링크 | 검증 수준 | 본 문서 |
|---|---|---|---|---|
| arXiv 2605.06125 | TEBench: Breaking, Stale, or Missing? | https://arxiv.org/abs/2605.06125 | 초록 | §3.1 |
| arXiv 2410.10628 | On the Diffusion of Test Smells in LLM-Generated Unit Tests | https://arxiv.org/abs/2410.10628v2 | 초록 | §3.2 |
| arXiv 2506.02954 | Mutation-Guided Unit Test Generation with a LLM (MUTGEN) | https://arxiv.org/abs/2506.02954 | 초록 | §3.2 |
| CIbSE | GEM: Strengthening LLM-Generated Unit Tests Using Mutation Feedback | https://sol.sbc.org.br/index.php/cibse/article/view/42441 | 초록 | §3.2 |
| arXiv 2601.22832 | Just-in-Time Catching Test Generation at Meta | https://arxiv.org/pdf/2601.22832 | 초록 | §3.2 |
| arXiv 2504.16472 | Harden and Catch for Just-in-Time Assured LLM-Based Software Testing | https://arxiv.org/html/2504.16472v2 | 초록 | §3.2 |
| tessl | test-removal-criteria 스킬 | https://tessl.io/registry/testland/test-removal-criteria/skills | 개요 본문 | §3.3 |
| STVR 2012 | Yoo & Harman, Regression testing minimization, selection and prioritization: a survey | https://acawiki.org/Regression_testing_minimization,_selection_and_prioritization:_a_survey | 2차 | §3.3 |
| IEEE Access 2023 | 커버리지·뮤테이션·축소 가능성 비교 | https://doaj.org/article/2c476261156943f588292e22db8300bd | 2차 | §3.3 |
| SWQD 2020 | Test suite minimization (Teamscale) | https://teamscale.com/hubfs/26978363/Publications/2020-test-suite-minimization-swqd.pdf | 2차 | §3.3 |
| arXiv 2607.18161 | Reducing AI-Generated CodeSlop via Agent Trajectory Minimization | https://huggingface.co/papers/2607.18161 | 초록 | §3.3 |
| FSE 2014 | Luo 외, An empirical analysis of flaky tests | https://2024.esec-fse.org/details/fse-2024-plenary-events/10/An-empirical-analysis-of-flaky-tests | 2차 | §3.4 |
| Google Testing Blog 2017 | Listfield, Where do our flaky tests come from? | https://testing.googleblog.com/2017/04/ (요약: https://blog.trafficparrot.com/2017/05/flaky-tests-at-google.html) | 2차 | §3.4 |
| arXiv 2504.16777 | Systemic Flakiness | https://arxiv.org/html/2504.16777v1 | 미정밀 | §3.4 |
| — | Kent Beck, Desirable Unit Tests (Test Desiderata) | https://newsletter.kentbeck.com/p/desirable-unit-tests | 본문 | §3.5 |
| — | Vaughan, The Agent Testing Lifecycle | https://codex.danielvaughan.com/2026/06/19/agent-testing-lifecycle-codex-cli-tdd-test-evolution-review-architecture/ | 본문 | §3.6 |
| — | Mutation Testing as a Quality Gate for AI-Generated Test Suites (agentpatterns.ai) | https://www.agentpatterns.ai/verification/mutation-testing-quality-gate/ | 2차 | §3.2 |
| — | Tests Beat Instructions for AI Coding Agents (caimito.net) | https://caimito.net/en/blog/2026/04/17/tests-beat-instructions-for-ai-coding-agents.html | 2차 | §3.6 |
| — | AGENTS.md 가이드 (tembo.io, eesel.ai 등) | https://www.tembo.io/blog/agents-md | 2차 | §3.6 |

### 6.3 저장소 내부 출처

- `docs/research/20260919-aidlc-research/` — `s1-s3_papers_deep_dive.md`, `llm_workflow_vs_papers_round1.md`, `01_solution_plan.md`, `02_baseline_llm_workflow.md`, `measure_regression_baseline.py`, `round3_deepdive_5papers.md`, `search_round3_phases_methodology_security.md`, `aidlc_reading_list.md`, `bundleB_hooks_harness.md`, `bundleD_reveng_security.md`
- `skills/wf-implement/SKILL.md` §2.4·§3.3~3.6·§5, `skills/wf-doc/references/templates.md` 검증 결과 템플릿 (`c4cde3f`)
- `archive/202609-cycles` 브랜치 `docs/work/20260920-regression-tier/` (ADR-004, req-design, test-map, work-log), `skills/wf-implement/references/verification-depth.md`

# llm_workflow × AI-DLC 논문 대조 — 1차

> 대상 저장소: https://github.com/bluesky5008/llm_workflow (HEAD `c4cde3f`, 2026-08-17)
> 대조 논문 7편: TDAD · Agent Skills Can Be Harmful · SKILL.md Smells · AI-DLC 2026 · LoopsBench · PROJECTMEM · Evaluating AGENTS.md (+ Codified Context, Reversa 보조)
> 작성: 2026-08-27. 논문 수치는 본문에서 재확인했고, 확인 못한 항목은 그렇게 표기함.

---

## 0. 한 줄 결론

워크플로우의 **상태 규율(작업 기록·인계·기준선)은 논문들이 지목한 장기 작업 병목에 정확히 대응하는 강점**이다. 반면 **회귀 검증은 "어떻게(절차)"만 있고 "무엇을(테스트 목록)"이 없으며**, 스킬 본문 부피와 검증 체크리스트 총량은 2026년 실증 논문들이 "성능을 깎는 패턴"으로 지목한 형태에 가깝다. 다음 스텝은 규칙을 더하는 방향이 아니라 **컨텍스트 산출물을 추가하고 절차 텍스트를 줄이는 방향**이 논문 근거에 부합한다.

---

## 1. 대조 기준 — 워크플로우 현황 (저장소에서 확인한 사실)

| 항목 | 현황 |
|---|---|
| 구조 | wf-design(요구·설계) → **사용자 승인 관문** → wf-implement(계획·구현·검증·통합). wf-doc(형식), wf-tree(계획 트리)는 횡단 계층 |
| 스킬 부피 | SKILL.md 4개 = 106KB(wf-implement 32.5KB/375줄, wf-doc 29.9KB, wf-design 23.6KB, wf-tree 20.4KB) + references 3개 43KB. 정식 경로 1세션에 통상 3개 로드 → 한글 기준 약 **45k–65k 토큰** 추정 |
| 위임 구조 | wf-design·wf-doc은 references/로 위임. **wf-implement·wf-tree는 references 없음** |
| 항상 로드 | CLAUDE.global.md 6줄(576자) — 저장소 개요 없이 비표준 규칙만 |
| TDD·검증 | §3.3 Red/Green/Refactor + 재현 테스트 + 특성화 테스트, §3.4 6단계 검증 + 실패 4분류, §3.5 자체 리뷰 22문항, §3.6 통합 시 최종 빌드·테스트 재실행, wf-doc §4 13문항, wf-tree §9 10문항 |
| 자율 범위 | 승인 후 기준선 안에서 자율, push/PR/배포/삭제는 별도 승인 (2모드 이분법) |
| 메모리 | docs/work/<ID>/work-log.md 산문 + decisions.md 등록부 + 훅 3종(세션 시작 재개 / transcript 1,500KB 임계 인계 / 컴팩션 후 재정렬). 파일 편집 전 조회 장치 없음 |
| 역공학 | 16단계, EV→OBS→RR→RD 증거 사슬, CON/GAP 분리, 5단 신뢰도 + 반증 조건 |

---

## 2. 논문별 대조

### 2.1 TDAD — 회귀를 줄인 것은 TDD 절차가 아니라 테스트 목록이었다

**논문 사실 (arXiv 2603.17973v2, 재확인)**
- SWE-bench Verified 100건, Qwen3-Coder 30B 4-bit, 32K 컨텍스트. 테스트 단위 회귀율: Vanilla **6.08%** → TDD 절차 프롬프트 **9.94%** → 의존 맵 제공 **1.82%**.
- 제공물은 `test_map.txt`(소스 파일→테스트 파일, 한 줄 한 매핑)와 **20줄 SKILL.md**("수정 → grep으로 관련 테스트 찾기 → 실행·고치기"). MCP·DB 없음, grep만.
- 자동 개선 루프에서 가장 효과 큰 변경은 **SKILL.md를 107줄 9단계 TDD 절차 → 20줄로 축약**한 것(해결률 12%→50%). 단 맵 없이 프롬프트만 줄이면 30%→20%로 악화.
- 저자의 설명: 절차 지시가 저장소 컨텍스트를 밀어냄 + TDD 지시가 더 야심찬 수정을 유도했는데 어떤 테스트를 확인할지 몰라 부수 피해. "context (which tests to check) outperforms procedure (how to do TDD)".
- 한계: 소형 모델·Python·통계 검정 없음. 인스턴스 단위 회귀율은 개선 없음. 프론티어 모델 재현은 미확인.

**대조**

| 논문 요소 | 워크플로우 | 판정 |
|---|---|---|
| 코드↔테스트 의존 맵 산출물 | 없음. §3.2 계획은 "수정 파일·작업 간 의존"만 | **공백** |
| 변경 후 어떤 테스트를 돌릴지 | §3.4 2단계 "변경 영역의 단위 테스트" — 영역 판단을 에이전트에 위임 | 부분 |
| 회귀 확인 | §3.5 "회귀가 없는가?" 질문만, 확인 수단 없음 | 부분 |
| 실패 분류·증거 기록 | §3.4 4분류, 실패→성공 전환 증거 | **논문보다 정교**. 단 변경 전 테스트 실행 기록이 의무가 아니라 "이번 변경으로 발생" 판정 근거가 약함 |
| 특성화 테스트 | §3.3 + 역공학 §8 | 논문에 없는 강점 |
| 절차형 TDD 지시 | §2.4+§3.3+wf-tree 자동 제안 | **긴장** — 논문의 악화 조건(119줄 절차)과 형태 유사 |

**시사점.** §3.3을 버릴 근거는 아니다(논문은 test-first vs test-after를 비교하지 않았고, TDAD의 SKILL.md는 사실상 사후 검증). 그러나 현 워크플로우는 F2P(새 동작) 쪽 지시가 두껍고 P2P(회귀) 쪽이 얇다. 논문이 효과를 본 변수는 **"어떤 테스트"라는 컨텍스트**이므로, 균형을 그쪽으로 옮기는 것이 근거에 부합한다.

### 2.2 Agent Skills Can Be Harmful + SKILL.md Smells — 스킬 자체가 실패 원인이 된다

**논문 사실 (2608.11888 / 2607.01456, 재확인)**
- 확정 실패 307건 중 기능 실패의 **68.8%는 Task-Implementation Fault**(관련 있어 보이는 스킬이 필수 요소를 오기입·누락). 효율 저하의 **62.6%는 과잉 절차**, 그중 **과잉 검증 36.8%** — 정의: "산출물이 나온 뒤의 반복 테스트·재빌드·**체크리스트 검증**". 컨텍스트 과부하 회귀 46건 중 43건은 **필수 스킬 본문 텍스트**가 원인.
- 권고: 필수 요구와 템플릿·예시 분리 / 실행 전 스킬-태스크 호환성 점검 / **검증 범위를 불확실성·변경 크기·예산에 조건화** / 선택 자료는 지연 로드.
- Smells: 238개 SKILL.md, 평균 10.5개 냄새, 99.6%가 1개 이상. 최다 **Rationalization Loophole 94%**("필수 단계를 건너뛰는 합리화를 막는 지침 없음"). 임계: 본문 5,000단어, description 1,024자.

**린트 결과 (4개 스킬 + 루트)**

| 냄새 | 판정 | 근거 |
|---|---|---|
| Rationalization Loophole | **비해당(부분)** | "판단이 애매하면 정식 경로", "실행 못한 검증은 성공 아님", "필수 게이트는 생략 제안 안 함" — 엄격 쪽 기본값이라 오히려 anti-loophole. 잔여 허점: 경량 경로 조건("국소적·되돌리기 쉬운")이 에이전트 자기판정이고 관찰 가능한 기준(파일 수·공개 심볼 변경)이 없음 |
| Undelegated Detail | **해당** (wf-implement, wf-tree) | references 없음. §2.4 결정 사다리, §3.5 22문항, §7 레이아웃이 본문. wf-tree는 hex 색상표·mermaid 예시·대형 트리 규칙이 본문 |
| Buried Gotchas | **해당** (전체) | 경고 헤더 없음. "설계 승인 ≠ 실행 승인"이 산문으로 3곳 반복, wf-tree "점선 방향이 UML과 반대"가 문단 속, wf-doc "링크 미충족 시 완료 금지"가 파일 끝 |
| Missing Utility Script | **해당** (wf-doc, wf-tree) | 링크·앵커 존재 검사, 트리 재생성, 노드 30 초과 분할을 LLM이 손으로 수행 |
| Lengthy Skill Body | 형식상 비해당, **실질 부분** | 692–1,190어절 < 5,000단어. 그러나 375줄은 Anthropic 500줄 권고의 75%이고, 구현 1건에 implement+doc+tree+templates ≈ 100KB가 적재 |
| Missing Example | 해당 (wf-implement) | 계획 항목·작업 기록·경량 보고 예시 0개 |
| Series of Commands | 부분 (§3.4) | 6단계 고정 순서. "위험에 비례" 단서는 있으나 생략 규칙 없음 |
| NVS/EWP/NAH/NPT, LSD, CSD, XID 등 | 비해당 | 검증·계획·승인·진행 추적이 모두 있음 |

**과잉 검증 판정: 해당(부분).** 작업 단위마다 §3.3 근접 검증 → §3.4 6단계 → §3.5 22문항 + 재검증 → §3.6 최종 빌드·테스트(§3.4와 중복 = 논문의 *repeated rebuilds*) → wf-doc 13문항 → wf-tree 10문항. 세 스킬에 걸쳐 **체크리스트 45문항**이 산출물 이후에 실행된다. 완화 장치("위험에 비례", 경량 경로, "자명한 한 줄은 테스트 불요")는 있으나 **어느 단계를 언제 생략하는지의 연산 규칙과 예산 신호가 없다**. 부수적으로 계획 항목 완료마다 work-log 갱신 + 트리 재생성 + 백링크 + decisions.md 갱신은 코드 변경 1건당 문서 파이프라인 4–5회(논문의 Heavy Implementation Pipeline 패턴).

**호환성 공백 (Artifact Misplacement 19.2%와 같은 유형).** `docs/requirements.md`·`docs/plan.md`·`docs/work/<id>/` 경로가 고정. 저장소가 `docs/adr/` 같은 자체 관례를 가질 때의 규칙이 없다. §3.3 "기존 구조를 따른다"는 코드에만 적용된다.

### 2.3 AI-DLC 2026 + LoopsBench — 관문 구조와 장기 작업 상태 규율

**AI-DLC 2026 사실**
- Intent(완료 기준 내장) → Unit(`depends_on` DAG, 독립 배포 가능) → Bolt(시간·일 단위 반복, 모드 지정). 3모드: HITL(매 단계 승인, 신규·비가역·고위험) / OHOTL(실시간 관찰·비차단 개입, 창의·주관·UX) / AHOTL(경계 내 자율, `COMPLETE`/`BLOCKED` 신호, 기계적 검증 가능 작업). "불확실하면 더 많은 감독이 기본". 모드 전환 트리거는 본문에서 확인 못함.
- Backpressure: "어떻게를 처방하지 말고 나쁜 작업을 거부하는 게이트를 만들어라". 테스트·`tsc --noEmit`·린트 0경고·보안 스캔·커버리지·p95 등을 **Stop 이벤트마다 하네스가 실행, 실패 시 block**. 추가 전용 래칫.
- Ralph Wiggum 루프: 시도→게이트 피드백→조정→반복, 반복 한도(예시 50)·차단 문서화.
- "Phase gates that once provided quality control now create friction" — 비판 대상은 **handoff**(다른 주체, 문서 전달, 컨텍스트 소실). 대안은 checkpoint(같은 에이전트, 컨텍스트 보존)와 Passes(렌즈별 반복, 역방향 정상).
- 메모리 5계층(Rules·Session·Project·Organizational·Runtime), `.ai-dlc/knowledge/`에 conventions·domain 등 횡단 지식.

**LoopsBench 사실 (2608.00267)**
- 112 태스크, 5,300+ 유닛 DAG, 의존 깊이 중앙값 6. 최고 조합 Opus 4.7 + Claude Code + outer continuation **25.0%**. 재시작형 Ralph 루프 **7.84%**(최저), dynamic workflows 24.1%(98라운드).
- 병목: "loop state discipline — missing dependencies, inflated patches, sparse tests". 계획의 의존 간선 F1 0.71(Claude Code), 패치 gold 대비 1.58×, 테스트 28 vs 네이티브 74.
- 회귀: 완료 유닛과 선행 유닛의 테스트를 이후 모든 계층에서 강제 → 회귀율 7.11%. **"Context-budget renewal does not remove regression pressure."**

**대조**

| 논문 요소 | 워크플로우 | 판정 |
|---|---|---|
| Unit `depends_on` DAG | TASK-NN + wf-tree `depends:`(분해와 순서 분리) | 일치 |
| 완료 기준(프로그램 검증) | AC-NN ↔ VER-NN, "실행 못한 검증은 성공 아님" | 부분 — AC가 하네스 게이트로 실행되지 않음 |
| 3 운영 모드 | 승인 후 자율(≈AHOTL) + 외부 작업 HITL 이분법. **OHOTL 없음**, 작업별 모드 선택 없음 | **공백** — dev-briefing(TASK-08·12)처럼 취향이 필요한 작업이 HITL 관문으로 처리됨 |
| Backpressure 하네스 게이트 | §3.4 검증 순서는 있으나 훅은 인계 신호만 주입, fail-open, Stop 차단 없음 | 부분 |
| Mob Elaboration + Adversarial Spec Review | wf-design §8 승인 관문(산출물 유사). 모순·가정·공백 적대적 검토 단계 없음 | 부분 |
| File-based memory | work-log·ADR·DCR·"상시 재개 가능 불변식" | 일치. 횡단 `knowledge/` 층은 없음 |
| Plan state (의존 누락) | `depends:` 표현은 있으나 의존 복원을 강제·검증하는 절차 없음 | 부분 |
| Code state (패치 팽창) | §2.4 결정 사다리·최소 diff | **강함** |
| Test state (희소) | "깨지면 실패하는 최소 1개" | 방향 일치, sparse 쪽 위험 |
| 회귀 압력 | §3.6 사이클 말미 재실행. **TASK 완료마다 선행 TASK 테스트 재실행 의무 없음** | 공백 |
| 컨텍스트 갱신 후 상태 손실 | 작업 기록 불변식 + post-compact "요약≠정본" + 임계 인계 | **핵심 강점** — LoopsBench 결론과 정확히 맞닿음 |

**시사점.** (1) "phase gates create friction"은 사용자 관문에 직접 적용되지 않는다 — 같은 에이전트가 문서 기준선을 들고 계속하므로 AI-DLC의 checkpoint에 가깝다. 진짜 긴장은 DCR 반환 흐름이 Passes보다 무겁고 "애매하면 중대"가 관문 빈도를 높인다는 점. (2) 재시작형 루프가 최악(7.84%)이었다는 결과는 사용자 훅이 "재시작 직전 상태 직렬화"를 강제하는 설계가 옳았음을 뒷받침한다. 다만 인계 프롬프트가 **완료 TASK의 회귀 의무(유지할 테스트 목록)**를 넘기지 않는다.

### 2.4 PROJECTMEM + Evaluating AGENTS.md (+ Codified Context, Reversa)

**PROJECTMEM 사실 (2606.12329)** — typed 이벤트 5종(issue/attempt[worked|failed|partial]/fix/decision/note) append-only JSONL, `summary.md`는 fold로 결정적 재생성(LLM 없음). `precheck_file(path)`가 편집 전 해당 경로의 failed attempt·open issue·high churn을 조회해 경고(advisory). 비밀 정보 정규식 자동 마스킹. 토큰 800–1,500 vs 재구성 5,000–20,000(자체 추정, 통제 실험 아님).

**Evaluating AGENTS.md 사실 (2602.11988 v2)** — None/LLM생성/개발자커밋 3조건. 성공률 차이 모두 비유의(LLM생성 −0.5%/−2%, 개발자커밋 +2.4%); **LLM생성 vs 개발자커밋 7%p만 유의(p=.038)**. 비용 +20–23%. 지시는 잘 준수됨(`uv` 언급 시 1.6회/인스턴스 vs <0.01). 결론: 저장소 개요는 무익, **비표준 관행만** 넣어라.

**대조 — 메모리**

| 항목 | PROJECTMEM | 워크플로우 | 판정 |
|---|---|---|---|
| 저장 단위 | typed 이벤트 | 산문 work-log + decisions.md | 차이가 핵심 |
| 재개 진입 | summary.md | 세션 시작 훅 → 인계 절 "다음 행동" | 동등 (사용자 쪽이 결정 이유·기각 대안 보존은 우월) |
| 편집 전 조회 | `precheck_file` | **없음** — 다른 작업 ID에서 같은 파일을 건드릴 때 과거 기록을 읽을 의무도, 파일 경로 색인도 없음 | **공백** |
| 비밀 마스킹 | 자동 | wf-doc §2.5 규칙(준수 의존) | 부분 |
| 컴팩션 방어 | 없음 | post-compact 훅 | 사용자 우월 |

**대조 — 컨텍스트 파일.** CLAUDE.global.md는 개요 없이 6줄 비표준 규칙만 → 논문 결론과 **정확히 일치**. 라우터(Hot)/SKILL.md 자동 로드(Warm)/references(Cold)는 Codified Context 3계층에 구조적으로 대응. 다만 Warm 계층이 세션당 45k–65k 토큰으로, 논문이 "+20% 비용"으로 문제 삼은 파일보다 한 자릿수 크다. 논문의 "무익"은 개요에 대한 판정이고 스킬은 지시이므로, 비용 대비 효과는 **"규칙이 실제 행동을 바꾸는가"**로 별도 측정해야 한다. wf-doc(서식 규칙 위주)이 Cold 후보.

**대조 — 역공학 (Reversa).** 절차 분해·신뢰도 분류(conflicting 독립 범주)·증거 사슬(OBS/RR 분리)·승인-의도 분리는 **사용자 쪽이 더 정교**. Reversa가 앞서는 것: 문서 단위 신뢰도 집계 수치(97.1%), spec-impact 매트릭스, 산출물이 실행 가능한 Gherkin 패리티 시나리오, 실제 적용 사례.

---

## 3. 횡단 발견 — 여러 논문이 같은 방향을 가리키는 것

**F1. "절차보다 컨텍스트"가 세 논문에서 독립적으로 나왔다.** TDAD(테스트 맵 > TDD 절차), AGENTS.md(개요 무익·비표준 규칙만), Skills Harmful(필수 본문 텍스트가 과부하 원인 43/46). 워크플로우는 규칙 텍스트가 두껍고 저장소 특화 컨텍스트 산출물(테스트 맵, 실패 등록부, known failure modes)이 없다.

**F2. 검증은 많지만 조건화가 없다.** 체크리스트 45문항 + 빌드·테스트 2회. "위험에 비례"라는 원칙은 있으나 생략 규칙·예산 신호가 없다. `wf-context-threshold.ps1`은 이미 예산 인식 인프라인데 인계에만 쓰이고 검증 깊이 조절에는 연결되지 않았다.

**F3. 상태 규율은 강점이다.** LoopsBench의 병목(상태 규율), AI-DLC의 file-based memory, PROJECTMEM의 재개 비용 절감 — 모두 사용자 워크플로우가 이미 갖춘 것. 이 부분은 유지·강화 대상이지 축소 대상이 아니다.

**F4. 공통 공백 4개.** (a) 회귀 의무 목록(선행 TASK 테스트를 후속 TASK에서 재실행), (b) 파일 키 실패 등록부(편집 전 조회), (c) 작업별 감독 모드(특히 비차단 관찰), (d) 하네스 수준 게이트(fail-open 신호 주입이 아닌 거부).

**F5. 조건 차이 경고.** TDAD는 4-bit 30B 모델·Python·SWE-bench 버그 수정이고 프론티어 재현 미확인. Skills Harmful은 Opus 4.6이라 프론티어에 적용 가능. AGENTS.md는 Sonnet 4.5·GPT-5.2. 사용자 환경(Claude Code, 주로 Python)에는 Skills Harmful·AGENTS.md 결과가 더 직접적이고, TDAD는 "메커니즘(절차가 컨텍스트를 밀어냄)"만 가져오고 수치는 재현 대상으로 봐야 한다.

---

## 4. 다음 스텝 후보 (통합)

우선순위는 **근거 강도 × 구현 비용 × 현 구조와의 충돌 없음**으로 매김. 전부 "측정 가능한 실험" 형태로 적음.

| # | 후보 | 근거 논문 | 편집 위치 | 측정 | 비용 |
|---|---|---|---|---|---|
| **S1** | **테스트 맵 산출물**: §3.1에서 변경 예정 파일→관련 테스트 맵(`docs/work/<ID>/test-map.md`) 생성(명명 규칙·import grep; Python이면 `pip install tdad`). §3.4 2단계·§3.5 회귀 질문이 이 맵을 입력으로 사용 | TDAD | wf-implement §3.1, §3.4 | 동일 과제 10–25건에서 맵 유/무 P2P 실패 수·빈 패치율 | 낮음 |
| **S2** | **회귀 의무 목록**: work-log 인계 절에 "완료 TASK별 유지 테스트" 표. §3.3 "가장 가까운 범위의 검증"을 "선행 TASK 테스트 포함"으로 확장 | LoopsBench, TDAD | wf-implement §3.3, §7; wf-doc work-log 템플릿 | 사이클 말미 §3.6에서 발견되는 회귀 건수 감소 | 낮음 |
| **S3** | **검증 깊이 표**: 경량 경로(1·2·6단계, §3.5 품질 블록만) / 소규모 정식(1–4·6) / 공개 계약·데이터·보안(전체). §3.6 최종 테스트는 "§3.4 이후 파일 변경 시만". threshold 메시지 수신 후엔 §3.5 전체 재검토 생략·미수행 기록 | Skills Harmful 권고③ | wf-implement §3.4–3.6 | 작업당 토큰·검증 반복 횟수, 회귀 미탐 건수(S2와 교차) | 낮음 |
| **S4** | **references/ 신설로 본문 다이어트**: wf-implement §2.4 사다리·§3.5 체크리스트·§7 레이아웃 → `references/`, wf-tree §7 렌더링 규칙 → `references/rendering.md`. 본문은 트리거 문장만. 목표 각 ≤200줄 | Skills Harmful 권고④, Smells UD, TDAD 107→20 | wf-implement, wf-tree | 세션당 규칙 토큰(전후), 규칙 준수율(재현 테스트 먼저 작성했는가·인계 절 갱신했는가) 5–10건 | 중간 |
| **S5** | **경고 헤더(Gotcha)**: "설계 승인≠실행 승인" 정본 1곳 + 요약, wf-doc 링크 미충족 규칙, wf-tree 점선 방향을 `> **주의**` 블록으로 | Smells BG | 3개 스킬 | 정성 | 낮음 |
| **S6** | **경량 경로 관찰 기준**: "변경 파일 ≤2, 공개 심볼 변경 0, 테스트 체계 밖 파일 없음" 같은 기계적 조건 추가 → RL 잔여 허점 봉쇄 | Smells RL | 루트 SKILL.md, CLAUDE.global.md, wf-design §1 | 경량/정식 판정 불일치 사례 수 | 낮음 |
| **S7** | **파일 키 실패 등록부**: work-log에 `## 시도 등록부` 표(경로·시도·worked/failed·링크), 완료 시 `docs/attempts.md`로 이관. PreToolUse(Edit/Write) 훅 4번째로 경로 grep → failed 행 있으면 경고 주입 | PROJECTMEM | wf-implement §7, wf-doc 템플릿, setup/hooks | 동일 실패 재시도 건수 | 중간 |
| **S8** | **TASK 모드 필드** `모드: hitl/ohotl/ahotl` + §2.3 자율 조건을 모드 선택표로 재구성 + wf-tree 표시 | AI-DLC 2026 | wf-doc plan 템플릿, wf-implement §2.3, wf-tree | 관문 대기 시간, 재승인 횟수 | 중간 |
| **S9** | **하네스 게이트 어댑터**: setup/hooks에 Stop 훅 — plan.md 검증 계획에서 테스트·린트 명령 추출·실행, 실패 시 block. 스킬 본문은 하네스 비의존 유지 | AI-DLC backpressure | setup/hooks | 미검증 완료 보고 건수 | 중간 |
| **S10** | **호환성 게이트**: "저장소에 기존 문서 관례가 있으면 그 관례를 따르고 매핑을 work-log에 기록" 1문장 | Skills Harmful 권고②, Artifact Misplacement | wf-design §6, wf-implement §7 | 정성 | 낮음 |
| S11 | Adversarial Spec Review를 wf-design §4.5에 추가(모순·가정·범위 공백) | AI-DLC | wf-design §4.5 | DCR 발생 건수 | 낮음 |
| S12 | 의존 복원 자기 검토: 파일 겹침·심볼 참조 시 `depends:` 후보 제안 | LoopsBench | wf-tree §9 | 계획 대비 실제 의존 누락 | 낮음 |
| S13 | 유틸 스크립트: wf-doc 링크·앵커 검사, wf-tree 재렌더 | Smells MUS | skills/*/scripts | 체크리스트 토큰 감소 | 중간 |
| S14 | 역공학 보강: 문서 단위 신뢰도 집계(선택), spec-impact 열, 단계 10–11 산출을 Gherkin/특성화 초안 형식으로 인계 | Reversa | reverse-engineering.md | 정성 | 낮음 |
| S15 | 라우터에 known failure modes 3–5줄 | Codified Context, AGENTS.md | CLAUDE.global.md 또는 프로젝트 CLAUDE.md | 반복 실수 재발 | 낮음 |
| S16 | 비밀 정보 마스킹 훅 (`docs/work/**` 기록 시 PROJECTMEM 패턴 검사) | PROJECTMEM, Security Debt | setup/hooks | 정성 | 낮음 |

**추천 묶음(1차 실험).** S1+S2+S3는 서로 맞물리고(테스트 맵 → 회귀 의무 → 조건화된 검증) 근거가 세 논문에서 겹치며 편집 범위가 wf-implement 한 파일에 집중된다. S4는 S1–S3와 같은 변경에서 하면 "본문 줄이면서 컨텍스트 산출물 추가"라는 논문 방향을 한 사이클에 실험할 수 있다. S7·S8·S9는 훅·템플릿이 걸려 2차로.

**주의.** S4는 §2.4·§3.5를 references로 내리면 "항상 읽히지 않을" 위험이 있다. 논문의 지연 로드 권고는 "명시적 트리거"를 전제하므로, 본문에 "자체 리뷰 시 references/review-checklist.md를 읽는다" 같은 트리거 문장을 남기고 준수율을 측정해야 한다.

---

## 5. 검증 노트

- TDAD 6.08/9.94/1.82%, 107→20줄·12→50%, "context outperforms procedure": 본문 재확인 CONFIRMED. "49줄 vs 119줄"은 §5.2 ablation 문맥(119→49로 줄이면 30→20%)에서만 등장.
- Skills Harmful 68.8% / 62.6% / 36.8% / 43 of 46 / 권고③ 문구: CONFIRMED.
- Smells 5,000단어 / 1,024자 / RL 94% / 정의: CONFIRMED. "99%"는 정확히는 "smell-free 스킬 1개뿐(99.6%)".
- AI-DLC 2026 모드 전환 트리거, LoopsBench "outer continuation" 정의, PROJECTMEM churn 임계값, Codified Context 스케일 임계 줄수: 본문에서 확인 못함.
- 저장소 수치(파일 크기·줄 수·references 유무·훅 3종·경로 고정)는 클론본에서 직접 확인.

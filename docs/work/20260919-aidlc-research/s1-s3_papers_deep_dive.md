# S1·S2·S3 근거 논문 정밀 분석 — wf-implement 편집 초안 포함

> 대상: 1차 대조 보고서의 추천 묶음 S1(테스트 맵)·S2(회귀 의무 목록)·S3(검증 깊이 표)의 근거 논문 3편.
> 순서: 요청대로 **2번(LoopsBench, S2) → 3번(Agent Skills Can Be Harmful, S3) → 1번(TDAD, S1)**.
> 각 장은 논문 구조 → 메커니즘·수치 → 한계 → wf-implement 어휘로 번역 → 편집 초안 → 실험 설계로 끝난다. 수치는 본문에서 재확인했고, 없는 것은 "본문에서 확인 못함"으로 표기. 작성 2026-08-27.

**1차 보고서 정정 2건.** (a) wf-implement §3.5 자체 리뷰는 22문항이 아니라 **18문항**(4+4+4+6)이며, 산출물 이후 체크리스트 총량은 45가 아니라 **41문항**(18+wf-doc §4 13+wf-tree §9 10). (b) LoopsBench Table 4의 루프별 RR은 분모가 서로 다를 가능성이 있어(아래 §1.4) 루프 간 RR 비교는 인용하지 않는 편이 안전하다.

---

# 1. LoopsBench — S2 "회귀 의무 목록"의 근거

arXiv 2608.00267v1, Microsoft·Nanjing·UCL·SJTU, 2026.7.

## 1.1 구조와 주장

핵심 주장은 한 문장이다. "Coding agent infrastructure is shifting from harness engineering toward loop engineering." 루프는 하네스를 대체하지 않고 그 위의 제어면이다 — "They add a higher level control surface over it, so objectives, progress criteria, and work distribution can persist across extended execution." 루프가 통제해야 할 세 축은 **task structure, state continuity, regression pressure**.

정의 정리:

| 용어 | 논문 정의 |
|---|---|
| harness | 형식 정의 없음(도구·실행·평가 인프라 계층으로 사용) |
| loop | 하네스 위의 지속 실행 제어면 |
| outer/external continuation | 평가자 측 외부 루프가 "attempts every unit"하도록 재시동. 프롬프트·횟수는 **본문에서 확인 못함**. 효과만: "Without external continuation, evaluated loop implementations cover a shallow prefix" |
| 루프 원형 4종(RQ3) | Codex goal mode("keeps a persistent objective"), Claude Code goal mode("session condition checked after each turn"), Claude dynamic workflows("task specific workers with narrower local contexts"), Ralph loop("starts a fresh invocation for residual work") |

## 1.2 벤치마크·게이트·회귀의 메커니즘

**규모.** 112 task(Course Labs 57, PR Sequences 29, Research Evolutions 26), 8언어, 9도메인, 5,300+ 개발 단위, 의존 깊이 중앙값 6.

**개발 단위** u = (요구사항, 파일/심볼 스코프, 전제 집합, 참조 패치, 표준 테스트).

**전제 DAG의 4가지 증거 패턴.** ① 순차 PR 체인, ② 모듈 재사용("v edits a file or symbol that u introduced"), ③ 생산자–소비자 API("v calls or imports an authoritative definition created by u"), ④ 조합적 계층화("v extends a subclass, schema, or interface declared by u"). 증거는 "hunk overlap on the same file"과 "symbol level dependence". 핫파일(대부분의 PR이 건드리는 파일)과 lockfile은 간선을 만들지 않는다.

**게이트 — 가장 중요한 두 문장.**
- "**The gate affects scoring rather than editing permission.** The evaluated loop remains free to edit across layers."
- "**Once a unit clears the gate, its tests and the tests of its predecessors are kept enforced as regression tests on every later layer**, scoring subsequent edits against both new work and completed obligations."

그리고 루프는 **무엇을 유지해야 하는지 통보받지 않는다**: "Checkpoint outcomes and the active obligation state are retained for evaluator side scoring." 회귀율 정의: "Percentage of previously passing test obligations that fail on later edits."

**Table 3 — RQ2 루프 추적 지표** (Edge F1 = 기록된 계획 vs 출처 DAG, PatchLen = 생성/참조 줄 수 비, #T = 루프가 작성한 테스트 수, Reg = 회귀율. 재확인 완료)

| 루프 | Edge F1 | CPR | WR | PatchLen | #T | Reg |
|---|---|---|---|---|---|---|
| Claude Code | 0.71 | 0.31 | 1.08 | 1.58 | 28 | 7.11% |
| Codex | 0.67 | 0.33 | 1.14 | 1.71 | 24 | 4.83% |
| GitHub Copilot | 0.58 | 0.41 | 0.92 | 1.83 | 22 | 6.91% |
| OpenHands | 0.39 | 0.85 | 0.39 | 2.31 | 16 | 2.46% |
| SWE-agent | 0.37 | 0.88 | 0.36 | 2.36 | 15 | 2.18% |
| mini-swe-agent | 0.27 | 0.97 | 0.24 | 2.54 | 11 | 0.24% |

**Table 4 — RQ3 루프 구현 4종** (재확인 완료)

| 루프 구현 | Rounds | Reg/run | RR |
|---|---|---|---|
| Codex goal mode | 32.76 | 0.34 | 20.59% |
| Claude Code goal mode | 34.69 | 0.13 | 17.65% |
| Claude dynamic workflows | 97.96 | 0.36 | 24.11% |
| Ralph loop(재시작형) | 13.24 | 0.17 | 7.84% |

"Context-budget renewal does not remove regression pressure. Dynamic workflows record 0.36 regression events per run despite distributing work across narrower worker contexts." → "**completed obligations still require explicit state tracking when workers return.**"

## 1.3 상태 규율 실패의 실제 모습

저자: "The long horizon gap centers on loop state discipline."
- 계획 상태: 최고 루프도 출처 증거 간선의 약 30%를 빠뜨림(Edge F1 0.71). 열린 루프의 CPR≈0.9·WR≈0.3은 사실상 계획 없는 직렬 실행.
- 코드 상태: 패치가 참조보다 1.58–2.54배 김 — 선행 단위 스코프를 건드릴 면적이 넓다.
- 테스트 상태: 5,300 단위에서 루프가 남긴 테스트 11–28개. "sparse test authoring … leaving earlier obligations with limited agent authored regression protection."

**주의해서 읽을 것.** 회귀율과 #T가 같은 방향이다(Claude Code #T 28·Reg 7.11%, mini-swe-agent #T 11·Reg 0.24%). 진행을 많이 한 루프일수록 지킬 의무가 많아 회귀가 *보이는* 것이지, 테스트를 많이 쓰면 회귀가 는다는 뜻이 아니다. 정성 트레이스 예시(무엇이 어떻게 깨졌는지)는 **본문에서 확인 못함**.

## 1.4 한계

저자 명시: DAG는 하한(설정·빌드·크로스 서비스 의존 누락), 출처 편향(모바일·프론트엔드 제외), 정확성은 공개 테스트에 묶임, 오염 위험, "Hidden checkpoint state can make regressions reflect limited feedback as well as regression discipline"(회귀가 규율 부족인지 피드백 부재인지 분리 불가).

추가 비판: (a) Table 4의 RR은 분모가 달라 보인다(20.59≈7/34, 24.11=27/112, 7.84=4/51). 같은 task 집합인지 확인 못함 → 루프 간 RR 비교는 신뢰하지 말 것. (b) Reg/run은 진행 깊이에 비례해 커지므로 dynamic workflows 0.36이 goal mode 0.13보다 "나쁘다"고 단정할 수 없다. (c) 논문은 "explicit state tracking"을 권고하면서 그 처방을 실험하지 않았다 — **용스님 워크플로우가 그 실험을 하게 된다.**

## 1.5 게이트 규칙을 wf-implement 어휘로 번역

| 논문 개념 | wf-implement 번역 |
|---|---|
| unit u, T_u | TASK와 그 TASK가 남긴 유지 테스트(§2.4 최소 검증 + 특성화 테스트 + 자동화한 인수 테스트) |
| clears the gate | TASK `completed` 전이 — Red→Green 증거가 있는 시점 |
| active obligation state | **회귀 의무 목록** — work-log의 정본 절 |
| kept enforced on every later layer | 후속 TASK의 Green·Refactor 확인, `completed` 전이, 통합, 재개 시 목록 전량 재실행 |
| regression event | 목록의 테스트가 "이전 성공"→"실패". §3.4 실패 분류의 "이번 변경으로 발생한 실패"로 분류, 비고에 `회귀(TASK-NN 의무)` |
| gate affects scoring, not editing | 선행 TASK 파일 편집 금지가 아니라, 편집 후 의무 테스트 통과를 완료 조건으로 |
| context-budget round | 세션·컴팩션·재개. 새 라운드는 목록을 통보받지 못하므로 **work-log가 통보 역할** |
| Edge F1 ≤ 0.71 | 의존성 필드로 재실행 대상을 고르면 30%+ 놓침 → **기본은 전량 재실행**, 선별은 실행 시간이 문제일 때만 |
| #T 11–28 | 목록이 비면 회귀를 볼 수 없다. TDD 테스트를 "완료 증거"에서 "유지 의무"로 승격 |

**목록에 담을 행.** 발행 TASK-ID / 테스트 식별자(파일::이름 또는 명령) / 실행 명령 / 보호 스코프(파일·심볼) / 마지막 성공 증거(일시·커밋) / 상태 `유지 | 대체(→DCR/TASK) | 폐기(이유)` / 비고(AC-ID).

**실행 시점.** (1) 후속 TASK의 Green 직후와 Refactor 종료 시, (2) TASK `completed` 전이와 같은 변경에서(행 추가 + 전량 통과 확인), (3) §3.1 재확인의 첫 행동, (4) §3.6 최종 빌드, (5) DCR 반환 후 재개 시(의미가 바뀐 테스트는 `대체`로, 삭제 금지).

**금지.** 의무 테스트를 통과시키려고 수정·삭제·제외하지 않는다. 회귀를 "기존 실패"로 재분류하려면 마지막 성공 증거보다 앞선 실패 증거가 있어야 한다.

## 1.6 wf-implement 편집 초안

**§3.3 구현 — 목록 뒤에 추가**

> - 각 TASK의 Green을 확인한 뒤와 Refactor를 마친 뒤, 작업 기록의 [회귀 의무 목록](#7-작업-기록과-저장-위치)을 전량 재실행한다. 선행 TASK의 파일·심볼을 편집하는 것은 허용하되, 그 TASK의 의무 테스트 통과가 현재 TASK의 완료 조건에 포함된다.
> - TASK를 `completed`로 바꿀 때는 같은 변경에서 그 TASK가 남긴 유지 테스트를 회귀 의무 목록에 추가하고, 목록 전량의 성공 증거를 기록한다. 추가할 테스트가 없으면(자명한 변경, TDD 부적용) 그 이유를 행으로 남긴다.
> - 의무 테스트가 이전 성공에서 실패로 바뀌면 **회귀 사건**이다. 테스트를 수정·제외하여 통과시키지 않고, 원인 TASK와 발견 TASK를 기록한 뒤 원인 코드를 고친다. 기준선 변경으로 테스트의 의미가 바뀌었다면 DCR과 함께 `대체`로 표기한다.

**§3.4 검증 — 실패 분류 문단 뒤**

> 회귀 의무 목록의 실패는 "이번 변경으로 발생한 실패"로 분류하고 비고에 `회귀(TASK-NN 의무)`를 적는다. 기존 실패로 재분류하려면 마지막 성공 증거보다 앞선 실패 증거가 있어야 한다.

**§3.6 통합 — 세 번째 항목 교체**

> - 통합된 상태에서 최종 빌드·테스트와 함께 회귀 의무 목록 전량을 재실행하고, 그 결과를 사이클의 마지막 증거로 기록한다. 목록의 `유지` 행이 모두 성공하지 않으면 통합을 완결로 보고하지 않는다.

**§3.1 현재 상태 재확인 — 항목 추가**

> - 작업 기록의 회귀 의무 목록이 있는가? 있다면 계획을 읽기 전에 전량 재실행하고 결과를 재개 기록에 남긴다. 새 세션은 이전 세션이 지키던 의무를 통보받지 못하므로, 이 목록이 유일한 통보다.

**§7 세션 인계 — 1번 뒤에 추가**

> 1-1. 회귀 의무 목록을 현재 상태로 갱신한다. 마지막 전량 재실행 시각과 결과를 적고, 재실행하지 못한 행은 `미수행`과 이유를 남긴다. 재개 프롬프트의 첫 행동은 이 목록의 재실행이다.

**§5 완료 조건 — 항목 추가**

> - 회귀 의무 목록의 `유지` 행이 통합 시점에 전량 성공했고, 회귀 사건이 있었다면 원인·발견 TASK와 해소 증거가 기록되었다.

**wf-doc work-log 템플릿 — `## 현재 상태` 뒤 절 추가** (형식은 wf-doc 소유, 의미·실행 시점은 wf-implement 소유라고 노트)

```markdown
## 회귀 의무 목록

| 발행 TASK | 테스트·명령 | 보호 스코프 | 마지막 성공 (일시·커밋) | 상태 | 비고 |
|---|---|---|---|---|---|
| TASK-25 | `pytest tests/test_tree.py::test_done_time` | `skills/wf-tree/render.py` | 2026-08-17 22:16 · a4d27ca | 유지 | AC-01 |

- 마지막 전량 재실행: YYYY-MM-DD HH:MM — 성공 N / 실패 N / 미수행 N
```

`## 재개 지점`에 `- 회귀 의무 재실행: <마지막 결과 또는 "미수행 — 재개 첫 행동">` 필드 추가.

## 1.7 실험 설계

- 단위: 정식 경로 사이클(TASK ≥ 3, 자동 테스트 있는 저장소, 세션 경계 ≥ 1). 스킬 문서만 고치는 사이클은 제외.
- 표본: 사전 — 최근 완료 사이클을 git log로 회고해 회귀 사건 기준선(추정 6–8건). 사후 — 10 사이클.
- 주 지표는 사건 수가 아니라 **발견 지연**(원인 TASK 완료 → 발견까지의 TASK 수·세션 수). 목표: 0 TASK·같은 세션. 보조: 재개 후 첫 의무 재실행까지 행동 수, 목록 크기(#T 대응), 통합 시 "완료→부분 완료" 재판정 수, 재실행 비용.
- 혼동: 모델·도구 버전, 난이도(TASK 수·변경 파일 수로 층화), 관찰자 효과(사건 수에 편향 → 발견 지연을 주 지표로), 목록이 클수록 재실행 생략(미수행 행 수 보고), 학습 효과(시간순 추세 병기).
- 판정: 발견 지연 중앙값이 "후속 TASK 1개 이상·세션 경계 초과"→"같은 TASK·같은 세션"으로 옮기고 미수행 행 0이면 채택. 재실행 비용이 과하면 의존성 선별을 후속으로(단 Edge F1 교훈대로 전량이 기본).

---

# 2. Agent Skills Can Be Harmful — S3 "검증 깊이 표"의 근거

arXiv 2608.11888v1, HUST·MSR·Microsoft·UIUC, 2026.8.

## 2.1 구조와 연구 질문

RQ1 대조 데이터셋 구축 → RQ2 기능 실패 원인 → RQ3 효율 회귀 원인 → RQ4 자동 귀속(SkillTriage). 확정 307건 = 기능 125 + 효율 182.

논문이 정의하는 "스킬 본문": "task-solving steps, implementation rules, workflow constraints, and checklists" + 검증 안내 "tests, expected outputs, debugging steps, or completion criteria". **wf-implement §3.4–3.6·§3.5·wf-doc §4는 정확히 이 정의에 들어간다.**

## 2.2 실험 설계의 규칙

| 항목 | 규정 |
|---|---|
| 벤치마크 | SkillsBench 84과제·11도메인, SWE-Skills-Bench 490 저장소 과제 |
| 스킬 확장 | smithery.ai·skillsmp.com 공개 스킬, 임베딩 코사인 ≥0.7 top-5 → 826→20,664 쌍 |
| 스택 | OpenCode 1.15.1 + Claude Opus 4.6. temperature·seed **본문에서 확인 못함** |
| 쌍 비교 | 과제·환경·검증기·모델 고정, 스킬만 변경. with/no-skill과 cross-skill(의미상 매칭된 다른 스킬) |
| 기능 실패 후보 | target FAIL ∧ reference PASS |
| 효율 회귀 후보 | 양쪽 PASS ∧ min(r_tok, r_time) > 1.0 ∧ max(r_tok, r_time) > T, **T = 2.0** |
| 반복 실행 | 없음 — 비결정성 통제는 T=2.0과 쌍 통제에만 의존 |
| 확정 | 정제(증거 부족·검증기 오탐·중복 제거) 후 수동 검토·그룹 합의. 주석자 수·카파 **본문에서 확인 못함** |
| 후보→확정 | 기능 315→125, 효율 350→182 (총 665→307). 절반 이상 탈락, 사유별 건수 없음 |

## 2.3 실패 분류 전체

**기능 실패 125건**

| 범주 | 하위 | 정의 | 건수 | 비율 | 예시 |
|---|---|---|---|---|---|
| Applicability Mismatch | — | 메타데이터 오도로 부적절한 과제에 적용 | 2 | 1.6% | RAG 백엔드 스킬이 라이브러리 과제에 붙어 요구 파일 생성을 범위 밖으로 간주 |
| Environment Mismatch | BDR | 스킬이 권장한 의존성·런타임이 환경에서 실패 | 5 | 4.0% | 확인 못함 |
| | ESM | 스킬이 패키지 해석·작업 디렉터리·버전을 바꿔 **에이전트의 자체 점검 환경 ≠ 검증기 환경** | 8 | 6.4% | 최신 openpyxl을 외부 설치하고 저장소 패키지를 sys.path에서 제외한 채 검증 |
| Task-Implementation Fault | OWG | 과도한 탐색·설정·감사가 예산 안 산출을 막음 | 4 | 3.2% | 확인 못함 |
| | **IRF** | 필수 요소를 잘못된 메서드·값·정책으로 구현 | 46 | **36.8%** | `(Exports−Imports)/GDP`에 `*100` 누락 → 100배 작은 값 |
| | **RRO** | 필수 요소 누락 | 36 | **28.8%** | RAG 설정에서 `model_name` 누락 |
| Artifact Misplacement | — | 과제가 지정한 경로와 다른 곳에 산출 | 24 | 19.2% | 스킬이 "실제 패키지는 langchain_classic"이라 안내해 다른 경로에 작성 |

**효율 회귀 182건 (T=2.0)**

| 범주 | 하위 | 정의 | 건수 | 비율 |
|---|---|---|---|---|
| Context Bloat | **SBCB** | 스킬 본문 자체가 매 호출을 비싸게 | 43 | 23.6% |
| | SMB | 보조 자료를 읽게 함 | 3 | 1.6% |
| Excessive Procedure | EE | 구현 전 과잉 탐색 | 17 | 9.3% |
| | HIP | 다단 변환·서브프로세스 등 무거운 구축 | 30 | 16.5% |
| | **EV** | "excessive or repeated tests, rebuilds, debugging attempts, or checklist verification after the main artifact has been produced" | 67 | **36.8%** |
| Dependency Resolution | — | 취약 의존성 설치·수리가 성공 궤적에 포함 | 22 | 12.1% |

CO/EP 구분: 호출당 비용만 커지고 단계 순서는 같으면 CO, 단계가 추가되면 EP.

Finding 3: "the overhead is almost entirely caused by mandatory skill-body text"(43/46). Finding 4: "skill authors should condition verification scope and pipeline depth on task uncertainty, change size, and budget rather than prescribing exhaustive workflows by default."

스킬 길이 vs 회귀 상관 수치: **본문에서 확인 못함.**

## 2.4 과잉 검증(EV)의 실제 모습과 wf-implement 대응

EV 개별 사례의 명령·반복 횟수·토큰 비율은 **본문에서 확인 못함**. 실체는 세 곳에서 간접 확인: 정의 한 문장(4 행위: 반복 테스트·재빌드·통과 후 디버깅·체크리스트 순회), EP 서두("skills turn optional activities into mandatory steps, including … repeated validation, and broad diagnostic checks"), SkillTriage 오류 분석("dependency repair nested within verification loops, … build commands serving dual implementation/verification roles"). SkillTriage의 phase 분할(pre-implementation / pipeline / post-implementation verification)과 action tag(test/debug/rebuild/check)가 EV의 조작적 정의다.

| EV 행위 | wf-implement·wf-doc 대응 지점 | 위험 형태 |
|---|---|---|
| 반복 테스트 | §3.3 근접 검증 → §3.4-2 → §3.5 "영향받는 검증 재수행" → §3.6 최종 → §5 | 같은 묶음이 최대 4회, 생략 조건 없음 |
| 재빌드 | §3.4-6 + §3.6 | 경량 변경에도 2회 |
| 체크리스트 | §3.5 18문항, wf-doc §4 13문항 | 경량 경로에서도 전부 순회 |
| 통과 후 디버깅 | §3.4 "기존 실패" 재현 시도 | 상한 없음 |
| 광범위 진단 | §3.4-5 비기능 | "관련" 기준 없어 전부 수행할 유인 |

**중요한 단서.** 논문은 EV가 기능 실패를 늘린다고 주장하지 않는다. EV 67건은 전부 PASS/PASS 쌍이다. 따라서 편집 목표는 검증을 줄이는 것이 아니라 **"동일 검증의 무조건 반복"을 조건부로 바꾸는 것**이다.

## 2.5 권고의 구체성

VII-A 핵심 문장: "agents need explicit policies for adapting verification scope and implementation-pipeline depth to **task uncertainty, repository size, change risk, and remaining token or execution-time budget**." 이 문장 외에 임계값·규칙은 **없다**. 변수 4개의 이름과 방향만 준다. 정책은 우리가 만든다.

관측 제안:
- **과제 불확실성**: wf-design 경량 조건("새 설계 결정 불요")과 §3.1 재확인이 이진 신호. 추가: Red→Green 전환 2회 이상 실패 → "높음".
- **저장소 크기**: 절대 크기보다 "관련 테스트 묶음 실행 시간". 전체 스위트 N분 초과 시 §3.4-2는 변경 영역만, 전체는 §3.6에서 1회.
- **변경 위험**: §4.2 중대 변경 목록 + §2.4 최소화 제외 영역이 이미 등급 정의 → 표의 행으로 재사용.
- **잔여 예산**: 유일한 신호는 `wf-context-threshold.ps1`(1,500KB, 재경고 300KB). 인계 신호를 "그 경계까지 남은 예산으로 새 전체 검증을 시작하지 말라"로 확장.

## 2.6 wf-implement 편집 초안 — 검증 깊이 표

§3.4 6단계 목록 뒤에 삽입. (Finding 3에 따라 표 본체는 `references/verification-depth.md`로 분리하고 SKILL.md에는 링크와 요약 두 줄만 두는 것을 권장.)

---

**검증 깊이 표**

검증은 변경 위험에 비례한다. `필수`는 생략할 수 없고, `조건부`는 괄호의 조건을 만족할 때만 수행하며 수행하지 않으면 생략 이유를 작업 기록에 남긴다. `—`는 기본 생략이며 이유 없이 생략할 수 있다. **같은 테스트 묶음을 통과 후에 다시 실행하는 것은 그 사이에 코드가 바뀐 경우에만 한다.**

| 단계 | 경량 경로 | 정식 — 소규모(내부 구현, 승인 범위 안, 단일 컴포넌트) | 정식 — 공개 계약·데이터 모델·보안·마이그레이션 |
|---|---|---|---|
| §3.4-1 포맷·정적 분석 | 필수(변경 파일만) | 필수(변경 파일만) | 필수(저장소 전체) |
| §3.4-2 변경 영역 단위 테스트 | 필수(변경 파일이 닿는 테스트만) | 필수 | 필수 |
| §3.4-3 통합 테스트 | — | 조건부(컴포넌트 경계를 넘는 경우) | 필수 |
| §3.4-4 인수 조건 시나리오 | —(인수 조건 없음) | 필수(해당 작업의 AC만) | 필수(전체 AC) |
| §3.4-5 비기능 | — | 조건부(기준선에 성능·호환성 목표가 명시된 경우) | 필수(보안·호환성) + 조건부(성능) |
| §3.4-6 빌드·실행 | 조건부(빌드 산출물·설정이 바뀐 경우) | 필수 1회 | 필수 |
| §3.5 요구사항·설계 블록 | —(범위 밖 변경 1문항만) | 필수 | 필수 |
| §3.5 정확성·안정성 블록 | 조건부(버그 수정인 경우) | 필수 | 필수 |
| §3.5 보안·운영 블록 | — | 조건부(입력 처리·로그·비밀 정보에 닿는 경우) | 필수 |
| §3.5 품질 블록 | 필수(디버그 코드·임시 파일 1문항 + 사다리 1문항) | 필수 | 필수 |
| §3.6 통합 후 재실행 | —(§3.4-2 결과를 최종 증거로) | 조건부(§3.5 이후 코드가 바뀐 경우 영향 범위만; 전체 묶음 1회) | 필수(전체 묶음 1회) |
| 회귀 의무 목록(§1) | —(경량 경로는 목록 없음) | 필수(Green 후·completed 전이·§3.6) | 필수 |
| wf-doc §4 자체 검토 | 경량 경로 문서 항목만(§2.8) | 필수 | 필수 |

경로 판정은 [wf-design 경량 경로 조건]과 [§4.2 중대한 변경] 목록을 그대로 쓴다. 세 번째 열 조건에 하나라도 해당하면 세 번째 열. [§2.4] 최소화 제외 영역(신뢰 경계 입력 검증, 데이터 손실 오류 처리, 보안·접근성)에 닿는 변경은 경량 경로로 판정되었더라도 세 번째 열.

다음 조건에서는 한 열 오른쪽(더 깊은 열)을 적용한다: Red→Green 전환 2회 이상 실패 / §3.1 재확인에서 기준선 이후 저장소 변경이 변경 영역과 겹침 / "원인을 확인하지 못한 실패"가 남아 있음.

**예산 신호 수신 후 규칙.** 세션 핸드오프 경고(threshold.md)를 받은 뒤:
- 진행 중인 계획 항목의 §3.4-1·2는 마친다. 새 계획 항목의 검증은 시작하지 않는다.
- §3.4-3~6과 §3.6 전체 재실행은 이번 세션에서 시작하지 않고 검증 절에 `미수행 — 예산 신호 후 인계`로 기록, 인계 절의 다음 행동에 남긴다. 미수행 검증을 성공으로 간주하지 않는다(§2.5).
- §3.5는 품질 블록만 수행하고 나머지는 다음 세션 첫 행동으로.
- 이 규칙은 검증을 면제하지 않는다. 시점을 옮길 뿐이며 완료 조건(§5)은 모든 필수 단계가 실제 수행된 뒤에만 충족된다.

---

§3.3 "각 작업 완료 시 가장 가까운 범위의 검증"에 덧붙일 문장: "이 검증은 §3.4-2에 해당하며, 코드가 바뀌지 않았으면 §3.4에서 반복하지 않고 그 결과를 증거로 인용한다."

## 2.7 실험 설계

- 처치: 표 없는 현재 SKILL.md(참조) vs 표 포함(대상). 논문의 쌍 비교 그대로.
- 표본: 경량 / 정식-소규모 / 정식-고위험 3층 × 10–15과제, 각 쌍 **3회 반복**(논문이 하지 않은 반복으로 실행 간 변동 분리).
- 지표: ① 작업당 토큰·시간, r_tok·r_time(경량·소규모에서 r<1, 고위험에서 r≈1이어야 함) ② 검증 반복 횟수 = 코드 변경 없이 동일 테스트 명령 재실행 횟수, 빌드 횟수, §3.5 순회 횟수(EV의 직접 조작화) ③ **회귀 미탐** = 각 과제에 뮤테이션(AC 하나를 깨는 변이)을 심고 검증이 잡는 비율 — 참조 대비 증가하지 않아야(비열등성) ④ 생략 이유 기록률.
- 혼동: 비결정성(3회 중앙값), 표 자체의 SBCB(references 분리판 vs 본문판 별도 처치), 경로 오판(정답 열을 사전 라벨, 오판율 보고), 예산 규칙(`CLAUDE_WF_THRESHOLD_KB` 낮춰 별도 하위 실험), 검증기 협소성(자동 검증기 있는 과제만 미탐 지표에).
- 판정: 층별 r_tok 감소 ∧ 미탐률 비열등 동시 만족 시 채택. 고위험 층 미탐 상승 → 3열을 더 깊게; 경량 층 r_tok 불변 → 1열 조건부를 `—`로.

---

# 3. TDAD — S1 "테스트 맵 산출물"의 근거

arXiv 2603.17973v2, Alonso·Yovine·Braberman, 2026.3. 코드 `github.com/pepealonso95/TDAD`, `pip install tdad`.

## 3.1 구조와 기여

§3 시스템(그래프 스키마·인덱싱·영향 분석·스킬 통합), §4 설정, §5 결과(Phase 1 / TDD 역설 / 트레이드오프 / Phase 2 / 자동 개선 루프), §6 한계. 문제 제기: SWE-bench는 P2P(pass-to-pass) 파손을 보고하지 않는다 — 바닐라 에이전트 100건에서 P2P 실패 562건(패치당 6.5건). 기여: 오픈소스 도구, 회귀율을 1급 지표로, 2모델×2프레임워크 실증, 자기 개선 루프, MIT 공개.

## 3.2 시스템 메커니즘

**인덱싱.** Python `ast`(Python 전용). 노드 File/Function/Class/Test, 엣지 CONTAINS/CALLS/IMPORTS/TESTS/INHERITS. NetworkX + pickle(`.tdad/graph.pkl`), Neo4j 선택. 저장소 코드에는 MD5 해시 기반 증분 갱신·`--force`. 테스트↔코드 연결(논문 §3.3, 우선순위): ① 명명 규칙 `test_foo.py→foo.py` ② 접두 매칭 ③ 디렉터리 근접. 저장소 `test_linker.py`는 별도로 naming(~0.7)/static analysis(~0.8)/coverage opt-in(~0.9)으로 TESTS 엣지 생성.

**영향 분석(`tdad impact`).** Direct 0.95 / Coverage 0.80 / Transitive 0.70(CALLS 1–3홉) / Imports 0.50. `score = 0.7·w_strategy + 0.3·confidence`. 티어 high ≥0.8, medium 0.5–0.8, low <0.5, 기본 cap 50. 변경 파일은 `--files`로 사용자가 직접 전달(git diff 자동 감지 없음).

**test_map.txt 형식**(논문에 예시 없음, 코드에서 확인):
```text
src/pkg/auth.py: tests/test_auth.py tests/integration/test_login.py
src/pkg/utils.py: tests/test_utils.py
```
**중요:** 이 파일은 TESTS 엣지를 파일 단위로 축약 + 파일명 휴리스틱을 합친 정적 파일이며, **가중 점수·티어·cap은 적용되지 않는다.** 점수화 결과는 `tdad impact`의 표로만.

**스킬 소비.** "no MCP server, API calls, or graph database is required at runtime." 에이전트는 `grep 'path/to/file.py' .tdad/test_map.txt`. 저장소 SKILL.md 본문 약 20줄: ①최소 변경 ②변경 파일마다 grep ③`pytest <files> -x -q`, 실패 시 고칠 때까지 ④맵에 없으면 `src/foo/bar.py→tests/test_bar.py` 규칙 또는 `grep -r 'from.*bar import\|import.*bar' tests/`. 규칙: "Never submit a patch without running impacted tests first", 전체 스위트가 아닌 최소 집합만.

## 3.3 실험 결과 전체

**Phase 1** — Qwen3-Coder 30B Q4_K_M, llama.cpp, 32K, temp 0, 15분/인스턴스, SWE-bench Verified 앞 100개.

| 지표 | Vanilla | TDD Prompt | GraphRAG+TDD |
|---|---|---|---|
| 해결률 | 31% | 31% | 29% |
| 비어 있지 않은 패치율 | 86% | 75% | 74% |
| P2P 총/실패 | 9,245 / 562 | 8,040 / 799 | 8,536 / 155 |
| 테스트 단위 회귀율 | 6.08% | 9.94% | **1.82%** |
| 인스턴스 단위 회귀율 | 30.2% (26/86) | 33.3% | 33.3% (25/74) |
| 파국적 회귀(P2P 전부 실패) | 3 | 5 | 1 |

**Phase 2** — Qwen3.5-35B-A3B 4-bit, OpenCode v1.2.24, 25개.

| 지표 | Baseline | TDAD Skill |
|---|---|---|
| 해결 | 6/25 (24%) | 8/25 (32%) |
| 패치 생성 | 10/25 (40%) | 17/25 (68%) |
| 회귀율 | 0% | 0% |

**자동 개선 루프.** Claude Code가 TDAD 소스에 한 번에 하나 변경, 단위 테스트 실패 시 즉시 롤백, 10개 인스턴스로 측정, 최고 갱신 시 스냅숏·하락 시 롤백, 5연속 롤백 시 강제 복원. 15회 중 4회 채택.

| 반복 | 변경 | 생성 | 해결 |
|---|---|---|---|
| 루프 전 | 107줄 9단계 TDD SKILL.md | 28% | 12% |
| 1 | SKILL.md 107→20줄 | 50% | **50%** |
| 5 | 정적 test_map.txt 내보내기 | 70% | 60% |
| 12 | 디렉터리 근접 점수 | 70% | 60% |
| 13 | import 기반 대체 매핑 | 80% | 60% |

기각된 11회: "AST 파서 확장, 그래프 빌더 재구성, SKILL.md를 더 규범적으로"는 모두 해결률 하락.

## 3.4 저자의 해석과 그 한계

저자: TDD 프롬프트가 해로운 이유는 ① 컨텍스트 치환(절차 지시가 30B 모델의 저장소 컨텍스트를 밀어냄) ② 국소화 없는 야심(파국 회귀 5 vs 3). "절차보다 컨텍스트". ablation: 그래프 없이 119→49줄로 줄이면 30%→20%(축약 자체는 이득 아님), 49→119줄은 31%로 동일(절차 텍스트 단독은 무해·무익).

한계(비판 포함):
- 통계 검정 없음, 단일 실행, 100/25/10 표본.
- **인스턴스 단위 회귀율은 30.2%→33.3%로 차이 없거나 악화.** 테스트 단위 70% 감소는 파국 회귀 3→1이 분모를 지배한 결과일 가능성(분해는 본문에서 확인 못함).
- 해결률 2pp 하락, 빈 패치 14%→26%. 회귀 감소의 일부는 "패치를 안 낸 결과".
- **Phase 2 회귀 0%/0%: 회귀 감소 효과를 전혀 검증 못함.** Phase 2 이득은 빈 패치 감소이며, 회귀 방지 메커니즘과 무관할 수 있음.
- 개선 루프 10개 인스턴스 과적합. 프론티어 재현 미확인("frontier models may not exhibit the TDD-prompting paradox"). Python·pytest·잘 테스트된 12개 저장소. 동적 디스패치·monkey-patch·fixture/parametrize 맹점.

## 3.5 Claude Code·실제 저장소로 무엇이 옮겨지는가

**옮겨지는 것(메커니즘).** "변경 파일→관련 테스트" 정적 매핑을 짧은 텍스트로 미리 계산해 두고 grep으로 부분 실행하는 패턴 — RTS 문헌(Legunsen 2016 정적 클래스 수준, Gligoric 2015 파일 수준, Chianti 2004 메서드 수준)의 에이전트 버전이며 모델과 무관. 파일 형식의 단순성과 fallback 규칙(명명 규칙→import grep). "긴 절차보다 대상 지정 정보".

**옮겨지지 않는 것(수치).** 70%·12→50%·24→32%는 4-bit 소형·32K·소표본 조건. Claude Code는 이미 관련 테스트를 찾아 실행하는 경향이 있어 절대 이득은 훨씬 작거나 0일 수 있다. TDD 역설은 컨텍스트 압박이 원인이라 200K에서 재현 근거 없음. 실제 저장소에는 F2P/P2P 정답 집합이 없어 측정을 설계해야 한다.

**적용 원칙.** wf-implement의 TDD 사이클과 6단계 검증을 "절차 축소" 결론으로 훼손하지 말 것. 옮길 것은 **§3.4-2 "변경 영역의 단위 테스트"에 대상 목록을 공급하는 입력**이다.

## 3.6 wf-implement 편집 초안

**§3.1 현재 상태 재확인 — "관련 테스트와 빌드가 현재 어떤 상태인가?" 뒤에 추가**

> - 이번 작업이 수정할 것으로 예상되는 파일 각각에 대해 관련 테스트를 식별하고 테스트 맵(`docs/work/<작업-ID>/test-map.md`)으로 남긴다. 맵의 테스트는 계획 수립 전에 한 번 실행하여 현재 상태(성공·기존 실패)를 기록한다. 맵에 항목이 없는 파일은 "관련 테스트 없음"으로 명시하고, 특성화 테스트 필요 여부를 [구현](#33-구현)에서 판단한다.

**§3.2 계획 수립** — "테스트와 검증 방법" → "테스트와 검증 방법(테스트 맵에서 가져온 관련 테스트 포함)". 문단 추가:

> 각 작업의 `관련 테스트:` 필드는 테스트 맵에서 채운다. 구현 중 계획에 없던 파일을 수정하게 되면 같은 변경에서 맵과 해당 작업의 필드를 갱신한다.

**§3.4 검증** — 2단계를 "변경 영역의 단위 테스트 — 테스트 맵의 관련 테스트를 모두 실행한다"로. 실패 분류 앞에:

> 맵에 있는 테스트를 실행하지 않았다면 그 검증은 수행하지 않은 것이다. 맵 밖의 실패가 발견되면 맵의 누락 원인(동적 디스패치, fixture, 명명 규칙 위반 등)을 작업 기록에 남긴다.

**§3.5 자체 리뷰** — "기존 동작에 의도하지 않은 회귀가 없는가?" →

> - 기존 동작에 의도하지 않은 회귀가 없는가? — 테스트 맵의 관련 테스트와 회귀 의무 목록이 변경 후 모두 성공했고, 맵에 없던 실행 파일이 변경 파일 목록에 남아 있지 않은가?

**plan 템플릿** — TASK 필드 `- 변경 대상:` 다음 줄에 `- 관련 테스트: <테스트 맵 참조 | 없음(사유)>`.

**맵 생성 2안.** A안 TDAD CLI: `pip install tdad && tdad index .` 후 `.tdad/test_map.txt`에서 변경 예정 파일 행만 옮김(`.tdad/`는 `.gitignore`). B안 수동: `src/a/b.py`에 대해 (1) `tests/test_b.py`·`tests/a/test_b.py`·`tests.py` 존재 확인 (2) `grep -rln 'from .*\bb\b import\|import .*\bb\b' tests/` (3) 합집합.

```markdown
## 테스트 맵
- 생성 방법: tdad index (balanced) | 수동(명명 규칙+import grep)
- 생성 시점: YYYY-MM-DD HH:MM, 기준 커밋: <sha>

| 변경 예정 파일 | 관련 테스트 | 근거 | 사전 실행 결과 |
|---|---|---|---|
| src/a/b.py | tests/test_b.py, tests/a/test_flow.py | 명명·import | 12 성공 |
| src/a/c.py | 없음 | 미검색 결과 없음 | 특성화 테스트 검토 |
```

## 3.7 실험 설계

- 2×2: (M0) 현행 / (M1) 현행+테스트 맵 × (P0) §3.3 현행 TDD 문단 / (P1) 3줄판("실패 테스트 먼저→최소 구현→리팩터"). 논문 ablation(축약만으로는 손해, 컨텍스트+축약이 이득)을 Claude Code에서 재검.
- 주 지표: **변경 전 통과하던 전체 스위트 중 변경 후 실패 수**(실험 종료 후 전체 스위트 1회 실행으로 측정, 맵만 돌린 결과와 분리). 보조: 빈 패치/포기율, 터치 파일 수, 맵 밖 실패 수(맵 재현율), 토큰·턴, AC 통과.
- 표본: 자체 Python 저장소에서 과거 커밋을 되돌린 작업 20–30개, 셀당 2회 이상 반복, 셀 교차 배치.
- 혼동: 맵 생성의 "탐색 효과"(맵은 주되 사전 실행 결과는 숨긴 M1' 셀로 분리), 회귀 기저율 0(파일럿에서 M0 P2P 실패 0이면 더 얽힌 작업 선택), 커버리지 편차(저장소 1개 고정), 세션 캐시(매 작업 새 세션).
- 판정: P2P 실패 수는 Wilcoxon 부호 순위, 빈 패치율은 McNemar. 효과 크기·구간 병기.

---

# 4. 세 편집을 한 사이클에 합치는 순서

세 편집은 같은 자료 흐름을 이룬다: **테스트 맵(§3.1, 작업 시작 시 "어떤 테스트가 관련인가")** → **회귀 의무 목록(§3.3/§7, 완료 TASK가 "무엇을 지켜야 하는가")** → **검증 깊이 표(§3.4, "언제 얼마나 돌리는가")**. 편집 순서 제안:

1. **wf-doc 템플릿 먼저**: work-log에 `## 회귀 의무 목록` 절, `## 테스트 맵` 절(또는 별도 test-map.md), plan TASK에 `관련 테스트:` 필드. 형식 소유자가 먼저 바뀌어야 wf-implement가 링크할 수 있다.
2. **wf-implement §3.1·§3.2**: 테스트 맵 생성·사전 실행.
3. **wf-implement §3.3·§3.6·§5·§7**: 회귀 의무 목록의 추가·재실행·인계.
4. **wf-implement §3.4 + `references/verification-depth.md`**: 검증 깊이 표. 표의 "회귀 의무 목록" 행이 3번을 참조하므로 마지막.
5. **§3.5 회귀 질문** 문구를 맵+목록 참조로 교체.

이 순서로 하면 사이클 하나가 정식 경로(요구·설계 승인 → TASK 5개)로 자연스럽게 돌아가고, 그 사이클 자체가 편집 후 첫 관측 표본이 된다.

**서로 상충하는 지점 하나.** S3의 표는 "같은 묶음은 코드가 바뀐 경우에만 재실행"인데, S2는 "Green 후·Refactor 후·completed 전이·통합·재개 시 전량 재실행"이다. 충돌이 아니라 층위가 다르다: S2의 목록은 *선행 TASK의 의무*이고 S3의 규칙은 *현재 TASK의 검증 단계 반복*이다. 표에 "회귀 의무 목록" 행을 따로 둔 이유가 그것이며, 목록 재실행 비용이 문제가 되면 S3의 예산 규칙(`미수행 — 예산 신호 후 인계`)이 S2에도 적용된다.

---

# 5. 검증 노트
- LoopsBench Table 3·4 전 행, "Once a unit clears the gate…", "explicit state tracking when workers return": 본문 재확인 CONFIRMED. outer continuation 기제·Ralph 프롬프트·정성 트레이스·Table 4 task 수: 확인 못함.
- Skills Harmful 분류 건수·비율, T=2.0, Finding 3·4, VII-A 문구: CONFIRMED. EV 개별 사례 수치, 주석자 수, 스킬 길이 상관: 확인 못함.
- TDAD Phase 1·2 표, 개선 루프 4회 채택 내역, ablation 119→49: CONFIRMED. test_map.txt 형식과 SKILL.md 본문은 논문이 아니라 GitHub 저장소 코드에서 확인.
- 저장소 실측: §3.5 18문항, wf-doc §4 13문항, wf-tree §9 10문항(1차 보고서의 22·45는 오기).

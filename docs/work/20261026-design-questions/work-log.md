# WORK-20261026-design-questions: 작업 기록 — 설계 질문 단계와 근거 강제 적대 검토

> 문서 유형: `work-log, verification, completion`
> 작업 ID: `20261026-design-questions`
> 상태: `completed`
> 기준선: `[REQ-DESIGN-design-questions](./req-design.md) v1` (승인일 2026-10-26)
> 작성일: 2026-10-26
> 최종 갱신: 2026-10-26
> 관련 문서: [ST-llm-workflow](../../status.md), [REQ-DESIGN-design-questions](./req-design.md), [PLAN-20261026-design-questions](./plan.md), [ADR-020](./ADR-020-설계-질문과-적대-검토.md), [설계 액션 아이템](../../research/20261025-aidlc-trends/05_design_action_items.md), [WORK-20261026-approval-gate](../20261026-approval-gate/work-log.md)

## 요약

- 목적: v2 설계 사이클 A(D-01~D-04)의 wf-design·wf-implement 진행을 기록한다.
- 현재 결론 또는 상태: 완료(2026-10-26 08:49) — TASK-01~05, AC-01~07 7/7. 구현 커밋 `96b249c`, 이 종결 커밋과 함께 push 대상.
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | related | [ST-llm-workflow](../../status.md) | 작업 목록 | 이 작업의 행 |
| input | baseline | [REQ-DESIGN-design-questions](./req-design.md) | document | v1 |
| input | plan | [PLAN-20261026-design-questions](./plan.md) | TASK-01~05 | 계획 |
| output | decision | [ADR-020](./ADR-020-설계-질문과-적대-검토.md) | document | `approved`. 등록부 행 |
| input | related | [WORK-20261026-approval-gate](../20261026-approval-gate/work-log.md) | 후속 작업 "실세션 확인 관찰" | 이 작업의 설계 단계에서 관찰(완료 문서는 수정하지 않음) |

## 기준선과 현재 계획

- 기준선: [REQ-DESIGN-design-questions](./req-design.md) v1 (승인일 2026-10-26)
- 계획: [PLAN-20261026-design-questions](./plan.md)(completed)

## 수행 기록

### 2026-10-26 — 착수와 §4.1 조사

- 발견 사항: 착수 HEAD `0410724`, 워킹트리 clean. 열린 작업 없음(status 보류 1건). wf-design 2,189/2,300. 질문 표 열 구성이 req-design 10건에 5종, 답 위치 3곳. design-change §2·verification-depth §6 모두 "명세가 둘 이상으로 해석됨" 출구가 없다. 사이클 2 뮤테이션(통합·코드 파일)과 D-04(승인 전·설계 문서)는 시점·대상·신호·소비자가 모두 달라 겹치지 않는다. review-checklist는 변경 대상 아님.
- 결정과 이유: 사용자 요청 — 사이클 A 착수, Q-D1·Q-D2·Q-D8을 승인 관문 질문으로. 질문 단계 점검을 이 문서에 자기 적용해 Q-04(어절 기준선 해석)를 추가. `questions.md`·표 린트는 범위 제외(새 형식은 대안이 없을 때만). C층 무변경이라 DCR 없음, ADR-020 하나. 05 머리말 상태 줄 갱신.
- 검증: `lint_worklog.py` 0 오류, `lint_skill.py` 0 오류(K3 경고만)
- 결과: 완료 — 2026-10-26 01:35

### 2026-10-26 — 승인 게이트 실세션 관찰(사이클 B 후속)

- 발견 사항: `awaiting-approval` 상태에서 판정 `approval_gate.py . skills/wf-design/SKILL.md` → exit 1 "기준선 미승인 req-design.md (awaiting-approval)".
- 수행 내용: 사용자 동의(응답 "시도한다") 후 `skills/wf-design/references/approval-request.md` 빈 줄 추가 Edit 1회 → 확인 창, 사용자 거부("Denied by user"). 창 내용 질문에 응답 "게이트 메시지가 보였다". `git status --short skills/` 비어 있음. 기본 권한 모드(`bypassPermissions` 미관찰).
- 결정과 이유: [20261026-approval-gate](../20261026-approval-gate/work-log.md#후속-작업) 후속 "실세션 확인 관찰" **해소** — 완료 문서는 고치지 않음. `bypassPermissions` 관찰은 남음.
- 검증: 위 판정 출력, Edit 거부 결과, `git status`
- 결과: 완료 — 2026-10-26 01:40

### 2026-10-26 — 적대 검토 시험 실행(D-04 자기 적용)

- 발견 사항: 새 맥락 서브에이전트(general-purpose, 읽기 전용 지시, 문서 경로·검토 규칙만 전달) 1라운드 — 지적 15(높음 1·중간 7·낮음 7), 제안 0, 약 119k 토큰·22 도구 호출·4분 21초. 높음 1건은 DCR 경로 연결 누락(FR-08이 DCR을 포함하나 DES·AC 없음) — 작성자 자체 검토(§4.5)에서 놓친 것. 반박 1건(9번: 어절 수 — 검토자가 `wc -w`로 셈, lint 기준은 Python split 35).
- 결정과 이유: 수용 14·반박 1. 상세는 [req-design 적대 검토](./req-design.md#적대-검토). ADR-020 상태를 템플릿 생명주기대로 `proposed`(15번).
- 검증: `lint_worklog.py` 0 오류
- 결과: 완료 — 2026-10-26 01:55

### 2026-10-26 — 적대 검토 2라운드와 승인 요청 준비

- 발견 사항: 2라운드(같은 검토자, 약 150k 토큰 누적·6 도구 호출·1분 25초) — 1~15 해소 12·남음 3(4 Q-03 예외 판정, 10 ADR 건수, 11 요약 다음 행동), 신규 4(16 DCR 재승인 요청 미연결 중간, 17~19 낮음 — 추적표, ADR 문구, 해석 사실 오류). 라운드 상한으로 종료.
- 결정과 이유: 남음·신규 7건 모두 작성자 수정, 검토자 재확인 없음을 표와 승인 요청에 공개. Q-03은 FR-04 예외 미충족 — 사용자 지시로 승인 관문에서 묻는다고 명시.
- 검증: `lint_worklog.py`·`lint_skill.py` 0 오류
- 결과: 완료 — 2026-10-26 02:00

### 2026-10-26 — 승인과 계획 수립

- 발견 사항: 사용자 응답 "권장안 전체 승인합니다. 계속 진행하세요" — Q-01~Q-04 권장안 채택, FR·DES 변경 없음. §3.1 재확인 08:28 — HEAD `0410724`+미커밋(docs/만), `유지` 4행 통과(TST-01 56, TST-02 86, TST-05 15).
- 결정과 이유: req-design v1·ADR-020 `approved`·등록부 갱신, [plan](./plan.md) TASK-01~05. 문서 전용이라 Red는 grep 부재로 대신(req-design 검증 전략).
- 검증: 위 테스트 출력, `lint_worklog.py`
- 결과: 완료 — 2026-10-26 08:30

### 2026-10-26 — TASK-01~04 문서 변경

- Red: `grep -c` 기대 문구 · 0410724+dirty · 문서 전용, 편집 전 기대 문구 0건과 references 2파일 부재
- 수행 내용: templates DES-03 a~d, references 2파일 신설, wf-design §2·§4.1·§4.5·§6.2, approval-request §1, design-change §2·§3G·§5, verification-depth §6.
- 결정과 이유: §6.2 예시는 templates로 이관(Q-04 (A)). 설치본은 심볼릭 링크라 동기화 불필요.
- 검증: grep 기대 문구 ≥1, `lint_skill.py` 0 오류, K3 wf-design 2,174·나머지 무변경, NFR-04 앵커 8개, 본문 하네스 명칭 0, wf-implement 본문 diff 없음
- 결과: 완료 — 2026-10-26 08:33

### 2026-10-26 — TASK-05 통합 검증

- Red: 해당 없음 — 통합 검증 TASK, 새 검사 없음
- 발견 사항: `유지` 4행 통과(08:36 — TST-01 56, TST-02 86(TST-04 16 포함), TST-05 15). 테스트 파일 변경 없음 → 재정비 관문 변경 없음. 코드 파일 변경 없음 → 변경 범위 뮤테이션 대상 없음.
- 결정과 이유: 자체 리뷰(diff) — 본문 §2·§4.1 링크가 §3.1 고위험 가정 확인과 충돌하지 않음(interview §2 7항목이 보안·데이터·인터페이스·호환성 포함). 줄바꿈 경고는 autocrlf 정규화(내용 diff 없음).
- 검증: 위 테스트 출력, `lint_skill.py`·`lint_worklog.py` 0 오류
- 결과: 완료 — 2026-10-26 08:48 (커밋·push 승인 대기 08:37 → 승인 08:40, 아래 종결 항목)

### 2026-10-26 — 완료 보고 관문 승인

- Red: 해당 없음 — 승인 기록
- 발견 사항: 완료 보고 관문(구현 커밋 범위 — skills/ 7파일 + docs/ 변경 전부, 종결 커밋, push 1회)에 사용자 응답 "승인을 기록하고 인계 준비".
- 결정과 이유: 커밋·push 승인으로 기록. 사용자 요청대로 실행 전 세션 인계 — closing ①부터 다음 세션에서 진행.
- 검증: `lint_worklog.py` 0 오류
- 결과: 완료 — 2026-10-26 08:40

### 2026-10-26 — 종결(closing ①~④)

- Red: 해당 없음 — 종결 절차
- 발견 사항: 재개 시 `git status --short`가 인계 절 미커밋 변경 한 줄과 일치(skills/ 7파일, docs/). ① 구현 커밋 `96b249c`. ② clean 08:47 — TST-01 56/56, TST-02 86 passed(TST-04 16 포함), TST-04 16 passed, TST-05 15 passed. ④ `git diff --name-only 96b249c` 전부 `docs/`.
- 결정과 이유: 대장 `유지` 4행 SHA를 `96b249c`로, 재정비 기록 1행(변경 없음). 05 머리말에 사이클 A 완료. req-design 추적표는 승인 기준선이라 수정하지 않고 결과는 아래 인수 조건별 결과에 둔다.
- 검증: 위 테스트 출력, `lint_worklog.py`·`lint_skill.py` 0 오류
- 결과: 완료 — 2026-10-26 08:49

## 설계와 달라진 점

- 없음 — §6.2 예시의 templates 이관은 승인된 Q-04 (A)·DES-01대로.

## 검증 결과

### 범위와 환경

- 대상 기준선 또는 구현: [REQ-DESIGN-design-questions](./req-design.md) v1, TASK-01~05
- 실행 환경: Windows 11, Python 3.14.2, pytest, hypothesis 6.170.9, PowerShell 5.1
- 제외 항목: TST-03(`격리`, `pptx` 미설치 — 기존, 무관). 코드 파일 변경 없음 → 변경 범위 뮤테이션 대상 없음

### 결과 요약

- 총계: 157 (성공 157 / 실패 0 / 미수행 0) — `유지` 4행(TST-04 16건은 TST-02에 포함, 중복 집계 안 함)
- 기준: `0410724` · 워킹트리 dirty(통합 08:36). `유지` 전량은 `96b249c` · clean(08:47)
- 명령:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1` 56/56
  - `python -m pytest skills/wf-doc/scripts/tests -q` 86(TST-04 16건 포함)
  - `python -m pytest skills/wf-doc/scripts/tests/test_lint_skill.py -q` 16
  - `python -m pytest skills/wf-tree/scripts/tests -q` 15
- 커버리지: N/A — 커버리지 도구 미사용
- 뮤테이션: N/A — 코드 파일 변경 없음
- 산출물: 없음

### 인수 조건별 결과

| 검증 ID | 인수 조건 | 방법·명령 | 결과 | 분류 | 증거 |
|---|---|---|---|---|---|
| VER-01 | AC-01 | grep `interview.md` 필수 문구, wf-design §2·§4.1 링크, `lint_skill.py` K4·K5 | 성공 | — | TASK-02·03 · 0 오류 |
| VER-02 | AC-02 | grep templates.md 질문 표 6열·`답`·사실 질문 규칙 | 성공 | — | TASK-01 |
| VER-03 | AC-03 | grep design-change §2 시작 조건·verification-depth §6 링크·인계 질문 한 줄, `git diff --stat 0410724 96b249c -- skills/wf-implement/SKILL.md` | 성공 | — | TASK-01·03·04 · diff 비어 있음 |
| VER-04 | AC-04 | grep `adversarial-review.md` FR-08~11·13 문구, §4.5 링크, approval-request §1, templates `## 적대 검토`, design-change §3G | 성공 | — | TASK-01~03 |
| VER-05 | AC-05 | `lint_skill.py` K3, grep §6.2 링크 | 성공 | — | wf-design 2,189 → 2,174, wf-implement 2,850·wf-doc 2,337·wf-tree 1,193 무변경 |
| VER-06 | AC-06 | req-design 질문 표·점검 문단·적대 검토 표 검토 | 성공 | — | [적대 검토](./req-design.md#적대-검토) 2라운드, 지적 19 |
| VER-07 | AC-07 | NFR-04 앵커 8개 grep, 하네스 명칭 grep, 린트 2종, `유지` 4행, ADR-020·등록부, closing.md | 성공 | — | 앵커 8/8 · 명칭 0 · ① `96b249c` · ② clean 08:47 · ④ 전부 `docs/` |

### 실패와 미수행 분석

- 실패 없음. 적대 검토 2라운드의 남음·신규 7건은 작성자 수정 후 검토자 재확인 없음(승인 요청에 공개, 승인됨).
- 질문 단계·적대 검토의 실사용 효과(다음 작업에서 질문 수·지적 수용률)는 이 작업에서 측정하지 않았다.

### 테스트 대장 변경

| 대상 | 현재 상태 → 제안 | 분류·증거 | 유일 검증 여부 | 승인 |
|---|---|---|---|---|
| 없음 | — | 변경 없음 — 테스트 파일·보호 스코프 무변경. Breaking 0 · Stale 0 · Missing 0 | — | 완료 보고 관문(변경 없음 보고, 2026-10-26 08:40) |

## 완료 보고

### 완료 상태

- 결과: 완료
- 완료 판단 근거: AC-01~07 성공, `유지` 4행 clean 통과(`96b249c`), 린트 2종 0 오류, 대장 변경 없음 보고

### 주요 변경

- wf-design `references/interview.md`(질문 단계)·`references/adversarial-review.md`(근거 강제 적대 검토) 신설
- wf-design 본문 §2·§4.1·§4.5·§6.2 연결(2,174어절), approval-request §1, design-change §2·§3G·§5
- wf-doc templates — 질문 표 6열·적대 검토 절·결정 등록부 형식·인계 질문 행, verification-depth §6 링크
- ADR-020 `approved`·등록부 행

### 통합 상태

- 구현 커밋 `96b249c`, 이 종결 커밋과 함께 origin push 대상(승인 2026-10-26 08:40, 완료 보고 관문 "승인을 기록하고 인계 준비"). 설치본은 저장소 심볼릭 링크라 동기화 불필요

### 남은 위험과 제한

- 적대 검토는 하네스별 실행 주체에 의존한다 — 새 맥락 검토자가 없는 환경에서는 미수행 기록으로 남는다.
- 2라운드 상한 뒤 남은 지적은 검토자 재확인 없이 승인 관문으로 넘어간다.
- 질문·적대 검토는 문서 규칙이라 기계 강제 없음(린트 검사 범위 제외).
- 적대 검토 1회 비용 약 119k~150k 토큰(시험 실행).

### 후속 작업

- `bypassPermissions` 모드에서 승인 게이트 `ask` 도달 관찰(사용자, 20261026-approval-gate에서 이월)
- 다음 정식 작업에서 질문 단계·적대 검토 실사용 관찰(질문 수, 지적 수용률, 토큰)
- 질문 표·적대 검토 표 린트는 범위 제외 — 필요 시 별도 작업

## 인계

- 다음 단계 또는 워크플로우: 없음
- 완료된 항목: TASK-01~05, AC-01~07, ADR-020 `approved`, 승인 게이트 실세션 관찰(해소)
- 미완료 항목: 없음
- 다음 행동: 없음

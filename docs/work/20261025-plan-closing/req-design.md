# REQ-DESIGN-plan-closing: plan 갱신 시점과 작업 종결 커밋 — 요구사항·설계

> 문서 유형: `requirements, design`
> 작업 ID: `20261025-plan-closing`
> 상태: `approved`
> 기준선: `v1` (승인일 2026-10-25)
> 작성일: 2026-10-25
> 최종 갱신: 2026-10-25
> 관련 문서: [WORK-20261025-plan-closing: 작업 기록](./work-log.md), [ADR-016: 작업 종결 커밋 규칙](./ADR-016-작업-종결-커밋-규칙.md), [REQ-DESIGN-plan-relocation](../20261009-plan-relocation/req-design.md), [ADR-003](../20260814-wf-tree-triggers/ADR-003-트리거-단일-관문.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: (1) 진행 중·완료 후의 plan이 실제 상태를 보이도록 갱신 시점을 정하고, (2) 마지막 커밋·push 시점에 모든 문서가 완료 상태가 되도록 종결 순서를 정한다.
- 현재 결론 또는 상태: v1 승인(2026-10-25), Q-01·Q-02 모두 (A).
- 다음 행동: wf-implement 계획 수립. 상세는 [인계](#인계).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | N/A | document | 이 작업의 루트 문서(스킬 규칙 변경, 선례 [skill-diet](../20261009-skill-diet/req-design.md)) |
| input | change | [REQ-DESIGN-plan-relocation](../20261009-plan-relocation/req-design.md) | FR-02, DES-02 | 온디맨드 렌더링을 부분 변경. 완료 문서라 역방향 링크 없음(NFR-03) |
| input | related | [ADR-003](../20260814-wf-tree-triggers/ADR-003-트리거-단일-관문.md) | 결정 | 재생성 규칙의 정본 위치(wf-implement §3.2) 유지. ADR-003 대체 관계에 관련 1행 |
| output | decision | [ADR-016](./ADR-016-작업-종결-커밋-규칙.md) | document | 종결 커밋 방식(A), 대안 B·C 기각 |
| output | implementation | [WORK-20261025-plan-closing](./work-log.md) | document | 승인 후 plan.md |

## 문제와 목적

사용자 요청(2026-10-25):

> plan 문서가 업데이트 되지 않은것 같아. … 이전 버전에서 매 task마다 업데이트 하던 것을 업데이트 하지 않도록 수정하면서 생긴 side effect 인것 같아.
>
> 마지막 커밋/푸쉬 시점에 모든 문서의 완료를 진행하고 싶어.

## 현재 상태 조사 (wf-design §4.1)

### 사실

- [wf-tree §생성 시점](../../../skills/wf-tree/SKILL.md#생성-시점): 트리는 "계획 최초 작성 시 1회"와 "사용자 요청 시"에만 생성하고, 상태·완료 시점 갱신은 "트리를 건드리지 않는다". [wf-implement §3.2](../../../skills/wf-implement/SKILL.md#32-계획-수립)도 같은 규칙을 가리킨다.
- plan의 머리말 `상태`·`## 요약`·`## 인계`에는 갱신 시점 규칙이 없다. §7 아카이빙은 work-log 인계 축약·status 행 제거만 정하고 plan에는 "옮기거나 축약하지 않는다"뿐이다.
- 결과: [regression-guard plan](../20261025-regression-guard/plan.md)이 종결·push 후에도 트리 "in-progress (0/8)". [status.md](../../status.md) 트리는 2026-10-09 생성본으로 이미 제거된 `20261009-plan-relocation`을 진행 중으로 보인다.
- 온디맨드 규칙은 plan-relocation FR-02(2026-10-09, `f9aa8c4`)가 도입했다. 근거는 손 렌더(Mermaid·ASCII)와 스냅숏의 비용. 같은 날 skill-diet(`a38ed25`, ADR-011)가 `render.py --write`를 도입해 재생성이 결정적 명령 1줄이 됐으나 시점 규칙은 재검토되지 않았다.
- 종결 순서: wf-implement §3.6 "커밋·push는 사용자 요청 범위", §7 아카이빙(종결 시 인계 축약·status 행 제거). 대장 `마지막 성공`은 SHA 형식이고(templates.md), 판정 스크립트 `regression_guard.py`는 그 SHA 이후 `유지` 테스트 파일 변경을 열린 작업 기록과 대조한다 — 기록이 닫히면 대조 근거가 사라진다.
- regression-guard 종결: 구현 커밋 `fe003ec` → clean 재실행 → 종결 커밋 `66e4907`(작업 기록에 "푸시"를 사전 서술) → push → plan 트리 갱신(미커밋). 마지막 push 뒤에 문서 변경이 남았다.
- 어절: wf-tree 1,200/1,200, wf-implement 2,846/2,850, wf-doc 2,337/2,350(lint_skill K3).

### 해석

- 갱신 공백의 원인은 "비용" 전제의 소멸이다. 재생성이 명령 1줄이면 상태 전이마다 하는 편이 동결 문서의 오표시보다 싸다.
- 종결 문제의 원인은 자기 참조다. 커밋은 자기 SHA를 담을 수 없고 push 결과는 push 전에 알 수 없다. 그래서 종결 기록이 마지막 커밋 뒤로 밀리거나 사전 서술이 된다.
- 종결 커밋이 문서만 바꾸면 구현 커밋에서 잰 3튜플(테스트 집합·SHA·명령)이 종결 커밋에서도 그대로 성립한다(테스트 대상 무변경).
- 커밋 없이 기록을 닫으면 대장 셀이 `+dirty`인 채 닫힌 기록이 남아, 이후 판정 스크립트가 그 작업의 테스트 변경을 위반으로 낸다. 종결은 구현 커밋을 전제해야 한다.

### 가정

- 저장소는 git을 쓰고 원격 push는 사용자 승인 범위다(현행 §2.3).
- 트리를 쓰지 않는 계획(TASK 3개 미만 등)은 트리 재생성 의무가 없다(현행 채택 기준 유지).

## 범위

### 포함

- `skills/wf-tree/SKILL.md` §생성 시점, §8 이후 갱신 문구
- `skills/wf-implement/SKILL.md` §3.2(완료 전이 갱신), §3.6(종결 커밋 포인터), §7 아카이빙 시점
- `skills/wf-implement/references/closing.md` 신설(종결 절차 본체)
- `skills/wf-doc/references/templates.md` plan·status 노트, 완료 보고 `통합 상태` 노트
- 자기 적용: 이 작업의 plan·종결, regression-guard plan 트리(재생성분 포함), status.md 트리

### 제외

- 대장 `마지막 성공` 형식·판독기 변경(대안 B·C — [ADR-016](./ADR-016-작업-종결-커밋-규칙.md))
- 종결 커밋의 기계 검사(린트·훅) — 후속 후보
- plan `## 인계`와 work-log 인계의 중복 정리

## 기능 요구사항

| ID | 이름 | 내용 |
|---|---|---|
| FR-01 | TASK 완료 전이 갱신 | TASK를 `completed`로 바꾸는 같은 변경에서 plan의 `상태`·`완료` 필드, `## 요약`의 현재 상태·다음 행동, 계획 트리(트리를 쓰는 계획만)를 갱신해야 한다 |
| FR-02 | 종결 시 plan 확정 | 작업을 종결하는 변경에서 plan 머리말 `상태: completed`, `## 요약`·`## 인계`의 다음 행동 "없음", 최종 트리를 확정해야 한다 |
| FR-03 | 포트폴리오 트리 | `status.md`의 행을 추가·제거하는 같은 변경에서 그 트리를 재생성해야 한다(Q-01) |
| FR-04 | 종결 순서 | 커밋을 수행하는 작업은 ① 구현 커밋 ② 그 SHA에서 `유지` 전량 재실행 ③ 종결 갱신 일괄(대장 SHA·재정비 기록, plan, work-log 종결·완료 보고, status 행·트리, 추적성) ④ 구현 커밋 이후 변경이 `docs/`뿐인지 확인 ⑤ 문서 전용 종결 커밋 ⑥ 승인된 경우 두 커밋을 한 번에 push 순서를 따라야 한다 |
| FR-05 | push 이후 무변경 | 문서에는 push 결과를 쓰지 않는다(`통합 상태`는 구현 커밋 SHA와 "종결 커밋과 함께 push 대상, 승인 일시"). push 뒤에 그 작업의 문서를 고치지 않으며, 필요하면 새 작업이나 경량 경로로 처리한다 |
| FR-06 | 커밋 전 종결 금지 | 구현 커밋이 승인되지 않으면 작업을 종결하지 않는다. 작업 상태는 `awaiting-approval`, 인계 다음 행동은 "커밋 승인 대기"(Q-02) |

## 비기능 요구사항

| ID | 이름 | 내용 |
|---|---|---|
| NFR-01 | 분량 | 본문 어절 상한 유지 — wf-tree ≤ 1,200, wf-implement ≤ 2,850, wf-doc ≤ 2,350(K3). 절차 본체는 references |
| NFR-02 | 린트·테스트 | `lint_skill.py`·`lint_worklog.py` 0 오류, 대장 `유지` 4행 통과 |
| NFR-03 | 완료 기록 불변 | 완료된 작업 기록·ADR 소급 수정 없음(ADR-003 대체 관계 1행 같은 역방향 링크만). regression-guard plan 트리 재생성은 현행 "사용자 요청 시"에 해당 |
| NFR-04 | 하네스 중립 | 규칙은 의무만 적고 훅·특정 하네스를 전제하지 않는다 |
| NFR-05 | 재개 비용 불변 | 세션 재개 절차는 트리를 읽지 않는다(session-resume §1 유지) |

## 인수 조건

| ID | 조건 |
|---|---|
| AC-01 | wf-tree §생성 시점에 plan의 TASK `completed` 전이·작업 종결, status의 행 추가·제거가 재생성 시점으로 있고 "트리를 건드리지 않는다" 문장이 없다(FR-01~03) |
| AC-02 | wf-implement §3.2에 완료 전이 같은 변경의 요약·트리 갱신 문장, §7 아카이빙에 plan 확정 항목과 `references/closing.md` 링크가 있다(FR-01·02) |
| AC-03 | `references/closing.md`에 FR-04의 6단계, 단계 ④의 확인 명령, FR-05·06 규칙이 있다 |
| AC-04 | templates.md plan·status 노트가 새 시점을, 완료 보고 `통합 상태` 노트가 FR-05 표기를 가리킨다 |
| AC-05 | `lint_skill.py` 0 오류(K3 상한 내, 고아 references 없음), `lint_worklog.py` 0 오류, `유지` 4행 통과(NFR-01·02) |
| AC-06 | 자기 적용 — 이 작업 plan의 트리가 TASK마다 재생성되고, 종결이 구현 커밋 + 문서 전용 종결 커밋 1회 push로 끝나며 push 뒤 이 작업 문서의 변경이 없다(`git log`·`git diff --name-only`로 확인) |
| AC-07 | ADR-016 `approved`, `decisions.md` 행, ADR-003 대체 관계에 관련 1행 |

## 설계

| ID | 이름 | 내용 |
|---|---|---|
| DES-01 | wf-tree 생성 시점 | §생성 시점을 3항으로 — ① 최초 작성 ② 상태 전이: plan은 TASK `completed` 전이·작업 종결, status는 행 추가·제거 ③ 사용자 요청. "트리를 건드리지 않는다" 문장 삭제, `render.py --write` 사용 명시. 어절 순증 0(같은 절 문장 압축). §8 "이후 갱신" 문구는 링크만 유지 |
| DES-02 | wf-implement §3.2 | "트리는 [생성 시점]에만 재생성하며 목록이 정본이다" → "같은 변경에서 `## 요약`과 트리([생성 시점])도 갱신한다. 목록이 정본이다". 재생성 규칙의 정본 위치는 ADR-003대로 §3.2 |
| DES-03 | wf-implement §3.6·§7 | §3.6 끝 문장에 "커밋하면 종결 순서는 [closing.md]"를 붙이고, §7 아카이빙 둘째 항목에 "plan 머리말·요약·인계·최종 트리"를 더한다. 순증 어절은 같은 절 축약으로 상쇄(≤ +4) |
| DES-04 | references/closing.md | 절: 1. 원칙(자기 참조, 마지막 커밋 = 완료), 2. 순서 6단계 표(단계·하는 일·확인), 3. 단계 ④ 명령 `git diff --name-only <구현 SHA>` 결과가 `docs/` 밖이면 종결 커밋 중단·구현 커밋부터 다시, 4. 기록 규칙(FR-05 표기, 사후 수정 금지), 5. 커밋 미승인(FR-06), 6. 커밋하지 않는 저장소(git 없음)는 종결 갱신을 한 변경에 모으는 것만 적용 |
| DES-05 | wf-doc 템플릿 | plan 노트(`## 계획 트리` 생성 시점 링크 문구), status 노트, 완료 보고 `### 통합 상태` 노트에 "push 결과 대신 push 대상·승인 일시, 정본은 git" |
| DES-06 | 자기 적용 | 이 작업도 TASK마다 트리 재생성, 종결은 closing.md 순서. 종결 변경에서 status.md 트리 재생성, regression-guard plan 트리(이미 재생성됨)는 구현 커밋에 포함 |

### 검증 전략

- AC-01~04: 통독과 `grep`(문장 존재·삭제).
- AC-05: 린트 2종, `유지` 4행(TST-01·02·04·05).
- AC-06: 종결 후 `git log --oneline -3`, `git diff --name-only <구현 SHA> <종결 SHA>`가 `docs/`뿐, push 후 `git status` clean.
- AC-07: `decisions.md`·ADR 머리말 대조.

## 가정과 미해결 질문

| ID | 질문 | 권장 | 이유 |
|---|---|---|---|
| Q-01 | `status.md` 트리도 행 추가·제거 시 재생성할까 — (A) 예, (B) plan만 | **(A)** — 사용자 채택 | 같은 원인(온디맨드)으로 이미 틀린 트리가 있다. 명령 1줄 |
| Q-02 | 구현 커밋 미승인 시 — (A) 종결하지 않고 `awaiting-approval`, (B) 종결 후 커밋은 나중 | **(A)** — 사용자 채택 | (B)는 `+dirty` 셀과 닫힌 기록이 남아 판정 스크립트가 이후 위반을 낸다 |

## 위험

| ID | 위험 | 영향 | 완화 |
|---|---|---|---|
| RISK-01 | 어절 상한(wf-tree 여유 0, wf-implement 4) | K3 오류 | 본체는 closing.md, 본문은 압축·링크 |
| RISK-02 | 종결 커밋에 코드·테스트가 섞임 | 대장 SHA 무효 | 단계 ④ 확인 명령 |
| RISK-03 | push 실패 | 문서의 "push 대상"과 원격 불일치 | 문서는 결과를 쓰지 않음 — git으로 재시도, 문서 무변경 |
| RISK-04 | TASK마다 plan diff 증가 | 리뷰 소음 | 결정적 생성물, `generated` 주석으로 구분 |

## 추적성

| 요구사항 | 설계 | 인수 조건 | 계획 |
|---|---|---|---|
| FR-01·02 | DES-01, DES-02, DES-03 | AC-01, AC-02 | 승인 후 plan.md |
| FR-03 | DES-01 | AC-01 | 승인 후 plan.md |
| FR-04~06 | DES-03, DES-04, DES-05 | AC-03, AC-04, AC-06 | 승인 후 plan.md |
| NFR-01~05 | DES-01~06 | AC-05, AC-07 | 승인 후 plan.md |

## 승인 기록

- 2026-10-25 — 사용자가 대화형 승인 관문에서 이 문서를 기준선 v1로 **승인**. 응답: Q-01 "(A) 예, status도 재생성", Q-02 "(A) 종결하지 않고 대기", "승인". [ADR-016](./ADR-016-작업-종결-커밋-규칙.md) 동시 승인.

## 인계

- 다음 단계 또는 워크플로우: wf-design §8 사용자 승인 관문 → 승인 시 wf-implement 계획 수립
- 시작 조건: 충족 — 이 문서 v1·ADR-016 승인(2026-10-25)
- 입력 문서와 기준선: 위 문서 연결
- 완료된 항목: §4.1 조사, 요구사항·설계·위험·추적표, ADR-016 초안, §4.5 일관성 검토
- 미완료 항목: 계획, 구현·검증
- 차단 요인: 없음
- 다음 행동: wf-implement 계획 수립

## 변경 이력

| 날짜 | 변경 내용 | 근거 | 상태 전이 | 작성·승인 |
|---|---|---|---|---|
| 2026-10-25 | 최초 작성 — 조사, FR-01~06, NFR-01~05, AC-01~07, DES-01~06, Q-01·02, RISK-01~04, ADR-016 초안 | 사용자 요청(plan 미갱신, 마지막 커밋 시점 완료), A안 선택 | draft → awaiting-approval | Claude(작성) |
| 2026-10-25 | 승인 — Q-01·Q-02 (A) 채택 기록, 승인 기록, 인계 | 사용자 승인 관문 응답 | awaiting-approval → approved, v1 | 사용자(승인) |

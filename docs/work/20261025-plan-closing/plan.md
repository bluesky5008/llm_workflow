# PLAN-20261025-plan-closing: 구현 계획 — plan 갱신 시점과 작업 종결 커밋

> 문서 유형: `plan`
> 작업 ID: `20261025-plan-closing`
> 상태: `completed`
> 기준선: [REQ-DESIGN-plan-closing](./req-design.md) `v1` (승인일 2026-10-25)
> 작성일: 2026-10-25
> 최종 갱신: 2026-10-25
> 관련 문서: [WORK-20261025-plan-closing: 작업 기록](./work-log.md), [ADR-016](./ADR-016-작업-종결-커밋-규칙.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 승인된 v1(FR-01~06)을 4개 TASK로 구현하고, 종결은 새 규칙(ADR-016)을 자기 적용한다.
- 현재 결론 또는 상태: TASK-01~04 완료(4/4).
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-plan-closing](./req-design.md) | FR-01~06, AC-01~07, DES-01~06 | v1 |
| input | decision | [ADR-016](./ADR-016-작업-종결-커밋-규칙.md) | document | approved |
| output | implementation | [WORK-20261025-plan-closing](./work-log.md) | 수행 기록 | TASK별 결과 |

## 기준선

- 관련 요구사항: FR-01~06, NFR-01~05
- 관련 설계: DES-01~06
- 관련 ADR·DCR: [ADR-016](./ADR-016-작업-종결-커밋-규칙.md), [ADR-003](../20260814-wf-tree-triggers/ADR-003-트리거-단일-관문.md)(정본 위치 유지)

## 작업 정의

- 목표: 트리·plan 갱신 시점 복원과 종결 커밋 순서의 규칙화.
- 범위: req-design [포함](./req-design.md#포함).
- 범위 밖: req-design [제외](./req-design.md#제외).
- 가정: §3.1 재확인(2026-10-25 23:43) — HEAD `66e4907`+미커밋(문서만), `유지` 4행 통과(TST-01 47, TST-02 68, TST-04 16, TST-05 13).
- 위험: RISK-01(어절 여유 wf-tree 0·wf-implement 4) — TASK마다 `lint_skill.py`로 확인.

## 계획 트리

<!-- generated: 2026-10-25 23:52 — scripts/render.py --view all -->

```text
[작업] 20261025-plan-closing — plan 갱신 시점과 작업 종결 커밋 ... completed (4/4)
├─ [✓] wf-tree 생성 시점 (DES-01) (TASK-01) ................... 2026-10-25 23:46
├─ [✓] wf-implement 본문과 closing.md (DES-02~04) (TASK-02) ... depends: TASK-01  2026-10-25 23:48
├─ [✓] wf-doc 템플릿 노트 (DES-05) (TASK-03) .................. depends: TASK-02  2026-10-25 23:49
└─ [✓] 통합과 종결 (자기 적용, DES-06) (TASK-04) .............. depends: TASK-01~03  2026-10-25 23:53
```

## 작업 목록

### TASK-01: wf-tree 생성 시점 (DES-01)

- 상태: completed
- 완료: 2026-10-25 23:46
- 상위: 없음
- 목표: §생성 시점을 3항(최초·상태 전이·요청)으로, "트리를 건드리지 않는다" 삭제
- 관련 요구사항과 설계: FR-01~03, DES-01, AC-01
- 변경 대상: `skills/wf-tree/SKILL.md`(§생성 시점, §8 이후 갱신), `skills/wf-tree/references/node-templates.md`(체크리스트 문구 필요 시)
- 의존성: 없음
- 위험: RISK-01 — 순증 0
- 검증 방법: 문서 변경이라 TDD 비대상(`Red: 해당 없음`). `lint_skill.py` 0 오류, grep(삭제 문장 부재)
- 완료 조건: AC-01

### TASK-02: wf-implement 본문과 closing.md (DES-02~04)

- 상태: completed
- 완료: 2026-10-25 23:48
- 상위: 없음
- 목표: §3.2 완료 전이 갱신, §3.6 종결 포인터, §7 아카이빙 plan 확정, `references/closing.md` 신설
- 관련 요구사항과 설계: FR-01·02·04~06, DES-02~04, AC-02·03
- 변경 대상: `skills/wf-implement/SKILL.md`, `skills/wf-implement/references/closing.md`(신설)
- 의존성: TASK-01(§생성 시점 앵커 참조)
- 위험: RISK-01 — 순증 ≤ 4
- 검증 방법: 문서 변경(`Red: 해당 없음`). `lint_skill.py` 0 오류(K3·고아 references), 통독
- 완료 조건: AC-02·03

### TASK-03: wf-doc 템플릿 노트 (DES-05)

- 상태: completed
- 완료: 2026-10-25 23:49
- 상위: 없음
- 목표: plan·status 노트의 생성 시점 문구, 완료 보고 `통합 상태` 노트
- 관련 요구사항과 설계: FR-05, DES-05, AC-04
- 변경 대상: `skills/wf-doc/references/templates.md`
- 의존성: TASK-02(closing.md 링크)
- 위험: 없음
- 검증 방법: 문서 변경(`Red: 해당 없음`). `lint_skill.py`, 통독
- 완료 조건: AC-04

### TASK-04: 통합과 종결 (자기 적용, DES-06)

- 상태: completed
- 완료: 2026-10-25 23:53
- 상위: 없음
- 목표: 자체 리뷰, 완료 보고 관문(커밋·push 승인), closing.md 순서로 종결
- 관련 요구사항과 설계: AC-05~07, DES-06
- 변경 대상: 작업 기록, plan, `docs/status.md`(행 제거·트리 재생성), regression-guard `plan.md` 트리(구현 커밋에 포함)
- 의존성: TASK-01~03
- 위험: RISK-02(종결 커밋에 코드 혼입) — 단계 ④ 확인
- 검증 방법: 린트 2종, `유지` 전량, 종결 후 `git log`·`git diff --name-only <구현 SHA> <종결 SHA>`
- 완료 조건: AC-05~07, wf-implement §5

## 검증 계획

- 자동: `lint_skill.py`(TST-04 대상), `lint_worklog.py`, `유지` 4행. 새 테스트 없음(문서 규칙 변경).
- AC 대응: AC-01 TASK-01, AC-02·03 TASK-02, AC-04 TASK-03, AC-05~07 TASK-04.
- 수동: 통독, 종결 후 git 확인.

## 마이그레이션과 롤백

- 마이그레이션: 없음(스킬 문서는 junction으로 즉시 반영).
- 롤백: `git revert`.

## 인계

- 다음 단계 또는 워크플로우: 없음
- 시작 조건: 충족
- 입력 문서와 기준선: 위 기준선
- 완료된 항목: §3.1 재확인, 계획, TASK-01~04
- 미완료 항목: 없음
- 차단 요인: 없음
- 다음 행동: 없음

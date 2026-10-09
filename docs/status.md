# ST-llm-workflow: 포트폴리오 — 진행 중 작업

> 문서 유형: `status`
> 작업 ID: `N/A — 포트폴리오(작업 상위 단위)`
> 상태: `in-progress`
> 기준선: `N/A — 포트폴리오. 최초 생성(범위) 승인은 [REQ-DESIGN-plan-relocation v1](./work/20261009-plan-relocation/req-design.md#승인-기록) 승인 관문이 겸함(2026-10-09)`
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [wf-tree 포트폴리오 생성과 갱신](../skills/wf-tree/SKILL.md#8-포트폴리오-생성과-갱신), [wf-implement 작업 기록과 저장 위치](../skills/wf-implement/SKILL.md#7-작업-기록과-저장-위치), [결정 등록부](./decisions.md)

## 요약

- 목적: 이 저장소에서 진행 중인 작업만 한 표로 조망한다. 완료 작업은 싣지 않으며, 이력은 `docs/work/` 각 폴더와 git이 정본이다.
- 현재 결론 또는 상태: 진행 중 0건·보류 1건. 사이클 4(`20261009-skill-diet`)는 완료 보고 종결로 행 제거(2026-10-09 20:19). 사이클 3(`20261009-test-lifecycle`)은 완료 보고 종결로 행 제거(2026-10-09 16:45). (사이클 1·2 작업은 완료 보고 종결로 행 제거 — 트리는 온디맨드 규칙에 따라 재생성하지 않음, 생성 일시 참조)
- 다음 행동: 아래 작업 목록의 `다음 행동` 열.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | approval | [REQ-DESIGN-plan-relocation](./work/20261009-plan-relocation/req-design.md#승인-기록) | document | 포트폴리오 최초 생성 승인(wf-tree §8)을 v1 승인 관문이 겸함. 이전 `docs/plan.md`를 대체(DES-05·07) |
| input | related | [PLAN-20261009-plan-relocation: 구현 계획](./work/20261009-plan-relocation/plan.md) | document | 이 문서를 만든 작업(완료, 행 제거됨) |
| output | related | [WORK-20260814-multiuser-workflow: 작업 기록](./work/20260814-multiuser-workflow/work-log.md) | document | 포함 작업(보류) |
| input | related | [WORK-20261009-test-lifecycle: 작업 기록](./work/20261009-test-lifecycle/work-log.md) | document | 포함했던 작업(사이클 3, 완료 — 행 제거됨). 테스트 대장 [REGISTER-llm-workflow](./test-register.md) 신설 |
| input | related | [WORK-20261009-worklog-diet: 작업 기록](./work/20261009-worklog-diet/work-log.md) | document | 포함했던 작업(사이클 2, 완료 — 행 제거됨). 이 문서의 행 정합은 그 작업의 린트(L8)가 검사 |
| input | related | [WORK-20261009-skill-diet: 작업 기록](./work/20261009-skill-diet/work-log.md) | document | 포함했던 작업(사이클 4, 완료 — 행 제거됨). 스킬 본문 다이어트·린트·render.py |

## 목표와 범위

- 목표: llm_workflow 저장소의 진행 중(`in-progress`·`awaiting-approval`·`on-hold`·`blocked`) 작업 전부를 한 표로 보인다.
- 행의 추가·제거: [wf-implement 작업 기록과 저장 위치](../skills/wf-implement/SKILL.md#7-작업-기록과-저장-위치) — 작업 기록 시작 시 추가, 완료 보고 종결 시 제거.
- 범위 밖: 완료 작업의 이력과 TASK 목록(각 작업 폴더의 `plan.md`·`work-log.md`가 정본), 작업 상태의 전이(각 작업의 소유자가 판정).

## 작업 목록

| 작업 ID | 제목 | 상태 | 계획·기록 | 의존 | 다음 행동 |
|---|---|---|---|---|---|
| 20260814-multiuser-workflow | 다인 사용 시나리오 토론 | on-hold | [work-log](./work/20260814-multiuser-workflow/work-log.md) | 20261009-plan-relocation | 재개 조건은 작업 기록 인계 절 — plan-relocation 완료 후 Q-04 재검토 |

## 계획 트리

<!-- generated: 2026-10-09 14:00 — 포트폴리오 최초 작성 시 1회 생성. 목록이 정본이며 트리는 요청 시에만 재생성 -->

```text
[포트폴리오] ST-llm-workflow — 진행 중 작업
├─ [▶] 20261009-plan-relocation 계획 문서 재배치 .......... in-progress (4/7)
└─ [ ] 20260814-multiuser-workflow 다인 사용 토론 ......... on-hold  depends: 20261009-plan-relocation
```

## 승인 기록

- 2026-10-09 — 최초 생성(범위 승인)은 [REQ-DESIGN-plan-relocation v1](./work/20261009-plan-relocation/req-design.md#승인-기록) 승인과 함께 사용자 승인(DES-05).

## 변경 이력

| 날짜 | 사건 | 근거 |
|---|---|---|
| 2026-10-09 | 최초 생성. `docs/plan.md`(저장소 관통 구현 계획, 완료 사이클 7개 축약 포함)를 대체 | [REQ-DESIGN-plan-relocation v1](./work/20261009-plan-relocation/req-design.md) DES-05·DES-07, TASK-05 |
| 2026-10-09 | `20261009-plan-relocation` 행 제거(완료 보고 종결, 2026-10-09 14:05) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-09 | `20261009-worklog-diet` 행 추가(wf-design 착수, 작업 기록 시작 — 사이클 2) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-09 | `20261009-worklog-diet` 행 제거(완료 보고 종결, 2026-10-09 15:25) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-09 | `20261009-test-lifecycle` 행 추가(wf-design 착수, 작업 기록 시작 — 사이클 3) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-09 | `20261009-test-lifecycle` 행 제거(완료 보고 종결, 2026-10-09 16:45) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-09 | `20261009-skill-diet` 행 추가(wf-design 착수, 작업 기록 시작 — 사이클 4) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-09 | `20261009-skill-diet` 행 제거(완료 보고 종결, 2026-10-09 20:19) | wf-implement §7 포트폴리오 행의 추가·제거 |

## 인계

- 다음 단계 또는 워크플로우: 각 작업의 작업 기록 인계 절
- 시작 조건: 없음
- 입력 문서와 기준선: 작업 목록의 `계획·기록` 열
- 완료된 항목: 해당 없음(완료 작업은 행을 제거)
- 미완료 항목: 작업 목록 전체
- 차단 요인: 없음
- 다음 행동: 작업 목록의 `다음 행동` 열

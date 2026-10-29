# ST-llm-workflow: 포트폴리오 — 진행 중 작업

> 문서 유형: `status`
> 작업 ID: `N/A — 포트폴리오(작업 상위 단위)`
> 상태: `in-progress`
> 기준선: `N/A — 포트폴리오. 최초 생성(범위) 승인은 [REQ-DESIGN-plan-relocation v1](./work/20261009-plan-relocation/req-design.md#승인-기록) 승인 관문이 겸함(2026-10-09)`
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-29
> 관련 문서: [wf-tree 포트폴리오 생성과 갱신](../skills/wf-tree/SKILL.md#8-포트폴리오-생성과-갱신), [wf-implement 작업 기록과 저장 위치](../skills/wf-implement/SKILL.md#7-작업-기록과-저장-위치), [결정 등록부](./decisions.md)

## 요약

- 목적: 이 저장소에서 진행 중인 작업만 한 표로 조망한다. 완료 작업은 싣지 않으며, 이력은 `docs/work/` 각 폴더와 git이 정본이다.
- 현재 결론 또는 상태: 진행 1건(`20261029-legacy-cleanup`, wf-implement TASK-05 통합 대기 — TASK-01~04 완료 2026-10-29), 보류 1건. `20261028-legacy-onboarding`(v2 레거시 묶음 ① 규칙, 대장 편입·커버리지 보호 스코프)은 완료 보고 종결로 행 제거(2026-10-28 01:49). `20261026-component-deps`(v2 설계 사이클 C, 기존 자산 대조·의존 표 검사·침식 점검)는 완료 보고 종결로 행 제거(2026-10-27 01:10). `20261026-design-questions`(v2 설계 사이클 A, 설계 질문·적대 검토)는 완료 보고 종결로 행 제거(2026-10-26 08:49). `20261026-approval-gate`(v2 설계 사이클 B, 승인 게이트)는 완료 보고 종결로 행 제거(2026-10-26 01:20). `20261026-test-quality`(v2 테스트 사이클 2, 품질 신호)는 완료 보고 종결로 행 제거(2026-10-26 00:31). `20261025-plan-closing`(plan 갱신 시점·종결 커밋 규칙)은 완료 보고 종결로 행 제거(2026-10-25 23:53). `20261025-regression-guard`(v2 테스트 사이클 1, 회귀 보호의 강제)는 완료 보고 종결로 행 제거(2026-10-25 23:30). `20261018-context-signal-v2`(DCR-013, 임계 훅 신호 v3)는 완료 보고 종결로 행 제거(2026-10-18 01:55). 사이클 4(`20261009-skill-diet`)는 완료 보고 종결로 행 제거(2026-10-09 20:19). 사이클 3(`20261009-test-lifecycle`)은 완료 보고 종결로 행 제거(2026-10-09 16:45). (사이클 1·2 작업은 완료 보고 종결로 행 제거 — 트리는 온디맨드 규칙에 따라 재생성하지 않음, 생성 일시 참조)
- 다음 행동: 아래 작업 목록의 `다음 행동` 열.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | approval | [REQ-DESIGN-plan-relocation](./work/20261009-plan-relocation/req-design.md#승인-기록) | document | 포트폴리오 최초 생성 승인(wf-tree §8)을 v1 승인 관문이 겸함. 이전 `docs/plan.md`를 대체(DES-05·07) |
| input | related | [PLAN-20261009-plan-relocation: 구현 계획](./work/20261009-plan-relocation/plan.md) | document | 이 문서를 만든 작업(완료, 행 제거됨) |
| output | related | [WORK-20260814-multiuser-workflow: 작업 기록](./work/20260814-multiuser-workflow/work-log.md) | document | 포함 작업(보류) |
| output | related | [WORK-20261028-legacy-onboarding: 작업 기록](./work/20261028-legacy-onboarding/work-log.md) | document | 포함했던 작업(완료 — 행 제거됨). v2 레거시 묶음 ① 규칙, ADR-023 |
| output | related | [WORK-20261026-component-deps: 작업 기록](./work/20261026-component-deps/work-log.md) | document | 포함했던 작업(완료 — 행 제거됨). v2 설계 사이클 C |
| input | related | [WORK-20261026-design-questions: 작업 기록](./work/20261026-design-questions/work-log.md) | document | 포함했던 작업(완료 — 행 제거됨). v2 설계 사이클 A, ADR-020 |
| input | related | [WORK-20261009-test-lifecycle: 작업 기록](./work/20261009-test-lifecycle/work-log.md) | document | 포함했던 작업(사이클 3, 완료 — 행 제거됨). 테스트 대장 [REGISTER-llm-workflow](./test-register.md) 신설 |
| input | related | [WORK-20261009-worklog-diet: 작업 기록](./work/20261009-worklog-diet/work-log.md) | document | 포함했던 작업(사이클 2, 완료 — 행 제거됨). 이 문서의 행 정합은 그 작업의 린트(L8)가 검사 |
| input | related | [WORK-20261009-skill-diet: 작업 기록](./work/20261009-skill-diet/work-log.md) | document | 포함했던 작업(사이클 4, 완료 — 행 제거됨). 스킬 본문 다이어트·린트·render.py |
| input | related | [WORK-20261018-context-signal-v2: 작업 기록](./work/20261018-context-signal-v2/work-log.md) | document | 포함했던 작업(완료 — 행 제거됨). 임계 훅 신호 v3·세션 재개 경량화, DCR-013 |
| input | related | [WORK-20261025-plan-closing: 작업 기록](./work/20261025-plan-closing/work-log.md) | document | 포함했던 작업(완료 — 행 제거됨). plan 갱신 시점·종결 커밋, ADR-016 |
| input | related | [WORK-20261026-approval-gate: 작업 기록](./work/20261026-approval-gate/work-log.md) | document | 포함했던 작업(완료 — 행 제거됨). v2 설계 사이클 B, ADR-018·DCR-019 |
| input | related | [WORK-20261026-test-quality: 작업 기록](./work/20261026-test-quality/work-log.md) | document | 포함했던 작업(완료 — 행 제거됨). v2 테스트 사이클 2, ADR-017 |
| input | related | [WORK-20261025-regression-guard: 작업 기록](./work/20261025-regression-guard/work-log.md) | document | 포함했던 작업(완료 — 행 제거됨). 회귀 보호의 강제, ADR-014·DCR-015 |

## 목표와 범위

- 목표: llm_workflow 저장소의 진행 중(`in-progress`·`awaiting-approval`·`on-hold`·`blocked`) 작업 전부를 한 표로 보인다.
- 행의 추가·제거: [wf-implement 작업 기록과 저장 위치](../skills/wf-implement/SKILL.md#7-작업-기록과-저장-위치) — 작업 기록 시작 시 추가, 완료 보고 종결 시 제거.
- 범위 밖: 완료 작업의 이력과 TASK 목록(각 작업 폴더의 `plan.md`·`work-log.md`가 정본), 작업 상태의 전이(각 작업의 소유자가 판정).

## 작업 목록

| 작업 ID | 제목 | 상태 | 계획·기록 | 의존 | 다음 행동 |
|---|---|---|---|---|---|
| 20261029-legacy-cleanup | v2 레거시 묶음 ② 규칙 — 독립 재정비 작업·`리팩터` 전이·대량 승인 계층화 | in-progress | [plan](./work/20261029-legacy-cleanup/plan.md) · [work-log](./work/20261029-legacy-cleanup/work-log.md) | 20261028-legacy-onboarding | TASK-05 통합·종결(AC-06) |
| 20260814-multiuser-workflow | 다인 사용 시나리오 토론 | on-hold | [work-log](./work/20260814-multiuser-workflow/work-log.md) | 20261009-plan-relocation | 재개 조건은 작업 기록 인계 절 — plan-relocation 완료 후 Q-04 재검토 |

## 계획 트리

<!-- generated: 2026-10-29 21:24 — scripts/render.py --view active -->

```text
[포트폴리오] ST-llm-workflow — 진행 중 작업 ... in-progress
├─ [▶] 20261029-legacy-cleanup v2 레거시 묶음 ② 규칙 — 독립 재정비 작업·`리팩터` 전이·대량 승인 계층화 ... in-progress  depends: 20261028-legacy-onboarding
└─ [ ] 20260814-multiuser-workflow 다인 사용 시나리오 토론 ............................................... on-hold  depends: 20261009-plan-relocation
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
| 2026-10-18 | `20261018-context-signal-v2` 행 추가(wf-design 설계 변경 착수, 작업 기록 시작) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-18 | `20261018-context-signal-v2` 행 제거(완료 보고 종결, 2026-10-18 01:55) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-25 | `20261025-regression-guard` 행 추가(wf-design 착수, 작업 기록 시작) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-25 | `20261025-regression-guard` 상태 awaiting-approval → approved(v1, ADR-014·DCR-015 승인, C층 v4) | 사용자 승인 관문 |
| 2026-10-25 | `20261025-regression-guard` 상태 approved → in-progress(plan.md 작성) | wf-implement §3.2 |
| 2026-10-25 | `20261025-regression-guard` 행 제거(완료 보고 종결, 2026-10-25 23:30) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-25 | `20261025-plan-closing` 행 추가(wf-design 착수, 작업 기록 시작) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-25 | `20261025-plan-closing` 상태 awaiting-approval → in-progress(v1 승인, plan.md 작성) | wf-implement §3.2 |
| 2026-10-25 | `20261025-plan-closing` 행 제거(완료 보고 종결, 2026-10-25 23:53), 트리 재생성(새 생성 시점 첫 적용) | wf-implement §7, wf-tree 생성 시점 |
| 2026-10-26 | `20261026-test-quality` 행 추가(wf-design 착수, 작업 기록 시작 — v2 테스트 사이클 2), 트리 재생성 | wf-implement §7 포트폴리오 행의 추가·제거, wf-tree 생성 시점 |
| 2026-10-26 | `20261026-test-quality` 상태 awaiting-approval → in-progress(v1 승인, plan.md 작성) | wf-implement §3.2 |
| 2026-10-26 | `20261026-test-quality` 행 제거(완료 보고 종결, 2026-10-26 00:31), 트리 재생성 | wf-implement §7, wf-tree 생성 시점 |
| 2026-10-26 | `20261026-approval-gate` 행 추가(wf-design 착수, 작업 기록 시작 — v2 설계 사이클 B), 트리 재생성 | wf-implement §7 포트폴리오 행의 추가·제거, wf-tree 생성 시점 |
| 2026-10-26 | `20261026-approval-gate` 상태 awaiting-approval → in-progress(v1 승인, plan.md 작성) | wf-implement §3.2 |
| 2026-10-26 | `20261026-approval-gate` 행 제거(완료 보고 종결, 2026-10-26 01:20), 트리 재생성 | wf-implement §7, wf-tree 생성 시점 |
| 2026-10-26 | `20261026-design-questions` 행 추가(wf-design 착수, 작업 기록 시작 — v2 설계 사이클 A), 트리 재생성 | wf-implement §7 포트폴리오 행의 추가·제거, wf-tree 생성 시점 |
| 2026-10-26 | `20261026-design-questions` 상태 awaiting-approval → in-progress(v1 승인, plan.md 작성), 트리 재생성 | wf-implement §3.2 |
| 2026-10-26 | `20261026-design-questions` 행 제거(완료 보고 종결, 2026-10-26 08:49), 트리 재생성 | wf-implement §7, wf-tree 생성 시점 |
| 2026-10-26 | `20261026-component-deps` 행 추가(wf-design 착수, 작업 기록 시작 — v2 설계 사이클 C), 트리 재생성 | wf-implement §7 포트폴리오 행의 추가·제거, wf-tree 생성 시점 |
| 2026-10-26 | `20261026-component-deps` 상태 in-progress → awaiting-approval(승인 요청) | wf-design §8 |
| 2026-10-27 | `20261026-component-deps` 상태 awaiting-approval → in-progress(v1 승인, 계획 작성) | wf-design §8, wf-implement §3.2 |
| 2026-10-27 | `20261026-component-deps` 행 제거(완료 보고 종결, 2026-10-27 01:10), 트리 재생성 | wf-implement §7, wf-tree 생성 시점 |
| 2026-10-28 | `20261028-legacy-onboarding` 행 제거(완료 보고 종결, 2026-10-28 01:49) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-29 | `20261029-legacy-cleanup` 행 추가(wf-design 착수, 작업 기록 시작 — v2 레거시 묶음 ②) | wf-implement §7 포트폴리오 행의 추가·제거 |
| 2026-10-29 | `20261029-legacy-cleanup` 상태 in-progress → awaiting-approval(승인 요청) | wf-design §8 |
| 2026-10-29 | `20261029-legacy-cleanup` 상태 awaiting-approval → in-progress(v1 승인, ADR-024 approved, 계획 작성 대기) | wf-design §8, wf-implement §3.2 |

## 인계

- 다음 단계 또는 워크플로우: 각 작업의 작업 기록 인계 절
- 시작 조건: 없음
- 입력 문서와 기준선: 작업 목록의 `계획·기록` 열
- 완료된 항목: 해당 없음(완료 작업은 행을 제거)
- 미완료 항목: 작업 목록 전체
- 차단 요인: 없음
- 다음 행동: 작업 목록의 `다음 행동` 열

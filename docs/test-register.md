# REGISTER-llm-workflow: 테스트 대장 — 저장소 현행 회귀 테스트

> 문서 유형: `test-register`
> 작업 ID: `N/A — 저장소 관통 현행 문서(작업 상위 단위). 신설은 [20261009-test-lifecycle](./work/20261009-test-lifecycle/plan.md) TASK-04`
> 상태: `in-progress`
> 기준선: `N/A — 현행 문서. 행의 등록·전이는 [wf-implement 검증 시점·실행 집합·대장 전이](../skills/wf-implement/references/verification-depth.md)가 결정`
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [wf-implement 작업 기록과 저장 위치](../skills/wf-implement/SKILL.md#7-작업-기록과-저장-위치), [wf-doc 테스트 대장 템플릿](../skills/wf-doc/references/templates.md#테스트-대장-test-register), [PLAN-20261009-test-lifecycle](./work/20261009-test-lifecycle/plan.md), [ST-llm-workflow](./status.md)

## 요약

- 목적: 이 저장소의 회귀 테스트 묶음을 한 표로 두고, 각 묶음의 보호 스코프·상태·마지막 성공(일시·SHA)과 재정비 관문의 결과를 누적한다. 완료 작업의 work-log는 동결되므로 전이의 정본은 이 문서다.
- 현재 결론 또는 상태: 신설(2026-10-09). `유지` 2행(TST-01·02), `격리` 1행(TST-03, 실행 환경 원인). 재정비 관문 1회(2026-10-09 통합, 변경 없음). `유지` 행 SHA는 clean 커밋 `7395a99`.
- 다음 행동: 다음 작업의 통합·재개 시 `유지` 행 전량 실행. TST-03 격리 해제는 [작업 기록 후속 작업](./work/20261009-test-lifecycle/work-log.md#후속-작업).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | related | [wf-implement 작업 기록과 저장 위치](../skills/wf-implement/SKILL.md#7-작업-기록과-저장-위치) | §7 테스트 대장 | 생성·갱신 시점의 소유자. 스킬 본문이라 역방향 링크는 §7의 경로 표로 갈음 |
| input | related | [wf-doc 테스트 대장 템플릿](../skills/wf-doc/references/templates.md#테스트-대장-test-register) | document | 형식의 정본 |
| input | implementation | [PLAN-20261009-test-lifecycle](./work/20261009-test-lifecycle/plan.md) | TASK-04 | 이 문서를 신설한 작업 |
| input | related | [WORK-20260809-claude-hooks](./work/20260809-claude-hooks/work-log.md) | document | TST-01 발행 작업(완료·동결, 역방향 링크 없음) |
| input | related | [PLAN-20261009-worklog-diet](./work/20261009-worklog-diet/plan.md) | document | TST-02 발행 작업, TST-01의 T03b 확장(DCR-007). 완료·동결, 역방향 링크 없음 |
| input | related | [WORK-20260809-dev-briefing](./work/20260809-dev-briefing/work-log.md) | document | TST-03 발행 작업(완료·동결, 역방향 링크 없음) |
| output | related | [WORK-20261009-test-lifecycle: 테스트 대장 변경](./work/20261009-test-lifecycle/work-log.md#테스트-대장-변경) | 테스트 대장 변경 | 신설 등록과 첫 재정비 관문 제안 |

## 대장

| ID | 테스트·명령 | 보호 스코프 | 크기 | 발행 작업 | 상태 | 마지막 성공 (일시 · SHA) | 비고 |
|---|---|---|---|---|---|---|---|
| TST-01 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1` (저장소 루트) | `setup/hooks/*.ps1`, `setup/hooks/messages/`, 훅 설치·SessionStart·임계·post-compact 동작(T01~T21, 22건) | medium | [20260809-claude-hooks](./work/20260809-claude-hooks/work-log.md) | 유지 | 2026-10-09 18:27 · 7395a99 | T03b는 [20261009-worklog-diet](./work/20261009-worklog-diet/plan.md) DCR-007이 추가. 같은 SHA 2회 통과(계획 §3.1 재확인 16:15 + TASK-04 16:38, 통합 16:42 재확인). 커밋 `7395a99` clean 재실행 통과(18:27)로 SHA 갱신 |
| TST-02 | `python -m pytest skills/wf-doc/scripts/tests -q` (저장소 루트) | `skills/wf-doc/scripts/lint_worklog.py`, 합본 work-log H2 8개·수행 기록 H3·인계 필드·`docs/status.md` 행 정합(L1~L8, 33건) | small | [20261009-worklog-diet](./work/20261009-worklog-diet/plan.md) | 유지 | 2026-10-09 18:27 · 7395a99 | 같은 SHA 2회 통과(계획 §3.1 재확인 16:15 + TASK-04 16:38, 통합 16:42 재확인). 커밋 `7395a99` clean 재실행 통과(18:27)로 SHA 갱신 |
| TST-03 | `python docs/presentation/tests/test_make_pptx.py` (저장소 루트) | `docs/presentation/make_pptx.py` 파싱·빌드·검증·디자인 적용(8건) | medium | [20260809-dev-briefing](./work/20260809-dev-briefing/work-log.md) | 격리(환경, 20261009-test-lifecycle 후속 작업) | 없음 — 이 대장 신설 이후 전체 통과 기록 없음 | 3/8 통과. 5건 `ModuleNotFoundError: No module named 'pptx'` — `python-pptx` 미설치 환경에서 통과를 확인할 수 없어 `유지` 진입 조건 미달. 설치 후 같은 SHA 2회 통과 시 `유지`로 전이 |

## 재정비 기록

| 일시 | 시점 | 작업 | 변경 요약 | 승인 |
|---|---|---|---|---|
| 2026-10-09 16:42 | 통합 | [20261009-test-lifecycle](./work/20261009-test-lifecycle/work-log.md#테스트-대장-변경) | 변경 없음 — Breaking 0 · Stale 0 · Missing 0(새 형식의 린트 검사는 NFR-03으로 범위 밖, 후속 후보). 폐기·병합 후보 0 | 완료 보고 관문(변경 없음 보고) |

## 변경 이력

| 날짜 | 사건 | 근거 |
|---|---|---|
| 2026-10-09 | 최초 생성. 자산 3묶음 등록 — TST-01·02 `유지`, TST-03 `격리(환경)`. 첫 재정비 관문 기록(통합, 변경 없음) | [REQ-DESIGN-test-lifecycle v1](./work/20261009-test-lifecycle/req-design.md) FR-04·FR-10, DES-03·DES-09; [PLAN-20261009-test-lifecycle](./work/20261009-test-lifecycle/plan.md) TASK-04 |
| 2026-10-09 | TST-01·02 마지막 성공을 clean 커밋 `7395a99`(18:27 재실행 22/22·33/33)로 갱신 | [작업 기록 후속 작업](./work/20261009-test-lifecycle/work-log.md#후속-작업) 1항, wf-implement §3.4 3튜플(워킹트리 clean) |

# TESTMAP-20260920-regression-tier: 테스트 맵

> 문서 유형: `test-map`
> 작업 ID: `20260920-regression-tier`
> 상태: `completed`
> 기준선: `v1` ([REQ-DESIGN-regression-tier](./req-design.md), 2026-09-20 승인)
> 작성일: 2026-09-20
> 최종 갱신: 2026-09-20
> 관련 문서: [PLAN-llm-workflow: 구현 계획](../../plan.md), [WORK-20260920-regression-tier: 작업 기록](./work-log.md)

## 요약

- 목적: 이 작업이 수정하는 파일의 관련 테스트를 식별한다. 변경 대상이 전부 산문(스킬 문서·템플릿)이라 자동 테스트는 없으며, 이 문서는 신설 `test-map` 유형의 자기 적용이다.
- 현재 결론 또는 상태: 변경 예정 파일 5개 + 신설 1개 전부 관련 테스트 없음. 검증은 통독·대조·스크립트 실행의 후행 검증으로 대체([작업 기록 검증 절](./work-log.md#검증)).
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-regression-tier](./req-design.md) | FR-04, DES-02 | 맵 생성 규정의 적용 대상 |
| output | related | [PLAN-llm-workflow](../../plan.md) | TASK-30~36 `관련 테스트` 필드 | 전부 `없음(산문)` |
| output | related | [WORK-20260920-regression-tier](./work-log.md) | 회귀 의무 목록, 검증 | 유지할 테스트 없음 |

## 생성 정보

- 생성 방법: 명명 규칙 + import grep — `tests/` 디렉터리와 `test_*.py`·`*.ps1` 테스트 하니스에서 변경 파일명 검색
- 생성 시점과 기준 커밋: 2026-09-20 15:05 · `c4cde3f` (워킹트리에 이 작업의 미커밋 변경 포함)

## 매핑

| 변경 예정 파일 | 관련 테스트 | 실행 명령 | 근거 | 사전 실행 (SHA · 결과) |
|---|---|---|---|---|
| skills/wf-implement/SKILL.md | 없음 | — | `grep -rl "wf-implement" setup/hooks/tests docs/presentation/tests` 결과 없음 — 산문 스킬 문서 | — (통독 검증) |
| skills/wf-implement/references/verification-depth.md | 없음 | — | 신설 파일, 산문 | — (통독 검증) |
| skills/wf-doc/SKILL.md | 없음 | — | 산문 스킬 문서 | — (통독 검증) |
| skills/wf-doc/references/templates.md | 없음 | — | 산문 템플릿 | — (통독 검증) |
| docs/plan.md | 없음 | — | 계획 문서. 트리는 목록에서 재생성 | — (규칙 대조) |
| docs/decisions.md | 없음 | — | 등록부 | — (통독) |

이 저장소의 자동 테스트 2종(`setup/hooks/tests/run-tests.ps1` T01~T21, `docs/presentation/tests/test_make_pptx.py` 8개)은 이 작업의 변경 파일을 참조하지 않으므로 관련 테스트가 아니다. 통합(§3.6)의 전체 스위트 1회 실행 의무는 이 작업에 자동 테스트가 없어 적용 대상이 없으며, 사유를 [작업 기록](./work-log.md#검증)에 남긴다.

## 맵 누락 기록

| 발견 시점 | 실패한 테스트 | 원인 파일 | 누락 원인 |
|---|---|---|---|
| — | — | — | 없음 |

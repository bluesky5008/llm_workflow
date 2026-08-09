# PLAN-llm-workflow: 구현 계획

> 문서 유형: `plan`
> 작업 ID: `20260809-claude-hooks`
> 상태: `completed`
> 기준선: `v1` ([REQ](./requirements.md)·[DESIGN](./design.md), 2026-08-09 승인)
> 작성일: 2026-08-09
> 최종 갱신: 2026-08-09
> 관련 문서: [DESIGN-llm-workflow: 설계](./design.md), [WORK-20260809-claude-hooks: 작업 기록](./work/20260809-claude-hooks/work-log.md)

## 요약

- 목적: 승인된 C층 훅 설계(DES-01~05)를 TDD로 구현·검증·통합한다.
- 현재 결론 또는 상태: TASK-01~06 완료. 테스트 21/21 성공, 실설치 완료. 실세션 관찰 2건은 [작업 기록 검증](./work/20260809-claude-hooks/work-log.md#검증)에 미수행으로 기록.
- 다음 행동: 없음 — 후속 작업은 작업 기록의 완료 보고 참조.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-llm-workflow: 요구사항](./requirements.md) | FR-01~05, AC-01~06 | 승인 기준선 v1 |
| input | baseline | [DESIGN-llm-workflow: 설계](./design.md) | DES-01~05 | 승인 기준선 v1 |
| output | implementation | [WORK-20260809-claude-hooks: 작업 기록](./work/20260809-claude-hooks/work-log.md) | document | 진행 상태·검증의 정본 |

## 작업 목록

- [x] TASK-01 — 훅 테스트 하니스 `setup/hooks/tests/run-tests.ps1` 작성. 견본 stdin JSON을 각 스크립트에 파이프해 stdout 계약을 검사한다. 선행 테스트(Red): 대상 스크립트 부재로 전 케이스 실패를 확인한다. 커버: AC-01, AC-02, AC-04, AC-05 상당 케이스.
- [x] TASK-02 — 공용 라이브러리 `wf-common.ps1`(입력 파싱·가드·work-log 스캔·상태 파일·UTF-8 출력)와 `wf-session-start.ps1` + `messages/resume.md` 구현 (DES-01, DES-05). 완료 조건: TASK-01의 session-start 케이스 Green.
- [x] TASK-03 — `wf-context-threshold.ps1` + `messages/threshold.md` 구현 (DES-02). 완료 조건: threshold 케이스(미만 무주입·초과 주입·재경고 억제·오류 fail-open) Green.
- [x] TASK-04 — `wf-post-compact.ps1` + `messages/post-compact.md` 구현 (DES-03). 완료 조건: post-compact 케이스(주입·기준점 재설정·가드) Green.
- [x] TASK-05 — `install-hooks.ps1` 병합 함수 + `setup_claude.ps1` 통합 (DES-04). 선행 테스트: 신규 생성·멱등 재실행·무관 설정 보존·경로 재지정 케이스를 TASK-01 하니스에 추가 후 Red→Green. 완료 조건: AC-03 상당 케이스 Green.
- [x] TASK-06 — README 설치·롤백 안내, 실제 사용자 환경 설치 실행, 실세션 검증 항목(AC-01·AC-06) 정리와 통합 확인.

의존성: TASK-01 → TASK-02(공용 라이브러리) → TASK-03·TASK-04(병렬 가능) → TASK-05 → TASK-06.

위험 높은 변경: TASK-05가 사용자 실 `settings.json`을 수정한다 — 병합 함수를 임시 경로 테스트로 먼저 검증한 뒤 실행한다.

## 검증 계획

각 AC의 검증 방법은 [설계 검증 전략](./design.md#검증-전략)을 따른다. 스크립트 계약은 테스트 하니스로, 설치는 임시 경로 테스트 후 실설치로, AC-01·AC-06의 실세션 관찰은 다음 새 세션에서 수행한다(이번 세션에서 불가한 항목은 미수행으로 보고).

## 인계

작업 기록 [WORK-20260809-claude-hooks](./work/20260809-claude-hooks/work-log.md)의 인계 절이 정본이다.

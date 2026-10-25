# PLAN-20261025-regression-guard: 구현 계획 — 회귀 보호의 강제

> 문서 유형: `plan`
> 작업 ID: `20261025-regression-guard`
> 상태: `completed`
> 기준선: [REQ-DESIGN-regression-guard](./req-design.md) `v1` (승인일 2026-10-25), [REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md) `v4`
> 작성일: 2026-10-25
> 최종 갱신: 2026-10-25
> 관련 문서: [WORK-20261025-regression-guard: 작업 기록](./work-log.md), [ADR-014](./ADR-014-회귀-보호-훅-강제-방식.md), [DCR-015](./DCR-015-C층-회귀-보호-훅-추가.md), [REGISTER-llm-workflow](../../test-register.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 승인된 v1(FR-01~08)을 8개 TASK로 구현한다. 순서는 R-01(대장 스키마)부터 — 이후 모든 판독기가 그 스키마를 읽는다.
- 현재 결론 또는 상태: TASK-01~08 완료(8/8).
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-regression-guard](./req-design.md) | FR-01~08, AC-01~10, DES-01~08 | v1 |
| input | baseline | [DESIGN-llm-workflow](../../design.md#컴포넌트와-책임) | DES-04·06·07 | v4 |
| input | decision | [ADR-014](./ADR-014-회귀-보호-훅-강제-방식.md), [DCR-015](./DCR-015-C층-회귀-보호-훅-추가.md) | document | approved |
| output | implementation | [WORK-20261025-regression-guard](./work-log.md) | 수행 기록 | TASK별 결과 |

## 기준선

- 관련 요구사항: req-design FR-01~08·NFR-01~06, REQ-llm-workflow FR-06·07·NFR-01 예외
- 관련 설계: req-design DES-01~08, DESIGN-llm-workflow DES-04·06·07
- 관련 ADR·DCR: [ADR-014](./ADR-014-회귀-보호-훅-강제-방식.md), [DCR-015](./DCR-015-C층-회귀-보호-훅-추가.md)

## 작업 정의

- 목표: 회귀 보호 규칙 3종의 기계 강제(판정 B층 + Claude 어댑터)와 충돌 출구·Red 증거 규칙.
- 범위: req-design [범위 포함](./req-design.md#포함).
- 범위 밖: req-design [제외](./req-design.md#제외) — Codex·SEMCo-Work 어댑터, pre-commit 설치, R-06~R-16.
- 가정: §3.1 재확인(2026-10-25 22:27) — HEAD `0d2279c`+미커밋(문서만), `유지` 4행 전량 통과(TST-01 29/29 이 세션 PS 5.1, TST-02 49, TST-04 16, TST-05 13; pytest는 사용자 승인으로 Python 3.14에 설치). 이 세션에서 PS 5.1 실행이 가능하므로 TST-01 Red·Green도 직접 수행한다.
- 위험: req-design RISK-01~10. 계획 고유 — (a) TASK-03 이후 이 작업 기록 자신이 `Red` 검사 대상(TASK-01·02 항목에도 `Red` 기입), (b) 기존 T18~T21은 SessionStart·PostToolUse 개수만 단언하므로 등록 추가로 깨지지 않을 것으로 보나, 깨지면 Breaking으로 기록하고 수정하지 않는다(재정비 관문).

## 계획 트리

<!-- generated: 2026-10-25 23:32 — scripts/render.py --view all -->

```text
[작업] 20261025-regression-guard — 회귀 보호의 강제 ... completed (8/8)
├─ [✓] 대장 스키마 — `테스트 파일` 열과 마지막 성공 셀 정규화 (R-01) (TASK-01) ............ 2026-10-25 22:32
├─ [✓] 하네스 중립 판정 스크립트 `regression_guard.py` (R-03 핵심, 대장 축소) (TASK-02) ... depends: TASK-01  2026-10-25 22:37
├─ [✓] `Red` 증거 필드 — 템플릿과 린트 (R-05) (TASK-03) ................................... depends: TASK-01  2026-10-25 22:56
├─ [✓] 명세·테스트 충돌 출구 (R-04) (TASK-04) ............................................. 2026-10-25 23:02
├─ [✓] Claude 편집 확인 훅 `wf-test-guard.ps1` (R-02) (TASK-05) ........................... depends: TASK-01, TASK-02  2026-10-25 23:08
├─ [✓] Claude 종료 래퍼 `wf-stop-gate.ps1` (R-03 어댑터) (TASK-06) ........................ depends: TASK-02, TASK-05  2026-10-25 23:11
├─ [✓] 설치 등록과 README (DES-04) (TASK-07) .............................................. depends: TASK-05, TASK-06  2026-10-25 23:16
└─ [✓] 통합 — 대장 등록, 실설치·실세션 관찰, 재정비 관문 (TASK-08) ........................ depends: TASK-01~07  2026-10-25 23:28
```

## 작업 목록

### TASK-01: 대장 스키마 — `테스트 파일` 열과 마지막 성공 셀 정규화 (R-01)

- 상태: completed
- 완료: 2026-10-25 22:32
- 상위: 없음
- 목표: 템플릿과 현행 대장이 DES-01·02 형식을 갖는다.
- 관련 요구사항과 설계: FR-01·02, DES-01·02, AC-01·02
- 변경 대상: `skills/wf-doc/references/templates.md`(대장 표·노트), `docs/test-register.md`(5행 소급, TST-01 셀 정규화 — 서술은 비고로)
- 의존성: 없음
- 위험: RISK-04(경로·glob 불일치)
- 검증 방법: 문서 변경이라 TDD 비대상(`Red: 해당 없음`). AC-02는 각 행 `테스트 파일` glob을 저장소에서 확장해 1개 이상 실재하는지, 마지막 성공 셀이 DES-02 정규식에 맞는지 일회성 스크립트로 확인. `lint_skill.py` 0 오류.
- 완료 조건: AC-01·02 충족.

### TASK-02: 하네스 중립 판정 스크립트 `regression_guard.py` (R-03 핵심, 대장 축소)

- 상태: completed
- 완료: 2026-10-25 22:37
- 상위: 없음
- 목표: DES-04 계약(exit 0/1/2, `TST-NN: <사유> <파일>`)과 DES-08 판독 규칙을 구현한다.
- 관련 요구사항과 설계: FR-04·08, NFR-03·04·05, DES-04·08, AC-04(핵심)·AC-05·AC-10
- 변경 대상: `skills/wf-doc/scripts/regression_guard.py`(신설), `skills/wf-doc/scripts/tests/test_regression_guard.py`(신설), `skills/wf-doc/scripts/tests/fixtures/test-register.sample.md`(공유 견본)
- 의존성: TASK-01(스키마)
- 위험: RISK-08(판독 불일치 — 견본으로 고정), Windows 경로·git 출력 인코딩
- 검증 방법: TDD. Red 먼저 — 임시 git 저장소 픽스처로 (1) 대장 부재 exit 0, (2) `유지` 테스트 파일 변경·기록 없음 exit 1, (3) 기록 있으면 exit 0, (4) 격리 전환·삭제·`테스트 파일` 변경 위반, (5) 닫힌 work-log의 기록은 무효, (6) 표 판독 불가 exit 2, (7) 견본 판독 결과. `lint_worklog.py`의 `CLOSED`를 재사용(import). 명령 `python -m pytest skills/wf-doc/scripts/tests -q`(TST-02).
- 완료 조건: 새 케이스 Red→Green, TST-02 기존 49 통과.

### TASK-03: `Red` 증거 필드 — 템플릿과 린트 (R-05)

- 상태: completed
- 완료: 2026-10-25 22:56
- 상위: 없음
- 목표: `TASK-` 항목의 `Red` 필드 필수·형식 검사.
- 관련 요구사항과 설계: FR-06, DES-06, AC-07
- 변경 대상: `skills/wf-doc/references/templates.md`(수행 기록 항목), `skills/wf-doc/scripts/lint_worklog.py`(L3, 항목 상한 8→9행), `skills/wf-doc/scripts/tests/test_lint_worklog.py`, 필요 시 `references/worklog-style.md`
- 의존성: TASK-01(같은 파일 templates.md)
- 위험: 열린 작업 기록이 이 기록 하나뿐인지 확인(다른 열린 기록의 TASK 항목이 새 오류를 내면 기록에 남김)
- 검증 방법: TDD. Red — 누락·형식 위반·`해당 없음` 통과·비 TASK 미검사 4케이스. 이후 이 작업 기록에 린트 0 오류.
- 완료 조건: AC-07 충족, TST-02 통과.

### TASK-04: 명세·테스트 충돌 출구 (R-04)

- 상태: completed
- 완료: 2026-10-25 23:02
- 상위: 없음
- 목표: `verification-depth.md` §6 신설, 주의 ④에서 링크.
- 관련 요구사항과 설계: FR-05, NFR-01, DES-05, AC-06
- 변경 대상: `skills/wf-implement/references/verification-depth.md`, `skills/wf-implement/SKILL.md`(주의 ④ 링크 + 같은 절 상쇄 축약)
- 의존성: 없음
- 위험: RISK-07(어절 여유 4)
- 검증 방법: 문서 변경이라 TDD 비대상. `lint_skill.py` 0 오류(K3 상한 2,850)와 어절 측정, 통독.
- 완료 조건: AC-06, K3 통과.

### TASK-05: Claude 편집 확인 훅 `wf-test-guard.ps1` (R-02)

- 상태: completed
- 완료: 2026-10-25 23:08
- 상위: 없음
- 목표: DESIGN-llm-workflow DES-06.
- 관련 요구사항과 설계: req-design FR-03, DES-03·07·08; REQ-llm-workflow FR-06, AC-07·09
- 변경 대상: `setup/hooks/wf-test-guard.ps1`(신설), `setup/hooks/wf-common.ps1`(대장 판독·경로 정규화·설정 경로 상수), `setup/hooks/messages/test-guard.md`, `setup/hooks/tests/run-tests.ps1`(T29~)
- 의존성: TASK-01(스키마), TASK-02(공유 견본)
- 위험: RISK-05(한글 `유지` — 코드포인트), RISK-03(`ask`의 자동 승인 모드 동작 — 실측은 TASK-08)
- 검증 방법: TDD. Red — 견본 대장·stdin JSON으로 `유지` 파일 ask, 설정 파일 ask, 미등록·대장 자체 무출력, 열 부재 무출력, 표 판독 불가 ask(`guard=error`), 대장 부재 무출력, 견본 판독 결과가 TASK-02와 일치. 명령은 TST-01.
- 완료 조건: 새 케이스 Red→Green, 기존 29 통과.

### TASK-06: Claude 종료 래퍼 `wf-stop-gate.ps1` (R-03 어댑터)

- 상태: completed
- 완료: 2026-10-25 23:11
- 상위: 없음
- 목표: DESIGN-llm-workflow DES-07.
- 관련 요구사항과 설계: req-design FR-04, DES-04; REQ-llm-workflow FR-07, AC-08·09
- 변경 대상: `setup/hooks/wf-stop-gate.ps1`(신설), `setup/hooks/messages/stop-gate.md`, `setup/hooks/tests/run-tests.ps1`
- 의존성: TASK-02(스크립트 계약), TASK-05(wf-common·러너 같은 파일)
- 위험: RISK-06·09(Python 호출 지연·부재)
- 검증 방법: TDD. Red — 판정 스크립트 경로를 가짜 스크립트(exit 0/1/2)로 대체 가능하게 하고 block·무출력·`stop_hook_active` 통과·Python 부재 통과·대장 부재 통과를 검사. 실제 스크립트로 1회 통합 케이스.
- 완료 조건: 새 케이스 Red→Green, 기존 통과.

### TASK-07: 설치 등록과 README (DES-04)

- 상태: completed
- 완료: 2026-10-25 23:16
- 상위: 없음
- 목표: `Install-WfHooks`가 PreToolUse·Stop을 멱등 등록, README 훅 설명 5종과 해제 방법.
- 관련 요구사항과 설계: REQ-llm-workflow FR-04, DESIGN DES-04, NFR-01
- 변경 대상: `setup/hooks/install-hooks.ps1`, `setup/hooks/tests/run-tests.ps1`(등록 5종·재실행 멱등 새 케이스), `README.md`
- 의존성: TASK-05, TASK-06
- 위험: 계획 위험 (b) — T18~T21이 깨지면 수정하지 않고 Breaking 기록
- 검증 방법: TDD. Red — 새 케이스(PreToolUse 1·Stop 1 등록, 재실행 무중복). 기존 T18~T21 통과 확인.
- 완료 조건: 새 케이스 통과, 기존 29 통과.

### TASK-08: 통합 — 대장 등록, 실설치·실세션 관찰, 재정비 관문

- 상태: completed
- 완료: 2026-10-25 23:28
- 상위: 없음
- 목표: 완료 조건 전체와 AC-03(실세션)·AC-08·09 확인.
- 관련 요구사항과 설계: AC-03·08·09, NFR-01·02, ADR-014 후속 작업
- 변경 대상: `docs/test-register.md`(TST-01·02 보호 스코프 확장, 마지막 성공), 작업 기록, `docs/status.md`
- 의존성: TASK-01~07
- 위험: RISK-03 — 자동 승인 모드에서 `ask` 미도달이면 그 모드만 `deny` 적용(ADR-014 결정 1, 경미한 변경으로 기록)
- 검증 방법: `lint_skill.py`·`lint_worklog.py` 0 오류, 전체 스위트 1회 + `유지` 전량 같은 SHA 2회, `setup_claude.ps1` 실설치 후 사용자와 실세션 관찰(`유지` 파일 편집 시도 → 확인 프롬프트, 자동 승인 모드 1회, 셸 편집 후 종료 차단 1회), 재정비 관문(Breaking·Stale·Missing).
- 완료 조건: wf-implement §5 전 항목, 완료 보고.

## 검증 계획

- 자동: TST-01(PS 5.1, 이 세션), TST-02(pytest). 새 테스트는 기존 행의 보호 스코프 확장으로 등록(새 행 없음 — 같은 명령이 실행).
- AC 대응: AC-01·02 TASK-01, AC-04·05·10 TASK-02·05·06, AC-06 TASK-04, AC-07 TASK-03, AC-03 TASK-05+08, AC-08·09 TASK-08.
- 수동: 실세션 관찰(TASK-08), 통독.

## 마이그레이션과 롤백

- 마이그레이션: `setup_claude.ps1` 재실행(TASK-08, 사용자 실행 또는 승인 후).
- 롤백: `git revert` 후 `setup_claude.ps1` 재실행, 또는 settings.json의 `wf-test-guard`·`wf-stop-gate` 항목 삭제.

## 인계

- 다음 단계 또는 워크플로우: 없음
- 시작 조건: 충족
- 입력 문서와 기준선: 위 기준선
- 완료된 항목: §3.1 재확인, 계획, TASK-01~08
- 미완료 항목: 없음
- 차단 요인: 없음
- 다음 행동: 없음

# WORK-20261025-regression-guard: 작업 기록 — 회귀 보호의 강제

> 문서 유형: `work-log, verification, completion`
> 작업 ID: `20261025-regression-guard`
> 상태: `in-progress`
> 기준선: `[REQ-DESIGN-regression-guard](./req-design.md) v1` (승인일 2026-10-25), C층 REQ·DESIGN-llm-workflow v4
> 작성일: 2026-10-25
> 최종 갱신: 2026-10-25
> 관련 문서: [ST-llm-workflow](../../status.md), [REQ-DESIGN-regression-guard](./req-design.md), [ADR-014](./ADR-014-회귀-보호-훅-강제-방식.md), [DCR-015](./DCR-015-C층-회귀-보호-훅-추가.md), [REGISTER-llm-workflow](../../test-register.md), [테스트 한정 액션 아이템](../../research/20261025-aidlc-trends/04_test_action_items.md)

## 요약

- 목적: v2 테스트 사이클 1(액션 아이템 R-01~R-05)의 wf-design·wf-implement 진행을 기록한다.
- 현재 결론 또는 상태: v1 승인(2026-10-25, Q-02 3층 구조). [PLAN](./plan.md) TASK-01~07 완료(7/8).
- 다음 행동: TASK-08. 상세는 [인계](#인계).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | related | [ST-llm-workflow](../../status.md) | 작업 목록 | 이 작업의 행 |
| input | baseline | [REQ-DESIGN-regression-guard](./req-design.md) | document | v1 승인(2026-10-25) |
| output | decision | [ADR-014](./ADR-014-회귀-보호-훅-강제-방식.md), [DCR-015](./DCR-015-C층-회귀-보호-훅-추가.md) | document | `approved`(2026-10-25). 등록부 행 |
| input | implementation | [PLAN-20261025-regression-guard](./plan.md) | TASK-01~08 | 구현 계획 |
| input | related | [테스트 한정 액션 아이템](../../research/20261025-aidlc-trends/04_test_action_items.md) | R-01~R-05 | 조사 입력 |

## 기준선과 현재 계획

- 기준선: [REQ-DESIGN-regression-guard](./req-design.md) v1(2026-10-25), [REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md) v4
- 계획: [PLAN-20261025-regression-guard](./plan.md) — TASK-01~08, 7/8 완료

## 수행 기록

### 2026-10-25 — 착수와 §4.1 조사

- 발견 사항: 대장에 테스트 소스 파일 열이 없고 TST-01 마지막 성공 셀이 형식 밖. wf-implement 본문 여유 4어절. 훅 문서상 PreToolUse `ask`·`deny`, Stop `block`·`stop_hook_active` 사용 가능, `ask`의 자동 승인 모드 동작은 명시 없음.
- 결정과 이유: 스킬·템플릿·린트는 req-design, 훅은 C층 기준선 변경이라 DCR-015로 분리(선례 worklog-diet). 강제 방식은 ADR-014 — 정당한 수정이 있어 차단 대신 확인.
- 검증: 없음 — 설계 단계. 린트는 승인 요청 전에 실행해 결과를 승인 관문에 보고.
- 결과: 완료 — 2026-10-25 22:30

### 2026-10-25 — 승인 관문 응답과 Q-02 재설계

- 발견 사항: 사용자 응답 Q-01 A·Q-03 B·Q-04 A(승인 의사). Q-02는 사내 에이전트(SEMCo-Work)까지 고려한 안을 요청. 원안 B와 Stop 판정은 Claude 전용이고, 대장 `유지` 행 축소가 보호 해제 경로임을 확인.
- 결정과 이유: 3층 구조(사용자 채택) — 판정은 하네스 중립 B층 스크립트, 설정 파일은 어댑터 선언, 편집 확인은 하네스별. FR-08 신설. 3문서 반영.
- 검증: `lint_worklog.py` 이 기록·status.md — 아래 결과 참조.
- 결과: 완료 — 반영본 사용자 승인, req-design v1·ADR-014·DCR-015 approved, REQ·DESIGN-llm-workflow v4, decisions·status 갱신

### 2026-10-25 — wf-implement §3.1 재확인과 계획 수립

- 발견 사항: HEAD `0d2279c`+미커밋(문서만). 이 세션에서 PS 5.1 실행 가능(TST-01 직접 수행). pytest 미설치 → 사용자 승인으로 Python 3.14에 `pip install --user pytest`.
- 결정과 이유: 8 TASK, R-01부터. 새 테스트는 TST-01·02 보호 스코프 확장(같은 명령). TASK-03 이후 이 기록 TASK 항목에 `Red` 필수.
- 검증: `유지` 전량 22:27 — TST-01 29/29, TST-02 49, TST-04 16, TST-05 13(모두 `0d2279c`+dirty). 트리 render.py.
- 결과: 완료 — 2026-10-25 22:35

### 2026-10-25 — TASK-01

- 발견 사항: 직전 세션 기록 시각(22:35·22:36)이 실제 시계보다 앞섬(파일 수정 22:29) — 이 항목부터 실측 시각. TST-01 셀의 `HEAD`는 당시 `6792a7d`(커밋 일시로 확인).
- 결정과 이유: TST-01 셀은 기존 사실을 정규화(서술·직전 clean `a38ed25`는 비고로, DES-02 예시 `7395a99`는 10-09 값이라 미채택). TST-02·05는 폴더 glob(새 테스트 파일 자동 포함).
- Red: 해당 없음 — 문서 변경
- 검증: AC-02 일회성 스크립트 PASS(5행, glob 실재·셀 정규식), `lint_skill.py` 0 오류
- 결과: 완료 — 2026-10-25 22:32

### 2026-10-25 — TASK-02

- 발견 사항: 실저장소 실행이 TST-01 위반 1건 — 셀 `6792a7d+dirty`의 미커밋분이 `0d2279c`로 커밋됨. 사양대로의 동작이라 22:27 재실행으로 셀 갱신 후 exit 0.
- 결정과 이유: `### 테스트 대장 변경` 절 안의 ID만 인정. HEAD 대장에 `테스트 파일` 열이 없으면 값 비교 생략(스키마 도입 전 오탐 방지). 견본에 `## 판독 기대` 표 — TASK-05가 같은 기대값을 읽음.
- Red: `python -m pytest skills/wf-doc/scripts/tests -q` · 0d2279c+dirty · 스텁(exit 0·빈 판독)에서 9 failed(22:34)
- 검증: `python -m pytest skills/wf-doc/scripts/tests -q` 63 passed(22:35)
- 결과: 완료 — 2026-10-25 22:37

### 2026-10-25 — TASK-03

- 발견 사항: 견본 `ENTRY`가 `Red` 없는 TASK 항목이라 통과 단언 다수가 깨짐 → FR-05 충돌 출구, 사용자 판정 (a) Breaking(22:40). 22:43 이 기록이 외부 저장으로 옛 판본(승인 대기)에 덮임 → 사용자 지시로 대화 기록에서 복구.
- 결정과 이유: 견본에 `Red` 1행만 추가(단언 무변경). ` · ` 최대 3분할(이유 안 `·` 허용), SHA 조각 백틱 허용.
- Red: `python -m pytest skills/wf-doc/scripts/tests -q` · 0d2279c+dirty · 9행·`Red` 누락·형식 위반 미검출 3 failed(22:52)
- 검증: `python -m pytest skills/wf-doc/scripts/tests -q` 68 passed(22:53), `lint_skill.py`·`lint_worklog.py` 0 오류
- 결과: 완료 — 2026-10-25 22:56

### 2026-10-25 — TASK-04

- 발견 사항: 계획이 상쇄 문장을 확정하지 않았음(DES-05 "계획 단계에서 확정") — 구현에서 확정. K3는 공백 분할 계수.
- 결정과 이유: 주의 ④ 끝에 `[충돌 출구]` 링크(+2어절), 같은 절 ①의 `별도`(실행 승인이 아니라는 앞 구절과 중복)·③의 `문서`(머리말은 문서 머리말뿐) 삭제(−2) → 2,846 유지. §2 끝에도 §6 포인터 1문장(references라 상한 무관).
- Red: 해당 없음 — 문서 변경
- 검증: `lint_skill.py` 0 오류(wf-implement 2,846어절), `유지` 전량 23:00 — TST-01 29/29, TST-02 68, TST-04 16, TST-05 13(`90af250`+dirty)
- 결과: 완료 — 2026-10-25 23:02

### 2026-10-25 — TASK-05

- 발견 사항: 첫 Green의 T35 실패는 헬퍼 결함(`[string]`이 `$null`→`''`, 빈 대장 생성) — 헬퍼만 수정. 실저장소: `test_lint_skill.py`→TST-02·04, 대장 무출력, 약 300ms.
- 결정과 이유: `Get-WfKeptTestFiles`는 `parse_register`와 같은 규칙. 출력은 `Write-WfJson`으로 공통화. 대장 자체는 판독 전 통과(깨진 대장 수리를 막지 않음). 자동 승인 모드 `deny`는 TASK-08 실측 후(ADR-014 결정 1).
- Red: `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1` · 90af250+dirty · 훅 스크립트 부재로 T29~T37 9 failed(23:04)
- 검증: TST-01 38/38(Green 23:05·전이 23:06), `유지` 전량 23:06(TST-02 68·04 16·05 13), `regression_guard.py .` exit 0
- 결과: 완료 — 2026-10-25 23:08

### 2026-10-25 — TASK-06

- 발견 사항: 실저장소 실행 무출력(TST-01이 `### 테스트 대장 변경`에 기록됨), 약 560ms(PS 기동 + Python). Python 부재 시험은 PATH를 System32로 한정해 재현.
- 결정과 이유: 테스트용 판정 경로 대체는 환경 변수 `CLAUDE_WF_GUARD_SCRIPT`(기존 `CLAUDE_WF_*` 관례). `Process`로 stdout·stderr를 비동기로 읽고 10초 대기(DES-07), stdout UTF-8. 판정 스크립트 부재도 통과.
- Red: `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1` · 90af250+dirty · 래퍼 부재로 T38~T44 7 failed(23:08)
- 검증: TST-01 45/45(Green·전이 23:09), `유지` 전량 23:09(TST-02 68·04 16·05 13), `regression_guard.py .` exit 0
- 결과: 완료 — 2026-10-25 23:11

### 2026-10-25 — TASK-07

- 발견 사항: 첫 Red가 러너 중단(`@($null).Count`=1) — 새 테스트에서 null 제거 후 단언 실패로 재현. T18~T21은 이벤트별 개수 단언이라 무영향(Breaking 없음).
- 결정과 이유: `New-WfEntry`가 빈 매처를 생략(Stop은 매처 없음). RISK-09 완화로 `setup_claude.ps1`이 Python 탐지 결과를 출력(계획 변경 대상 밖, req-design 위험 대응 범위 — 경미). README 훅 5종·회귀 보호만 끄는 방법.
- Red: `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1` · 90af250+dirty · 등록 없음으로 T45·T46 2 failed(23:13)
- 검증: TST-01 47/47(Green·전이 23:14), `유지` 전량 23:14(TST-02 68·04 16·05 13), `setup_claude.ps1` 구문 오류 0(실행은 TASK-08)
- 결과: 완료 — 2026-10-25 23:16

## 설계와 달라진 점

없음 — 경미한 구현 결정(`CLAUDE_WF_GUARD_SCRIPT` 테스트 대체, 설정 파일 사유 `settings`, `setup_claude.ps1` Python 탐지)은 TASK-05~07 수행 기록. 자동 승인 모드 `deny`는 ADR-014 결정 1의 조건(ask 미도달)이 관찰되지 않아 미적용.

## 검증 결과

### 범위와 환경

- 대상 기준선 또는 구현: [REQ-DESIGN-regression-guard](./req-design.md) v1, C층 v4 — TASK-01~08
- 실행 환경: 사용자 PC Windows PS 5.1(훅), Python 3.14(린트·pytest), Claude Code VS Code 확장 실세션(권한 모드 `auto`)
- 제외 항목: `bypassPermissions` 모드의 ask 도달(미관찰 — 남은 위험)

### 결과 요약

- 총계: 10 (성공 10 / 실패 0 / 미수행 0)
- 기준: `90af250` · 워킹트리 dirty(전체 스위트 23:16, `유지` 2회 23:17)
- 명령: `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1` 47/47
- 명령: `python -m pytest skills/wf-doc/scripts/tests skills/wf-tree/scripts/tests -q` 81 passed
- 명령: `python docs/presentation/tests/test_make_pptx.py` 3/8(TST-03 격리, `pptx` 미설치 — 환경, 기존)
- 커버리지: N/A — PS 러너·pytest에 커버리지 도구 미설정
- 산출물: 없음

### 인수 조건별 결과

| 검증 ID | 인수 조건 | 방법·명령 | 결과 | 분류 | 증거 |
|---|---|---|---|---|---|
| VER-01 | AC-01 | 템플릿 통독 | 성공 | — | TASK-01 |
| VER-02 | AC-02 | 일회성 스크립트(glob 실재·셀 정규식) | 성공 | — | TASK-01 |
| VER-03 | AC-03 | TST-01 T29~T37 + 실세션 ① | 성공 | — | 47/47 `90af250`+dirty; transcript `PreToolUse:Edit` ask(TST-05)·승인 23:20 |
| VER-04 | AC-04 | TST-02 + TST-01 T38~T44 + 실세션 ③ | 성공 | — | 68·47 passed; 종료 1회 차단(TST-05) 23:22 |
| VER-05 | AC-05 | TST-01 T35·T42 | 성공 | — | 47/47 |
| VER-06 | AC-06 | `lint_skill.py`, 통독 | 성공 | — | TASK-04, 2,846어절 |
| VER-07 | AC-07 | TST-02 L3 `Red` 5건 | 성공 | — | TASK-03 |
| VER-08 | AC-08 | 린트 2종 + `유지` 같은 상태 2회 | 성공 | — | 0 오류; TST-01 47·TST-02 68 ×2(23:17) |
| VER-09 | AC-09 | `decisions.md`·머리말 대조 | 성공 | — | ADR-014·DCR-015 `approved`, REQ·DESIGN v4 |
| VER-10 | AC-10 | TST-02 | 성공 | — | 68 passed |

### 실패와 미수행 분석

없음.

### 테스트 대장 변경

| 대상 | 현재 상태 → 제안 | 분류·증거 | 유일 검증 여부 | 승인 |
|---|---|---|---|---|
| 대장 스키마 | `테스트 파일` 열 신설·5행 소급, TST-01 셀 정규화·갱신(`0d2279c`+dirty) | TASK-01, AC-02 스크립트 PASS | — | 형식 변경(행 상태 무변경) — 승인 23:26 |
| TST-02 | 유지 → 유지(보호 스코프 확장: `regression_guard.py` 14건, 총 63) | 등록 — 63 passed(22:35, `0d2279c`+dirty) | — | 등록(승인 불요) · 일괄 승인 23:26 |
| TST-02 | 유지 → 유지(`test_lint_worklog.py` 견본 `ENTRY`에 `- Red: 해당 없음 — 견본` 1행, 단언 무변경) | Breaking — FR-06이 정상 항목 정의를 바꿈. FR-05 충돌 출구 사용자 판정 (a)(22:40) | — | 완료 보고 관문 — 승인 23:26 |
| TST-02 | 유지 → 유지(보호 스코프 확장: L3 `Red` 5건, 총 68) | 등록 — 68 passed(22:53, `0d2279c`+dirty) | — | 등록(승인 불요) · 일괄 승인 23:26 |
| TST-01 | 유지 → 유지(보호 스코프 확장: `wf-test-guard.ps1` T29~T37 9건, 총 38) | 등록 — 38/38(23:05·23:06, `90af250`+dirty) | — | 등록(승인 불요) · 일괄 승인 23:26 |
| TST-01 | 유지 → 유지(보호 스코프 확장: `wf-stop-gate.ps1` T38~T44 7건, 총 45) | 등록 — 45/45(23:09, `90af250`+dirty) | — | 등록(승인 불요) · 일괄 승인 23:26 |
| TST-01 | 유지 → 유지(보호 스코프 확장: 설치 등록 T45~T46 2건, 총 47) | 등록 — 47/47(23:14, `90af250`+dirty) | — | 등록(승인 불요) · 일괄 승인 23:26 |
| 재정비 관문 | TST-01: Breaking 0·Stale 0(T18~T21 개수 단언 유효)·Missing 0. TST-02: Breaking 1(위 견본 행)·Stale 0·Missing 0. TST-04·05 보호 스코프 무변경. 폐기·병합 후보 0 | 통합 23:17 | — | 완료 보고 관문 — 승인 23:26 |

## 완료 보고

초안 — 완료 보고 관문 승인 대기. AC-01~10 10/10 성공(위 표). 남은 위험: `bypassPermissions`에서 ask 도달 미관찰, 훅 timeout 10초와 래퍼 내부 10초 대기가 같아 판정이 길면 하네스가 먼저 끊음(결과는 통과 — fail-open과 같음), Codex·SEMCo-Work 어댑터는 범위 밖. 종결 전 필요: 커밋 후 clean 재실행으로 `유지` 행 SHA 갱신 — 기록이 닫히면 `### 테스트 대장 변경`이 무효가 되어, 미커밋 SHA 기준이면 판정이 TST-01·02 변경을 위반으로 낸다.

## 인계

- 다음 단계 또는 워크플로우: wf-implement — [PLAN](./plan.md) TASK-08부터
- 시작 조건: 충족 — req-design v1, ADR-014·DCR-015 approved, C층 v4
- 입력 문서와 기준선: [req-design](./req-design.md) v1, [REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md) v4, [PLAN](./plan.md)
- 완료된 항목: 설계·승인(v1), §3.1 재확인(`유지` 전량 통과 22:27), 계획(TASK-01~08, 트리), TASK-01~07
- 미완료 항목: TASK-08
- 차단 요인: 없음
- 미커밋 변경: TASK-04(`verification-depth.md` §6, wf-implement 주의 절)·TASK-05~07(`setup/` 훅 2종·wf-common·메시지·러너·설치·setup, README, 대장 TST-01 행)와 plan·이 기록 — TASK-03까지 사용자 지시로 커밋 `90af250`·push(2026-10-25 22:58). `docs/research/20261025-aidlc-trends/06·07`은 병렬 세션 산출물이라 커밋 제외(22:43 이 기록 덮어쓰기와 같은 시각)
- 관찰: 임계 훅이 `signal=bytes`(usage 파싱 폴백)로 반복 발화(직전 세션 2회, 그 전 세션 1517→2482KB 여러 차례, 이번 세션 1553KB 경고 후 사용자 지시로 TASK-06까지 진행, 2473KB) — ADR-012 후속 관찰 대상
- 다음 행동: TASK-08 — 사용자 일괄 승인 대기(대장 변경 표, Breaking 1 포함)·커밋 지시 대기. 승인 후: 대장 `## 재정비 기록` 1행, 커밋→clean `유지` 재실행→SHA 갱신, plan·status·REQ/DESIGN 추적성 갱신, 기록 종결. 관찰 ①②③ 완료(23:23).
- 재개 프롬프트: 작업 20261025-regression-guard 재개 — docs/work/20261025-regression-guard/work-log.md의 인계 절을 읽고 "다음 행동"부터 진행하라.

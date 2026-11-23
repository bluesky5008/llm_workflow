# PLAN-20261122-hook-friction: 구현 계획 — 회귀 보호 판정 완화와 선행 변경 편입

> 문서 유형: `plan`
> 작업 ID: `20261122-hook-friction`
> 상태: `in-progress`
> 기준선: [REQ-DESIGN-hook-friction](./req-design.md) `v1` (승인일 2026-11-22)
> 작성일: 2026-11-22
> 최종 갱신: 2026-11-23
> 관련 문서: [WORK-20261122-hook-friction: 작업 기록](./work-log.md), [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md), [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 승인된 v1(FR-01~08, NFR-01~05, DES-01~09)을 7개 TASK로 구현하고, 종결은 closing.md 순서를 따른다.
- 현재 결론 또는 상태: TASK-01~06 완료(6/7), TASK-07 진행 중(자체 리뷰·뮤테이션·전체 스위트 완료, 완료 보고 관문 승인 대기).
- 다음 행동: TASK-07 — 작업 기록 인계 절의 다음 행동.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-hook-friction](./req-design.md) | FR-01~08, AC-01~08, DES-01~09 | v1 |
| input | decision | [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md) | document | approved |
| input | change | [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md) | document | approved, C층 v5 → v6 |
| output | implementation | [WORK-20261122-hook-friction](./work-log.md) | 수행 기록 | TASK별 결과 |

## 기준선

- 관련 요구사항: FR-01~08, NFR-01~05
- 관련 설계: DES-01~09
- 관련 ADR·DCR: [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md), [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md), [ADR-014](../20261025-regression-guard/ADR-014-회귀-보호-훅-강제-방식.md)(결정 1·3 유지)

## 작업 정의

- 목표: B층 내용 판정·지문 해소, 가드 순수 추가·세션 기억, 게이트 반복 억제, 설치·메시지, 분류 규정, C층 v6와 선행 변경 사후 기록.
- 범위: req-design [범위](./req-design.md#범위)의 포함 항목.
- 범위 밖: req-design [범위](./req-design.md#범위)의 범위 밖 항목.
- 가정: §3.1 재확인(2026-11-22 22:46) — HEAD `46600de`(= `origin/main`) + 미커밋(문서만: 이 작업 폴더·`docs/status.md`·`docs/decisions.md`), `유지` 4행 통과(TST-01 59, TST-02 113, TST-04 16, TST-05 16). 요구사항·설계는 현재 코드 구조에 그대로 적용 가능.
- 위험: 보호 테스트 파일(`run-tests.ps1`, `skills/wf-doc/scripts/tests/*.py`) 편집은 TASK-02의 새 가드가 들어가기 전까지 기존 가드가 편집마다 확인을 묻는다(정상 — 이 작업이 고치는 마찰 자체). 편집은 TASK당 가능한 한 적은 호출로 묶는다. 테스트 파일 변경은 작업 기록 `### 테스트 대장 변경`에 적어 종료 판정을 통과시키고, TASK-01 이후에는 지문과 함께 적는다.

## 계획 트리

<!-- generated: 2026-11-23 21:29 — scripts/render.py --view active -->

```text
[작업] 20261122-hook-friction — 회귀 보호 판정 완화와 선행 변경 편입 ... in-progress (6/7)
├─ [✓] B층 판정 — 패턴 파일·내용 판정·지문 해소 (DES-01·02) (TASK-01) ... 2026-11-22 23:11
├─ [✓] 가드 순수 추가·세션 기억 (DES-03·04) (TASK-02) ................... depends: TASK-01  2026-11-23 00:22
├─ [✓] 게이트 세션 반복 억제 (DES-05) (TASK-03) ......................... depends: TASK-01, TASK-02  2026-11-23 00:41
├─ [✓] 설치 등록·메시지 (DES-06·07) (TASK-04) ........................... depends: TASK-02, TASK-03  2026-11-23 20:13
├─ [✓] 보호 테스트 변경 분류 규정 (DES-08) (TASK-05) .................... 2026-11-23 00:49
├─ [✓] C층 v6와 선행 변경 사후 기록 (DES-09) (TASK-06) .................. depends: TASK-01~04  2026-11-23 20:23
└─ [▶] 통합과 종결 (TASK-07) ............................................ depends: TASK-01~06
```

## 작업 목록

### TASK-01: B층 판정 — 패턴 파일·내용 판정·지문 해소 (DES-01·02)

- 상태: completed
- 완료: 2026-11-22 23:11
- 상위: 없음
- 목표: `test-disable-patterns.txt` 신설(FR-02 최소 목록). `regression_guard.py` — 후보 `--no-renames` + 미추적 보호 파일, 파일별 `--unified=0` diff의 위치 기반 헤더 판별, 삭제 줄·패턴 추가 줄 판정, 지문(삭제·패턴 줄 내용 SHA-1 8자, 이진 `bin`), 출력 ` [지문]`·축소 ` [-]`, `recorded()` 줄 단위 (행 ID, 지문) 해소, 패턴 파일 없음 exit 2
- 관련 요구사항과 설계: FR-01·02·05, NFR-02·05, DES-01·02, AC-03·05(B층)
- 변경 대상: `skills/wf-doc/scripts/test-disable-patterns.txt`(신설), `skills/wf-doc/scripts/regression_guard.py`, `skills/wf-doc/scripts/tests/test_regression_guard.py`(TST-02 보호 — 기존 가드 확인)
- 의존성: 없음
- 위험: 기존 테스트 6건 `Breaking` — 출력 지문 접미(`test_changed_test_file_without_record_fails`·`test_quarantine_without_record_fails`·`test_row_deleted_without_record_fails`·`test_test_file_value_changed_without_record_fails`), 행 ID만 기록 → 지문 필요(`test_changed_test_file_with_record_passes`·`test_cleanup_batch_record_passes_refactor_and_discard`). 승인된 DCR-026의 B층 계약 변경이므로 FR-07 (3) 예외 — 대장 변경 절에 지문과 함께 기록. 패턴 표본·픽스처 줄은 실행 시 조합(AC-05). 첫 보호 파일 편집의 가드 `ask`에서 사유가 Claude에게 보이는지 관찰(A-04)
- 검증 방법: Red — AC-03 케이스(줄 추가 커밋·워킹트리 exit 0, 삭제 exit 1 + 지문, 패턴 줄, 값 없는 `return`, 지문 불변·변화, `git mv` + 삭제, 미추적 패턴 파일, 지문 해소, 패턴 파일 없음 exit 2)와 AC-05 B층 표본을 먼저 작성·실행해 현 구현에서 실패 확인. Green 후 TST-02 전량
- 완료 조건: AC-03, AC-05의 B층 절반

### TASK-02: 가드 순수 추가·세션 기억 (DES-03·04)

- 상태: completed
- 완료: 2026-11-23 00:22
- 상위: 없음
- 목표: `wf-common.ps1` — `Get-WfGuardState`/`Set-WfGuardState`(`<sid>.guard.json`), `Get-WfDisablePatterns`, `Get-WfToolInputHash`, `Test-WfPureAddition`(메모리 적용·CRLF 정규화·두 포인터 부분열·패턴). `wf-test-guard.ps1` — `hook_event_name` 분기(PreToolUse: 설정 파일·NotebookEdit → `ask`, 테스트 행 → `approved` → 순수 추가 → `asked` 기록 + `ask`; PostToolUse: (경로, 해시) 일치 시 `approved`)
- 관련 요구사항과 설계: FR-01·03·04, NFR-03·04·05, DES-03·04, AC-01·02·05(C층)
- 변경 대상: `setup/hooks/wf-common.ps1`, `setup/hooks/wf-test-guard.ps1`, `setup/hooks/tests/run-tests.ps1`(TST-01 보호)
- 의존성: TASK-01(패턴 파일, AC-05 표본 대조)
- 위험: 고정 `session_id`(`wf-test-tg`)의 상태 파일이 실행 간 남음 — 새 기억 테스트는 실행마다 고유 `session_id`, 스위트 시작에 테스트 세션 가드 상태 삭제 줄 추가(순수 추가). PS 5.1 ASCII 전용 소스(한글은 코드포인트·메시지 파일)
- 검증 방법: Red — T57~(AC-01 케이스 전부, AC-02 4케이스, AC-05 C층 표본) 먼저. Green 후 TST-01 전량
- 완료 조건: AC-01, AC-02, AC-05의 C층 절반

### TASK-03: 게이트 세션 반복 억제 (DES-05)

- 상태: completed
- 완료: 2026-11-23 00:41
- 상위: 없음
- 목표: `wf-stop-gate.ps1` — 판정 exit 1 출력 행 → 키(`행 ID|파일|지문`), `stopKeys`에 없는 키가 있으면 추가 후 `block`, 모두 있으면 무출력, 상태 실패 시 `block`
- 관련 요구사항과 설계: FR-06, NFR-04, DES-05, AC-04
- 변경 대상: `setup/hooks/wf-stop-gate.ps1`, `setup/hooks/tests/run-tests.ps1`
- 의존성: TASK-01(지문 출력 형식), TASK-02(가드 상태 함수, 같은 테스트 파일)
- 위험: 기존 T38~T44의 고정 `session_id`(`wf-test-sg`) — 실행 간 억제로 두 번째 실행부터 T38 실패할 수 있다. 스위트 시작의 기존 정리 줄(`wf-test-*.json`)이 `wf-test-sg.guard.json`도 지운다(TASK-02 확인)
- 검증 방법: Red — AC-04 케이스(같은 키 재차단 없음, 부분집합 무출력, 새 키 차단, 다른 세션 차단) 먼저. Green 후 TST-01 전량, 스위트 2회 연속 실행으로 상태 잔류 없음 확인
- 완료 조건: AC-04

### TASK-04: 설치 등록·메시지 (DES-06·07)

- 상태: completed
- 완료: 2026-11-23 20:13
- 상위: 없음
- 목표: `install-hooks.ps1` PostToolUse에 가드 기록 항목(총 7개), `messages/test-guard.md`·`stop-gate.md` 판단 기준 문구, T18·T19·T21 PostToolUse 기대값 1 → 2(`Breaking` — DCR-026 승인이 §6 판정 (b)), `setup_claude.ps1` 재실행(설정 백업 scratchpad, 외부 항목 보존 확인)
- 관련 요구사항과 설계: FR-04·07, DES-06·07, AC-06(메시지)·AC-08(설치)
- 변경 대상: `setup/hooks/install-hooks.ps1`, `setup/hooks/messages/test-guard.md`, `setup/hooks/messages/stop-gate.md`, `setup/hooks/tests/run-tests.ps1`, `~/.claude/settings.json`(설치 결과, 저장소 밖)
- 의존성: TASK-02, TASK-03(같은 테스트 파일, 등록 대상 스크립트)
- 위험: 전역 설정 변경 — 백업 후 재실행, 이 세션부터 PostToolUse 기록 동작
- 검증 방법: Red — T18·T19·T21 기대값 2로 먼저 바꿔 실패 확인(현 설치 1개). 메시지는 문서 변경(`Red: 해당 없음`). Green 후 TST-01 전량
- 완료 조건: AC-08의 설치 항목, AC-06의 메시지 항목

### TASK-05: 보호 테스트 변경 분류 규정 (DES-08)

- 상태: completed
- 완료: 2026-11-23 00:49
- 상위: 없음
- 목표: verification-depth `## 9. 보호 테스트 변경의 판정` 신설(FR-07 표·기록 예·`Breaking`·기록 없는 경우·닫을 때 SHA 갱신), §6 첫 문단 포인터, §2 문장 2곳 개정, wf-implement 주의 ④·§3.3 금지문, lightweight-path §4 1문장, templates 대장 변경 예시 1행
- 관련 요구사항과 설계: FR-07, NFR-01, DES-08, AC-06
- 변경 대상: `skills/wf-implement/references/verification-depth.md`, `skills/wf-implement/SKILL.md`, `skills/wf-design/references/lightweight-path.md`, `skills/wf-doc/references/templates.md`
- 의존성: 없음
- 위험: wf-implement 본문 여유 34어절(K3) — 순증 ≤ 25. 설치 메시지(DES-07)가 §9를 가리키므로 메시지 TASK와 같은 세션 안에서 완료
- 검증 방법: 문서 변경(`Red: 해당 없음`). `lint_skill.py` 오류 0·K3, grep(§9 앵커·주의 ④·§3.3·§2·§6)
- 완료 조건: AC-06의 규정 항목

### TASK-06: C층 v6와 선행 변경 사후 기록 (DES-09)

- 상태: completed
- 완료: 2026-11-23 20:23
- 상위: 없음
- 목표: DCR-026 변경 항목대로 `docs/requirements.md`·`docs/design.md` v6, REQ-DESIGN-regression-guard DES-08 `\|` 문구·변경 이력 1행, approval-request §4, README 훅 설명(§3.6 문서 일관성 — §4.1 경미로 기록), DCR-026 `completed`·결정 등록부
- 관련 요구사항과 설계: FR-08, DES-09, AC-07
- 변경 대상: `docs/requirements.md`, `docs/design.md`, `docs/work/20261025-regression-guard/req-design.md`, `skills/wf-design/references/approval-request.md`, `README.md`, [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md), `docs/decisions.md`
- 의존성: TASK-01~04(실제 동작과 일치)
- 위험: 닫힌 작업 문서 편집 — 정본 문구 보완과 변경 이력 1행만
- 검증 방법: 문서 변경(`Red: 해당 없음`). DCR-026 변경 항목 표 대조, `lint_worklog.py`·`lint_skill.py`
- 완료 조건: AC-07

### TASK-07: 통합과 종결

- 상태: in-progress
- 상위: 없음
- 목표: 전체 스위트 + `유지` 전량, 변경 범위 뮤테이션(`regression_guard.py` 판정·지문·해소, `Test-WfPureAddition`, 게이트 억제 — 수동 뮤턴트 1~3개씩), 재정비 관문(TST-01·02 보호 스코프 확장, `Breaking` 기록), 지연 측정(NFR-03·RISK-04), 실세션 관찰(테스트 추가 편집 무확인), 자체 리뷰(review-checklist), 완료 보고 관문(대장 변경·커밋·push 범위 승인), closing.md 종결(TST-01·02 마지막 성공 SHA 갱신 — `46600de` 포함)
- 관련 요구사항과 설계: NFR-01~05, AC-08
- 변경 대상: `docs/test-register.md`, 이 작업 문서, `docs/status.md`
- 의존성: TASK-01~06
- 위험: 뮤턴트 잔류 — 해시 대조
- 검증 방법: 린트 2종, `유지` 전량, `git diff --name-only <구현 SHA>`
- 완료 조건: AC-08, closing.md ②~⑤

## 검증 계획

| 인수 조건 | TASK | 방법 |
|---|---|---|
| AC-01 | TASK-02 | 훅 테스트 T57~(TST-01) |
| AC-02 | TASK-02 | 훅 테스트(TST-01) |
| AC-03 | TASK-01 | pytest(TST-02) |
| AC-04 | TASK-03 | 훅 테스트(TST-01) |
| AC-05 | TASK-01·02 | pytest와 훅 테스트의 같은 표본 |
| AC-06 | TASK-04·05 | grep·`lint_skill.py` |
| AC-07 | TASK-06 | DCR-026 변경 항목 대조 |
| AC-08 | TASK-04·07 | 설치 테스트, `유지` 전량, 린트, `regression_guard.py .` |

## 마이그레이션과 롤백

- 설치: TASK-04에서 `setup_claude.ps1` 재실행(멱등, PostToolUse 1개 추가). 백업은 scratchpad. 롤백은 `install-hooks.ps1`에서 항목을 빼고 재실행하거나 백업 복원.
- 코드·문서 롤백은 커밋 되돌림. 가드 상태 파일은 `%TEMP%` 휘발성 데이터.

## 인계

- 다음 단계 또는 워크플로우: wf-implement §3.4~§3.6 — TASK-07
- 시작 조건: 충족(TASK-07의 의존 TASK-01~06 완료)
- 입력 문서와 기준선: [REQ-DESIGN-hook-friction](./req-design.md) v1, 이 계획
- 완료된 항목: 계획 작성, TASK-01~06(TASK-05를 TASK-04보다 먼저 수행)
- 미완료 항목: TASK-07
- 차단 요인: 없음
- 다음 행동: TASK-07 — 작업 기록 인계 절의 다음 행동.

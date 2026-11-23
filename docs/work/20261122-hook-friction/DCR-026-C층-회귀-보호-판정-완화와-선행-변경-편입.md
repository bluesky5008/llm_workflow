# DCR-026: C층 회귀 보호 판정 완화와 선행 변경 편입 — 순수 추가 통과·세션 반복 억제, `46600de` 사후 기록

> 문서 유형: `dcr`
> 작업 ID: `20261122-hook-friction`
> 상태: `completed`
> 기준선: `v5 → v6` (승인일 2026-11-22) ([REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md))
> 작성일: 2026-11-22
> 최종 갱신: 2026-11-23
> 관련 문서: [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md), [REQ-DESIGN-hook-friction](./req-design.md), [REQ-llm-workflow: 요구사항](../../requirements.md), [DESIGN-llm-workflow: 설계](../../design.md), [WORK-20261122-hook-friction: 작업 기록](./work-log.md), [DCR-015](../20261025-regression-guard/DCR-015-C층-회귀-보호-훅-추가.md), [DCR-019](../20261026-approval-gate/DCR-019-C층-승인-게이트-훅-추가.md), [ADR-012](../20261018-context-signal-v2/ADR-012-컨텍스트-신호-usage-파싱.md)

## 요약

- 목적: C층 회귀 보호(DES-06·07)의 위반 정의를 변경 내용 단위로 바꾸고 세션 반복을 억제한다. 저장소 밖 선행 변경 `46600de`가 바꾼 C층·B층 동작을 기준선에 사후 기록한다.
- 현재 결론 또는 상태: 완료(2026-11-23) — 승인(2026-11-22), REQ·DESIGN v6 반영(TASK-06). 구현 커밋 `32f2f41`.
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | change | [REQ-llm-workflow](../../requirements.md) | 요약, FR-06·07, NFR-01, AC-07·08 | v5 → v6 |
| input | change | [DESIGN-llm-workflow](../../design.md) | DES-02·04·06·07·09, 계약, 상태 파일, 설정값, 흐름, 검증, 위험, 대안과 결정 | v5 → v6 |
| input | requirement | [REQ-DESIGN-hook-friction](./req-design.md) | FR-01~08, DES-01~09 | 변경 사유 |
| input | decision | [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md) | 결정 1~5 | 판정 단위·억제·판정 범위 |

## 변경 사유와 증거

- 사용자 보고(2026-11-22): 원치 않는 선택 강요의 대부분이 C(편집 시 회귀 보호)·D(종료 시 회귀 보호)이며 Claude의 일반 질문으로 온다.
- 조사([REQ-DESIGN-hook-friction 확인된 사실](./req-design.md#확인된-사실)): 보호 단위가 파일·폴더이고 판정이 파일 이름 단위라 순수 추가도 위반. 판정이 상태를 남기지 않아 반복. 착수 시점 실제 차단 1건(`46600de`, 3파일 모두 순수 추가).
- `46600de`(2026-11-22 push, 원 작성 2026-11-11)는 기준선 문서 갱신 없이 C층·B층 동작을 바꿨다.

## 기존 기준선과 설계

- v5: 훅 6종. DES-06 = `유지` 테스트 파일·설정 파일 경로면 무조건 `ask`, 상태 없음. DES-07 = `regression_guard.py` exit 1이면 Stop마다 `block`(재진입만 통과). B층 계약 출력 `TST-NN: <사유> <파일>`. DES-02 설정값 기본 130000/20000, usage는 1단 중첩까지 판독. 대장 판독은 `|`로만 칸을 나눔. 승인 게이트 판정은 상태 값 전체·`"…"`·`“…”` 인용과 "응답" 낱말.

## 제안 설계

1. FR-06(v6): 보호 대상 편집 전 확인은 유지하되, 대장 `유지` 행 테스트 파일에 대한 Edit·MultiEdit·Write를 메모리에서 적용한 결과가 **순수 추가**(변경 전 줄이 같은 순서로 모두 남고 새 줄에 비활성화 구문 없음, 새 파일 포함)면 확인하지 않는다. 같은 세션에서 `ask` 뒤 그 편집 그대로 실행된(PostToolUse 경로·도구 입력 해시 일치) 테스트 파일은 다시 확인하지 않는다. 게이트 설정 파일과 NotebookEdit는 항상 확인한다.
2. FR-07(v6): 판정은 테스트 파일 변경을 내용으로 본다 — 마지막 성공 SHA 대비(이름 변경 감지 끔) diff에 삭제 줄이 있거나 더한 줄이 비활성화 구문에 맞으면 위반이고 지문(삭제·패턴 줄 내용 해시)을 붙인다. 테스트 파일 위반은 열린 작업 기록에 행 ID와 지문이 함께 있어야 해소된다. 같은 세션에서 이미 차단한 (행 ID·파일·지문) 키만 남았으면 다시 차단하지 않는다.
3. C층 DES-04·05·06·07·09와 B층 계약·데이터 파일: [REQ-DESIGN-hook-friction DES-01~09](./req-design.md#설계).
4. 선행 변경 사후 기록: DES-02 설정값 400000/100000(1M 컨텍스트 창 기준, 2026-11-11 사용자 결정 — ADR-012의 130k/20k를 정밀화, 신호 방식은 그대로), usage 객체 임의 깊이 중첩 판독(균형 그룹, 최상위 키 우선), DES-09 대장 칸 분할의 GFM `\|` 이스케이프, B층 `approval_gate.py`의 상태 첫 백틱 값 판독과 응답 인용(「…」, "사용자" 줄).

## 변경 항목

| 대상 | 변경 전 | 변경 후 | 이유 |
|---|---|---|---|
| REQ 요약 | v5 | v6 — 회귀 보호 판정 완화, 선행 변경 기록 | 범위 |
| REQ FR-06 | 보호 대상 편집 시 확인 | + 순수 추가 제외, 세션 기억, 설정 파일·NotebookEdit 예외 없음 | 제안 설계 1 |
| REQ FR-07 | 기록 없는 `유지` 테스트 파일 변경이면 Stop마다 1회 차단, 행 ID로 해소 | 변경 = 내용 기준(삭제 줄·비활성화 구문, 이름 변경 감지 끔), 테스트 파일 위반은 행 ID + 지문으로 해소, 같은 키는 세션당 1회 | 제안 설계 2 |
| REQ NFR-01 | 예외: FR-06·08 가드 fail-to-ask | + FR-06 순수 추가 판정 예외도 확인 쪽(fail-to-ask), 가드 상태 실패는 기억 없음으로 진행 | NFR-04 |
| REQ AC-07·08 | 경로 일치 → `ask`, 위반 → `block` | + 순수 추가 무출력·기억 무출력(AC-07), 같은 위반 재차단 없음·지문(AC-08) | 제안 설계 1·2 |
| DESIGN DES-02·설정값 | 130000/20000, 1단 중첩 | 400000/100000, 임의 깊이 중첩 | 선행 변경 |
| DESIGN DES-04 | 6개 항목 | 7개(PostToolUse 2개: DES-02, DES-06 기록) | 제안 설계 1 |
| DESIGN DES-06 | 경로 일치 → `ask` | PreToolUse/PostToolUse 분기, 순수 추가·기억 | 제안 설계 1 |
| DESIGN DES-07 | exit 1 → `block` | + (행 ID·파일·지문) 키가 모두 `stopKeys`에 있으면 억제, 새 키가 있으면 차단 후 집합에 추가 | 제안 설계 2 |
| DESIGN DES-09 | 공용 함수 | + 가드 상태, 패턴 로드, 순수 추가 판정, `\|` 칸 분할 | 제안 설계 1, 선행 변경 |
| DESIGN 데이터와 인터페이스 | 상태 파일 `<sid>.json`, B층 출력 `TST-NN: <사유> <파일>`, 해소 = 행 ID | + `<sid>.guard.json` `{asked:[{path,hash}], approved, stopKeys}`, B층 출력 끝 ` [지문8]`·해소 = 테스트 파일 위반은 행 ID + 지문, 패턴 파일 `skills/wf-doc/scripts/test-disable-patterns.txt`, 승인 판정 인용 규칙 | 제안 설계 1~4 |
| DESIGN 흐름·검증·위험 | v5 | + 순수 추가 판정 실패 → `ask`, T57~, RISK(패턴 밖 무력화, 억제 무시) | ADR-025 감수 단점 |
| DESIGN 대안과 결정 | ADR-014·018 | + ADR-025 | 결정 기록 |
| 스킬 | approval-request §4 "따옴표로 인용" | + 「…」·"사용자" 줄 인용 명시 | 선행 변경 |
| REQ-DESIGN-regression-guard DES-08 | 칸은 `\|`로 구분 | + GFM `\|` 이스케이프는 칸 내용, 변경 이력 1행 | 선행 변경(판독 규칙 정본) |
| 코드 | — | `regression_guard.py`, `test-disable-patterns.txt`, `wf-test-guard.ps1`, `wf-stop-gate.ps1`, `wf-common.ps1`, `install-hooks.ps1`, `messages/test-guard.md`·`stop-gate.md`, 테스트 | 구현 |

## 영향 범위

- 전역 훅이라 `docs/test-register.md`를 쓰는 모든 저장소에 적용된다. 대장이 없는 저장소는 무동작(기존).
- 열린 작업 기록의 `### 테스트 대장 변경` 기록: 대장 축소 위반은 기존대로 행 ID로 해소된다. 테스트 파일 위반은 지문이 함께 있어야 해소되므로, 다른 저장소에서 행 ID만 적힌 열린 기록은 순수 추가가 아닌 위반이 키마다 세션당 1회 차단되고 지문을 더하면 해소된다.
- 이 저장소의 진행 중 작업: 이 작업뿐.

## 고려한 대안

- [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md) 대안 B~E.

## 구현된 코드의 처리

- 선행 변경 `46600de`는 이미 구현·push됨 — 유지한다. 테스트 59/59·pytest 통과(2026-11-22). TDD Red 증거 없음을 작업 기록에 남긴다.
- 나머지는 구현 전 제안.

## 마이그레이션과 롤백

- 설치: `setup_claude.ps1` 재실행(멱등) — PostToolUse 항목 1개 추가. 롤백: `install-hooks.ps1`의 `$desired`에서 PostToolUse 기록 항목을 빼고 재실행, 판정 변경은 커밋 되돌림. 가드 상태 파일은 `%TEMP%` 휘발성 데이터.

## 검증 방법

- TST-01 T57~(AC-01·02·04·05, 설치 7개), TST-02 `test_regression_guard.py` 추가(AC-03·05), `lint_skill.py`·`lint_design.py`·`lint_worklog.py`, 설치 후 실세션에서 테스트 추가 편집 1회 무확인 관찰.
- 기존 TST-01 T18·T19·T21의 PostToolUse 기대값 1 → 2는 이 DCR의 C층 DES-04 변경에 따른 `Breaking` 수정이다 — 이 DCR의 승인이 §6 판정 (b)이며, 작업 기록 `### 테스트 대장 변경`에 지문과 함께 기록한다(선례 DCR-019 T45·T46).

## 남은 위험

- 패턴 밖 무력화 삽입 통과(ADR-025 감수 단점).
- `bypassPermissions`에서 `ask` 미도달 가능성(C층 RISK-06과 공통).

## 승인 기록

- 2026-11-22 22:43 — 사용자가 [REQ-DESIGN-hook-friction](./req-design.md) v1과 함께 **승인**. 응답: Q-01~05 "전부 권장안", "승인합니다".

## 변경 이력

| 날짜 | 변경 내용 | 근거 | 상태 전이 | 작성·승인 |
|---|---|---|---|---|
| 2026-11-22 | 최초 작성 — FR-06·07, NFR-01, AC-07·08, DES-02·04·06·07·09, 계약, 선행 변경 사후 기록 제안 | REQ-DESIGN-hook-friction, ADR-025 | → draft | Claude(작성) |
| 2026-11-22 | 적대 검토 1라운드 반영 — 제안 설계 1·2(메모리 적용 판정, 해시 일치 기억, `--no-renames`, 지문 단위 해소·키 억제), 변경 항목(FR-07, 데이터와 인터페이스, REQ-DESIGN-regression-guard DES-08), 검증 방법(T18·T19·T21 `Breaking`) | 적대 검토 1라운드 지적 1~4·7·9·12 | draft 유지 | Claude(작성) |
| 2026-11-22 | 적대 검토 2라운드 반영 — 제안 설계 3 범위, DES-07 행 키 집합, 영향 범위 해소 계약·전역 영향. 승인 요청 | 적대 검토 2라운드 지적 19~22 | draft → awaiting-approval | Claude(작성) |
| 2026-11-22 | 승인 | 사용자 응답 "승인합니다" | awaiting-approval → approved | 사용자(승인) |
| 2026-11-23 | 완료 — REQ·DESIGN v6 반영(TASK-06), 구현은 TASK-01~05(구현 커밋은 TASK-07 통합에서) | wf-implement TASK-06 | approved → completed | Claude(작성) |
| 2026-11-23 | 구현 커밋 `32f2f41`, 작업 종결(TASK-07) | 완료 보고 관문(2026-11-23 21:36 "전부 승인") | completed 유지 | Claude(작성) |

## 인계

- 다음 단계 또는 워크플로우: 없음
- 다음 행동: 없음

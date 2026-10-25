# DCR-019: C층에 승인 게이트 훅 추가 — 기준선 미승인 작업의 제품 코드 편집 확인

> 문서 유형: `dcr`
> 작업 ID: `20261026-approval-gate`
> 상태: `approved`
> 기준선: `v4 → v5` (승인일 2026-10-26) ([REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md))
> 작성일: 2026-10-26
> 최종 갱신: 2026-10-26
> 관련 문서: [ADR-018: 승인 게이트의 판정](./ADR-018-승인-게이트-판정.md), [REQ-DESIGN-approval-gate](./req-design.md), [REQ-llm-workflow: 요구사항](../../requirements.md), [DESIGN-llm-workflow: 설계](../../design.md), [WORK-20261026-approval-gate: 작업 기록](./work-log.md), [DCR-015](../20261025-regression-guard/DCR-015-C층-회귀-보호-훅-추가.md)

## 요약

- 목적: C층 훅 기준선에 6번째 훅(PreToolUse 승인 게이트)과 B층 판정 계약을 추가한다.
- 현재 결론 또는 상태: 승인(2026-10-26). REQ·DESIGN v5 반영은 구현 TASK.
- 다음 행동: 구현 TASK에서 REQ·DESIGN v5 반영.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | change | [REQ-llm-workflow](../../requirements.md) | 요약, 범위, FR-05, NFR-01, AC | v4 → v5 |
| input | change | [DESIGN-llm-workflow](../../design.md) | DES-04, 계약, 흐름, 검증, 위험, 대안과 결정 | v4 → v5 |
| input | requirement | [REQ-DESIGN-approval-gate](./req-design.md) | FR-01~05, DES-01~04·08 | 변경 사유 |
| input | decision | [ADR-018](./ADR-018-승인-게이트-판정.md) | 결정 1~4 | 판정 방식 |

## 변경 사유와 증거

- wf-design §8 승인 관문에 강제 장치가 없다(REQ-DESIGN-approval-gate §4.1 조사). 사이클 1이 테스트 보호에 쓴 훅 구조(DCR-015)를 승인에 재사용한다.

## 기존 기준선과 설계

- v4: 훅 5종(SessionStart·임계·post-compact·`wf-test-guard`·`wf-stop-gate`), PreToolUse는 DES-06 하나, B층 계약은 `regression_guard.py` 하나. NFR-01 예외는 FR-06 가드뿐.

## 제안 설계

1. FR-08(v5): 파일 편집 도구가 제품 코드(기본 `docs/` 밖, 루트 `.wf-gate.json`으로 덮어쓰기)를 바꾸려 할 때, 열린 작업 기록 중 기준선이 승인되지 않은 것이 있으면(경량 표지 작업은 기계 조건 위반 시) 실행 전에 확인을 요청한다.
2. DES-08(v5): `wf-approval-gate.ps1` — PreToolUse(matcher `Edit|Write|MultiEdit|NotebookEdit`). `docs/work/` 없음, 또는 `.wf-gate.json`이 없고 `docs/` 경로면 무출력(Python 미호출). `approval_gate.py <cwd> <대상>`을 5초 제한 호출, exit 1 → `ask`, exit 2·타임아웃·Python 부재 → `ask`(fail-to-ask), 0 → 무출력. `deny` 없음.
3. B층 계약 추가: `python approval_gate.py <루트> <대상>` → 0 통과(무출력) / 1 확인 필요(`<작업 ID>: <사유>` 행) / 2 내부 오류.

## 변경 항목

| 대상 | 변경 전 | 변경 후 | 이유 |
|---|---|---|---|
| REQ 요약·범위 | 훅 5종 | 훅 6종(+ 승인 게이트) | 범위 확장 |
| REQ FR-05 | `docs/work/` 없으면 무동작, FR-06·07은 대장 없으면 무동작 | + v5: FR-08은 `docs/work/` 없으면 무동작 | 무동작 조건 |
| REQ FR | FR-01~07 | + FR-08 | 제안 설계 1 |
| REQ NFR-01 | 예외: FR-06 가드 fail-to-ask | 예외: FR-06·FR-08 가드 fail-to-ask | ADR-018 결정 4 |
| REQ NFR-03 | 파일 크기 확인 수준의 작업만 | + v5: DES-08은 제품 경로에서만 판정 스크립트를 호출하고 추가 지연 중앙값 ≤ 300ms(REQ-DESIGN-approval-gate NFR-02, 실측 175.5ms) | 적용 중 발견한 누락 |
| REQ AC | AC-01~09 | + AC-10 미승인 → `ask`·승인 → 무출력, AC-11 `docs/` 경로·`docs/work/` 없음 → Python 미호출 무출력, AC-12 판정 오류·Python 부재 → `ask` | 제안 설계 2 |
| DESIGN DES-04 | 5개 항목 병합 | 6개 항목(PreToolUse 2개) | 설치 |
| DESIGN DES | DES-01~07 | + DES-08 | 제안 설계 2 |
| DESIGN 계약 | B층 `regression_guard.py` | + `approval_gate.py` 행 | 제안 설계 3 |
| DESIGN 흐름 | 가드·실패(v4) | + DES-08 가드·실패 | fail-to-ask |
| DESIGN 검증 전략 | T29~T46 | + T47~(DES-08) | 검증 |
| DESIGN 위험 | RISK-04~07 | + RISK-08 자기 승인, RISK-09 판정 기동 지연, RISK-10 열린 작업 다수 시 확인 소음 | ADR-018 감수 단점 |
| DESIGN 대안과 결정 | ADR-014 | + ADR-018 | 결정 기록 |
| 코드 | — | `setup/hooks/wf-approval-gate.ps1`, `messages/approval-gate.md`, `install-hooks.ps1`, `tests/run-tests.ps1`, `skills/wf-doc/scripts/approval_gate.py`·테스트 | 구현 |

## 영향 범위

- 전역 훅이라 `docs/work/`를 쓰는 모든 저장소에 적용된다. `docs/work/`가 없는 저장소는 무동작.
- 이 저장소의 진행 중 작업: 없음(이 작업 자체는 승인 후 구현하므로 게이트 통과).
- 기존 훅 5종의 동작은 바뀌지 않는다.

## 고려한 대안

- [ADR-018](./ADR-018-승인-게이트-판정.md) 대안 B~E.

## 구현된 코드의 처리

- 해당 없음 — 구현 전 제안.

## 마이그레이션과 롤백

- 설치: `setup_claude.ps1` 재실행(멱등). 롤백: `install-hooks.ps1`의 `$desired`에서 항목을 빼고 재실행하면 우리 항목이 정리된다. 판정 스크립트는 독립 파일이라 삭제만으로 무력화(훅은 Python 부재처럼 `ask` — 롤백 시 훅 등록부터 뺀다).

## 검증 방법

- TST-01 T47~(AC-10~12, 설치 멱등), TST-02 `test_approval_gate.py`, 지연 측정(REQ-DESIGN-approval-gate NFR-02), 설치 후 실세션 통과 관찰.

## 남은 위험

- `bypassPermissions`에서 `ask` 미도달 가능성(C층 RISK-06과 공통) — 사용자 관찰 후 별도 DCR.

## 승인 기록

- 2026-10-26 — 사용자가 [REQ-DESIGN-approval-gate](./req-design.md) v1과 함께 **승인**. 응답: Q-01 "docs/ 밖 + glob 선언", Q-02 "상태 + 응답 인용", Q-03 "5개", "승인".

## 변경 이력

| 날짜 | 변경 내용 | 근거 | 상태 전이 | 작성·승인 |
|---|---|---|---|---|
| 2026-10-26 | 최초 작성 — FR-08, DES-08, B층 계약, AC-10~12, RISK-08~10 제안 | REQ-DESIGN-approval-gate, ADR-018 | draft → awaiting-approval | Claude(작성) |
| 2026-10-26 | 승인 — FR-08에 `.wf-gate.json` 덮어쓰기 반영 | 사용자 승인 관문 응답 | awaiting-approval → approved | 사용자(승인) |
| 2026-10-26 | 변경 항목에 REQ NFR-03(v5 예외) 추가 — 적용 중 발견한 누락, 승인된 REQ-DESIGN-approval-gate NFR-02 범위의 문서 보완 | wf-implement §4.1 경미 | — | Claude(작성) |

## 인계

- 다음 단계 또는 워크플로우: wf-implement 구현 TASK에서 REQ·DESIGN v5 반영
- 다음 행동: 구현 TASK

# DCR-007: 세션 핸드오프 훅의 닫힘 상태에 `on-hold` 추가

> 문서 유형: `dcr`
> 작업 ID: `20261009-worklog-diet`
> 상태: `approved`
> 기준선: `v2` (승인일 2026-10-09, v1 → v2) ([REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md), 2026-08-09 승인 기준선)
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [REQ-llm-workflow: 요구사항](../../requirements.md), [DESIGN-llm-workflow: 설계](../../design.md), [REQ-DESIGN-worklog-diet: 요구사항·설계](./req-design.md), [WORK-20260814-multiuser-workflow: 작업 기록](../20260814-multiuser-workflow/work-log.md), [WORK-20261009-worklog-diet: 작업 기록](./work-log.md)

## 요약

- 목적: 세션 시작·컴팩션 사후 훅이 "미완료 작업 기록"을 고를 때 `on-hold`(의도적 보류) 작업을 제외한다.
- 현재 결론 또는 상태: 승인(`approved`, 2026-10-09) — [REQ-DESIGN-worklog-diet Q-02](./req-design.md#가정과-미해결-질문) 포함 결정. REQ·DESIGN-llm-workflow 기준선 v2 발행. 구현·검증은 wf-implement(이 작업의 계획).
- 다음 행동: 구현(정규식·테스트)과 검증(AC-07) — [작업 기록](./work-log.md).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-llm-workflow](../../requirements.md#기능-요구사항) | FR-01, AC-01 | 변경 대상 요구사항(v1) |
| input | baseline | [DESIGN-llm-workflow](../../design.md#컴포넌트와-책임) | DES-01, DES-03, 데이터와 인터페이스 "미완료 판정" | 변경 대상 설계(v1) |
| input | related | [REQ-DESIGN-worklog-diet](./req-design.md) | FR-07, DES-08, Q-02 | 이 DCR을 발생시킨 작업 |
| input | related | [WORK-20260814-multiuser-workflow](../20260814-multiuser-workflow/work-log.md) | 머리말 상태 `on-hold` | 증거: 보류 작업이 매 세션 재개 안내에 포함됨 |
| output | verification | TBD — 승인 후 이 작업의 `plan.md`·`work-log.md`에 TASK·VER로 연결 | — | 가상 링크 금지. 생성 시 양쪽 갱신 |

## 변경 사유와 증거

- `20260814-multiuser-workflow`를 2026-10-09에 `on-hold`로 전환한 뒤, 세션 시작 훅이 매 세션 이 작업을 "미완료 작업 기록"으로 주입한다. 보류의 재개 조건은 "보완 사이클 3건 완료 후 사용자 지시"라 세션마다의 재개 안내는 노이즈다.
- 현행 판정: `setup/hooks/wf-common.ps1`의 `Get-WfOpenWorkLogs`가 머리말 상태가 `(completed|superseded|rejected|withdrawn)`이 아니면 열린 작업으로 본다. `on-hold`는 wf-doc 상태 어휘에서 "의사결정 또는 정보 확보를 위해 의도적으로 보류됨"이며, 재개는 사용자 결정으로 일어난다.
- 사이클 1 세션(2026-10-09)에서 이미 "훅 정규식에 on-hold를 추가하는 것은 테스트가 딸린 동작 변경이라 사이클 2의 아카이빙 규칙과 함께 다루는 것을 권한다"고 인계됐다.

## 기존 기준선과 설계

- [FR-01](../../requirements.md#기능-요구사항): "현재 저장소의 `docs/work/`에 완료되지 않은 작업 기록이 있으면, 그 목록과 '재개 절차를 먼저 적용하라'는 지시를 세션 컨텍스트로 주입해야 한다."
- [AC-01](../../requirements.md#인수-조건): "미완료 기록이 없으면 어떤 재개 지시도 주입되지 않는다."
- [DES-01](../../design.md#컴포넌트와-책임): "`> 상태:`를 읽어 완료 계열(`completed`, `superseded`, `rejected`, `withdrawn`) 이외의 작업 기록을 찾는다." 데이터와 인터페이스의 "미완료 판정(DES-01)"도 같은 목록.
- 구현: `wf-common.ps1` 정규식 `` `(completed|superseded|rejected|withdrawn)` ``, 테스트 T01·T03·T14·T16.

## 제안 설계

"완료되지 않은"을 "열린"으로 정의하고, 열린 상태를 `on-hold`를 제외한 비완료 계열로 한정한다. `blocked`는 재개 조건이 없어 진행 불가인 상태이므로 사람의 주의가 필요해 계속 주입한다.

## 변경 항목

| 대상 | 변경 전 | 변경 후 | 이유 |
|---|---|---|---|
| REQ-llm-workflow FR-01 | "완료되지 않은 작업 기록" | "열린 작업 기록(머리말 상태가 `completed`·`superseded`·`rejected`·`withdrawn`·`on-hold`가 아닌 것)" | 보류는 사용자 결정으로만 재개되므로 세션마다 안내할 대상이 아님 |
| REQ-llm-workflow AC-01 | "미완료 기록이 없으면" | "열린 기록이 없으면(보류만 있는 경우 포함)" | FR-01과 정합 |
| DESIGN-llm-workflow DES-01, 데이터와 인터페이스 "미완료 판정" | 완료 계열 4종 | 닫힘 계열 5종(`on-hold` 추가). 용어 "완료 계열" → "닫힘 계열" | 구현 계약 명시 |
| `setup/hooks/wf-common.ps1` `Get-WfOpenWorkLogs` | `(completed\|superseded\|rejected\|withdrawn)` | `(completed\|superseded\|rejected\|withdrawn\|on-hold)` | 1토큰 |
| `setup/hooks/tests/run-tests.ps1` | T03(완료만 → 무주입) | T03b 추가: `on-hold`만 있을 때 무주입, 기준점 기록 | 회귀 방지. Red 실행 먼저 |
| `setup/hooks/messages/resume.md` | "완료되지 않은 작업 기록" | 변경 없음(문구는 열린 기록에 대해 여전히 참) | — |

## 영향 범위

- 요구사항과 인수 조건: FR-01·AC-01 문구. FR-02~05, AC-02~06 무영향.
- 인터페이스와 데이터: 훅 입출력 계약 무변경. 상태 파일 무변경.
- 보안과 운영: 없음. fail-open 유지.
- 진행 중인 구현: 없음(C층 구현은 2026-08-09 완료 상태). 이 DCR은 새 작업에서 발생했으므로 보류할 구현이 없다.
- 테스트와 문서: 테스트 1케이스 추가(21 → 22). `docs/requirements.md`·`docs/design.md` 머리말 기준선 v2, 변경 이력 1행. 린트(DES-05)의 L8 열림 판정도 같은 5종 목록을 사용한다.
- 포트폴리오: `docs/status.md`의 `on-hold` 행은 유지(포트폴리오는 보류 작업을 싣는다 — 훅 주입과 별개).

## 고려한 대안

| 대안 | 장점 | 단점 |
|---|---|---|
| A. 현행 유지(보류도 주입) | 변경 없음 | 보류가 길어질수록 매 세션 노이즈. CLAUDE.md 진입 규칙이 "완료되지 않은 작업"을 확인하라고 하므로 모델이 매번 보류 기록을 열어 봄 |
| B. `on-hold` 제외 (채택) | 노이즈 제거. 1토큰 + 테스트 1개 | 보류 작업의 존재를 세션 시작 시 잊을 수 있다 → `docs/status.md`에 행이 남고, 재개는 사용자 지시로만 일어나므로 수용 |
| C. `on-hold`·`blocked` 모두 제외 | 주입 최소 | `blocked`는 재개 조건이 없어 사람의 개입이 필요한 상태. 숨기면 안 됨 |

## 구현된 코드의 처리

- 유지: 훅 3종·설치 로직·메시지 파일 전부.
- 수정: `wf-common.ps1` 정규식 1토큰, `run-tests.ps1` 케이스 1개.
- 되돌림: 없음.

## 마이그레이션과 롤백

- 마이그레이션: 없음(설정·상태 파일 무변경). 설치된 훅은 저장소 파일을 절대 경로로 실행하므로 `git pull`로 반영.
- 롤백: 해당 커밋 `git revert`. 요구사항·설계 문서의 v2 표기도 같은 커밋에 있어 함께 되돌아간다.

## 검증 방법

- `powershell -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1` — 추가 케이스만 실패하는 Red 실행 후 Green 실행(22/22). 결과는 이 작업의 work-log 검증 표(AC-07).
- 실세션 관찰: 이 저장소에서 새 세션 시작 시 `20260814-multiuser-workflow`가 재개 안내에 나타나지 않음(수동, 선택).

## 남은 위험

- 보류 작업을 잊을 위험 → `docs/status.md` 행과 사용자 지시 재개 조건으로 수용(대안 B 단점).
- 번호에 관한 주의: 보관 브랜치 `archive/202609-cycles`에는 DCR-006이 있고 DCR-007은 없다. 이 문서는 main 이력의 [결정 등록부](../../decisions.md) 기준 다음 번호다.

## 승인 기록

- 2026-10-09 — [REQ-DESIGN-worklog-diet v1](./req-design.md#승인-기록) 승인 관문에서 사용자 응답 "권장안 전체 승인"(Q-02 포함). 이 문서 `approved`, [REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md) 기준선 v2 발행.

## 변경 이력

| 날짜 | 변경 | 근거 | 상태 또는 기준선 | 작성자·승인자 |
|---|---|---|---|---|
| 2026-10-09 | 최초 작성 | 사이클 1 세션 인계(2026-10-09), `20260814-multiuser-workflow` on-hold 전환 후 관찰 | proposed | Claude(작성) |
| 2026-10-09 | 재승인, 요구사항·설계 기준선 v2 발행 | 사용자 승인(대화형 관문, Q-02 포함) | proposed → approved, v1 → v2 | 사용자(승인) |

## 인계

- 다음 단계 또는 워크플로우: wf-implement — 이 작업의 계획에 TASK로 포함(DES-08)
- 시작 조건: 충족(2026-10-09 승인)
- 입력 문서와 기준선: 위 문서 연결
- 완료된 항목: 변경 항목·영향·대안·검증 방법
- 미완료 항목: 구현·검증(AC-07), 추적 링크(문서 연결 verification 행)
- 차단 요인: 없음

# WORK-20261028-legacy-onboarding: 작업 기록 — 레거시 테스트 대장 편입·커버리지 기반 보호 스코프

> 문서 유형: `work-log, verification, completion`
> 작업 ID: `20261028-legacy-onboarding`
> 상태: `in-progress`
> 기준선: `N/A — 승인 전(wf-design 진행 중)`
> 작성일: 2026-10-28
> 최종 갱신: 2026-10-28
> 관련 문서: [REQ-DESIGN-legacy-onboarding](./req-design.md), [ST-llm-workflow](../../status.md), [테스트 액션 아이템](../../research/20261025-aidlc-trends/04_test_action_items.md)

## 요약

- 목적: v2 레거시 묶음 ①(04 R-13 대장 편입 + R-11 커버리지 기반 보호 스코프) 규칙의 wf-design·wf-implement 진행을 기록한다.
- 현재 결론 또는 상태: wf-design §4.1 조사 완료, 질문 단계 전.
- 다음 행동: [인계](#인계) 절.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | related | [ST-llm-workflow](../../status.md) | 작업 목록 | 이 작업의 행 |
| input | related | [테스트 액션 아이템](../../research/20261025-aidlc-trends/04_test_action_items.md) | R-13, R-11 | 입력(조사 트랙) |
| input | baseline | [REQ-DESIGN-legacy-onboarding](./req-design.md) | document | 초안(승인 전) |

## 기준선과 현재 계획

- 기준선: 없음 — [REQ-DESIGN-legacy-onboarding](./req-design.md) 초안 작성 중
- 계획: 없음 — 승인 후 plan.md

## 수행 기록

### 2026-10-28 — 착수와 §4.1 조사

- 발견 사항: 착수 HEAD `539c80c`, clean. `유지` 진입은 Green+`completed` 2회라 편입에 그대로 못 씀. `격리` 사유에 기존 실패 없음. 판독기 둘 다 `유지` 접두만 봄 → 괄호 분류 추가는 코드 무변경. `보호 스코프` `미확정` 규칙 없음(관련 행 판정 불가). wf-implement 2,850/2,850. 커버리지 도구 미설치.
- 결정과 이유: 사용자 요청 "진행시켜" — 이 저장소 할 일 1번. 외부 저장소 적용·측정은 범위 밖. 컨텍스트 임계 신호로 조사 경계에서 인계.
- 검증: 해당 없음 — 조사
- 결과: 완료 — 2026-10-28 01:05

### 2026-10-28 — 질문 단계와 초안

- 결정과 이유: 점검 7항목 중 범위·데이터에서 Q-01·03·04를 초안 전에 물음(구조 질문). 답 전부 권장안 — 독립 편입 작업(경량), `미확정` 행은 관련 행 아님, R-11은 편입 + 통합 관문 일부. Q-02·Q-05 후보는 가정 A-01·DES-03. C층 무변경이라 DCR 없음, ADR-023(ADR-009 확장).
- 검증: `lint_design.py` req-design exit 0
- 결과: 완료 — 2026-10-28 01:30

### 2026-10-28 — 적대 검토 1라운드

- 결정과 이유: 17건(중간 6·낮음 10·제안 1) 전부 수용. 핵심은 FR-03 제외의 수명(편입 시점 예외·`격리` 1:1·추가 금지·해제 시 제거)과 명령 셀 파이프 금지(판독 분할). `격리` 무보호는 RISK-06. 상세는 [req-design 적대 검토](./req-design.md#적대-검토).
- 검증: `lint_design.py` exit 0
- 결과: 완료 — 2026-10-28 01:50

## 설계와 달라진 점

없음 — 승인 전.

## 검증 결과

### 범위와 환경

- 대상 기준선 또는 구현: 없음 — 승인 전

### 결과 요약

- 총계: N/A — 승인 전

### 인수 조건별 결과

| 검증 ID | 인수 조건 | 방법·명령 | 결과 | 증거 |
|---|---|---|---|---|

### 실패와 미수행 분석

없음.

## 완료 보고

### 완료 상태

- 결과: TBD — 완료 보고 종결 시 기입

## 인계

- 다음 단계 또는 워크플로우: wf-design §8 승인 관문
- 시작 조건: 충족(적대 검토 2라운드 완료)
- 입력 문서와 기준선: [REQ-DESIGN-legacy-onboarding](./req-design.md) `awaiting-approval`, [ADR-023](./ADR-023-레거시-테스트-대장-편입.md) `proposed`
- 완료된 항목: §4.1 조사, 질문 단계, 초안·ADR-023, §4.5, 적대 검토 1라운드
- 미완료 항목: 승인
- 차단 요인: 없음
- 다음 행동: 승인 응답을 받아 승인 기록(req-design·ADR-023·decisions), 이후 wf-implement 계획. 미커밋 변경: req-design·ADR-023·work-log·`docs/decisions.md`.
- 재개 프롬프트: 작업 20261028-legacy-onboarding 재개 — docs/work/20261028-legacy-onboarding/work-log.md의 인계 절을 읽고 "다음 행동"부터 진행하라.

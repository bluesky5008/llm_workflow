# PLAN-20261026-component-deps: 구현 계획 — 기존 자산 대조·컴포넌트 의존 검사·설계 침식 점검

> 문서 유형: `plan`
> 작업 ID: `20261026-component-deps`
> 상태: `completed`
> 기준선: [REQ-DESIGN-component-deps](./req-design.md) `v1` (승인일 2026-10-27)
> 작성일: 2026-10-27
> 최종 갱신: 2026-10-27
> 관련 문서: [WORK-20261026-component-deps: 작업 기록](./work-log.md), [ADR-021](./ADR-021-컴포넌트-의존-표와-설계-린트.md), [DCR-022](./DCR-022-C층-공용-모듈과-의존-표-명시.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 승인된 v1(FR-01~09, DES-01~05)을 6개 TASK로 구현하고, 종결은 closing.md 순서를 따른다.
- 현재 결론 또는 상태: TASK-01~06 완료(6/6).
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-component-deps](./req-design.md) | FR-01~09, AC-01~08, DES-01~05 | v1 |
| input | decision | [ADR-021](./ADR-021-컴포넌트-의존-표와-설계-린트.md) | document | approved |
| input | change | [DCR-022](./DCR-022-C층-공용-모듈과-의존-표-명시.md) | 변경 항목 | approved, 명확화(v5 유지) |
| output | implementation | [WORK-20261026-component-deps](./work-log.md) | 수행 기록 | TASK별 결과 |

## 기준선

- 관련 요구사항: FR-01~09, NFR-01~06
- 관련 설계: DES-01~05
- 관련 ADR·DCR: [ADR-021](./ADR-021-컴포넌트-의존-표와-설계-린트.md), [DCR-022](./DCR-022-C층-공용-모듈과-의존-표-명시.md)

## 작업 정의

- 목표: `lint_design.py`(D1~D10)와 테스트, templates 의존 표, wf-design 본문(순증 0), 침식 점검 문항, C층 `docs/design.md` 적용.
- 범위: req-design [포함](./req-design.md#포함). 범위 밖: [제외](./req-design.md#제외).
- 가정: §3.1 재확인(2026-10-27) — HEAD `6535663`+미커밋(이 작업 문서·status·decisions만), `유지` 4행 통과(TST-01 56, TST-02 86(TST-04 16 포함), TST-05 15).
- 위험: 문서 TASK의 Red는 grep 기대 문구 부재로 대신한다(req-design 검증 전략). 어절 상쇄 실패 시 RISK-05.

## 계획 트리

<!-- generated: 2026-10-27 01:10 — scripts/render.py --view all -->

```text
[작업] 20261026-component-deps — 기존 자산 대조·컴포넌트 의존 검사·설계 침식 점검 ... completed (6/6)
├─ [✓] `lint_design.py`와 테스트 (DES-02) (TASK-01) ............ 2026-10-27 00:58
├─ [✓] templates 설계 템플릿 의존 표 (DES-01) (TASK-02) ........ depends: TASK-01  2026-10-27 01:01
├─ [✓] wf-design 본문 §4.1·§4.3·§4.5 (DES-03) (TASK-03) ........ depends: TASK-02  2026-10-27 01:03
├─ [✓] 침식 점검 문항 (DES-04) (TASK-04) ....................... depends: TASK-02  2026-10-27 01:04
├─ [✓] C층 `docs/design.md` 적용 (DES-05, DCR-022) (TASK-05) ... depends: TASK-01, TASK-02  2026-10-27 01:06
└─ [✓] 통합과 종결 (TASK-06) ................................... depends: TASK-01~05  2026-10-27 01:09
```

## 작업 목록

### TASK-01: `lint_design.py`와 테스트 (DES-02)

- 상태: completed
- 완료: 2026-10-27 00:58
- 상위: 없음
- 목표: D1~D10 검사, ID 펼침(범위·나열·링크), 추적표 없음 처리, 기본 대상·출력·exit 0/1/2
- 관련 요구사항과 설계: FR-04~06, NFR-02, DES-02, AC-03
- 변경 대상: `skills/wf-doc/scripts/lint_design.py`(신설), `skills/wf-doc/scripts/tests/test_lint_design.py`(신설)
- 의존성: 없음
- 위험: 추적표 표기 변형(RISK-03) — 동결 문서의 표기를 견본에 포함
- 검증 방법: Red — `test_lint_design.py` 먼저, 모듈 없음 실패 확인 후 구현. Green 후 TST-02
- 완료 조건: AC-03

### TASK-02: templates 설계 템플릿 의존 표 (DES-01)

- 상태: completed
- 완료: 2026-10-27 01:01
- 상위: 없음
- 목표: `## 컴포넌트와 책임` DES 표 아래 5열 골격과 노트 1개(양방향·`—`·ID 표기·소유 데이터·출처 3형식·`N/A`·외부 계약·`lint_design.py`)
- 관련 요구사항과 설계: FR-02·03, DES-01, AC-01·02
- 변경 대상: `skills/wf-doc/references/templates.md`
- 의존성: TASK-01(노트가 스크립트를 가리킴)
- 위험: wf-doc 본문 무변경(NFR-01)
- 검증 방법: Red — grep `| ID | 의존 | 피의존 | 소유 데이터 | 출처 |` 부재. Green 후 grep, `lint_skill.py`
- 완료 조건: AC-02, AC-01의 templates 항목

### TASK-03: wf-design 본문 §4.1·§4.3·§4.5 (DES-03)

- 상태: completed
- 완료: 2026-10-27 01:03
- 상위: 없음
- 목표: §4.1 재사용 후보 1항, §4.3 의존 관계 링크와 마지막 문단 축약, §4.5 의존 표 문항
- 관련 요구사항과 설계: FR-01·07, NFR-01·06, DES-03, AC-01·04
- 변경 대상: `skills/wf-design/SKILL.md`
- 의존성: TASK-02(링크 대상)
- 위험: 어절 순증(RISK-05)
- 검증 방법: Red — grep `재사용 후보 자산` 부재. Green 후 grep, `body_words` ≤ 2,174, K4
- 완료 조건: AC-01·04

### TASK-04: 침식 점검 문항 (DES-04)

- 상태: completed
- 완료: 2026-10-27 01:04
- 상위: 없음
- 목표: review-checklist "요구사항과 설계" 3문항과 대조 기준 1줄, verification-depth §5 1문장
- 관련 요구사항과 설계: FR-08, DES-04, AC-05
- 변경 대상: `skills/wf-implement/references/review-checklist.md`, `skills/wf-implement/references/verification-depth.md`
- 의존성: TASK-02(의존 표 링크)
- 위험: wf-implement 본문 무변경(AC-05)
- 검증 방법: Red — grep `의존 표에 없는 새 의존` 부재. Green 후 grep, `git diff --stat 6535663 -- skills/wf-implement/SKILL.md` 빈 출력
- 완료 조건: AC-05

### TASK-05: C층 `docs/design.md` 적용 (DES-05, DCR-022)

- 상태: completed
- 완료: 2026-10-27 01:06
- 상위: 없음
- 목표: DES-09 불릿·의존 표, 추적표 DES-09, 머리말·문서 연결·변경 이력(v5 유지)
- 관련 요구사항과 설계: FR-09, DES-05, AC-06
- 변경 대상: `docs/design.md`, DCR-022·등록부(상태 `completed`)
- 의존성: TASK-01(검사), TASK-02(형식)
- 위험: 의존 관계 오기 — 구현 시 `setup/hooks/*.ps1` grep 재확인
- 검증 방법: Red — `lint_design.py docs/design.md` 무출력(표 없음) 확인, 표 추가 후 exit 0·무출력
- 완료 조건: AC-06

### TASK-06: 통합과 종결

- 상태: completed
- 완료: 2026-10-27 01:09
- 상위: 없음
- 목표: 린트 3종, `유지` 전량, 대장 TST-02 보호 스코프·건수, 수동 뮤턴트 1~3개, 자체 리뷰(침식 점검 자기 적용), 재정비 관문, 완료 보고 관문, closing.md 종결
- 관련 요구사항과 설계: NFR-01~06, AC-07·08
- 변경 대상: `docs/test-register.md`, 이 작업 문서, `docs/status.md`, 05 머리말(필요 시)
- 의존성: TASK-01~05
- 위험: 없음
- 검증 방법: 린트 3종 기본 실행, `유지` 전량, `git diff --name-only <구현 SHA>`
- 완료 조건: AC-07·08

## 인계

- 다음 단계 또는 워크플로우: 없음
- 완료된 항목: 계획, TASK-01~06
- 미완료 항목: 없음
- 다음 행동: 없음

## 변경 이력

| 날짜 | 변경 내용 | 근거 | 상태 전이 | 작성·승인 |
|---|---|---|---|---|
| 2026-10-27 | 최초 작성 — TASK-01~06 | REQ-DESIGN-component-deps v1 | → in-progress | Claude(작성) |
| 2026-10-27 | TASK-01~05 completed | 작업 기록 수행 기록 | in-progress 유지 | Claude(작성) |
| 2026-10-27 | TASK-06 completed, 작업 종결 | 작업 기록 완료 보고, 구현 커밋 `59c46a1` | in-progress → completed | Claude(작성) |

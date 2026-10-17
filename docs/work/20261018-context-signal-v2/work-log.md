# WORK-20261018-context-signal-v2: 작업 기록 — 컨텍스트 임계 신호 v3와 재개 경량화

> 문서 유형: `work-log, verification, completion`
> 작업 ID: `20261018-context-signal-v2`
> 상태: `completed`
> 기준선: `v3` ([DESIGN-llm-workflow](../../design.md)·[REQ-llm-workflow](../../requirements.md), 2026-10-18 승인, [DCR-013](./DCR-013-컨텍스트-신호-v3-재개-경량화.md))
> 작성일: 2026-10-18
> 최종 갱신: 2026-10-18
> 관련 문서: [DCR-013](./DCR-013-컨텍스트-신호-v3-재개-경량화.md), [ADR-012](./ADR-012-컨텍스트-신호-usage-파싱.md), [DESIGN-llm-workflow](../../design.md), [REQ-llm-workflow](../../requirements.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 임계 훅의 신호를 transcript usage 파싱으로 교체하고(ADR-012), 세션 재개의 읽기 범위를 규정해 인계 고정비를 줄인다(DCR-013).
- 현재 결론 또는 상태: 완료(2026-10-18 01:55) — DCR-013 승인, 기준선 v3, 구현·검증(Windows PS 5.1 29/29) 완료. 커밋·push는 사용자 지시(2026-10-18 01:46)에 따라 사용자 측에서 실행.
- 다음 행동: 없음

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | change | [DCR-013](./DCR-013-컨텍스트-신호-v3-재개-경량화.md) | 변경 항목, 검증 방법 | 이 작업의 범위를 정의 |
| input | decision | [ADR-012](./ADR-012-컨텍스트-신호-usage-파싱.md) | document | `approved`(2026-10-18) |
| input | baseline | [DESIGN-llm-workflow](../../design.md#컴포넌트와-책임) | DES-02 | v3(2026-10-18) |
| input | related | [ST-llm-workflow](../../status.md) | 작업 목록 | 행 추가(2026-10-18) |

## 기준선과 현재 계획

- 기준선: [DESIGN-llm-workflow v3](../../design.md)·[REQ-llm-workflow v3](../../requirements.md), [ADR-012](./ADR-012-컨텍스트-신호-usage-파싱.md), [DCR-013](./DCR-013-컨텍스트-신호-v3-재개-경량화.md)
- 계획: 별도 `plan.md` 없음 — 작업 단위가 DCR-013 변경 항목 표 1개이고 구현이 승인 시점에 이미 프로토타입으로 완료되어 있어, 남은 TASK는 "Windows 검증·완료 보고" 하나다(wf-implement §3.2 트리 생략 조건 충족).

## 수행 기록

### 2026-10-18 — wf-design (원인 분석·DCR·ADR·프로토타입)

- 발견 사항: transcript 바이트/토큰 비율이 작업 유형 의존(Edit `originalFile`, Read 이중 기록, thinking). 훅 입력에 사용량 필드 없음(문서 재확인). assistant 줄 `message.usage`가 실제 프롬프트 크기.
- 결정과 이유: 신호를 usage 파싱으로 교체하고 바이트는 폴백(ADR-012 대안 E). 재개 읽기 범위를 references로 규정(DCR-013 R2) — 본문 어절 상한 때문에 포인터만 본문에.
- 검증: `setup/hooks/tests/run-tests.ps1` pwsh 7.4(Linux) — Red 21/29(T22·T24~T28 실패) → Green 27/29(T19·T21은 경로 구분자 환경 실패). 파싱 4~74ms(5MB 합성 transcript).
- 결과: 부분 완료 — 2026-10-18 01:40 (승인 대기)

### 2026-10-18 — 재승인·기준선 v3 발행

- 결정과 이유: 사용자 승인("좋은 제안입니다. 승인하겠습니다."). design-change §5 승인 절차 1~6 수행 — DCR-013·ADR-012 `approved`, ADR-001 `superseded`(본문 무수정), REQ·DESIGN v3(가정·Q-01·RISK-02·AC-02 / DES-02·제약·데이터·RISK-05·검증 전략), decisions.md.
- 검증: 링크·앵커 검사 0 깨짐(신규·수정 문서), `lint_worklog.py`·`lint_skill.py` 0 오류
- 결과: 완료 — 2026-10-18 01:50

### 2026-10-18 — Windows 검증·통합

- 결정과 이유: 사용자가 Windows PS 5.1에서 훅 테스트 실행(`passed: 29  failed: 0`) → VER-04 환경 실패 해소. 재정비 관문: 변경 없음(아래 테스트 대장 변경). 커밋·push는 사용자 지시로 사용자 측 실행 — 이 세션은 사용자 컴퓨터의 셸이 없어 명령을 제공.
- 검증: TST-01 Windows 29/29(사용자 실행). TST-02·04·05는 pytest 미설치 환경이라 대체 러너로 59/62(capsys 의존 3건 미수행, 린트·렌더 코드 무변경).
- 결과: 완료 — 2026-10-18 01:55

## 설계와 달라진 점

- 없음(기준선 변경 자체가 이 작업의 대상 — DCR-013).

## 검증 결과

### 범위와 환경

- 대상 기준선 또는 구현: 기준선 v3 구현(워킹트리, 미커밋)
- 실행 환경: (a) Windows PowerShell 5.1, 사용자 실행(2026-10-18 01:46) — 정본. (b) pwsh 7.4.6 / Linux 컨테이너(개발 중 Red→Green). (c) Python 테스트는 pytest 미설치 컨테이너에서 대체 러너
- 제외 항목: 실세션 관찰(ADR-012 후속 작업)

### 결과 요약

- 총계: 29 (성공 29 / 실패 0 / 미수행 0) — Windows PS 5.1. 보조: Python 대장 묶음 62 중 59 성공·3 미수행(러너 제약)
- 기준: 워킹트리 dirty(미커밋), HEAD `main` — 커밋 후 clean 재실행으로 대장 SHA 갱신 필요
- 명령: `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1`(Windows, 사용자) · `python -m pytest skills/wf-doc/scripts/tests -q`·`skills/wf-tree/scripts/tests -q`(대체 러너)
- 커버리지: N/A — 셸 스크립트 계약 테스트
- 산출물: 없음

### 인수 조건별 결과

| 검증 ID | 인수 조건 | 방법·명령 | 결과 | 분류 | 증거 |
|---|---|---|---|---|---|
| VER-01 | AC-02(usage 신호) | T22~T28 | 성공 | — | Red 6건 실패 → Green 7/7 |
| VER-02 | AC-02(폴백 회귀) | T07~T13 | 성공 | — | 기존 케이스 무수정 통과 |
| VER-03 | AC-04 fail-open | T06·T12 | 성공 | — | 무출력·exit 0 |
| VER-04 | AC-03 설치 | T18~T21 | 성공 | — | Windows PS 5.1 29/29(2026-10-18 01:46, 사용자 실행). Linux에서의 T19·T21 실패는 경로 구분자 환경 원인으로 확인됨 |
| VER-05 | 대장 `유지` 행 회귀(TST-02·04·05) | 대체 러너 | 성공 | — | 59/62, capsys 의존 3건 미수행. 해당 코드 무변경 |

### 실패와 미수행 분석

- T19·T21(개발 중 Linux 실행): `Test-WfOwnEntry`의 `\\setup\\hooks\\` 패턴이 Linux 경로와 불일치 — 환경 원인, Windows 29/29로 해소 확인.
- TST-02·04·05의 3건 미수행: 컨테이너에 pytest가 없어(패키지 저장소 차단) 대체 러너 사용, `capsys` 픽스처 미지원. 린트·렌더 코드는 이 작업에서 무변경. 커밋 후 Windows clean 재실행으로 대장 SHA를 갱신한다(후속 작업).

### 테스트 대장 변경

| 대상 | 현재 상태 → 제안 | 분류·증거 | 유일 검증 여부 | 승인 |
|---|---|---|---|---|
| TST-01 | 유지 → 유지(보호 스코프 확장: T22~T28 usage 신호 7건, 총 29건) | 등록 — Windows 29/29 | — | 등록(승인 불요) |
| 재정비 관문 | — | Breaking 0(TST-01 29/29) · Stale 0 · Missing 0(새 동작은 T22~T28이 보호). 폐기·병합 후보 0 | — | 완료 보고 관문(변경 없음 보고) |

## 완료 보고

### 완료 상태

- 결과: 완료
- 완료 판단 근거: DCR-013 변경 항목 전부 반영, AC-02(usage·폴백)·AC-03·AC-04 검증 성공, 린트 0 오류, 기준선 v3 문서 일관. wf-implement §5 조건 충족(커밋은 사용자 범위).

### 주요 변경

- 훅: `wf-context-threshold.ps1` 2단 신호(usage 토큰 1차·바이트 폴백·`signal=` 표기), `wf-common.ps1` `Get-WfContextTokens`·상태 파일 `lastWarnedTokens`.
- 테스트: T22~T28(픽스처 3함수) 추가, 29건.
- 스킬: `wf-implement/references/session-resume.md` 신설(재개 최소 읽기 집합), SKILL.md 포인터 3곳, wf-doc 인계 블록 자기완결 형식, 훅 메시지 2개 정정.
- 문서: REQ·DESIGN v3, ADR-012 승인·ADR-001 대체, DCR-013, decisions·status·test-register·README.

### 통합 상태

- 로컬 사본에 완결 반영. 커밋·push는 사용자 지시(01:46)로 사용자 측 실행 — 명령은 대화형 보고에 제공. 설치된 훅은 절대 경로로 저장소 파일을 실행하므로 다음 세션부터 적용.

### 남은 위험과 제한

- [DCR-013 남은 위험](./DCR-013-컨텍스트-신호-v3-재개-경량화.md#남은-위험) 참조. 추가: TST-02·04·05는 이번 사이클에서 pytest 정식 실행이 없었다(코드 무변경).

### 후속 작업

- 커밋 후 Windows clean 워킹트리에서 TST-01·02·04·05 재실행 → `docs/test-register.md` 마지막 성공 SHA 갱신(사용자 또는 다음 세션, wf-implement §3.4 3튜플).
- 실세션 2주 관찰 후 `CLAUDE_WF_THRESHOLD_TOKENS` 기본값 1회 보정([ADR-012 후속 작업](./ADR-012-컨텍스트-신호-usage-파싱.md#후속-작업)).
- Claude Code 훅 입력에 사용량 필드가 생기면 파싱을 그 필드로 교체하는 ADR.

## 인계

- 다음 단계 또는 워크플로우: 없음
- 완료된 항목: 원인 분석, ADR-012·DCR-013 승인, REQ·DESIGN v3, 구현(훅·테스트·references·메시지·templates·README), 검증(Windows 29/29), 테스트 대장 갱신
- 미완료 항목: 없음
- 다음 행동: 없음

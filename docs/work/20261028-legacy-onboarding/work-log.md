# WORK-20261028-legacy-onboarding: 작업 기록 — 레거시 테스트 대장 편입·커버리지 기반 보호 스코프

> 문서 유형: `work-log, verification, completion`
> 작업 ID: `20261028-legacy-onboarding`
> 상태: `completed`
> 기준선: `[REQ-DESIGN-legacy-onboarding](./req-design.md) v1` (승인일 2026-10-28)
> 작성일: 2026-10-28
> 최종 갱신: 2026-10-28
> 관련 문서: [REQ-DESIGN-legacy-onboarding](./req-design.md), [ST-llm-workflow](../../status.md), [테스트 액션 아이템](../../research/20261025-aidlc-trends/04_test_action_items.md)

## 요약

- 목적: v2 레거시 묶음 ①(04 R-13 대장 편입 + R-11 커버리지 기반 보호 스코프) 규칙의 wf-design·wf-implement 진행을 기록한다.
- 현재 결론 또는 상태: 완료(2026-10-28) — TASK-01~06, AC-01~08 성공, 구현 커밋 `a5577b4`.
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | related | [ST-llm-workflow](../../status.md) | 작업 목록 | 이 작업의 행 |
| input | related | [테스트 액션 아이템](../../research/20261025-aidlc-trends/04_test_action_items.md) | R-13, R-11 | 입력(조사 트랙) |
| input | baseline | [REQ-DESIGN-legacy-onboarding](./req-design.md) | FR-01~07, DES-01~05 | v1 |
| input | implementation | [PLAN-20261028-legacy-onboarding](./plan.md) | TASK-01~06 | 현재 계획 |

## 기준선과 현재 계획

- 기준선: [REQ-DESIGN-legacy-onboarding](./req-design.md) v1, [ADR-023](./ADR-023-레거시-테스트-대장-편입.md)
- 계획: [PLAN-20261028-legacy-onboarding](./plan.md) TASK-01~06 완료

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

### 2026-10-28 — §3.1 재확인과 계획

- 발견 사항: HEAD `739fe6b` clean, `30b01fc` 이후 변경은 `docs/`만. 대상 파일 구조가 req-design 서술과 일치 — 기준선 적용 가능. `lint_skill.py` 경고만.
- 결정과 이유: `유지` SHA ≠ HEAD라 전량 재실행. TST-01 명령(`-ExecutionPolicy Bypass`)은 자동 모드 분류기가 거부 — 우회하지 않고 미수행, 사용자 판단 대기. TASK-01(특성화)을 먼저 둬 판독 무변경을 문서 변경 전에 고정. 트리 사용(6 TASK·의존).
- 검증: TST-02 105 passed(TST-04 포함), TST-04 16, TST-05 16 — `739fe6b` clean, 01:23, 대장 명령 그대로. TST-01 미수행.
- 결과: 완료 — 2026-10-28 01:25

### 2026-10-28 — TASK-01

- 결정과 이유: 인라인 견본 3행(`유지`+명령줄 제외·`미확정`, `격리(기존 실패, …)`+파이프 없는 실패 메시지, `격리(불일치, …)`). `유지` 행 glob을 `tests/unit/*.py`로 둬 `격리` 파일과 겹치지 않게 함(fnmatch `*`는 `/`도 매칭). 공유 견본 무변경.
- 검증: TST-02 106 passed ×2(`739fe6b`+dirty, 01:27). 단언 실패 가능성 — `kept` 변형 2종 메모리 적용: `not 폐기` killed, `'유지' in` survived(이 입력에서 동치).
- Red: 해당 없음 — 특성화(판독 무변경 고정, DES-05)
- 결과: 완료 — 2026-10-28 01:28

### 2026-10-28 — TASK-02

- 결정과 이유: 노트 3곳 — `보호 스코프` `미확정` 불릿·모든 셀 파이프 금지 불릿 신설(`마지막 성공` 앞), `상태` 예에 `격리(기존 실패, …)`, 재정비 기록 불릿에 시점 `편입`·`승인` 값. `미확정`·편입은 verification-depth §1·§7로 링크.
- 검증: grep 5문구 각 1건. `lint_skill.py` K4 앵커 없음 1건(`#7-대장-편입`) — TASK-03에서 대상 절 생성으로 해소 예정.
- Red: `grep -c 격리(기존 실패 templates.md` · 739fe6b+dirty · 0건
- 결과: 완료 — 2026-10-28 01:29

### 2026-10-28 — TASK-03

- 결정과 이유: (a) §7 — 불릿 4개 + 2회 결과 3분기 표 + 불릿 4개. 불일치 행 `마지막 성공`은 `없음 — 편입 2회 불일치`(3형식 안, FR-02 미정 칸의 표기). 도구는 예시 3종만(NFR-03). (b) §2 `유지` 허용 시점·`격리` 의미·진입, 표 아래 `격리` 통합 실행 1문장. (c) §1 관련 행 문단 끝 2문장. (d) §3 새 순서 2, 기존 2·3 → 3·4(번호 참조처 grep 0건).
- 검증: AC-01~03 문구 grep 각 ≥1. `lint_skill.py` 오류 0 — TASK-02의 K4 앵커 해소.
- Red: `grep -c '## 7. 대장 편입' verification-depth.md` · 739fe6b+dirty · 0건
- 결과: 완료 — 2026-10-28 01:30

### 2026-10-28 — TASK-04

- 결정과 이유: §3.1 불릿을 질문(빌드 상태 포함)은 두고 재실행 조건 서술을 §1 재개 행 링크 + "재개가 아니어도"로 갈음, 편입 링크 추가(DES-03). 이관 불필요.
- 검증: `lint_skill.py` 오류 0, wf-implement 본문 2,849어절(2,850 → 순증 −1). grep `#7-대장-편입` 1건.
- Red: `grep -c '#7-대장-편입' skills/wf-implement/SKILL.md` · 739fe6b+dirty · 0건
- 결과: 완료 — 2026-10-28 01:30

### 2026-10-28 — TASK-05

- 결정과 이유: §1 예 목록 끝에 편입 1항과 §7 링크(DES-04).
- 검증: grep `대장 편입` 1건, `lint_skill.py` 오류 0. 시각 정정 — TASK-02·03 완료 시각을 처음에 실제보다 늦게(01:31·01:36) 적어 `date` 확인 후 01:29·01:30으로 고침.
- Red: `git show HEAD:skills/wf-design/references/lightweight-path.md | grep -c 대장 편입` · 739fe6b · 0건(편집 전 내용 = HEAD)
- 결과: 완료 — 2026-10-28 01:30
- 전이 실행: TASK-02~05 `completed` 전이분 `유지` 재실행 — TST-02 106·TST-04 16·TST-05 16 통과(`739fe6b`+dirty, 01:31). TST-01 미수행(권한). `regression_guard.py`·`setup/hooks/` diff 0.

### 2026-10-28 — TASK-06 통합 검증·자체 리뷰

- 발견 사항: 재개 상태가 인계 절과 일치(HEAD `739fe6b`). TST-01 대장 명령은 자동 모드 분류기가 4회 거부 — 명령 변경은 별개 검증(§3.4)이라 우회 안 함.
- 결정과 이유: 자체 리뷰 전 항목 — 문서 4·테스트 1만 변경, 새 코드·의존·범위 밖 변경 없음, 수정 없음. 뮤테이션 대상 코드 0. 관문 순서 2는 커버리지 도구 미설치로 생략. 관문 응답 "모두 승인"(01:42) — TST-02 105→106, 커밋·push.
- 검증: 린트 3종 오류 0, TST-02 106·TST-04 16·TST-05 16(01:38), TST-01 56/56(사용자 터미널, 01:42), TST-03 3/8(`격리`), 가드 diff 0 — `739fe6b`+dirty.
- Red: 해당 없음 — 통합
- 결과: 완료 — 2026-10-28 01:49
- 종결: ① `a5577b4` → ② clean TST-02 106·TST-04 16·TST-05 16(01:45), TST-01 56(사용자 터미널, 01:47)

## 설계와 달라진 점

없음.

## 검증 결과

### 범위와 환경

- 대상 기준선 또는 구현: [REQ-DESIGN-legacy-onboarding](./req-design.md) v1, [ADR-023](./ADR-023-레거시-테스트-대장-편입.md), TASK-01~05
- 실행 환경: Windows 11, Python 3.14.2, pytest, PowerShell 5.1(TST-01은 자동 모드 분류기 거부로 사용자 터미널에서 실행)
- 제외 항목: TST-03(`격리`, 기존·무관 — 결과만 기록)

### 결과 요약

- 총계: 178 (성공 178 / 실패 0 / 미수행 0) — `유지` 4행(TST-04 16건은 TST-02 106건에 포함, 중복 집계 안 함)
- 기준: `739fe6b` · 워킹트리 dirty(통합 01:38, TST-01은 사용자 실행 01:42경)
- 명령:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1` 56/56(사용자 실행)
  - `python -m pytest skills/wf-doc/scripts/tests -q` 106
  - `python -m pytest skills/wf-doc/scripts/tests/test_lint_skill.py -q` 16
  - `python -m pytest skills/wf-tree/scripts/tests -q` 16
  - `python docs/presentation/tests/test_make_pptx.py` 3/8(`격리`, 완료 판정 제외)
- 커버리지: N/A — 커버리지 도구 미설치
- 뮤테이션: N/A — 착수 SHA `539c80c` 이후 바뀐 코드 파일 없음(스킬 문서·테스트만, `regression_guard.py` 무변경)
- 산출물: 없음

### 인수 조건별 결과

| 검증 ID | 인수 조건 | 방법·명령 | 결과 | 분류 | 증거 |
|---|---|---|---|---|---|
| VER-01 | AC-01 | grep verification-depth §7 문구, 도구명 문맥 | 성공 | — | TASK-03 · 도구명은 `예:` 괄호 안 1곳 |
| VER-02 | AC-02 | grep §1 `미확정`·뮤테이션, §2 표 `편입`·`기존 실패`·`격리` 통합 실행 | 성공 | — | TASK-03 |
| VER-03 | AC-03 | grep §3 순서 2 | 성공 | — | TASK-03 |
| VER-04 | AC-04 | grep templates 4문구 | 성공 | — | TASK-02 |
| VER-05 | AC-05 | grep §3.1 `#7-대장-편입`, `lint_skill.py` | 성공 | — | TASK-04 · 2,849어절 · 오류 0(01:38) |
| VER-06 | AC-06 | grep lightweight-path `대장 편입` | 성공 | — | TASK-05 |
| VER-07 | AC-07 | `python -m pytest skills/wf-doc/scripts/tests -q` | 성공 | — | `test_onboarding_notation_protects_only_kept_rows` · 106 passed · `739fe6b`+dirty 01:38 |
| VER-08 | AC-08 | `유지` 4행, `git diff --stat 739fe6b -- skills/wf-doc/scripts/regression_guard.py setup/hooks/`, `lint_design.py`·`lint_worklog.py` | 성공 | — | TST-01 56/56(사용자 실행, `739fe6b`+dirty) · TST-02 106 · TST-05 16 · diff 빈 출력 · 린트 exit 0 |

### 실패와 미수행 분석

- 실패·미수행 없음.
- TST-01은 `-ExecutionPolicy Bypass` 명령이 자동 모드 분류기에 거부되어(2026-10-28 4회) 사용자가 같은 명령을 자기 터미널에서 실행하고 출력을 붙여 넣었다 — 명령 무변경이라 3튜플 유지.
- 재정비 관문 순서 2: 커버리지 도구 미설치로 생략 — `미확정` 행도 없음.

### 테스트 대장 변경

| 대상 | 현재 상태 → 제안 | 분류·증거 | 유일 검증 여부 | 승인 |
|---|---|---|---|---|
| TST-02 | `유지` 105 → `유지` 106, 보호 스코프에 편입 표기 판독 특성화 추가 | Missing 1(DES-05) → `test_regression_guard.py` 인라인 견본 1건 추가, 공유 견본·기존 단언 무변경. Breaking 0 · Stale 0 | AC-07의 유일 검증 | 완료 보고 관문(2026-10-28 01:42 "모두 승인") |
| 관문 요약 | 변경이 닿은 행 TST-02만(TST-01·04·05 보호 스코프 무변경) | Breaking 0 · Stale 0 · Missing 1(위 행). 커버리지 재계산 생략(도구 없음). 폐기·병합 후보 0 | — | 완료 보고 관문(2026-10-28 01:42 "모두 승인") |

## 완료 보고

### 완료 상태

- 결과: 완료
- 완료 판단 근거: AC-01~08 성공, `유지` 4행 통과(`a5577b4` clean), 린트 3종 0 오류, 재정비 관문 승인

### 주요 변경

- verification-depth §7 대장 편입 신설, §1 `미확정`·뮤테이션, §2 `유지` 편입·`격리` 기존 실패, §3 순서 2 커버리지 재계산
- templates 테스트 대장 노트(`미확정`·`격리(기존 실패, …)`·파이프 금지·시점 `편입`)
- wf-implement §3.1 편입 링크(2,849어절), lightweight-path 편입 예시
- `test_regression_guard.py` 편입 표기 판독 특성화 1건(TST-02 106), ADR-023 `approved`

### 통합 상태

- 구현 커밋 `a5577b4`, 이 종결 커밋과 함께 origin push 대상(승인 2026-10-28 01:42, 완료 보고 관문 "모두 승인"). 설치본은 저장소 심볼릭 링크라 동기화 불필요

### 남은 위험과 제한

- 편입 절차·커버리지 재계산은 이 저장소에서 실제로 적용되지 않았다 — 대장 밖 기존 테스트가 없고 커버리지 도구도 없다. 외부 코드 저장소 첫 적용에서 검증된다.
- `격리` 행은 보호를 받지 않는다(RISK-06). 판독기 무변경이라 표기 오류(파이프 등)는 린트가 잡지 않는다.
- TST-01은 자동 모드 분류기가 Bypass 명령을 거부해 사용자 터미널 실행에 의존한다.

### 후속 작업

- 기존 코드 저장소 적용 첫날 편입 실행과 비용·`격리` 건수 기록(04 레거시 묶음 ①의 적용 단계), 이어서 레거시 묶음 ②(R-14~R-16)
- TST-01 실행 경로 — 권한 규칙 또는 분류기 허용 방법 검토

## 인계

- 다음 단계 또는 워크플로우: 없음
- 완료된 항목: TASK-01~06, AC-01~08, ADR-023 `approved`
- 미완료 항목: 없음
- 다음 행동: 없음

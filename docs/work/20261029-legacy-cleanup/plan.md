# PLAN-20261029-legacy-cleanup: 구현 계획 — 독립 재정비 작업·`리팩터` 처분·대량 승인 계층화 규칙

> 문서 유형: `plan`
> 작업 ID: `20261029-legacy-cleanup`
> 상태: `in-progress`
> 기준선: [REQ-DESIGN-legacy-cleanup](./req-design.md) `v1` (승인일 2026-10-29)
> 작성일: 2026-10-29
> 최종 갱신: 2026-10-29
> 관련 문서: [WORK-20261029-legacy-cleanup: 작업 기록](./work-log.md), [ADR-024](./ADR-024-독립-재정비-작업과-리팩터-표기.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 승인된 v1(FR-01~09, DES-01~05)을 5개 TASK로 구현하고, 종결은 closing.md 순서를 따른다.
- 현재 결론 또는 상태: TASK-01~04 완료(2026-10-29 21:47) — TASK-05 통합 pending.
- 다음 행동: TASK-05.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-legacy-cleanup](./req-design.md) | FR-01~09, AC-01~06, DES-01~05 | v1 |
| input | decision | [ADR-024](./ADR-024-독립-재정비-작업과-리팩터-표기.md) | document | approved |
| output | implementation | [WORK-20261029-legacy-cleanup](./work-log.md) | 수행 기록 | TASK별 결과 |

## 기준선

- 관련 요구사항: FR-01~09, NFR-01~03
- 관련 설계: DES-01~05
- 관련 ADR·DCR: [ADR-024](./ADR-024-독립-재정비-작업과-리팩터-표기.md). DCR 없음(C층 무변경)

## 작업 정의

- 목표: 독립 재정비 작업 규칙(`verification-depth.md` §8 신설, §2·§3 보강), 템플릿 노트 3곳(templates), 본문 포인터(wf-implement §3.3·§3.6, wf-design §4.2), 판독 무변경의 특성화 테스트.
- 범위: req-design [범위](./req-design.md#범위)의 포함. 범위 밖: 같은 절의 범위 밖.
- 가정: §3.1 재확인(2026-10-29 21:29) — HEAD `8184b5c` clean, `a5577b4` 이후 변경은 `docs/`와 wf-implement SKILL.md 중복 문장 정리(`e1ffa64`)뿐. `유지` 재실행 TST-01 56·TST-04 16·TST-05 16 통과. TST-02는 pytest tmp가 C:일 때 `test_main_exit_codes` 1건 환경 실패(드라이브 교차 `relpath`), tmp 루트를 D:로 두면 106 통과 — [작업 기록](./work-log.md#수행-기록) 참조. pytest·hypothesis는 사용자 Python 3.13에 이번에 설치.
- 위험: 문서 TASK의 Red는 grep 기대 문구 부재로 대신한다. wf-implement 본문 여유 57어절·wf-design 131어절 — TASK-04에서 넘치면 중복 문장 이관(NFR-01). TST-02 환경 실패는 통합에서 tmp 루트 D:로 재실행해 전량 통과를 확인한다.

## 계획 트리

<!-- generated: 2026-10-29 21:48 — scripts/render.py --view all -->

```text
[작업] 20261029-legacy-cleanup — 독립 재정비 작업·`리팩터` 처분·대량 승인 계층화 규칙 ... in-progress (4/5)
├─ [✓] 판독 특성화 테스트 (DES-04) (TASK-01) ... 2026-10-29 21:42
├─ [✓] templates 노트 (DES-02) (TASK-02) ....... 2026-10-29 21:44
├─ [✓] 재정비 규칙 (DES-01) (TASK-03) .......... depends: TASK-02  2026-10-29 21:46
├─ [✓] 본문 포인터 (DES-03·05) (TASK-04) ....... depends: TASK-03  2026-10-29 21:47
└─ [ ] 통합과 종결 (TASK-05) ................... depends: TASK-01~04
```

## 작업 목록

### TASK-01: 판독 특성화 테스트 (DES-04)

- 상태: completed
- 완료: 2026-10-29 21:42
- 상위: 없음
- 목표: `test_regression_guard.py`에 tmp git 픽스처 재사용 1건 — `비고`에 `리팩터(…)`가 있는 `유지` 행의 테스트 파일 변경과 다른 행의 `유지 → 폐기` 축소를, 열린 작업 기록 `### 테스트 대장 변경`에 `유지 → 유지(리팩터)`·`유지 → 폐기` 행으로 기록하면 exit 0, 기록이 없으면 exit 1
- 관련 요구사항과 설계: NFR-02, DES-04, AC-05
- 변경 대상: `skills/wf-doc/scripts/tests/test_regression_guard.py`(공유 견본·기존 케이스 무변경)
- 의존성: 없음 — 표기는 req-design FR-04·FR-06에 확정되어 templates 편집을 기다리지 않는다. 파일·심볼 겹침 없음
- 위험: 대장 TST-02 `유지` 테스트 파일 수정이라 `### 테스트 대장 변경`에 106→107 기록 필수(가드). 기존 `test_changed_test_file_with_record_passes`와 겹치지 않게 `리팩터` 비고·`폐기` 축소 둘을 한 견본에서 함께 본다
- 검증 방법: Red `해당 없음 — 특성화`(판독 무변경 고정). 단언이 실패할 수 있음은 같은 테스트에서 기록 제거 시 exit 1로 보인다. Green 후 TST-02 107 ×2(tmp 루트 D:)
- 완료 조건: AC-05

### TASK-02: templates 노트 (DES-02)

- 상태: completed
- 완료: 2026-10-29 21:44
- 상위: 없음
- 목표: 요구사항 노트 1불릿(재정비 작업의 `### 대상 TST 범위·배치·성공 기준` 필수 절, §8 링크), 작업 기록 `### 테스트 대장 변경` 예시 행 `유지 → 유지(리팩터)`(유일 검증 `해당 없음`, 승인 `배치 1 승인(2026-01-03, "전부")`), 테스트 대장 노트에 `비고` `리팩터(분류, 일시)`·재정비 기록 시점 `재정비 작업`
- 관련 요구사항과 설계: FR-01·04·06·07·09, DES-02, AC-03
- 변경 대상: `skills/wf-doc/references/templates.md`(요구사항 노트·작업 기록 예시·테스트 대장 노트)
- 의존성: 없음 — §8 링크 앵커는 재정비 규칙 작업이 만들며 링크 검사는 통합의 `lint_skill`에서
- 위험: wf-doc 본문 무변경(K3 2,337/2,350). 예시 행에 파이프 문자 없음
- 검증 방법: Red — grep `유지 → 유지(리팩터)` 부재. Green 후 grep 4문구, `lint_skill.py`
- 완료 조건: AC-03

### TASK-03: 재정비 규칙 (DES-01)

- 상태: completed
- 완료: 2026-10-29 21:46
- 상위: 없음
- 목표: (a) `## 8. 독립 재정비 작업` 신설 — FR-01~03·06·07(형태·필수 절 4요소·D-6 정본·분리 행 범위·제품 코드 동결·배치 절차 (a)~(h)·성공 기준 5항과 항목별 복구·승인 계층·기록). (b) §2 표 `병합`·`폐기` 허용 시점에 「독립 재정비 작업(§8)」, 재생성 문장 뒤에 `리팩터` 단락(FR-04). (c) §3 첫 문장 시점에 배치 추가, 4조건 표 `유일 검증 아님`에 FR-05, `사용자 승인`에 §8 계층 포인터 — `증거` 행 무변경
- 관련 요구사항과 설계: FR-01~07, NFR-03, DES-01, AC-01·02
- 변경 대상: `skills/wf-implement/references/verification-depth.md`
- 의존성: TASK-02(표기·템플릿 링크)
- 위험: 특정 도구 의무 문구 금지(NFR-03). 본문(§3.6 「완료 보고 관문 일괄」)과 다르면 본문 우선이므로 TASK-04 전까지는 §8 승인 단위가 본문과 어긋난 상태 — 같은 커밋에 묶는다
- 검증 방법: Red — grep `## 8. 독립 재정비 작업` 부재. Green 후 AC-01·02 문구 grep, 도구명 grep이 예시 문맥에만 있음, `lint_skill.py`
- 완료 조건: AC-01, AC-02

### TASK-04: 본문 포인터 (DES-03·05)

- 상태: completed
- 완료: 2026-10-29 21:47
- 상위: 없음
- 목표: wf-implement §3.3 금지문에 독립 재정비 작업 예외 링크, §3.6 끝에 승인 단위·반영 시점이 다름을 말하는 §8 포인터 1문장; wf-design §4.2 「측정 가능한 인수 조건」 뒤 재정비 작업 필수 절 1문장
- 관련 요구사항과 설계: FR-08·09, NFR-01, DES-03·05, AC-04
- 변경 대상: `skills/wf-implement/SKILL.md`, `skills/wf-design/SKILL.md`(넘치면 이관 대상 references 1곳)
- 의존성: TASK-03(링크 대상 §8)
- 위험: 어절 순증(NFR-01) — wf-implement 여유 57, wf-design 131
- 검증 방법: Red — grep `독립 재정비 작업` 부재(두 SKILL.md). Green 후 grep, `lint_skill.py` 오류 0·본문 ≤ 2,850·≤ 2,300
- 완료 조건: AC-04

### TASK-05: 통합과 종결

- 상태: pending
- 상위: 없음
- 목표: 린트 3종, `유지` 전량(TST-01 포함, TST-02는 tmp 루트 D:), 대장 TST-02 보호 스코프 106→107, 자체 리뷰, 재정비 관문(변경 없음 1행), 완료 보고 관문, closing.md 종결
- 관련 요구사항과 설계: NFR-01~03, AC-06
- 변경 대상: `docs/test-register.md`, 이 작업 문서, `docs/status.md`, 04 머리말(필요 시)
- 의존성: TASK-01~04
- 위험: TST-02 환경 실패(tmp C:)를 통합 증거에 남기고 D: 루트로 통과를 확인 — 제외·수정하지 않는다
- 검증 방법: `lint_design.py`·`lint_skill.py`·`lint_worklog.py` 기본 실행, `유지` 전량, `git diff --stat 8184b5c -- skills/wf-doc/scripts/regression_guard.py setup/hooks/` 빈 출력
- 완료 조건: AC-06

## 검증 계획

- 문서 TASK(02~04): grep Red → 편집 → grep Green, `lint_skill.py` 오류 0.
- 코드 TASK(01): 특성화 — TST-02 같은 SHA 2회.
- 통합: `유지` 전량 1회 + 전체 스위트(= `유지` 4행 + TST-03 `격리` 결과 기록).
- 뮤테이션: 변경 대상 코드 없음(`regression_guard.py` 무변경) — 생략 이유를 검증 결과에 기록.

## 마이그레이션과 롤백

해당 없음 — 문서·테스트 추가만. 롤백은 구현 커밋 revert.

## 인계

- 다음 단계 또는 워크플로우: TASK-05
- 완료된 항목: TASK-01~04
- 미완료 항목: TASK-05
- 다음 행동: TASK-05 — 통합과 종결(AC-06).

## 변경 이력

| 날짜 | 변경 내용 | 근거 | 상태 전이 | 작성·승인 |
|---|---|---|---|---|
| 2026-10-29 | 최초 작성 — TASK-01~05 | REQ-DESIGN-legacy-cleanup v1 | → in-progress | Claude(작성) |
| 2026-10-29 | TASK-01 완료 | TST-02 107 ×2 | in-progress 유지 | Claude(작성) |
| 2026-10-29 | TASK-02 완료(미커밋 — §8 앵커는 TASK-03) | grep 4문구 | in-progress 유지 | Claude(작성) |
| 2026-10-29 | TASK-03·04 완료, TASK-02~04 한 커밋 | lint_skill 오류 0, K3 2,816/2,192 | in-progress 유지 | Claude(작성) |

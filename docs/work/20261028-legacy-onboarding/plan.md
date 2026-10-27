# PLAN-20261028-legacy-onboarding: 구현 계획 — 레거시 테스트 대장 편입·커버리지 기반 보호 스코프

> 문서 유형: `plan`
> 작업 ID: `20261028-legacy-onboarding`
> 상태: `in-progress`
> 기준선: [REQ-DESIGN-legacy-onboarding](./req-design.md) `v1` (승인일 2026-10-28)
> 작성일: 2026-10-28
> 최종 갱신: 2026-10-28
> 관련 문서: [WORK-20261028-legacy-onboarding: 작업 기록](./work-log.md), [ADR-023](./ADR-023-레거시-테스트-대장-편입.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 승인된 v1(FR-01~07, DES-01~05)을 6개 TASK로 구현하고, 종결은 closing.md 순서를 따른다.
- 현재 결론 또는 상태: TASK-01~05 완료(5/6).
- 다음 행동: [인계](#인계).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-legacy-onboarding](./req-design.md) | FR-01~07, AC-01~08, DES-01~05 | v1 |
| input | decision | [ADR-023](./ADR-023-레거시-테스트-대장-편입.md) | document | approved |
| output | implementation | [WORK-20261028-legacy-onboarding](./work-log.md) | 수행 기록 | TASK별 결과 |

## 기준선

- 관련 요구사항: FR-01~07, NFR-01~03
- 관련 설계: DES-01~05
- 관련 ADR·DCR: [ADR-023](./ADR-023-레거시-테스트-대장-편입.md). DCR 없음(C층 무변경)

## 작업 정의

- 목표: 편입 규칙(`verification-depth.md` §7·§1·§2·§3), 대장 표기(templates), wf-implement §3.1 트리거(어절 순증 0), 경량 경로 예시, 판독 무변경 특성화 테스트.
- 범위: req-design [범위](./req-design.md#범위)의 포함. 범위 밖: 같은 절의 범위 밖.
- 가정: §3.1 재확인(2026-10-28 01:23) — HEAD `739fe6b` clean, `30b01fc` 이후 변경은 `docs/`만. `유지` 재실행 TST-02 105·TST-04 16·TST-05 16 통과, TST-01 미수행(실행 권한 거부 — [작업 기록](./work-log.md#2026-10-28--31-재확인과-계획) 참조).
- 위험: 문서 TASK의 Red는 grep 기대 문구 부재로 대신한다. wf-implement 본문이 이미 2,850/2,850이라 TASK-04에서 상쇄 실패 시 NFR-01 위반(DES-03 "넘치면 다른 중복 문장 이관").

## 계획 트리

<!-- generated: 2026-10-28 01:40 — scripts/render.py --view all -->

```text
[작업] 20261028-legacy-onboarding — 레거시 테스트 대장 편입·커버리지 기반 보호 스코프 ... in-progress (5/6)
├─ [✓] 판독 확인 특성화 테스트 (DES-05) (TASK-01) ...... 2026-10-28 01:28
├─ [✓] templates 테스트 대장 노트 (DES-02) (TASK-02) ... 2026-10-28 01:29
├─ [✓] 편입 규칙 (DES-01) (TASK-03) .................... depends: TASK-02  2026-10-28 01:30
├─ [✓] wf-implement §3.1 트리거 (DES-03) (TASK-04) ..... depends: TASK-03  2026-10-28 01:30
├─ [✓] 경량 경로 예시 (DES-04) (TASK-05) ............... depends: TASK-03  2026-10-28 01:30
└─ [▶] 통합과 종결 (TASK-06) ........................... depends: TASK-01~05
```

## 작업 목록

### TASK-01: 판독 확인 특성화 테스트 (DES-05)

- 상태: completed
- 완료: 2026-10-28 01:28
- 상위: 없음
- 목표: `test_regression_guard.py`에 인라인 견본 1건 — `격리(기존 실패, …)`·`미확정`·명령줄 제외 옵션 명령 행·비고 실패 메시지 형태가 든 대장에서 파싱 오류 없이 `유지` 행만 보호
- 관련 요구사항과 설계: NFR-02, DES-05, AC-07
- 변경 대상: `skills/wf-doc/scripts/tests/test_regression_guard.py`(공유 견본 무변경)
- 의존성: 없음 — DES-02 표기는 req-design에 확정되어 templates 편집을 기다리지 않는다. 파일·심볼 겹침 없음
- 위험: 공유 견본·`len(cases)` 보존(T37). 대장 TST-02 `유지` 테스트 파일 수정이라 `### 테스트 대장 변경`에 105→106 기록 필수(가드)
- 검증 방법: Red `해당 없음 — 특성화`(판독 무변경 고정). 단언이 실패할 수 있음은 견본의 `격리` 행 테스트 파일을 변경했을 때 보호되지 않음·`유지` 행 변경 시 실패를 같은 테스트에서 함께 단언해 보인다. Green 후 TST-02 106 ×2
- 완료 조건: AC-07

### TASK-02: templates 테스트 대장 노트 (DES-02)

- 상태: completed
- 완료: 2026-10-28 01:29
- 상위: 없음
- 목표: `보호 스코프`의 `미확정`, 상태 예 `격리(기존 실패, 후속 작업 ID)`, 대장 모든 셀 파이프 금지, 재정비 기록 시점 `편입`과 `승인` 값 `N/A — 경량 경로(편입)`
- 관련 요구사항과 설계: FR-02~04·07, DES-02, AC-04
- 변경 대상: `skills/wf-doc/references/templates.md`(테스트 대장 절)
- 의존성: 없음
- 위험: wf-doc 본문 무변경(K3 2,337/2,350)
- 검증 방법: Red — grep `격리(기존 실패` 부재. Green 후 grep 4문구, `lint_skill.py`
- 완료 조건: AC-04

### TASK-03: 편입 규칙 (DES-01)

- 상태: completed
- 완료: 2026-10-28 01:30
- 상위: 없음
- 목표: (a) `## 7. 대장 편입` 신설(FR-01~04·07), (b) §2 표 `유지` 허용 시점 편입·`격리` 의미와 진입의 기존 실패·`격리` 행 통합 실행, (c) §1 `미확정` 제외·뮤테이션 포함, (d) §3 순서 1과 2 사이 통합 한정 커버리지 재계산
- 관련 요구사항과 설계: FR-01~07, NFR-03, DES-01, AC-01~03
- 변경 대상: `skills/wf-implement/references/verification-depth.md`
- 의존성: TASK-02(표기 링크)
- 위험: 특정 커버리지 도구 의무 문구 금지(NFR-03). 주의 ④·§3.3 제외 금지와의 관계 문장 누락(적대 검토 18)
- 검증 방법: Red — grep `## 7. 대장 편입` 부재. Green 후 AC-01~03 문구 grep, 도구명 grep이 예시 문맥에만 있음, `lint_skill.py`
- 완료 조건: AC-01~03

### TASK-04: wf-implement §3.1 트리거 (DES-03)

- 상태: completed
- 완료: 2026-10-28 01:30
- 상위: 없음
- 목표: §3.1 테스트 상태 불릿을 빌드 상태 확인 + §1 재개 행 링크 + §7 편입 링크로 교체
- 관련 요구사항과 설계: FR-01, NFR-01, DES-03, AC-05
- 변경 대상: `skills/wf-implement/SKILL.md`(넘치면 이관 대상 references 1곳)
- 의존성: TASK-03(링크 대상 §7)
- 위험: 어절 순증(NFR-01) — 넘치면 다른 중복 문장을 references로 이관
- 검증 방법: Red — grep `대장 편입` 부재(SKILL.md). Green 후 grep, `lint_skill.py` 오류 0·본문 ≤ 2,850
- 완료 조건: AC-05

### TASK-05: 경량 경로 예시 (DES-04)

- 상태: completed
- 완료: 2026-10-28 01:30
- 상위: 없음
- 목표: lightweight-path §1 예시에 "기존 테스트의 대장 편입(테스트 무수정)"
- 관련 요구사항과 설계: FR-01, DES-04, AC-06
- 변경 대상: `skills/wf-design/references/lightweight-path.md`
- 의존성: TASK-03(편입 절 링크)
- 위험: 없음
- 검증 방법: Red — grep `대장 편입` 부재(lightweight-path.md). Green 후 grep, `lint_skill.py`
- 완료 조건: AC-06

### TASK-06: 통합과 종결

- 상태: in-progress
- 상위: 없음
- 목표: 린트 3종, `유지` 전량(TST-01 포함), 대장 TST-02 보호 스코프 105→106, 자체 리뷰, 재정비 관문(이 작업이 FR-06의 첫 적용 — 커버리지 도구 없음이라 생략 이유 기록), 완료 보고 관문, closing.md 종결
- 관련 요구사항과 설계: NFR-01~03, AC-08
- 변경 대상: `docs/test-register.md`, 이 작업 문서, `docs/status.md`, 04 머리말(필요 시)
- 의존성: TASK-01~05
- 위험: TST-01 실행 권한(§3.1에서 거부) — 해소 못 하면 완료 조건 미충족으로 보고
- 검증 방법: `lint_design.py`·`lint_skill.py`·`lint_worklog.py` 기본 실행, `유지` 전량, `git diff --stat 739fe6b -- skills/wf-doc/scripts/regression_guard.py setup/hooks/` 빈 출력
- 완료 조건: AC-08

## 검증 계획

- 문서 TASK(02~05): grep Red → 편집 → grep Green, `lint_skill.py` 오류 0.
- 코드 TASK(01): 특성화 — TST-02 같은 SHA 2회.
- 통합: `유지` 전량 1회 + 전체 스위트(= `유지` 4행 + TST-03 `격리` 결과 기록).
- 뮤테이션: 변경 대상 코드 없음(`regression_guard.py` 무변경) — 생략 이유를 검증 결과에 기록.

## 마이그레이션과 롤백

해당 없음 — 문서·테스트 추가만. 롤백은 구현 커밋 revert.

## 인계

- 다음 단계 또는 워크플로우: wf-implement §3.3 구현
- 완료된 항목: §3.1 재확인, 계획, TASK-01~05
- 미완료 항목: TASK-06
- 다음 행동: TASK-06 — 통합 검증·리뷰·완료 보고 관문 승인 완료(01:42). closing.md ② 이후 종결.

## 변경 이력

| 날짜 | 변경 내용 | 근거 | 상태 전이 | 작성·승인 |
|---|---|---|---|---|
| 2026-10-28 | 최초 작성 — TASK-01~06 | REQ-DESIGN-legacy-onboarding v1 | → in-progress | Claude(작성) |

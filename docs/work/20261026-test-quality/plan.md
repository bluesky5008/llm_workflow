# PLAN-20261026-test-quality: 구현 계획 — 테스트 품질 신호와 재정비 관문 보강

> 문서 유형: `plan`
> 작업 ID: `20261026-test-quality`
> 상태: `in-progress`
> 기준선: [REQ-DESIGN-test-quality](./req-design.md) `v1` (승인일 2026-10-26)
> 작성일: 2026-10-26
> 최종 갱신: 2026-10-26
> 관련 문서: [WORK-20261026-test-quality: 작업 기록](./work-log.md), [ADR-017](./ADR-017-변경-범위-뮤테이션.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 승인된 v1(FR-01~10)을 6개 TASK로 구현하고, 종결은 [closing.md](../../../skills/wf-implement/references/closing.md) 순서를 따른다.
- 현재 결론 또는 상태: TASK-01~05 완료(5/6), TASK-06 통합 수행·완료 보고 관문 대기.
- 다음 행동: 완료 보고 관문 → 종결.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-test-quality](./req-design.md) | FR-01~10, AC-01~09, DES-01~09 | v1 |
| input | decision | [ADR-017](./ADR-017-변경-범위-뮤테이션.md) | document | approved |
| output | implementation | [WORK-20261026-test-quality](./work-log.md) | 수행 기록 | TASK별 결과 |

## 기준선

- 관련 요구사항: FR-01~10, NFR-01~07
- 관련 설계: DES-01~09
- 관련 ADR·DCR: [ADR-017](./ADR-017-변경-범위-뮤테이션.md), [ADR-009](../20261009-test-lifecycle/ADR-009-테스트-재정비-관문.md)(정밀화 대상, 대체 아님)

## 작업 정의

- 목표: 재정비 관문 규칙 보강, 대역 기준·냄새, 변경 범위 뮤테이션, 속성 테스트 선택지와 두 시범.
- 범위: req-design [포함](./req-design.md#포함).
- 범위 밖: req-design [제외](./req-design.md#제외).
- 가정: §3.1 재확인(2026-10-26 00:15) — HEAD `3cf621e`+미커밋(문서만), `유지` 4행 통과(TST-01 47, TST-02 68, TST-04 16, TST-05 13). 사용자 미추적 파일 `06_design_kickoff_prompt.md`·`07_parallel_tasks.md`는 건드리지 않고 커밋에서 제외.
- 위험: RISK-01(wf-implement 어절 여유 0) — TASK-02·03에서 `lint_skill.py`로 확인. RISK-02(뮤턴트 잔류) — TASK-05에서 해시 대조.

## 계획 트리

<!-- generated: 2026-10-26 00:29 — scripts/render.py --view all -->

```text
[작업] 20261026-test-quality — 테스트 품질 신호와 재정비 관문 보강 ... in-progress (5/6)
├─ [✓] 재정비 관문 — 재생성·격리 진단·병합 증거 (DES-01·02) (TASK-01) ... 2026-10-26 00:21
├─ [✓] 대역 기준·냄새·속성 테스트 문단 (DES-03·04·07) (TASK-02) ......... depends: TASK-01  2026-10-26 00:21
├─ [✓] 변경 범위 뮤테이션 규칙과 여섯째 필드 (DES-05·06) (TASK-03) ...... depends: TASK-02  2026-10-26 00:22
├─ [✓] 속성 테스트 시범 (DES-09) (TASK-04) .............................. depends: TASK-02  2026-10-26 00:24
├─ [✓] 수동 뮤테이션 시범 (DES-08) (TASK-05) ............................ depends: TASK-03, TASK-04  2026-10-26 00:27
└─ [▶] 통합과 종결 (TASK-06) ............................................ depends: TASK-01~05
```

## 작업 목록

### TASK-01: 재정비 관문 — 재생성·격리 진단·병합 증거 (DES-01·02)

- 상태: completed
- 완료: 2026-10-26 00:21
- 상위: 없음
- 목표: verification-depth §2 표 뒤 문단에 재생성(실패 중 → §6, 통과 중 → `병합` 4조건, 진행 중 금지)·격리 진단 순서 2문장, §3 `증거` 행 중복 증거 강도 순서 교체, 1단계 Missing에 survived 입력
- 관련 요구사항과 설계: FR-01~03·07, DES-01·02, AC-01·02
- 변경 대상: `skills/wf-implement/references/verification-depth.md` §2·§3
- 의존성: 없음
- 위험: NFR-02 — 절 제목 불변
- 검증 방법: 문서 변경이라 TDD 비대상(`Red: 해당 없음`). `lint_skill.py` 0 오류, grep(재생성·순서 의존·kill 집합 문장)
- 완료 조건: AC-01·02(§3 Missing 링크는 TASK-03의 §5 절차를 가리키므로 앵커만 `#5-검증-결과-기록`)

### TASK-02: 대역 기준·냄새·속성 테스트 문단 (DES-03·04·07)

- 상태: completed
- 완료: 2026-10-26 00:21
- 상위: 없음
- 목표: wf-implement §2.4 첫 두 항목을 "동작을 검증한다. 대역은 외부 경계(…)에서만, fake 우선." / "결정적이다(시계·난수는 주입)."로(12→12어절), §4에 Over-mock·Mirror 행, Empty / Trivial 징후에 Print-only, §4 표 아래 R-09 선택 문단
- 관련 요구사항과 설계: FR-04·05·09, DES-03·04·07, AC-03·07(문단 부분)
- 변경 대상: `skills/wf-implement/SKILL.md` §2.4, `skills/wf-implement/references/verification-depth.md` §4
- 의존성: TASK-01(같은 파일)
- 위험: RISK-01 — 본문 어절 순증 0
- 검증 방법: 문서 변경(`Red: 해당 없음`). `lint_skill.py` K3 2,850 이하, grep
- 완료 조건: AC-03, AC-07의 문단 항목

### TASK-03: 변경 범위 뮤테이션 규칙과 여섯째 필드 (DES-05·06)

- 상태: completed
- 완료: 2026-10-26 00:22
- 상위: 없음
- 목표: §1 통합 행에 "+ 변경 범위 뮤테이션(§5)", §5 다섯 → 여섯 필드와 뮤테이션 절차 문단(대상·실행·도구·복원 해시·실패 분리·기록·목표 비율 없음), templates.md 골격 1줄·노트, wf-implement §3.4 열거 토큰에 "뮤테이션"
- 관련 요구사항과 설계: FR-06~08, DES-05·06, AC-04·05
- 변경 대상: `skills/wf-implement/references/verification-depth.md` §1·§5, `skills/wf-doc/references/templates.md`, `skills/wf-implement/SKILL.md` §3.4
- 의존성: TASK-02(같은 파일 2개)
- 위험: RISK-01 — §3.4는 토큰 내부 삽입(어절 0)
- 검증 방법: 문서 변경(`Red: 해당 없음`). `lint_skill.py`, `grep -rn "다섯 필드"` 0건, 통독
- 완료 조건: AC-04·05

### TASK-04: 속성 테스트 시범 (DES-09)

- 상태: completed
- 완료: 2026-10-26 00:24
- 상위: 없음
- 목표: `skills/wf-tree/scripts/tests/test_render_props.py`에 `render.py` 불변식 2~3개(후보: `width` 가법성, `plain` 멱등성, 생성 TASK 표의 `parse_plan_items` ID·상태 보존, `build_tree` 항목 1회 출현), `@settings(derandomize=True, database=None, deadline=None)`, 최상단 일반 import. `python -m pip install hypothesis`, README 테스트 전제에 `hypothesis`, TST-05 보호 스코프·건수 갱신
- 관련 요구사항과 설계: FR-10, NFR-07, DES-09, AC-07
- 변경 대상: `skills/wf-tree/scripts/tests/test_render_props.py`(신설 — TST-05 보호 경로라 편집 확인 훅 확인), `README.md`, `docs/test-register.md`(TST-05)
- 의존성: TASK-02(R-09 문단이 시범의 근거 규칙)
- 위험: RISK-07·08. 속성 테스트가 `render.py` 결함을 찾으면 기록 후 사용자에게 수정 여부 질문(범위 변경)
- 검증 방법: Red — `hypothesis` 설치 전 TST-05 명령 실행 → 수집 오류(FR-10 증거). Green — 설치 후 통과. 결정성 — 같은 SHA 2회 결과 동일. 단언의 실패 가능성은 TASK-05 뮤턴트로 확인
- 완료 조건: AC-07, TST-05 등록 갱신(같은 SHA 2회 통과)

### TASK-05: 수동 뮤테이션 시범 (DES-08)

- 상태: completed
- 완료: 2026-10-26 00:27
- 상위: 없음
- 목표: `render.py`·`lint_worklog.py` 각각 수동 뮤턴트 3개(기존 테스트를 읽고 실제 결함형 — 경계·분기 반전·반환값). 파일마다 `git hash-object` 기록 → 1개 적용 → TST-05 또는 TST-02 → 결과 → 복원 → 해시 대조. survived·동치는 `### 테스트 대장 변경`에 Missing 후보·이유
- 관련 요구사항과 설계: FR-06~08, DES-08, AC-06
- 변경 대상: 없음(제품 코드는 적용·복원만), `work-log.md` 검증 결과
- 의존성: TASK-03(기록 형식), TASK-04(TST-05에 속성 테스트 포함 — kill 출처를 예제/속성으로 구분 기록)
- 위험: RISK-02·04·05
- 검증 방법: 시범 자체가 검증(`Red: 해당 없음 — 제품 코드 무변경`). 종료 시 두 파일 해시 = 착수 시 값, `git status`에 두 파일 변경 없음
- 완료 조건: AC-06

### TASK-06: 통합과 종결

- 상태: in-progress
- 완료: —
- 상위: 없음
- 목표: ADR-009 대체 관계에 관련 1행, 전체 테스트 스위트 1회 + `유지` 전량, 이 작업의 뮤테이션 필드 `N/A — 변경 코드 파일 없음`(시범은 VER), 재정비 관문, 자체 리뷰(review-checklist), 완료 보고 관문, closing.md 순서로 종결
- 관련 요구사항과 설계: NFR-01~07, AC-08·09
- 변경 대상: `docs/work/20261009-test-lifecycle/ADR-009-테스트-재정비-관문.md`(대체 관계 1행), `docs/test-register.md`, 이 작업 문서, `docs/status.md`, `docs/requirements.md`·`design.md` 무변경 확인
- 의존성: TASK-01~05
- 위험: RISK-02(종결 ① 전 뮤턴트 흔적 없음 확인)
- 검증 방법: 린트 2종, `유지` 전량, `git diff --name-only <구현 SHA>`가 `docs/`뿐
- 완료 조건: AC-08·09

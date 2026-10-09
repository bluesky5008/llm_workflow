# PLAN-20261009-skill-diet: 구현 계획 — 스킬 다이어트·정리

> 문서 유형: `plan`
> 작업 ID: `20261009-skill-diet`
> 상태: `completed`
> 기준선: `v1` ([REQ-DESIGN-skill-diet](./req-design.md), 2026-10-09 승인)
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [REQ-DESIGN-skill-diet: 요구사항·설계](./req-design.md), [ADR-010: 스킬 문서의 계층 규칙](./ADR-010-스킬-문서-계층-규칙.md), [ADR-011: wf-tree 축소](./ADR-011-wf-tree-축소.md), [WORK-20261009-skill-diet: 작업 기록](./work-log.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 기준선 v1(FR-01~11, NFR-01~08, DES-01~12)을 references 신설 → 본문 재배치 → 스크립트 2종(TDD) → 검증·통합의 작업 9개로 번역하고 AC-01~12로 검증한다.
- 현재 결론 또는 상태: 완료(2026-10-09 20:19) — TASK-01~09 `completed`.
- 다음 행동: 없음 — 결과는 [작업 기록 완료 보고](./work-log.md#완료-보고). 진행 상태는 아래 작업 목록이 정본.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-skill-diet](./req-design.md) | FR-01~11, NFR-01~08, AC-01~12, DES-01~12 | 승인 기준선 v1 |
| input | decision | [ADR-010](./ADR-010-스킬-문서-계층-규칙.md), [ADR-011](./ADR-011-wf-tree-축소.md) | document | 계층 규칙·린트, wf-tree 축소 |
| output | implementation | [WORK-20261009-skill-diet: 작업 기록](./work-log.md) | document | 수행 기록·검증 결과의 정본 |
| input | related | [ST-llm-workflow: 포트폴리오](../../status.md) | document | 이 작업이 등재된 포트폴리오 |

## 기준선

- 관련 요구사항: [FR-01~11, NFR-01~08, AC-01~12](./req-design.md#기능-요구사항)
- 관련 설계: [DES-01~12](./req-design.md#설계)
- 관련 ADR·DCR: [ADR-010](./ADR-010-스킬-문서-계층-규칙.md), [ADR-011](./ADR-011-wf-tree-축소.md). DCR 없음

## 작업 정의

- 목표: 스킬 3종의 세부를 references·scripts로 재배치하고, 경고 절·스킬 린트·wf-tree 축소·렌더 스크립트를 두어 본문 합을 10,446 → ≤ 8,700어절로 줄이되 의미와 앵커를 보존한다.
- 범위·범위 밖·가정·위험: [기준선 문서](./req-design.md#범위) 참조.
- §3.1 재확인(2026-10-09 19:41, HEAD `0962f3c`): 기준선 이후 저장소 변경 없음, 타인 미커밋 변경 없음(미커밋은 이 작업 문서와 미추적 조사 폴더 2개). 대장 `유지` 행 SHA `7395a99` ≠ HEAD라 전량 재실행 — TST-01 22/22, TST-02 33/33. TST-03은 `격리`(변경 없음).
- 트리 사용 결정: **사용** — 작업 9개, 의존(TASK-02→01, TASK-04→03, TASK-05→01·03, TASK-07→06, TASK-08→02·04·05·07, TASK-09→전체).
- TDD 적용: 스크립트 2종(TASK-06 render.py, TASK-08 lint_skill.py)은 실패하는 pytest를 먼저 작성한다. Markdown 변경(TASK-01~05·07)은 [wf-implement §3.3](../../../skills/wf-implement/SKILL.md#33-구현)의 "사이클을 적용할 수 없는 변경"으로 분류하고 TASK-09의 후행 검증(통독·grep·어절 측정·앵커 전수·린트)으로 대체한다.
- 작업 순서의 이유: references 파일이 본문 트리거 문장의 링크 대상이므로 references(TASK-01·03·06)가 본문(TASK-02·04·07)보다 먼저. wf-design 주의 절(TASK-05)은 정본 콜아웃이 가리킬 boundaries.md 2개가 있어야 한다. 린트(TASK-08)는 K7(주의 절)·K4(링크) 때문에 본문 4개가 끝나야 실제 스킬에서 exit 0이 된다. 트리 재생성(FR-10)은 render.py 완료 후 TASK-09에서.
- 깊이: 전부 `상위: 없음`(깊이 1) — ADR-011 상한 2 이내.

## 계획 트리

<!-- generated: 2026-10-09 20:20 — scripts/render.py --view all -->

```text
[작업] 20261009-skill-diet — 스킬 다이어트·정리 ... completed (9/9)
├─ [✓] wf-doc references 신설 (TASK-01) ...................... 2026-10-09 19:44
├─ [✓] wf-doc 본문 재배치 (TASK-02) .......................... depends: TASK-01  2026-10-09 19:46
├─ [✓] wf-implement references 신설 (TASK-03) ................ 2026-10-09 19:52
├─ [✓] wf-implement 본문 재배치 (TASK-04) .................... depends: TASK-03, TASK-01  2026-10-09 19:54
├─ [✓] wf-design 주의 절과 정본 콜아웃 링크 갱신 (TASK-05) ... depends: TASK-01, TASK-03  2026-10-09 19:55
├─ [✓] wf-tree render.py(TDD)와 references (TASK-06) ......... 2026-10-09 20:05
├─ [✓] wf-tree 본문 축소 (TASK-07) ........................... depends: TASK-06  2026-10-09 20:06
├─ [✓] lint_skill.py(TDD)와 README (TASK-08) ................. depends: TASK-02, TASK-04, TASK-05, TASK-07  2026-10-09 20:09
└─ [✓] 검증·자체 리뷰·통합 (TASK-09) ......................... depends: TASK-01~08  2026-10-09 20:19
```

## 작업 목록

### TASK-01: wf-doc references 신설

- 상태: completed
- 완료: 2026-10-09 19:44
- 상위: 없음
- 목표: `skills/wf-doc/references/boundaries.md`(wf-design·wf-implement 경계 소유권 표 2개 + 정본 콜아웃, 각 표 위에 본문 적용 규칙 링크), `references/linking.md`(하이퍼링크 세부 규칙 7개 + 추적표 골격 + 관계 어휘), `references/templates.md`에 절 추가 — 공통 머리말(§2.3 코드블록), 추적 식별자 목록(§2.6 코드블록 2개), 인계 블록(§2.7 코드블록 2개) — 와 목차 항목. 본문 문장은 옮기되 바꾸지 않는다.
- 관련 요구사항과 설계: FR-03, NFR-03, NFR-07 / DES-03
- 변경 대상: `skills/wf-doc/references/boundaries.md`(신설), `skills/wf-doc/references/linking.md`(신설), `skills/wf-doc/references/templates.md`
- 의존성: 없음
- 위험: templates.md 합본 work-log 절은 건드리지 않는다(NFR-05). 신설 파일 120행 이내
- 검증 방법: TDD 부적용(산문). 이동 전후 문장 grep 대조, `wc -l`. TASK-09에서 AC-02
- 완료 조건: 세 파일에 이관 대상 전부가 있고 TST-02 33/33

### TASK-02: wf-doc 본문 재배치

- 상태: completed
- 완료: 2026-10-09 19:46
- 상위: 없음
- 목표: SKILL.md에서 경계표 2개(H3 제목·적용 규칙은 유지), §2.3·§2.6·§2.7 코드블록, 중복 문서 연결 예시, 하이퍼링크 세부 규칙 7개를 제거하고 각 자리에 트리거 문장(DES-09)을 둔다. 핵심 5개 규칙 유지. `## 주의 — 자주 틀리는 것` 절(DES-07 wf-doc 4항)을 경계 절 뒤·§1 앞에 신설. 정본 콜아웃의 표 링크를 boundaries.md로.
- 관련 요구사항과 설계: FR-03, FR-07, FR-09, NFR-02, NFR-03 / DES-03, DES-07, DES-09, DES-10
- 변경 대상: `skills/wf-doc/SKILL.md`
- 의존성: TASK-01
- 위험: `#추적-식별자`·`#23-공통-머리말-작성`·`#27-인계와-재개-지점-작성`·`#wf-design과의-경계`·`#wf-implement와의-경계` 앵커 유지. 어절 ≤ 2,350
- 검증 방법: TDD 부적용. 어절 측정, 가드 수(≥35), 링크 검사. TASK-09에서 AC-02·06·08
- 완료 조건: 본문에 코드블록이 §2.5 표지 1개뿐이고 어절 ≤ 2,350, 가드 ≥ 35

### TASK-03: wf-implement references 신설

- 상태: completed
- 완료: 2026-10-09 19:52
- 상위: 없음
- 목표: `skills/wf-implement/references/boundaries.md`(wf-design↔wf-implement 소유권 표 12행 + 정본 콜아웃), `references/review-checklist.md`(§3.5 문항 20개, 4묶음 제목 유지). 각 파일 머리에 본문 절 링크와 소유 관계 1문장.
- 관련 요구사항과 설계: FR-02, NFR-03, NFR-07 / DES-02
- 변경 대상: `skills/wf-implement/references/boundaries.md`(신설), `skills/wf-implement/references/review-checklist.md`(신설)
- 의존성: 없음
- 위험: 없음
- 검증 방법: TDD 부적용. 문장 대조 grep. TASK-09에서 AC-01
- 완료 조건: 두 파일에 표 12행·문항 20개가 원문 그대로 있다

### TASK-04: wf-implement 본문 재배치

- 상태: completed
- 완료: 2026-10-09 19:54
- 상위: 없음
- 목표: 경계 절에서 표를 빼고 한 문단 요약 + 적용 규칙 6항 + 반환 흐름 + 트리거. §3.5를 트리거 2문장 + "발견한 문제는 수정…" 문장으로. §3.2 "작업 간 의존성" 항목에 S12 문장(DES-08). `## 주의 — 자주 틀리는 것` 절(DES-07 wf-implement 5항, ①이 정본)을 wf-doc 경계 절 뒤·§1 앞에. §2.3 끝 "설계 승인은 위 작업의 실행 승인이 아니다"와 경계 규칙 6항은 정본 링크를 붙인 한 문장으로. wf-doc 정본 콜아웃의 표 링크를 wf-doc boundaries.md로.
- 관련 요구사항과 설계: FR-02, FR-06, FR-07, FR-09, NFR-02, NFR-03 / DES-02, DES-07, DES-08, DES-09, DES-10
- 변경 대상: `skills/wf-implement/SKILL.md`
- 의존성: TASK-03(링크 대상), TASK-01(wf-doc boundaries.md 링크 대상)
- 위험: 절 번호·제목 불변(§2.4·§3.1·§3.3 텍스트 참조). 어절 ≤ 2,850, 가드 ≥ 24
- 검증 방법: TDD 부적용. 어절·가드 측정, 링크 검사. TASK-09에서 AC-01·05·06·08
- 완료 조건: 경계 절에 표 없음, §3.5에 문항 없음, S12 문장·주의 절 존재, 어절 ≤ 2,850

### TASK-05: wf-design 주의 절과 정본 콜아웃 링크 갱신

- 상태: completed
- 완료: 2026-10-09 19:55
- 상위: 없음
- 목표: `## 주의 — 자주 틀리는 것` 절(DES-07 wf-design 3항, ①은 wf-implement 정본 링크)을 wf-implement 경계 절 뒤·§1 앞에. 경계 규칙 5항을 정본 링크가 붙은 한 문장으로. 정본 콜아웃 2곳의 표 링크를 wf-doc·wf-implement `references/boundaries.md`로 갱신. 그 외 무변경.
- 관련 요구사항과 설계: FR-07, FR-09, NFR-02 / DES-07, DES-10
- 변경 대상: `skills/wf-design/SKILL.md`
- 의존성: TASK-01, TASK-03
- 위험: 어절 ≤ 2,300(순증 ≤ 40), 가드 ≥ 18
- 검증 방법: TDD 부적용. 어절 측정, 링크 검사. TASK-09에서 AC-06·08
- 완료 조건: 주의 절 존재, 콜아웃 링크 2곳 갱신, 어절 ≤ 2,300

### TASK-06: wf-tree render.py(TDD)와 references

- 상태: completed
- 완료: 2026-10-09 20:05
- 상위: 없음
- 목표: `skills/wf-tree/references/rendering.md`(현행 §7 표기 어휘·완료 시점 파생·접기·뷰 4종·손 렌더 시 표기, §2 예시 트리)와 `references/node-templates.md`(§3 유형 표 15행 + 매핑, §9 문항 9개 + S12 문항, 삭제된 분기 템플릿 7행의 근거 규정 위치 안내 없음 — 삭제 목록은 ADR-011). `scripts/render.py`를 DES-05 계약대로 TDD로: Red — `scripts/tests/test_render.py`(파싱 2·중첩 2·접기 1·뷰 2·depends 1·완료 시점 1·write 1·경고 2 = 12) 작성·실패 확인 → Green → Refactor. 표준 라이브러리, stdout utf-8.
- 관련 요구사항과 설계: FR-04(references 부분), FR-05, FR-06(문항), NFR-06, NFR-07, NFR-08 / DES-04, DES-05, DES-08
- 변경 대상: `skills/wf-tree/references/rendering.md`(신설), `skills/wf-tree/references/node-templates.md`(신설), `skills/wf-tree/scripts/render.py`(신설), `skills/wf-tree/scripts/tests/test_render.py`(신설)
- 의존성: 없음
- 위험: RISK-03 — 표기 재현. rendering.md를 먼저 쓰고 그 표기로 골든 작성. `status.md` 표 형식은 바꾸지 않음(L8)
- 검증 방법: 선행 — pytest Red 12 실패 → Green 12 통과. `python skills/wf-tree/scripts/render.py docs/work/20261009-skill-diet/plan.md` 실행 확인. TASK-09에서 AC-03·04
- 완료 조건: pytest 12/12, 이 plan.md를 입력으로 TASK-01~09 라인·depends 출력, references 2개 120행 이내

### TASK-07: wf-tree 본문 축소

- 상태: completed
- 완료: 2026-10-09 20:06
- 상위: 없음
- 목표: §2 "깊이는 제한하지 않는다"를 상한 2단계 문장으로 교체, 예시 코드블록 제거(references 링크). §3을 포인터 2문장 + ★ 3종으로. §4를 `## 4. 필수 게이트` 3행 표 + 생략 금지 문장으로(비게이트 7행 삭제). §7: 매체 1문단·생성 시점 절 유지, 표기·접기·대형 트리 세칙 제거, render.py 트리거와 손 렌더 대체 규정. §9: 트리거만. `## 주의` 절(DES-07 wf-tree 4항). description 갱신(FR-04).
- 관련 요구사항과 설계: FR-04, FR-06, FR-07, FR-09, NFR-02, NFR-03 / DES-04, DES-07, DES-09, DES-10
- 변경 대상: `skills/wf-tree/SKILL.md`
- 의존성: TASK-06
- 위험: `#생성-시점`·`#5-데이터-모델과-식별자`·`#단일-소스-원칙`·`#7-렌더링`·`#8-포트폴리오-생성과-갱신` 앵커 유지. 어절 ≤ 1,200, 가드 ≥ 20
- 검증 방법: TDD 부적용. 어절·가드 측정, 링크 검사. TASK-09에서 AC-03·06·08·09
- 완료 조건: §3 표 없음, §4 3행, §7 트리거, 주의 절, 어절 ≤ 1,200

### TASK-08: lint_skill.py(TDD)와 README

- 상태: completed
- 완료: 2026-10-09 20:09
- 상위: 없음
- 목표: `skills/wf-doc/scripts/lint_skill.py`를 DES-06 계약대로 TDD로: Red — `scripts/tests/test_lint_skill.py`(K1~K7 실패·통과 쌍 14 + 대상 탐색 1) → Green → Refactor. `lint_worklog` 헬퍼 import. README 실행 기준 절에 ADR-010 포인터와 린트 명령·시점 1문단. 실제 4스킬에 실행해 exit 0 확인.
- 관련 요구사항과 설계: FR-01(README), FR-08, NFR-05, NFR-06, NFR-08 / DES-01, DES-06
- 변경 대상: `skills/wf-doc/scripts/lint_skill.py`(신설), `skills/wf-doc/scripts/tests/test_lint_skill.py`(신설), `README.md`
- 의존성: TASK-02, TASK-04, TASK-05, TASK-07(실제 스킬 exit 0)
- 위험: RISK-06 헬퍼 결합 — import를 `read_lines`·`outside_fences`·`headings`·`slug`·`anchors_of`·`Finding`에 한정. TST-02 명령이 pytest 폴더 전체라 새 테스트가 같은 명령에 합류 — 대장 비고에 건수 갱신
- 검증 방법: 선행 — pytest Red 15 실패 → Green 통과. `python skills/wf-doc/scripts/lint_skill.py` exit 0. TASK-09에서 AC-07
- 완료 조건: pytest 통과, 4스킬 린트 exit 0, README 문단 존재

### TASK-09: 검증·자체 리뷰·통합

- 상태: completed
- 완료: 2026-10-09 20:19
- 상위: 없음
- 목표: AC-01~12 판정(VER-01~12), 자체 리뷰(references/review-checklist.md 읽고 전 항목), 통합 — 전체 스위트 1회(TST-01·02·04·05) + `유지` 행 전량 + 재정비 관문(변경이 닿은 보호 스코프: TST-02의 `lint_worklog.py`는 무변경이라 Breaking 0 예상). `render.py --write`로 이 plan.md 트리 재생성(FR-10). 대장에 TST-04·05 등록(같은 SHA 2회). req-design 추적표 작업 열 기입. `git diff --stat`로 완료 기록 무변경. 완료 보고·인계 축약·포트폴리오 행 제거.
- 관련 요구사항과 설계: FR-09, FR-10, FR-11, NFR-01~05 / DES-10, DES-11, DES-12
- 변경 대상: `docs/work/20261009-skill-diet/work-log.md`, `plan.md`, `req-design.md`(추적표), `docs/test-register.md`, `docs/status.md`
- 의존성: TASK-01~08
- 위험: 어절 상한 미달 시 해당 본문 TASK로 되돌아가 상쇄(의미 삭제 금지, RISK-04)
- 검증 방법: 검증 계획 절의 명령
- 완료 조건: wf-implement §5 완료 조건 전부, 린트 2종 0 오류, 포트폴리오 행 제거

## 검증 계획

| AC | 방법·명령 | TASK |
|---|---|---|
| AC-01, AC-02, AC-03, AC-05, AC-06, AC-09, AC-12 | 해당 절 통독·grep, `wc -l` | TASK-09 |
| AC-04 | `python -m pytest skills/wf-tree/scripts/tests -q`, `python skills/wf-tree/scripts/render.py docs/work/20261009-skill-diet/plan.md [--write]` | TASK-06, TASK-09 |
| AC-07 | `python -m pytest skills/wf-doc/scripts/tests -q`, `python skills/wf-doc/scripts/lint_skill.py` | TASK-08, TASK-09 |
| AC-08 | 어절·가드 측정 스크립트(req-design 조사 절 함수, `PYTHONIOENCODING=utf-8`) | TASK-02·04·05·07(작업 중), TASK-09 |
| AC-10 | `lint_skill.py` K4, `lint_worklog.py` L6, `grep -rhoE "skills/.*#"` 전수 대조, `git diff --stat docs/work/2026*` | TASK-09 |
| AC-11 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1`, pytest 2폴더, 대장 행 확인 | TASK-09 |

## 마이그레이션과 롤백

- 마이그레이션: 없음 — 기존 완료 기록의 트리·문서는 동결. 새 규칙은 이 작업의 plan.md부터.
- 롤백: 커밋 전에는 `git checkout -- skills README.md docs/test-register.md`와 신설 파일 삭제, 커밋 후에는 `git revert`. 신설 references·scripts는 되돌리면 사라지고 본문은 원문으로 복귀한다.

## 인계

- 다음 단계 또는 워크플로우: 없음
- 완료된 항목: TASK-01~09
- 미완료 항목: 없음
- 다음 행동: 없음

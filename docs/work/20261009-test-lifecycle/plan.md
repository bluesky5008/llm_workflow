# PLAN-20261009-test-lifecycle: 구현 계획 — 검증 기록과 회귀 수명주기

> 문서 유형: `plan`
> 작업 ID: `20261009-test-lifecycle`
> 상태: `completed`
> 기준선: `v1` ([REQ-DESIGN-test-lifecycle](./req-design.md), 2026-10-09 승인)
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [REQ-DESIGN-test-lifecycle: 요구사항·설계](./req-design.md), [ADR-007: 검증 결과의 3튜플 앵커](./ADR-007-검증-결과-3튜플-앵커.md), [ADR-008: 테스트 대장의 저장소 관통 배치](./ADR-008-테스트-대장-저장소-관통.md), [ADR-009: 테스트 재정비 관문](./ADR-009-테스트-재정비-관문.md), [WORK-20261009-test-lifecycle: 작업 기록](./work-log.md)

## 요약

- 목적: 기준선 v1(FR-01~11, NFR-01~06, DES-01~10)을 wf-doc 템플릿·wf-implement 본문과 references·테스트 대장 신설·자기 적용의 작업 6개로 번역하고 AC-01~11로 검증한다.
- 현재 결론 또는 상태: TASK-01~06 완료(2026-10-09 16:45). 작업 완료 — 결과는 [작업 기록](./work-log.md#완료-보고).
- 다음 행동: 없음 — 후속 작업은 [작업 기록 완료 보고](./work-log.md#후속-작업).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-test-lifecycle](./req-design.md) | FR-01~11, NFR-01~06, AC-01~11, DES-01~10 | 승인 기준선 v1 |
| input | decision | [ADR-007](./ADR-007-검증-결과-3튜플-앵커.md), [ADR-008](./ADR-008-테스트-대장-저장소-관통.md), [ADR-009](./ADR-009-테스트-재정비-관문.md) | document | 3튜플, 대장 위치, 관문 |
| output | implementation | [WORK-20261009-test-lifecycle: 작업 기록](./work-log.md) | document | 수행 기록·검증 결과의 정본 |
| input | related | [ST-llm-workflow: 포트폴리오](../../status.md) | document | 이 작업이 등재된 포트폴리오 |

## 기준선

- 관련 요구사항: [FR-01~11, NFR-01~06, AC-01~11](./req-design.md#기능-요구사항)
- 관련 설계: [DES-01~10](./req-design.md#설계)
- 관련 ADR·DCR: [ADR-007](./ADR-007-검증-결과-3튜플-앵커.md), [ADR-008](./ADR-008-테스트-대장-저장소-관통.md), [ADR-009](./ADR-009-테스트-재정비-관문.md). DCR 없음

## 작업 정의

- 목표: 검증 결과의 정량 기록 형식과 테스트 대장·수명주기·재정비 관문을 스킬 규정과 템플릿에 반영하고, 이 저장소의 대장을 신설해 자기 적용한다.
- 범위·범위 밖·가정·위험: [기준선 문서](./req-design.md#범위) 참조.
- §3.1 재확인(2026-10-09 16:15, HEAD `1f98f7e`): 기준선 이후 저장소 변경 없음, 타인 미커밋 변경 없음(미커밋은 이 작업의 승인 기록뿐). 테스트 상태 — 린트 pytest 33/33, 훅 러너 22/22, pptx 테스트 3/8(5건 `ModuleNotFoundError: pptx` — 환경 원인의 기존 실패). pptx 자산은 `유지` 진입 조건(통과)을 채우지 못하므로 TASK-04에서 `격리`로 등록하고 이유를 기록한다(§4.1 경미한 변경 — 격리의 운영 의미 "계속 실행, 완료 미차단, 후속 작업 등록"에 부합).
- 트리 사용 결정: **사용** — 작업 6개, 의존(TASK-03→02, TASK-04→01, TASK-05→01·04, TASK-06→전체).
- TDD 적용: 변경 대상이 전부 Markdown 규칙·템플릿·대장 문서라 [wf-implement §3.3](../../../skills/wf-implement/SKILL.md#33-구현)의 "사이클을 적용할 수 없는 변경"으로 분류하고 TASK-06의 후행 검증(grep·통독·린트·pytest·어절 측정·측정 스크립트)으로 대체한다. 코드 변경은 없다(NFR-03: 린트 무변경).
- 작업 순서의 이유: 템플릿(TASK-01)이 대장·검증 표 형식의 정본이므로 대장 신설(TASK-04)보다 먼저. references(TASK-02)가 본문 트리거 문장의 링크 대상이므로 본문(TASK-03)보다 먼저. 자기 적용(TASK-05)은 형식과 대장이 모두 있어야 한다.

## 계획 트리

<!-- generated: 2026-10-09 16:20 — 계획 최초 작성 시 1회 생성. 이후 목록이 정본이며 트리는 요청 시에만 재생성 -->

```text
[작업] 20261009-test-lifecycle — 검증 기록과 회귀 수명주기 .................. in-progress (0/6)
├─ [ ] 구현: wf-doc 템플릿 — 검증 결과 형식·test-register 템플릿·유형표 (TASK-01)
├─ [ ] 구현: wf-implement references/verification-depth.md 신설 (TASK-02)
├─ [ ] 구현: wf-implement 본문 §2.4·§3.1·§3.3~3.6·§5·§7 + 어절 상쇄 (TASK-03) ... depends: TASK-02
├─ [ ] 문서화: docs/test-register.md 신설 — 자산 3묶음 등록 (TASK-04) ........... depends: TASK-01
│   └─ [ ] 테스트: 자산 3묶음 실행·SHA 기록 (선행)
├─ [ ] 전환: 자기 적용 — work-log 검증 결과 형식·재정비 관문 1회 (TASK-05) ..... depends: TASK-01, TASK-04
│   └─ [ ] 롤백 준비: 전환 전 사본 보관 (필수)
└─ [ ] 검증: AC-01~11 판정, 자체 리뷰, 통합, 등록부 (TASK-06) .................. depends: TASK-01~05
```

## 작업 목록

### TASK-01: wf-doc 템플릿·유형 — 검증 결과 형식과 test-register

- 상태: completed
- 완료: 2026-10-09 16:15
- 상위: 없음
- 목표: `templates.md` 합본 work-log의 `### 결과 요약`을 DES-02 고정 필드로, `### 인수 조건별 결과` 표에 `분류` 열, `### 실패와 미수행 분석` 뒤에 `### 테스트 대장 변경` H3와 표. 노트에 증거 SHA·명령 필수와 분류 어휘. `test-register` 템플릿 신설(DES-03 절·열, 40행 이내)과 목차·필수 연결 행. wf-doc SKILL.md §2.1 유형표에 `test-register` 행.
- 관련 요구사항과 설계: FR-02, FR-04, FR-07(c), NFR-02, NFR-03 / DES-02, DES-03
- 변경 대상: `skills/wf-doc/references/templates.md`, `skills/wf-doc/SKILL.md`
- 의존성: 없음
- 위험: H2 추가 금지(NFR-03) — H3·표·필드만 추가. 불릿 필드 300자 이하
- 검증 방법: TDD 부적용(산문). TASK-06에서 AC-02·AC-03 통독·grep, 린트 pytest 33/33 유지
- 완료 조건: 합본 H2가 8개 그대로이고 DES-02·03의 필드·열·절이 모두 있다

### TASK-02: wf-implement references/verification-depth.md 신설

- 상태: completed
- 완료: 2026-10-09 16:15
- 상위: 없음
- 목표: 시점별 실행 집합 표(DES-05), 상태·전이 표(DES-04, 진입 조건 포함), 재정비 관문 4조건과 분류 5종·증거 기준(DES-06), 테스트 작성 체크리스트 6항(DES-07). 본문 §3.4가 의미 규칙, 이 문서가 표라는 관계 문장. 100행 이내.
- 관련 요구사항과 설계: FR-05, FR-06, FR-07, FR-08, FR-09, NFR-02 / DES-04, DES-05, DES-06, DES-07
- 변경 대상: `skills/wf-implement/references/verification-depth.md`(신설)
- 의존성: 없음(본문 앵커 `#34-검증` 등은 기존)
- 위험: 보관 설계 표의 Stop 훅 행·깊이 표를 끌어오지 않도록 범위 고정(Q-02)
- 검증 방법: TDD 부적용. TASK-06에서 AC-04 통독, `wc -l`
- 완료 조건: 네 표가 있고 100행 이내, 본문으로의 링크가 유효

### TASK-03: wf-implement 본문 — 의미 규칙과 어절 상쇄

- 상태: completed
- 완료: 2026-10-09 16:30
- 상위: 없음
- 목표: §2.4 테스트 작성 기준 5항(FR-08). §3.1 재개 시 `유지` 행 재실행 조건. §3.3 `completed` 전이의 등록·격리와 진행 중 기존 테스트 수정·제외·삭제 금지. §3.4 3튜플 귀속·인용 조건·별개 검증·분류 SHA 근거(DES-01), 결과 요약 정량 기록과 산출물 세 층(FR-02·03), references 트리거 문장(FR-09). §3.5 B/S/M 문항과 인용 SHA 문항(DES-06). §3.6 재정비 관문 한 문단. §5 1항("테스트 대장이 갱신되었다"). §7 소유 파일에 `docs/test-register.md`와 "대장이 없으면 첫 `completed` 전이에서 신설". 어절 상쇄는 DES-08 후보(§3.5 중복 문항, §3.4 4분류 문장, §3.3 §2.4 중복)에서.
- 관련 요구사항과 설계: FR-01, FR-02, FR-03, FR-05, FR-06, FR-07, FR-08, FR-09, NFR-02, NFR-05 / DES-01, DES-06, DES-07, DES-08
- 변경 대상: `skills/wf-implement/SKILL.md`
- 의존성: TASK-02(트리거 링크 대상)
- 위험: RISK-03 어절 상한 — 상쇄는 중복 문장에 한정하고 의미 삭제 금지. 작업 중 어절을 측정한다
- 검증 방법: TDD 부적용. TASK-06에서 AC-01·05·06 grep·통독, AC-09 어절 측정
- 완료 조건: AC-01·05·06의 grep 조건 충족, wf-implement+wf-doc 어절 합 ≤ 6,348

### TASK-04: docs/test-register.md 신설

- 상태: completed
- 완료: 2026-10-09 16:40
- 상위: 없음
- 목표: TASK-01 템플릿으로 `docs/test-register.md`(`REGISTER-llm-workflow`) 신설. TST-01 훅 러너(`powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1`, 22), TST-02 린트(`python -m pytest skills/wf-doc/scripts/tests -q`, 33), TST-03 pptx(`python docs/presentation/tests/test_make_pptx.py`, 3/8)를 보호 스코프·크기·발행 작업·상태·마지막 성공(일시·SHA)과 함께 등록. TST-01·02는 `유지`(같은 SHA 2회 통과: §3.1 재확인 1회 + 이 TASK 1회), TST-03은 `격리`(환경 원인, 후속 작업 비고). `## 재정비 기록`은 TASK-05 관문까지 빈 표.
- 관련 요구사항과 설계: FR-04, FR-05, FR-10 / DES-03, DES-09
- 변경 대상: `docs/test-register.md`(신설)
- 의존성: TASK-01
- 위험: 미커밋 상태라 SHA가 HEAD `1f98f7e` + dirty — 대장에 워킹트리 상태를 함께 적고, 커밋 후 SHA 갱신은 후속 작업으로 기록
- 검증 방법: 선행 — 자산 3묶음을 기록된 명령 그대로 실행해 결과·SHA를 행에 기입. TASK-06에서 AC-03
- 완료 조건: 행 3개가 템플릿 열을 모두 채우고 상태 어휘가 DES-04와 같다

### TASK-05: 자기 적용 — 작업 기록 검증 결과 형식과 재정비 관문

- 상태: completed
- 완료: 2026-10-09 16:44
- 상위: 없음
- 목표: 이 작업 `work-log.md`의 `## 검증 결과`를 DES-02 형식으로 전환(결과 요약 고정 필드, `분류` 열, `### 테스트 대장 변경` H3). 재정비 관문 1회 — 이 작업의 변경이 닿은 보호 스코프(스킬 산문·템플릿)의 테스트를 B/S/M으로 분류하고 폐기·병합 후보 유무를 기록(없으면 "변경 없음"). 결과를 대장 `## 재정비 기록`에 1행. req-design 추적표 작업 열을 TASK 링크로.
- 관련 요구사항과 설계: FR-02, FR-07, FR-10, NFR-03 / DES-02, DES-06, DES-09
- 변경 대상: `docs/work/20261009-test-lifecycle/work-log.md`, `req-design.md`, `docs/test-register.md`
- 의존성: TASK-01, TASK-04
- 위험: 전환 중 재개 정보 유실
- 롤백 준비(필수): 전환 전 work-log 사본을 스크래치에 보관하고 실패 시 복원. 커밋 후 `git revert`
- 검증 방법: TDD 부적용. 린트 0 오류, 측정 스크립트 기록률. TASK-06에서 AC-07·08
- 완료 조건: 린트 exit 0, 검증 표 각 행에 분류·SHA·명령, 대장 변경 H3에 관문 결과

### TASK-06: 검증·자체 리뷰·통합

- 상태: completed
- 완료: 2026-10-09 16:45
- 상위: 없음
- 목표: AC-01~11 판정(VER-01~11), §3.5 자체 리뷰(새 문항 2개 포함), 통합 — 전체 스위트 1회(자산 3묶음) + 대장 `유지` 행 전량, `docs/decisions.md` 행 확인, 어절 측정, `git diff --stat`로 완료 기록 무변경, 완료 보고와 인계 축약, 포트폴리오 행 제거.
- 관련 요구사항과 설계: FR-11, NFR-01, NFR-02, NFR-03, NFR-06 / DES-08, DES-10
- 변경 대상: `docs/work/20261009-test-lifecycle/work-log.md`, `docs/status.md`, `docs/decisions.md`(확인)
- 의존성: TASK-01~05
- 위험: 어절 상한 미달 시 TASK-03으로 되돌아가 상쇄 추가
- 검증 방법: 검증 계획 절의 명령
- 완료 조건: wf-implement §5 완료 조건 전부, 린트 0 오류, 포트폴리오 행 제거

## 검증 계획

| AC | 방법·명령 | TASK |
|---|---|---|
| AC-01, 05, 06 | `grep -n` 키워드(3튜플·인용·격리·Breaking·재정비 관문·test-register) + 해당 절 통독 | 06 |
| AC-02, 03 | 템플릿·유형표·필수 연결 grep, `docs/test-register.md` 절·행 대조, `python -m pytest skills/wf-doc/scripts/tests -q` 33/33 | 06 |
| AC-04 | `wc -l skills/wf-implement/references/verification-depth.md` ≤ 100, 표 4개 통독 | 06 |
| AC-07 | `python skills/wf-doc/scripts/lint_worklog.py` exit 0, 검증 표 열 대조 | 05, 06 |
| AC-08 | `python docs/research/20260919-aidlc-research/measure_regression_baseline.py .` 이 작업 행 100% | 05, 06 |
| AC-09 | 어절 측정(req-design 조사 절의 Python 함수) ≤ 6,348 | 03, 06 |
| AC-10 | `git diff --stat` 완료 기록·선행 ADR·DCR·린트 스크립트 무변경, pytest 33/33 | 06 |
| AC-11 | `docs/decisions.md` ADR-007~009 행 `approved`·재발행 비고 | 06 |

## 마이그레이션과 롤백

- 마이그레이션: 없음. 기존 완료 work-log는 소급하지 않는다(NFR-01). 대장은 신설이며 다른 저장소는 첫 `completed` 전이에서 신설한다(§7 규정).
- 롤백: 커밋 전 추적 파일은 `git checkout -- <파일>`, 신설 파일은 삭제. 커밋 후 `git revert`. TASK-05 전환 전 사본 보관.

## 인계

- 다음 단계 또는 워크플로우: wf-implement §3.3 구현 — 진행 상태와 재개는 [작업 기록 인계](./work-log.md#인계)가 정본
- 시작 조건: 충족 — 기준선 v1, §3.1 재확인 완료
- 입력 문서와 기준선: [REQ-DESIGN-test-lifecycle v1](./req-design.md), ADR-007~009
- 완료된 항목: 계획 수립, 계획 트리 생성, TASK-01~06
- 미완료 항목: 없음
- 차단 요인: 없음

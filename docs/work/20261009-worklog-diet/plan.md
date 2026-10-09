# PLAN-20261009-worklog-diet: 구현 계획 — 작업 기록 다이어트·아카이빙·린트

> 문서 유형: `plan`
> 작업 ID: `20261009-worklog-diet`
> 상태: `completed`
> 기준선: `v1` ([REQ-DESIGN-worklog-diet](./req-design.md), 2026-10-09 승인)
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [REQ-DESIGN-worklog-diet: 요구사항·설계](./req-design.md), [ADR-005: 작업 기록의 수명주기](./ADR-005-작업-기록-수명주기.md), [ADR-006: 작업 기록 린트의 B층 배치](./ADR-006-작업-기록-린트-B층.md), [DCR-007: 훅 닫힘 상태에 on-hold 추가](./DCR-007-훅-닫힘-상태-on-hold.md), [WORK-20261009-worklog-diet: 작업 기록](./work-log.md)

## 요약

- 목적: 기준선 v1(FR-01~09, NFR-01~04, DES-01~10)을 템플릿·스킬 본문·린트 스크립트·훅·자기 적용의 작업 7개로 번역하고 AC-01~09로 검증한다.
- 현재 결론 또는 상태: 완료 — TASK-01~07 완료(2026-10-09 15:25), AC-01~09 9/9. 결과는 [작업 기록](./work-log.md#완료-보고).
- 다음 행동: 없음

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-worklog-diet](./req-design.md) | FR-01~09, NFR-01~04, AC-01~09, DES-01~10 | 승인 기준선 v1 |
| input | decision | [ADR-005](./ADR-005-작업-기록-수명주기.md), [ADR-006](./ADR-006-작업-기록-린트-B층.md) | document | 아카이빙 시점, 린트 위치·언어 |
| input | change | [DCR-007](./DCR-007-훅-닫힘-상태-on-hold.md) | 변경 항목 | TASK-05의 입력(C층 v2) |
| output | implementation | [WORK-20261009-worklog-diet: 작업 기록](./work-log.md) | document | 수행 기록·검증 결과의 정본 |
| input | related | [ST-llm-workflow: 포트폴리오](../../status.md) | document | 이 작업이 등재된 포트폴리오 |

## 기준선

- 관련 요구사항: [FR-01~09, NFR-01~04, AC-01~09](./req-design.md#기능-요구사항)
- 관련 설계: [DES-01~10](./req-design.md#설계)
- 관련 ADR·DCR: [ADR-005](./ADR-005-작업-기록-수명주기.md), [ADR-006](./ADR-006-작업-기록-린트-B층.md), [DCR-007](./DCR-007-훅-닫힘-상태-on-hold.md)

## 작업 정의

- 목표: 작업 기록 합본 템플릿·필드 축소·아카이빙 시점·린트 실행 시점을 스킬에 반영하고, 린트 스크립트와 교정 규칙을 신설하며, 훅의 닫힘 상태에 `on-hold`를 추가하고, 이 작업의 기록에 자기 적용한다.
- 범위·범위 밖·가정·위험: [기준선 문서](./req-design.md#범위) 참조.
- 트리 사용 결정: **사용** — 작업 7개, 의존(TASK-04→01, TASK-06→01·04, TASK-07→전체).
- TDD 적용: TASK-04(린트)와 TASK-05(훅)는 자동 테스트 체계(pytest, `run-tests.ps1`)가 있어 Red→Green을 적용한다. TASK-01·02·03·06은 Markdown 규칙 문서라 [wf-implement §3.3](../../../skills/wf-implement/SKILL.md#33-구현)의 "사이클을 적용할 수 없는 변경"으로 분류하고 TASK-07의 후행 검증(grep·통독·린트·어절 측정)으로 대체한다.
- 작업 순서의 이유: 합본 절 목록의 정본은 템플릿(TASK-01)이므로 린트(TASK-04)보다 먼저 확정한다. 린트가 있어야 자기 적용(TASK-06)을 기계로 판정할 수 있다.

## 계획 트리

<!-- generated: 2026-10-09 14:50 — 계획 최초 작성 시 1회 생성. 이후 목록이 정본이며 트리는 요청 시에만 재생성 -->

```text
[작업] 20261009-worklog-diet — 작업 기록 다이어트·아카이빙·린트 ............ in-progress (0/7)
├─ [ ] 구현: wf-doc 템플릿 — 합본 템플릿·수행 기록 필드·verification/completion 포인터 (TASK-01)
├─ [ ] 구현: wf-doc 본문 §2.1·§2.7·§4 + references/worklog-style.md (TASK-02)
├─ [ ] 구현: wf-implement §7 아카이빙·린트 시점, §5 완료 조건 (TASK-03)
├─ [ ] 구현: 린트 스크립트 lint_worklog.py (TASK-04) ........................ depends: TASK-01
│   ├─ [ ] 테스트: pytest L1~L9 실패 fixture (선행)
│   └─ [ ] 리뷰: 자체 리뷰 → TASK-07
├─ [ ] 구현: DCR-007 — wf-common.ps1 정규식, run-tests T03b (TASK-05)
│   ├─ [ ] 테스트: T03b Red 실행 (선행)
│   └─ [ ] 검증: AC-07 호환성(기존 21케이스 통과) → TASK-07
├─ [ ] 전환: 자기 적용 — 이 작업 work-log 합본 전환, 추적 링크 (TASK-06) ... depends: TASK-01, TASK-04
│   └─ [ ] 롤백 준비: git checkout 경로 기록 (필수)
└─ [ ] 검증: AC-01~09 판정, 자체 리뷰, 통합 (TASK-07) ....................... depends: TASK-01~06
```

## 작업 목록

### TASK-01: wf-doc 템플릿 — 합본 템플릿과 수행 기록 필드

- 상태: completed
- 완료: 2026-10-09 14:58
- 상위: 없음
- 목표: `templates.md`의 work-log 절을 "작업 기록 합본" 템플릿(FR-03의 H2 8개·H3)으로 교체하고 수행 기록 골격을 FR-01 필드로 바꾼다. verification·completion 절은 합본의 해당 절을 가리키는 포인터로 축소한다.
- 관련 요구사항과 설계: FR-01, FR-03, NFR-02 / DES-01
- 변경 대상: `skills/wf-doc/references/templates.md`(목차 포함)
- 의존성: 없음
- 위험: RISK-05 — 포인터 문장으로 단독 파일 사용을 보장
- 검증 방법: TDD 부적용(산문). TASK-07에서 AC-01 통독·grep
- 완료 조건: 합본 템플릿 H2가 FR-03과 순서까지 같고 `변경 파일` 필드가 없다

### TASK-02: wf-doc 본문과 교정 규칙 참조 문서

- 상태: completed
- 완료: 2026-10-09 15:02
- 상위: 없음
- 목표: wf-doc §2.1 합본 규칙, §2.7 완료 시 인계 축약 형태, §4 자체 검토 항목 교체(린트 0 오류, 실행 불가 시 수동 검토 기록), 산문 교정 참조 링크. `references/worklog-style.md` 신설(변환표, 전후 예시 1쌍, 린트 코드별 교정 방법).
- 관련 요구사항과 설계: FR-04(b), FR-05, NFR-04 / DES-03, DES-04
- 변경 대상: `skills/wf-doc/SKILL.md`, `skills/wf-doc/references/worklog-style.md`(신설)
- 의존성: 없음
- 위험: 본문 어절 증가(NFR-04) — 세부는 references로
- 검증 방법: TDD 부적용. TASK-07에서 AC-06·AC-09
- 완료 조건: §4의 링크·앵커 수동 항목이 없고 린트 항목이 있으며 worklog-style.md가 링크된다

### TASK-03: wf-implement §7·§5

- 상태: completed
- 완료: 2026-10-09 15:10
- 상위: 없음
- 목표: §7 작업 기록 내용 목록 교체, 불변식의 변경 파일 문구 교체, 아카이빙 시점 소절(FR-04 a·b·c), 린트 소절(실행 시점 3곳·명령·오류 시 미전달·Python 부재 대체). §5 완료 조건 1항.
- 관련 요구사항과 설계: FR-01, FR-02, FR-04, FR-06, NFR-04 / DES-02
- 변경 대상: `skills/wf-implement/SKILL.md`
- 의존성: 없음
- 위험: 본문 어절 증가 — 기존 중복 문장 삭제로 상쇄
- 검증 방법: TDD 부적용. TASK-07에서 AC-02·AC-09
- 완료 조건: AC-02의 grep 조건 충족

### TASK-04: 린트 스크립트 lint_worklog.py (TDD)

- 상태: completed
- 완료: 2026-10-09 15:16
- 상위: 없음
- 목표: DES-05의 L1~L9 검사를 표준 라이브러리로 구현. 기본 대상 탐색(열린 work-log + status.md), 인자 경로, 출력 형식, exit code, 상단 상수.
- 관련 요구사항과 설계: FR-02, FR-06, NFR-03 / DES-05, DES-07
- 변경 대상: `skills/wf-doc/scripts/lint_worklog.py`, `skills/wf-doc/scripts/tests/test_lint_worklog.py`(신설)
- 의존성: TASK-01(절 목록 정본)
- 위험: 앵커 슬러그 규칙 불일치(한글 제목) — 사이클 1 검사 스크립트와 같은 규칙 사용
- 검증 방법: 선행 테스트 — 검사 항목별 실패 fixture로 Red 실행(`python -m pytest skills/wf-doc/scripts/tests -q`), Green 후 저장소 루트 실행 exit code. 최초 실패·성공 실행을 작업 기록에 남김
- 완료 조건: pytest 전부 통과, 저장소 루트 실행 exit 0(이 작업 work-log는 TASK-06 전이라 오류가 날 수 있으며 그 경우 TASK-06 후 재실행)

### TASK-05: DCR-007 — 훅 닫힘 상태에 on-hold (TDD)

- 상태: completed
- 완료: 2026-10-09 15:21
- 상위: 없음
- 목표: `wf-common.ps1`의 닫힘 정규식에 `on-hold` 추가, `run-tests.ps1`에 T03b(on-hold만 있을 때 무주입·기준점 기록).
- 관련 요구사항과 설계: FR-07 / DES-08, DCR-007 변경 항목
- 변경 대상: `setup/hooks/wf-common.ps1`, `setup/hooks/tests/run-tests.ps1`
- 의존성: 없음
- 위험: 기존 21케이스 회귀 — 전체 러너로 확인
- 검증 방법: 선행 테스트 — T03b를 먼저 추가해 실패(Red) 확인 후 정규식 수정(Green). `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1`
- 완료 조건: 22/22 통과, Red 실행 기록

### TASK-06: 자기 적용 — 작업 기록 합본 전환과 추적 링크

- 상태: completed
- 완료: 2026-10-09 15:22
- 상위: 없음
- 목표: 이 작업의 `work-log.md`를 TASK-01 합본 템플릿으로 전환(현재 상태·미완료 항목·재개 지점 절 제거, 수행 기록 필드 교체, 검증 결과·완료 보고 절 골격). req-design 추적표 작업 열과 DCR-007 문서 연결 verification 행을 TASK 링크로 채운다.
- 관련 요구사항과 설계: FR-08, NFR-01 / DES-09
- 변경 대상: `docs/work/20261009-worklog-diet/work-log.md`, `req-design.md`, `DCR-007-훅-닫힘-상태-on-hold.md`
- 의존성: TASK-01, TASK-04
- 위험: 전환 중 재개 정보 유실 — 인계 절을 먼저 갱신한 뒤 절 제거
- 롤백 준비(필수): 커밋 전 `git checkout -- <파일>`는 미추적 폴더라 불가 → 전환 전 사본을 스크래치에 보관하고 실패 시 복원. 커밋 후 `git revert`
- 검증 방법: TDD 부적용. 린트 실행(`python skills/wf-doc/scripts/lint_worklog.py`) 0 오류
- 완료 조건: AC-04 충족(H2 ≤ 8, 펜스 0, 불릿 ≤ 300자, 항목 ≤ 8행, ≤ 13KB, 린트 0 오류)

### TASK-07: 검증·자체 리뷰·통합

- 상태: completed
- 완료: 2026-10-09 15:25
- 상위: 없음
- 목표: AC-01~09 판정(VER-01~09), wf-implement §3.5 자체 리뷰, 링크 전수 검사, 어절 측정, 완료 보고 작성, status.md 행 제거(FR-04 b 자기 적용).
- 관련 요구사항과 설계: AC-01~09 전체
- 변경 대상: `work-log.md`(검증 결과·완료 보고), `docs/status.md`, `docs/decisions.md`(불일치 시)
- 의존성: TASK-01~06
- 위험: 없음
- 검증 방법: [검증 계획](#검증-계획)
- 완료 조건: AC-01~09 결과 기록, 실패 0 또는 실패 분류 기록

## 검증 계획

| 검증 ID | 인수 조건 | 방법 | 수행 TASK |
|---|---|---|---|
| VER-01 | AC-01 | templates.md H2 목록 추출(Python)과 FR-03 대조, `변경 파일` grep | TASK-07 |
| VER-02 | AC-02 | wf-implement §7·§5 grep("아카이빙", "린트", "변경 파일") | TASK-07 |
| VER-03 | AC-03 | pytest Red/Green 기록, 저장소 루트 실행 exit code | TASK-04, TASK-07 |
| VER-04 | AC-04 | 린트 실행 + 파일 크기·H2 수·불릿 길이 측정 | TASK-06, TASK-07 |
| VER-05 | AC-05 | `git diff --stat docs/work/2026080* docs/work/20260817* docs/work/20261009-plan-relocation` | TASK-07 |
| VER-06 | AC-06 | wf-doc §4 grep, worklog-style.md 존재·링크 | TASK-07 |
| VER-07 | AC-07 | run-tests.ps1 Red(21/22)·Green(22/22) 기록, REQ·DESIGN v2·등록부 grep | TASK-05, TASK-07 |
| VER-08 | AC-08 | decisions.md grep, 링크 전수 검사 스크립트 | TASK-07 |
| VER-09 | AC-09 | 어절 측정(같은 함수) 합 ≤ 6,351 | TASK-07 |

## 마이그레이션과 롤백

- 마이그레이션: 완료 로그 7편은 손대지 않는다(NFR-01). 새 템플릿은 이 작업부터 적용.
- 롤백: 커밋 전 `git checkout -- skills setup docs/requirements.md docs/design.md docs/decisions.md docs/status.md` + 새 폴더·파일 삭제. 커밋 후 해당 커밋 `git revert`. 훅은 저장소 파일을 직접 실행하므로 되돌리면 즉시 반영.

## 인계

- 다음 단계 또는 워크플로우: 없음
- 완료된 항목: TASK-01~07(2026-10-09 15:25)
- 미완료 항목: 없음
- 다음 행동: 없음

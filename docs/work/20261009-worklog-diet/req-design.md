# REQ-DESIGN-worklog-diet: 작업 기록 다이어트·아카이빙·린트 — 요구사항·설계

> 문서 유형: `requirements, design`
> 작업 ID: `20261009-worklog-diet`
> 상태: `approved`
> 기준선: `v1` (승인일 2026-10-09)
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [wf-implement SKILL](../../../skills/wf-implement/SKILL.md), [wf-doc SKILL](../../../skills/wf-doc/SKILL.md), [wf-doc 템플릿](../../../skills/wf-doc/references/templates.md), [REQ-DESIGN-plan-relocation(사이클 1)](../20261009-plan-relocation/req-design.md), [ADR-005: 작업 기록의 수명주기](./ADR-005-작업-기록-수명주기.md), [ADR-006: 작업 기록 린트의 B층 배치](./ADR-006-작업-기록-린트-B층.md), [DCR-007: 훅 닫힘 상태에 on-hold 추가](./DCR-007-훅-닫힘-상태-on-hold.md), [WORK-20261009-worklog-diet: 작업 기록](./work-log.md)

## 요약

- 목적: 작업 진행 중 작업 기록(work-log)에 쌓이는 로그와 산문을 줄인다. (4) 로그의 아카이빙 시점을 상태 전이에 고정하고, (5) 산문을 기계적으로 잡아내는 린트와 교정 규칙을 두고, (6) 작업 기록 템플릿의 필드와 중복 절을 줄인다. 요구사항·설계 문서는 다이어트 대상이 아니다(사용자 요구 6).
- 현재 결론 또는 상태: 기준선 v1 승인(2026-10-09) — Q-01~Q-05 전부 권장안, ADR-005·006 승인, DCR-007 승인(REQ·DESIGN-llm-workflow v2). 구현은 [작업 기록](./work-log.md).
- 다음 행동: wf-implement 계획 수립·구현([작업 기록](./work-log.md) 인계 절).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | N/A | document | 이 작업의 루트 문서. 변경 대상이 스킬 규칙·스크립트이며 C층 훅 기준선과 시스템이 다르다(선례: [plan-relocation](../20261009-plan-relocation/req-design.md)). 단 Q-02 포함 시 C층 기준선은 DCR-007로 변경 |
| input | related | [REQ-DESIGN-plan-relocation](../20261009-plan-relocation/req-design.md) | 제외 절, 후속 작업 | 사이클 1. 스냅숏 의무 폐지·작업별 plan을 전제로 이 작업이 시작됨 |
| input | related | [wf-implement §5·§6·§7](../../../skills/wf-implement/SKILL.md#7-작업-기록과-저장-위치), [wf-doc §2.1·§2.7·§4](../../../skills/wf-doc/SKILL.md#21-문서-유형-결정), [wf-doc work-log·verification·completion 템플릿](../../../skills/wf-doc/references/templates.md#작업-기록-work-log) | 변경 대상 절 | 조사(2026-10-09)에서 확인한 현행 규칙 |
| input | related | [묶음 A — 스킬 다이어트 설계(조사)](../../research/20260919-aidlc-research/bundleA_skill_diet.md) | §2.3, §3.1, §5 | 냄새는 자연 치유되지 않음 → 도입 시점 차단(린트). 판정 규칙 R1~R5. 린트 체크리스트. 조사 기록이라 역방향 링크 없음(불변 기록) |
| input | related | [묶음 B — 훅·하네스(조사)](../../research/20260919-aidlc-research/bundleB_hooks_harness.md) | §(a) 투자 배분 | "모델이 자주 어기는 규칙부터 훅·스크립트로 승격". 조사 기록이라 역방향 링크 없음 |
| input | related | [WORK-20260814-multiuser-workflow](../20260814-multiuser-workflow/work-log.md) | 머리말 상태 | `on-hold` 작업이 매 세션 훅에 잡히는 실례(Q-02·DCR-007의 증거) |
| output | decision | [ADR-005: 작업 기록의 수명주기](./ADR-005-작업-기록-수명주기.md) | FR-04, DES-06 | 아카이빙 = 상태 전이 시 축약 + 제자리 동결. `approved`(2026-10-09) |
| output | decision | [ADR-006: 작업 기록 린트의 B층 배치](./ADR-006-작업-기록-린트-B층.md) | FR-06, DES-07 | 린트 위치·언어·실행 방식. `approved`(2026-10-09) |
| output | change | [DCR-007: 훅 닫힘 상태에 on-hold 추가](./DCR-007-훅-닫힘-상태-on-hold.md) | FR-07, DES-08 | Q-02 포함 결정(2026-10-09). [REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md) v1 → v2 승인. `approved` |
| output | implementation | [WORK-20261009-worklog-diet: 작업 기록](./work-log.md) | document | 진행 기록. 구현 계획(`plan.md`)은 승인 후 wf-implement가 작성 |

**산출물 위치에 대한 결정:** 선행 스킬 변경 작업들과 동일하게 작업 폴더의 통합 req-design 문서로 둔다. 승인 관문에서 사용자 확인을 받는다.

## 문제와 목적

사용자의 사용 경험(2026-10-09 세션, 요구 4·5·6 원문):

> 4) 작업기록, 인계절 등의 작업중 쌓이는 로그들의 적절한 아카이빙 타이밍을 설정한다.
> 5) 문서작업 중 산문이 발생하는 경우에 대한 문서 교정 방안을 마련한다.
> 6) 5번과 연계하여 문서의 다이어트안을 준비한다. 이 다이어트는 설계와 요구사항 도출에 관련되어있지 않고, 작업기록을 중심으로 작업 진행도중 발생하는 로그와 산문에 대한 다이어트를 뜻한다.

같은 세션에서 사용자가 승인한 사이클 편성의 방향: 상태 전이 기반 아카이빙, 조사 기록의 판정 규칙 R1~R5 적용, 작업 기록 린트. 사이클 1(계획 문서 재배치)이 스냅숏 의무를 없앤 뒤에 진행한다는 조건은 충족됐다(2026-10-09 14:08 완료).

## 현재 상태 조사 (wf-design §4.1)

### 사실

- **작업 기록 내용 규정**: [wf-implement §7](../../../skills/wf-implement/SKILL.md#7-작업-기록과-저장-위치)은 작업 기록에 "기준선과 현재 계획, 실제 수행 내용, 변경 파일, 발견과 결정, 실행한 검증, 설계와 달라진 점, 미완료 항목과 재개 지점"을 포함하라고 하고, 상시 재개 가능 불변식에서 "계획 항목 하나를 완료할 때마다 갱신", "git으로 재구성할 수 있는 내용(변경 파일 목록, diff 세부)은 간결하게"를 규정한다. 검증 결과(`verification`)와 완료 보고(`completion`)는 별도 파일 없이 work-log에 합치고 "각 유형의 필수 절을 유지"한다. §5 완료 조건과 §6 최종 보고는 이 합본 절을 전제한다.
- **템플릿**: [work-log 템플릿](../../../skills/wf-doc/references/templates.md#작업-기록-work-log)은 현재 상태(3필드), 수행 기록 항목(수행 내용·변경 파일·발견 사항·결정과 이유·실행한 검증·결과 6필드), 설계와 달라진 점, 미완료 항목, 재개 지점(3필드). [verification 템플릿](../../../skills/wf-doc/references/templates.md#검증-결과-verification)은 7절(범위와 환경, 결과 요약, 인수 조건별 결과, 실패와 미수행 분석, 비기능 검증, 남은 위험, 재검증 조건). [completion 템플릿](../../../skills/wf-doc/references/templates.md#완료-보고-completion)은 10절(완료 상태, 완료한 내용, 주요 변경, 설계와 달라진 점, 인수 조건 충족 여부, 검증 결과와 증거, 통합 상태, 남은 위험과 제한, 후속 작업, 인계). 여기에 [wf-doc §2.7](../../../skills/wf-doc/SKILL.md#27-인계와-재개-지점-작성)의 인계 절(7필드 + 재개 프롬프트)이 더해진다. 템플릿 행수: work-log 39, verification 37, completion 33.
- **실측(2026-10-09, Python, 저장소 루트)**: 작업 기록 8편은 76~234행, 8.7~26.0KB. 사이클 1(`20261009-plan-relocation`) work-log가 최대 — 234행, 26,030바이트, H2 13개·H3 24개, 수행 기록 68행, 완료 보고 56행, 검증 결과 46행. 불릿 90개 중 300자 초과 6개, 최장 680자. 같은 의미의 절이 한 파일에 중복: 설계와 달라진 점 2곳, 남은 위험 2곳, 인계 2곳, "다음 행동"이 요약·현재 상태·재개 지점·인계·완료 보고 인계 5곳. 완료 로그 7편 중 4편은 계획 트리 스냅숏 22~30행을 가진다(동결).
- **아카이빙**: 현행 규정에 개념이 없다. 완료 로그는 `docs/work/<작업-ID>/`에 영구히 그대로 남는다. 훅(`setup/hooks/wf-common.ps1`)은 `docs/work/*/work-log.md` 머리말의 상태만 읽으므로 완료 로그의 위치·내용은 훅 동작과 무관하다. 완료 작업 폴더로 들어오는 링크: `docs/requirements.md` 13곳, `docs/design.md` 18곳, `docs/decisions.md` 8곳, `docs/status.md`, 스킬 예시 1곳, 훅 주석 1곳.
- **훅 닫힘 상태**: `completed|superseded|rejected|withdrawn`. `on-hold`는 열린 작업으로 취급되어 매 세션 재개 안내에 등장한다(현재 `20260814-multiuser-workflow` 1건). 이 판정은 [REQ-llm-workflow FR-01](../../requirements.md#기능-요구사항)·[DESIGN-llm-workflow DES-01](../../design.md#컴포넌트와-책임) 기준선 v1의 일부라 바꾸려면 DCR이 필요하다(사이클 1 세션에서도 "사이클 2와 함께"로 권고됨).
- **도구와 선례**: Python 3.13·pytest 9.1 가용. 저장소에 Python 선례(`docs/presentation/make_pptx.py` + `tests/`, 조사 폴더의 `measure_regression_baseline.py`)가 있고 훅 테스트는 PowerShell 자체 러너(`setup/hooks/tests/run-tests.ps1`, 21케이스). `skills/`는 `~/.claude/skills/`로 junction되므로 `skills/` 아래의 스크립트는 이 워크플로우를 설치한 모든 저장소에서 실행할 수 있다. [REQ-llm-workflow 범위](../../requirements.md#범위)는 "B층 독립 스크립트(재개 가능성 린트 등) — 필요가 확인되면 별도 작업"으로 남겨 두었다.
- **스킬 본문 어절(NFR-04 기준값, `len(text.split())`, frontmatter 제외)**: wf-implement 3,214, wf-doc 3,137. 합 6,351.
- **조사 근거**: [묶음 A §2.3](../../research/20260919-aidlc-research/bundleA_skill_diet.md) — "한번 들어온 냄새는 거의 제거되지 않는다", 유일하게 검증된 개입 지점은 도입 시점 차단(커밋 전 린트). §3.1 판정 규칙 R1(항상 필요한 판단 규칙은 본문)·R2(절차 세부는 references)·R4(기계적으로 재현 가능한 것은 스크립트). [묶음 B §(a)](../../research/20260919-aidlc-research/bundleB_hooks_harness.md) — 규칙은 짧게, 자주 어기는 규칙은 스크립트·훅으로 승격.

### 해석

- 비대화의 원인은 셋이다. (a) 합본 시 세 유형의 필수 절을 모두 유지하라는 규정이 같은 의미의 절을 2~5중으로 만든다. (b) 수행 기록 필드 6개 중 `수행 내용`은 계획의 TASK 목표와, `변경 파일`은 git과 중복이며 둘 다 산문으로 자란다. (c) "간결하게"라는 불변식은 산문 규칙이라 집행 수단이 없다 — 가장 최근 로그가 가장 크다는 실측이 이를 보인다. 조사가 내린 결론(산문 규칙 추가가 아니라 기계적 검사)과 같다.
- 아카이빙은 파일 이동이 아니라 **상태 전이 시점의 축약과 동결**로 정의하는 것이 비용이 가장 낮다. 이동은 들어오는 링크 40여 곳의 수리를 매번 요구하고, 사이클 1이 세운 완료 문서 불변 원칙과도 충돌한다. 훅은 위치에 의존하지 않으므로 이동의 이점이 없다.
- 린트는 `skills/` 아래 Python 표준 라이브러리 스크립트가 적합하다. 다른 저장소에서도 동작해야 하고(이식성), 하네스에 의존하지 않아야 하며(README 실행 기준), 저장소에 Python·pytest 선례가 있다. 훅(C층) 연동은 범위 밖이다.
- 완료 로그 7편은 소급 다이어트하지 않는다. 동결 기록이며 git이 정본이다(사이클 1 NFR-02 선례).

### 가정

- 이 저장소의 사용자는 1인이다.
- 린트를 실행하는 환경에 Python 3.9 이상이 있다. 없으면 wf-doc §4의 수동 검토로 대체하고 그 사실을 작업 기록에 남긴다(RISK-03).
- 상한값(DES-05의 상수)은 이 작업의 측정값으로 정한 초깃값이며 두 사이클 운용 후 조정할 수 있다.

## 범위

### 포함

- `skills/wf-implement/SKILL.md` — §7 작업 기록 내용 목록·아카이빙 시점·린트 실행 시점, §5 완료 조건 1항
- `skills/wf-doc/SKILL.md` — §2.1 합본 규칙, §2.7 완료 시 인계 축약, §4 자체 검토(링크·앵커 수동 항목 → 린트 결과)
- `skills/wf-doc/references/templates.md` — work-log·verification·completion을 합본 템플릿 하나로, 수행 기록 골격 필드 축소
- 신규 `skills/wf-doc/references/worklog-style.md` — 산문 교정 규칙(변환표)
- 신규 `skills/wf-doc/scripts/lint_worklog.py` + `skills/wf-doc/scripts/tests/test_lint_worklog.py`
- Q-02 포함 시: [DCR-007](./DCR-007-훅-닫힘-상태-on-hold.md), `setup/hooks/wf-common.ps1` 정규식 1토큰, `run-tests.ps1` 케이스 1개, `docs/requirements.md`·`docs/design.md` v2
- 이 작업의 자기 적용(작업 기록을 새 합본 템플릿으로, 린트 0 오류)
- ADR-005·ADR-006 발행·등록, `docs/decisions.md`, `docs/status.md`

### 제외

- 완료된 작업 기록 7편의 소급 다이어트·이동(동결 기록, NFR-01)
- 요구사항·설계 문서(`req-design.md`, `requirements.md`, `design.md`)와 `plan.md`의 다이어트 — 사용자 요구 6이 명시적으로 제외
- 스킬 본문(SKILL.md) 린트(조사 AI-13의 ★ 항목) — 대상이 다르다. 별도 작업
- 린트의 훅(C층) 집행(Stop·PreCommit 훅) — 이 작업은 수동 실행과 스킬의 실행 시점 규정까지. 후속 작업 후보
- 경량 경로 문서(wf-doc §2.8)의 형식 — 변경 없음. 린트는 정식 경로 work-log만 검사
- 테스트 결과·커버리지 기록 형식 — 사이클 3

## 기능 요구사항

| ID | 항목 | 내용 |
|---|---|---|
| FR-01 | 수행 기록 필드 축소 | TASK별 수행 기록 항목의 필드를 `결정과 이유`(필수, 없으면 `없음`), `발견 사항`(선택), `검증`(필수 — VER 링크, 실행 명령 1줄, 또는 `없음 — 이유`), `결과`(필수 — 완료·부분 완료·차단 + `YYYY-MM-DD HH:MM`)로 줄인다. `수행 내용`은 계획의 TASK 목표와 다르게 수행했을 때만 쓰는 선택 필드. `변경 파일` 필드는 폐지한다(git이 정본, 미커밋 변경은 인계 절 한 줄) — [Q-03](#가정과-미해결-질문) |
| FR-02 | 분량 상한 | 수행 기록 항목 하나는 8행·600자 이하, 불릿 하나는 300자 이하, 작업 기록에 펜스 코드블록 0개(명령·경로는 인라인 코드). 파일 12KB 초과는 경고. 상한은 린트가 검사하고(FR-06) 초과분은 교정 규칙(FR-05)으로 줄인다 — [Q-04](#가정과-미해결-질문) |
| FR-03 | 합본 단일 템플릿 | work-log + verification + completion 합본의 절 목록을 하나로 고정하고 같은 의미의 절은 한 번만 둔다. H2: 요약, 문서 연결, 기준선과 현재 계획, 수행 기록, 설계와 달라진 점, 검증 결과(H3: 범위와 환경·결과 요약·인수 조건별 결과·실패와 미수행 분석), 완료 보고(H3: 완료 상태·주요 변경·통합 상태·남은 위험과 제한·후속 작업), 인계 — 8개. 삭제: 현재 상태, 미완료 항목, 재개 지점, 비기능 검증(표의 NFR 행으로), 남은 위험·재검증 조건(완료 보고의 남은 위험과 제한·후속 작업으로), 완료한 내용·설계와 달라진 점·인수 조건 충족 여부·검증 결과와 증거·인계(completion 쪽 중복) |
| FR-04 | 아카이빙 시점 | 상태 전이를 트리거로 한다([ADR-005](./ADR-005-작업-기록-수명주기.md)). (a) TASK `completed` 전이 = 그 TASK의 수행 기록 항목을 한 번 확정해 쓰는 시점. 진행 중 메모는 항목이 아니라 인계 절의 다음 행동에만 둔다. (b) 작업 `completed`(완료 보고 종결) = 인계 절 축약(재개 프롬프트·미커밋 변경·시작 조건 제거, 다음 행동 `없음`), 기준선과 현재 계획의 진행 서술 삭제, `docs/status.md` 행 제거(기존 규칙). (c) 완료 로그는 작업 폴더에 제자리 동결 — 이동·소급 편집 없음 — [Q-01](#가정과-미해결-질문), [Q-05](#가정과-미해결-질문) |
| FR-05 | 산문 교정 규칙 | 린트가 지적한 산문을 필드로 바꾸는 변환 규칙을 `references/worklog-style.md`에 둔다: 결정은 "선택 — 이유" 한 문장, 사실은 수치·링크, 경과 서술은 삭제, 반복 설명은 정본 링크. wf-doc §4 자체 검토에서 링크·앵커 수동 검사 항목을 "린트 0 오류"로 교체한다 |
| FR-06 | 린트 스크립트 | `skills/wf-doc/scripts/lint_worklog.py`(Python 3 표준 라이브러리)가 머리말, 합본 절 목록·순서·중복, 수행 기록 필드·분량, 펜스, 불릿 길이, 로컬 링크·앵커, 인계 절(열린 상태의 7필드·재개 프롬프트 형식, completed의 `다음 행동: 없음`), `docs/status.md` 행 정합, 파일 크기를 검사한다. 기본 대상은 열린 상태의 work-log 전부와 `docs/status.md`, 인자로 경로를 주면 그 파일. 오류가 있으면 exit 1. 실행 시점은 wf-implement §7이 규정: TASK 완료 기록 후, 세션 인계 전, 완료 보고 종결 전([ADR-006](./ADR-006-작업-기록-린트-B층.md)) |
| FR-07 | 훅 닫힘 상태(조건부) | [Q-02](#가정과-미해결-질문) 포함 시: 세션 시작·컴팩션 사후 훅의 "미완료" 판정에서 `on-hold`를 제외한다([DCR-007](./DCR-007-훅-닫힘-상태-on-hold.md)). 요구사항 FR-01 문구·설계 DES-01 완료 계열·`wf-common.ps1` 정규식·훅 테스트 1케이스. Q-02 제외 시 이 FR과 DES-08·AC-07은 무효이며 DCR-007은 `withdrawn` |
| FR-08 | 자기 적용 | 이 작업의 작업 기록을 승인 후 새 합본 템플릿과 필드로 전환하고 린트 0 오류로 유지한다. 완료 보고 종결 시 FR-04(b)를 적용한다 |
| FR-09 | ADR·DCR 정합 | ADR-005·ADR-006을 발행·등록하고 승인 시 `approved`. DCR-007은 Q-02 결정에 따라 `approved` 또는 `withdrawn`. 등록부 행이 파일과 일치한다 |

## 비기능 요구사항

| ID | 항목 | 내용 |
|---|---|---|
| NFR-01 | 완료 문서 보존 | 완료 작업 기록 7편, 선행 req-design 6편, ADR-001~004·DCR-002의 내용은 바꾸지 않는다. 역방향 링크 행 추가만 허용 |
| NFR-02 | 템플릿 축소 | templates.md의 work-log·verification·completion 세 템플릿(현재 109행)이 합본 템플릿 하나로 줄고, 합본 H2가 8개 이하 |
| NFR-03 | 린트 결정성·이식성 | 표준 라이브러리만 사용, 네트워크 없음, 저장소 루트 기준 상대 경로만 전제(`docs/work/*/work-log.md`, `docs/status.md`), 이 저장소에서 1초 이내. 같은 입력에 같은 출력 |
| NFR-04 | 스킬 본문 증가 억제 | wf-implement·wf-doc SKILL.md 본문 어절 합(현재 6,351)이 작업 전 이하. 규칙 세부는 references·scripts로 보낸다 |

## 인수 조건

| ID | 조건 |
|---|---|
| AC-01 | templates.md에 work-log 합본 템플릿이 하나 있고 H2 절이 FR-03 목록과 순서까지 같다. verification·completion 독립 템플릿은 제거되거나 합본의 해당 절을 가리키는 포인터만 남는다. 수행 기록 골격 필드가 FR-01과 같고 `변경 파일`이 없다 |
| AC-02 | wf-implement §7에 아카이빙 시점 (a)(b)(c)와 린트 실행 시점 3곳이 있고 §5 완료 조건에 린트 통과 1항이 있다. "변경 파일"을 작업 기록 필수 내용으로 두는 규정이 0건 |
| AC-03 | 저장소 루트에서 `python skills/wf-doc/scripts/lint_worklog.py`가 exit 0. pytest가 검사 항목(L1~L9)마다 실패 입력에서 오류를 내고 통과 입력에서 내지 않음을 보이며, 각 테스트의 최초 실패 실행과 구현 후 성공 실행이 기록된다 |
| AC-04 | 이 작업의 work-log가 린트 0 오류이고, H2 8개 이하, 펜스 0, 불릿 300자 이하, 항목 8행 이하, 파일 13KB 이하(사이클 1 work-log 26KB의 50%) |
| AC-05 | 완료 작업 기록 7편·선행 req-design 6편·ADR·DCR 파일의 `git diff`가 역방향 링크 행 추가 외 무변경 |
| AC-06 | wf-doc §4의 링크·앵커 수동 검사 항목이 린트 결과 항목으로 교체되고, `references/worklog-style.md`가 존재하며 wf-doc SKILL.md에서 링크된다 |
| AC-07 | (Q-02 포함 시) `run-tests.ps1`에 on-hold 케이스가 추가되어 전체 통과(22/22), 추가 전 그 케이스만 실패하는 실행이 기록된다. `docs/requirements.md`·`docs/design.md`가 v2이고 DCR-007이 `approved`로 등록된다 |
| AC-08 | `docs/decisions.md`에 ADR-005·ADR-006 행(approved)이 있고, skills·docs 상대 링크 전수 검사에서 이 작업이 닿은 파일의 깨진 링크 0건 |
| AC-09 | wf-implement·wf-doc SKILL.md 본문 어절 합이 6,351 이하(같은 측정 방법) |

## 설계

| ID | 설계 요소 | 내용 |
|---|---|---|
| DES-01 | 합본 템플릿 | templates.md의 `## 작업 기록 (work-log)` 절을 "작업 기록 합본(work-log, verification, completion)" 템플릿으로 교체: FR-03의 8개 H2와 H3, 수행 기록 골격(`### YYYY-MM-DD — TASK-NN` + FR-01 필드), 검증 표(기존 열 유지), 완료 상태 필드, 인계 블록(§2.7 참조). `## 검증 결과 (verification)`·`## 완료 보고 (completion)` 절은 "별도 파일로 둘 때만 합본의 해당 절을 그대로 사용한다"는 3행 포인터로 축소. 문서 유형 `verification`·`completion`과 문서 ID `VERIFY-`·`RESULT-`는 유지(머리말 표기용) |
| DES-02 | wf-implement §7·§5 | §7 작업 기록 내용 목록을 "기준선과 현재 계획, TASK별 결정과 이유·발견·검증·결과, 설계와 달라진 점, 검증 결과, 완료 보고, 인계"로 교체. 불변식 문단의 "변경 파일 목록은 간결하게"를 "변경 파일은 기록하지 않는다(git 정본), 미커밋 변경만 인계 절에 한 줄"로. **아카이빙 시점** 소절 신설(FR-04 a·b·c). **린트** 소절 신설: 실행 시점 3곳, 명령, 오류 시 기록을 전달하지 않음, Python 부재 시 수동 검토 대체 기록. §5 완료 조건에 "작업 기록 린트가 0 오류" 1항 |
| DES-03 | wf-doc SKILL | §2.1 "여러 유형을 한 파일에 합치면 각 유형의 필수 절을 유지"를 "합본 템플릿이 있는 조합은 그 절 목록을 따르고 같은 의미의 절을 반복하지 않는다"로. §2.7에 완료 시 인계 블록의 축약 형태(다음 단계 `없음`, 완료된 항목, 미완료 `없음`, 다음 행동 `없음` — 4필드) 1문단. §4 자체 검토의 "모든 로컬 링크의 대상 파일이 존재하고…" 항목을 "작업 기록 린트가 0 오류인가(실행 불가 시 수동 검토와 그 사실 기록)"로 교체. 산문 교정은 `references/worklog-style.md` 링크 1문장 |
| DES-04 | 교정 규칙 참조 문서 | `skills/wf-doc/references/worklog-style.md`: 변환표(서술 유형 → 필드·형태, 5행 내외)와 전후 예시 1쌍(사이클 1 work-log의 680자 불릿 → 3행). 린트 코드(L1~L9)별 교정 방법 표. 60행 이내 |
| DES-05 | 린트 스크립트 | `skills/wf-doc/scripts/lint_worklog.py`. 입력: 인자 없음 → 현재 디렉터리에서 `docs/` 탐색(없으면 상위로 3단계), `docs/work/*/work-log.md` 중 머리말 상태가 닫힘 계열(`completed`·`superseded`·`rejected`·`withdrawn`, Q-02 포함 시 `on-hold`도) 아닌 파일 + `docs/status.md`; 인자 있음 → 지정 파일. 파서: 머리말 블록쿼트 필드, H2/H3 순서, 불릿, 펜스, 링크 `[..](..)`, GitHub 슬러그 앵커. 검사: L1 머리말 필수 필드·상태 어휘, L2 H2 목록·순서·중복(합본 템플릿), L3 수행 기록 항목 필드(필수 3개)·8행·600자, L4 펜스 0, L5 불릿 ≤300자, L6 링크·앵커 유효, L7 인계 절(열림: 7필드+재개 프롬프트 형식, completed: `다음 행동: 없음`·재개 프롬프트 없음), L8 status.md 정합(열림 ↔ 행 존재), L9 파일 >12KB 경고. 출력 `경로:행: E|W Lx 메시지`, 오류 1건 이상이면 exit 1. 상한값은 파일 상단 상수. 테스트 `scripts/tests/test_lint_worklog.py`(pytest, 문자열 fixture, 항목당 실패·통과 1쌍) |
| DES-06 | 수명주기 결정 | [ADR-005](./ADR-005-작업-기록-수명주기.md): 아카이빙은 이동이 아니라 상태 전이 시 축약·동결. 트리거 표 3행. 대안(달력 기준 이동, `docs/work/archive/` 이동, git 태그만) 비교 |
| DES-07 | B층 배치 결정 | [ADR-006](./ADR-006-작업-기록-린트-B층.md): 위치 `skills/wf-doc/scripts/`(junction으로 전 저장소 이식), 언어 Python 표준 라이브러리, 실행은 수동 + 스킬 규정 시점, 훅 연동은 후속. 대안(PowerShell/`setup/`, 저장소 로컬 `tools/`, Stop 훅 즉시 도입) 비교 |
| DES-08 | 훅 닫힘 상태(조건부) | [DCR-007](./DCR-007-훅-닫힘-상태-on-hold.md): REQ-llm-workflow FR-01 "완료되지 않은" → "열린(`on-hold` 제외)", DESIGN DES-01 완료 계열에 `on-hold`, `wf-common.ps1` 정규식 `(completed|superseded|rejected|withdrawn|on-hold)`, `run-tests.ps1`에 T03b(on-hold만 있을 때 무주입). 승인 시 REQ·DESIGN v2. 린트 L8의 열림 판정도 같은 목록을 쓴다 |
| DES-09 | 자기 적용 | 승인 후 첫 TASK에서 이 작업의 work-log를 DES-01 합본으로 전환(현재 상태·재개 지점 절 제거, 수행 기록 필드 교체). 이후 TASK 완료마다 FR-04(a), 종결 시 FR-04(b). 린트는 구현 직후부터 이 파일에 적용 |
| DES-10 | ADR·DCR 발행 | ADR-005·006은 이 문서와 함께 `proposed` → 승인 시 `approved`. DCR-007은 Q-02 포함 시 같은 관문에서 재승인(요구사항 변경 분류), 제외 시 `withdrawn`. 번호는 main 이력 기준(등록부 마지막 ADR-004의 다음). 보관 브랜치 `archive/202609-cycles`의 ADR-005·DCR-006과 번호가 겹치는 사실을 각 문서에 기록 |

### 검증 전략

- AC-01·02·06·09: 템플릿·스킬 파일 통독과 grep, 어절 측정(같은 Python 함수). 명령과 결과를 작업 기록에 남긴다.
- AC-03: pytest Red→Green(검사 항목별 실패 fixture 먼저), 저장소 루트 실행 exit code.
- AC-04·08: 린트 실행 결과와 링크 전수 검사 스크립트(사이클 1 VER-07 방법 재사용).
- AC-05: `git diff --stat` 대상 파일.
- AC-07: `run-tests.ps1` 실행(추가 케이스 Red 실행 포함).

## 가정과 미해결 질문

| ID | 질문 | 권장 | 근거 | 결정(2026-10-09) |
|---|---|---|---|---|
| Q-01 | 완료 작업 폴더를 `docs/work/archive/`로 이동할 것인가? | **이동 없음**(제자리 동결) | 들어오는 링크 40여 곳 수리, 훅은 위치 무관, 완료 문서 불변(사이클 1 NFR-02). 조망은 `docs/work/` 목록과 git | **이동 없음** |
| Q-02 | 훅의 닫힘 상태에 `on-hold`를 추가할 것인가(DCR-007, C층 기준선 v2)? | **포함** | 보류 작업이 매 세션 재개 안내에 섞여 노이즈. 변경은 정규식 1토큰+테스트 1개. 단 REQ·DESIGN-llm-workflow 재승인(v2)이 필요해 관문이 하나 늘어남 | **포함** — DCR-007 승인 |
| Q-03 | 수행 기록의 `변경 파일` 필드를 폐지할 것인가? | **폐지** | git이 정본. 재개에 필요한 것은 미커밋 변경뿐이며 인계 절 한 줄로 충분. 대안: 유지하되 1행 상한 | **폐지** |
| Q-04 | 린트 상한값(항목 8행·600자, 불릿 300자, 파일 12KB 경고)을 이 값으로 시작할 것인가? | **이 값으로 시작** | 사이클 1 실측(최장 불릿 680자, 26KB)의 절반 수준. 상수로 두고 두 사이클 후 조정 | **이 값으로 시작** |
| Q-05 | 완료 시 인계 절을 축약(재개 프롬프트 제거)할 것인가? | **축약** | 완료 로그의 재개 프롬프트·미커밋 목록은 무의미. 완료된 항목·후속 작업만 남긴다. 대안: 전체 유지 | **축약** |

## 위험

| ID | 위험 | 영향 | 완화 |
|---|---|---|---|
| RISK-01 | 필드 축소로 결정 근거가 유실 | 재개·감사 시 이유 불명 | `결정과 이유` 필수, 린트 L3이 빈 필드를 오류로 |
| RISK-02 | 상한이 빡빡해 기록을 회피하거나 분할 | 기록 품질 저하 | 오류·경고 2단계, 상한은 상수(Q-04), 두 사이클 후 조정 |
| RISK-03 | Python 부재 환경 | 린트 미실행 | wf-doc §4 수동 검토 대체 + 작업 기록에 미실행 기록(DES-03) |
| RISK-04 | ADR-005·DCR-007 번호가 보관 브랜치와 겹침 | 브랜치 간 혼동 | main 이력 기준 발행을 문서·등록부에 명시(DES-10) |
| RISK-05 | verification·completion 단독 파일을 쓰는 다른 저장소 | 템플릿 부재 | DES-01 포인터("합본의 해당 절을 사용") 유지 |
| RISK-06 | Q-02 포함 시 C층 재승인이 이 작업의 승인과 섞임 | 승인 범위 모호 | 승인 관문에서 DCR-007을 별도 항목으로 묻고 결과를 각 문서에 따로 기록 |

## 추적성

| 요구사항 | 설계 | 작업 | 검증 |
|---|---|---|---|
| FR-01 | DES-01, DES-02 | [TASK-01](./plan.md#task-01-wf-doc-템플릿--합본-템플릿과-수행-기록-필드), [TASK-03](./plan.md#task-03-wf-implement-75) | AC-01, AC-02 |
| FR-02 | DES-05, DES-04 | [TASK-04](./plan.md#task-04-린트-스크립트-lint_worklogpy-tdd), [TASK-06](./plan.md#task-06-자기-적용--작업-기록-합본-전환과-추적-링크) | AC-03, AC-04 |
| FR-03 | DES-01, DES-03 | [TASK-01](./plan.md#task-01-wf-doc-템플릿--합본-템플릿과-수행-기록-필드) | AC-01 |
| FR-04 | DES-02, DES-06, DES-09 | [TASK-03](./plan.md#task-03-wf-implement-75), [TASK-06](./plan.md#task-06-자기-적용--작업-기록-합본-전환과-추적-링크), [TASK-07](./plan.md#task-07-검증자체-리뷰통합) | AC-02, AC-04 |
| FR-05 | DES-03, DES-04 | [TASK-02](./plan.md#task-02-wf-doc-본문과-교정-규칙-참조-문서) | AC-06 |
| FR-06 | DES-05, DES-07 | [TASK-04](./plan.md#task-04-린트-스크립트-lint_worklogpy-tdd) | AC-03 |
| FR-07 | DES-08 | [TASK-05](./plan.md#task-05-dcr-007--훅-닫힘-상태에-on-hold-tdd) | AC-07 |
| FR-08 | DES-09 | [TASK-06](./plan.md#task-06-자기-적용--작업-기록-합본-전환과-추적-링크) | AC-04 |
| FR-09 | DES-10 | [TASK-07](./plan.md#task-07-검증자체-리뷰통합) | AC-08 |
| NFR-01 | DES-09 | [TASK-06](./plan.md#task-06-자기-적용--작업-기록-합본-전환과-추적-링크), [TASK-07](./plan.md#task-07-검증자체-리뷰통합) | AC-05 |
| NFR-02 | DES-01 | [TASK-01](./plan.md#task-01-wf-doc-템플릿--합본-템플릿과-수행-기록-필드) | AC-01 |
| NFR-03 | DES-05 | [TASK-04](./plan.md#task-04-린트-스크립트-lint_worklogpy-tdd) | AC-03 |
| NFR-04 | DES-02, DES-03, DES-04 | [TASK-02](./plan.md#task-02-wf-doc-본문과-교정-규칙-참조-문서), [TASK-03](./plan.md#task-03-wf-implement-75), [TASK-07](./plan.md#task-07-검증자체-리뷰통합) | AC-09 |

작업 열은 [PLAN-20261009-worklog-diet](./plan.md)의 TASK 링크(2026-10-09, TASK-06에서 기입).

## 승인 기록

| 기준선 | 일자 | 결과 | 근거 |
|---|---|---|---|
| v1 | 2026-10-09 | 승인 | 대화형 승인 관문에서 사용자 응답 "권장안 전체 승인" — Q-01~Q-05 전부 권장안, ADR-005·006, DCR-007(Q-02 포함 → C층 기준선 v2), 산출물 위치(작업 폴더 통합 문서) 포함 |

## 인계

- 다음 단계 또는 워크플로우: wf-implement(계획 수립, [wf-implement §1](../../../skills/wf-implement/SKILL.md#1-시작-조건)) — 진행 상태는 [작업 기록](./work-log.md)
- 시작 조건: 충족 — 이 문서 v1 승인(2026-10-09)
- 입력 문서와 기준선: 이 문서 v1, [ADR-005](./ADR-005-작업-기록-수명주기.md)·[ADR-006](./ADR-006-작업-기록-린트-B층.md)(approved), [DCR-007](./DCR-007-훅-닫힘-상태-on-hold.md)(approved, REQ·DESIGN-llm-workflow v2)
- 완료된 항목: §4.1 조사, 요구사항·설계·위험·추적표, ADR 2건·DCR 1건, §4.5 일관성 검토, 기준선 v1 승인
- 미완료 항목: 구현·검증(wf-implement)
- 차단 요인: 없음

## 변경 이력

| 날짜 | 변경 | 근거 | 상태 또는 기준선 | 작성자·승인자 |
|---|---|---|---|---|
| 2026-10-09 | 초안 작성(§4.1 조사, FR-01~09, NFR-01~04, AC-01~09, DES-01~10, Q-01~05, RISK-01~06), ADR-005·006·DCR-007 초안과 함께 §4.5 검토 후 승인 요청 | 사용자 요구 4·5·6(2026-10-09 세션), 사이클 편성 승인 | draft → awaiting-approval | Claude(작성) |
| 2026-10-09 | 기준선 v1 승인, `approved`. Q-01~Q-05 전부 권장안, ADR-005·006 승인, DCR-007 승인(C층 v2) | 대화형 승인 관문 사용자 응답 "권장안 전체 승인" | awaiting-approval → approved, v1 | 사용자(승인) |

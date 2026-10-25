# REQ-DESIGN-approval-gate: 승인 게이트와 경량 경로 기계 조건 — 요구사항·설계

> 문서 유형: `requirements, design`
> 작업 ID: `20261026-approval-gate`
> 상태: `approved`
> 기준선: `v1` (승인일 2026-10-26)
> 작성일: 2026-10-26
> 최종 갱신: 2026-10-26
> 관련 문서: [WORK-20261026-approval-gate: 작업 기록](./work-log.md), [ADR-018: 승인 게이트의 판정 원천과 방식](./ADR-018-승인-게이트-판정.md), [DCR-019: C층 승인 게이트 훅 추가](./DCR-019-C층-승인-게이트-훅-추가.md), [설계 액션 아이템](../../research/20261025-aidlc-trends/05_design_action_items.md), [ADR-014](../20261025-regression-guard/ADR-014-회귀-보호-훅-강제-방식.md), [REQ-llm-workflow](../../requirements.md), [DESIGN-llm-workflow](../../design.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: v2 설계 사이클 B — wf-design §8 "승인 이외의 응답에서는 구현을 시작하지 않는다"를 편집 시점 훅으로 강제하고(D-05, S28), 그 통과 조건인 경량 경로에 기계 조건을 둔다(D-06, S6). 승인 요청 분량을 줄이고(D-07, S26), ADR 작성 시 직전 ADR을 참조하게 한다(D-08, S25).
- 현재 결론 또는 상태: v1 승인(2026-10-26). Q-01 (B) `docs/` 밖 + 선언 파일, Q-02 (A) 상태 + 응답 인용, Q-03 상한 5.
- 다음 행동: wf-implement 계획 수립. 상세는 [인계](#인계).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | related | [설계 액션 아이템](../../research/20261025-aidlc-trends/05_design_action_items.md) | 사이클 B D-05~D-08, Q-D3~Q-D6·Q-D9 | 입력(조사 트랙, 승인 대상 아님). Q-D7 (B) 사용자 채택 2026-10-26 |
| input | change | [REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md) | FR-05, NFR-01, DES-04, 계약·흐름·검증·위험 | v4 → v5 — [DCR-019](./DCR-019-C층-승인-게이트-훅-추가.md) |
| input | related | [ADR-014](../20261025-regression-guard/ADR-014-회귀-보호-훅-강제-방식.md) | 결정 1·3·5 | `ask` 우선, 가드만 fail-to-ask, 3층 구조를 재사용 |
| output | decision | [ADR-018](./ADR-018-승인-게이트-판정.md) | document | 판정 원천(작업 기록 `기준선` 링크), Python 판정 + PS 어댑터, `deny` 보류 |
| output | change | [DCR-019](./DCR-019-C층-승인-게이트-훅-추가.md) | document | C층 기준선 v5 |
| output | implementation | [WORK-20261026-approval-gate](./work-log.md) | document | 승인 후 plan.md |

## 문제와 목적

사용자 요청(2026-10-26): 05 액션 아이템 확인, 사이클 B를 먼저 이 세션에서 착수(Q-D7 (B)). wf-design의 승인 관문은 규칙만 있고 강제가 없다 — 승인 전에 제품 코드를 바꿔도 아무것도 막지 않는다. 근거(05 D-05): 프롬프트 속 계획 준수 약 22~45%, 제어 흐름 강제로 개선(2609.38108 `[노트]`), AI-DLC v2의 결정론적 관문 `[노트]`. 판단형 조건은 우회된다(Rationalization Loophole 94%, 2607.01456 `[노트]`)는 점이 경량 경로 기계 조건의 이유다.

## 현재 상태 조사 (wf-design §4.1)

### 사실

- **훅(C층 v4):** PreToolUse `wf-test-guard.ps1`(DES-06)은 `permission_mode`를 읽지 않고 항상 `ask`만 낸다(`deny` 경로 없음). `Write-WfPermission`(wf-common.ps1:170)은 `deny`도 받는다. `cwd`가 저장소 루트, 대상은 `tool_input.file_path`/`notebook_path`, 내부 예외는 `ask`(fail-to-ask), 바깥 catch는 무출력. Stop `wf-stop-gate.ps1`(DES-07)은 `$env:CLAUDE_WF_GUARD_SCRIPT` 또는 `$PSScriptRoot` 기준 `regression_guard.py`를 `python`으로 10초 제한 호출한다. 등록은 `install-hooks.ps1`의 `$desired`(:47-61), 우리 항목은 `\setup\hooks\wf-[a-z-]+\.ps1$`로 식별·멱등.
- **열린 작업 판정:** PS `Get-WfOpenWorkLogs`(머리말 12행 내 닫힘 계열), Python `lint_worklog.worklog_state`·`CLOSED`(5종, `on-hold` 포함). `head_fields`·`section`·`fields_in` 헬퍼가 있다.
- **기준선 표기:** 작업 기록 머리말 `기준선:`에 기준선 문서 링크가 있다(예: `[REQ-DESIGN-test-quality](./req-design.md) v1`, 승인 전 `— 미승인`). 경량 경로 문서는 `기준선: N/A — 경량 경로로 기준선 없음`(wf-doc §2.8:199) — 현재 이를 쓰는 작업 폴더는 없다.
- **승인 기록 형식 2종:** 불릿 `- 날짜 — 사용자가 대화형 승인 관문에서 … **승인**. 응답: "…"`(최근 작업), 표 `| v1 | 날짜 | 승인 | 대화형 승인 관문에서 사용자 응답 "승인" … |`(이전 작업). 둘 다 `응답` + 따옴표 인용을 담는다.
- **제품 코드 정의:** 저장소에 경로 상수가 없다. 산문(wf-design :37·57·63·66)뿐. 게이트 설정 선언은 `Get-WfGateSettingsPaths`(ADR-014 ② 층)뿐.
- **wf-design 본문:** 2,288/2,300어절. §1 경량 경로 절 68~84행(106어절), §8 첫 두 문단 280·282행(73어절). `#적용-제외--경량-경로` 링크 5곳(README, 01_REQUIREMENTS_AND_DESIGN, wf-doc §2.8, wf-implement §1, closing.md), `#8-사용자-승인-관문` 링크 10여 곳.
- **템플릿:** ADR 절 templates.md 321~359행. 경량 경로 템플릿 절은 없고 :94가 wf-doc §2.8을 가리킨다.
- **테스트:** TST-01 `run-tests.ps1` T01~T46(47건), `Invoke-Guard`가 `permission_mode='default'` 고정. TST-02 `skills/wf-doc/scripts/tests/`(68건, `test_regression_guard.py` 20건).
- **관찰 공백:** `auto` 모드에서 `ask`가 사용자에게 닿음은 관찰됨, `bypassPermissions`는 미관찰(regression-guard 작업 기록, C층 RISK-06).
- 열린 작업 없음, 모든 req-design `approved`. 다음 전역 번호 018(등록부 마지막 ADR-017).

### 해석

- **판정 원천은 작업 기록의 `기준선` 링크가 가장 일반적이다.** req-design 작업, DCR 작업(`context-signal-v2`처럼 req-design이 없음), 경량 표지를 같은 필드 하나로 읽는다. 링크된 문서의 머리말 `상태`와 `## 승인 기록`의 응답 인용을 함께 보면 "조용한 자기 승인"을 "기록된 승인"으로 바꿀 수 있다(Q-02).
- **판정은 Python B층이 맞다.** Markdown 링크·절 파싱은 `lint_worklog` 헬퍼로 이미 있고, 다른 하네스도 같은 스크립트를 부를 수 있다(ADR-014 결정 5). PS 재구현은 RISK-07 같은 판독 불일치를 하나 더 만든다. 대신 매 편집 지연이 생기므로 `docs/` 경로·`docs/work/` 부재는 PS에서 먼저 걸러 Python을 부르지 않는다.
- **`deny`는 이번에 넣지 않는다.** ADR-014 결정 1은 "`ask`가 사람에게 닿지 않음이 확인된 모드에서만 `deny`"이고, 확인된 모드가 아직 없다. `bypassPermissions` 관찰은 사용자가 그 모드로 세션을 열어야 해서 에이전트가 수행할 수 없다 — 검증 항목으로 남긴다.
- **경량 표지는 우회 통로가 될 수 있다.** 표지만 읽으면 정식 작업에 표지를 쓰는 것으로 게이트를 피한다. 표지를 쓴 작업에는 기계 조건(파일 수, 민감 파일, 새 파일)을 판정에 걸어야 한다. 기록 없는 경량 작업은 열린 작업이 아니므로 게이트와 무관하다.
- **이관으로 본문 여유가 생긴다.** §1 경량 경로 106어절·§8 두 문단 73어절을 references로 보내고 요약·링크만 남기면 약 100어절 이상이 줄어 사이클 A의 자리가 생긴다. 제목(앵커)은 유지해 외부 링크를 깨지 않는다.

### 가정

- Windows에서 `python` 기동 비용은 수십~백수십 ms로, `powershell.exe` 기동(수백 ms)에 비해 작다 — TASK에서 실측한다(NFR-02).
- 승인 게이트는 전역 훅(`~/.claude/settings.json`)이라 이 구조(`docs/work/`)를 쓰는 다른 저장소에도 적용된다 — 의도한 동작이다.

## 범위

### 포함

- 저장소별 제품 코드 선언 `.wf-gate.json`(루트, 선택 — Q-01 (B))의 판독, `skills/wf-doc/scripts/approval_gate.py`(신설, B층 판정)와 테스트 `skills/wf-doc/scripts/tests/test_approval_gate.py`(TST-02에 합류)
- `setup/hooks/wf-approval-gate.ps1`(신설), `wf-common.ps1`(필요한 경우 헬퍼), `messages/approval-gate.md`(신설), `install-hooks.ps1` 등록, `tests/run-tests.ps1` T47~(TST-01 확장)
- `skills/wf-design/SKILL.md` §1 경량 경로 절과 §8 첫 두 문단 축약, `references/lightweight-path.md`·`references/approval-request.md`(신설)
- `skills/wf-doc/references/templates.md` ADR 절 1문장(D-08), 승인 기록 절 응답 인용 1문장, wf-doc §2.8 경량 표지가 판정에 쓰인다는 링크(어절 순증 0)
- C층 `docs/requirements.md`·`docs/design.md` v5(DCR-019), README 훅 목록, 이 작업 문서·ADR-018·DCR-019·등록부·status 행·05 문서 머리말 상태 줄
- 설치(`setup_claude.ps1` 재실행)와 이 저장소에서의 실세션 확인

### 제외

- `deny` 경로(확인된 미도달 모드가 없음 — 관찰 후 별도 DCR), 셸 편집을 잡는 종료 시 그물(Q-D6 (a) — 2주 운용 후 판단)
- 이 저장소의 `.wf-gate.json` 작성(기본값으로 충분 — 필요 시 별도)
- AI-DLC 프로필 대조 예시(D-06 부가 항목), 사이클 A·C 항목
- 공개 인터페이스·스키마·보안 영향의 기계 판정(경로 목록으로 일반화할 수 없음 — 판단형 조건으로 남김)

## 기능 요구사항

| ID | 이름 | 내용 |
|---|---|---|
| FR-01 | 승인 전 제품 코드 편집 확인 | 파일 편집 도구가 제품 코드를 바꾸려 할 때(제품 코드: 기본은 루트 아래 `docs/` 밖 전부, 루트의 선택 선언 `.wf-gate.json`이 `exclude` glob로 제외하고 `product` glob로 `docs/` 안을 추가 — `exclude` 우선, Q-01 (B)), 열린 작업 기록 중 기준선이 승인되지 않은 것이 있으면 실행 전에 사용자 확인을 요청해야 한다. 이유에는 작업 ID·기준선 문서·상태와 wf-design §8 포인터가 있어야 한다 |
| FR-02 | 승인 판정 | 기준선은 작업 기록 머리말 `기준선:`의 링크 문서가 모두 상태 `approved`·`completed`이고 그 `## 승인 기록`에 사용자 응답 인용(`응답` + 따옴표)이 있을 때만 승인된 것으로 본다(Q-02). 링크가 없으면 미승인이다 |
| FR-03 | 통과 | 제품 코드가 아닌 경로, `docs/work/` 없는 저장소, 열린 작업 없음, 모든 열린 작업의 기준선 승인 — 각각 무출력으로 통과해야 한다. 닫힘 계열(`on-hold` 포함)은 열린 작업이 아니다 |
| FR-04 | 경량 경로 기계 조건 | 열린 작업이 경량 표지(`기준선: N/A — 경량 경로`)면 다음을 모두 만족할 때만 통과한다: (a) 제품 코드 변경 파일(미추적 포함)과 대상의 합집합이 5개 이하(Q-03), (b) 대상이 게이트 설정 파일·의존성 선언 파일·`.wf-gate.json`이 아님, (c) 대상이 새 파일이면 테스트 파일. 어기면 위반 조건을 이유로 확인을 요청한다 |
| FR-05 | 실패 정책 | 판정이 오류·타임아웃·Python 부재면 확인을 요청한다(가드 fail-to-ask, ADR-014 결정 3). 훅 입력 파싱 실패 등 바깥 예외는 무출력 |
| FR-06 | 경량 경로 규칙 | wf-design 경량 경로에 판단형 3조건과 FR-04 기계 조건을 함께 둔다. 기계 조건은 상한이지 허가가 아니다(통과해도 판단형 조건 적용). 규칙 본체는 references |
| FR-07 | 승인 요청 분량 | 대화형 승인 요청은 한 화면 요약(사용자가 고를 결정, 주요 위험, 남은 질문)과 산출물 링크로 구성하고 30줄 이내를 목표로 한다. 현행 필수 항목은 "요약 또는 링크"로 충족한다. 경량 경로는 승인 요청이 없다 |
| FR-08 | 승인 기록의 응답 인용 | 승인을 기록할 때 사용자 응답을 따옴표로 인용한다(FR-02의 판정 대상) |
| FR-09 | ADR 직전 참조 | ADR을 쓰기 전에 등록부의 최근 ADR 3~5개(같은 주제가 있으면 우선)를 읽고 절 구성·분량·어휘를 맞춘다 |

## 비기능 요구사항

| ID | 이름 | 내용 |
|---|---|---|
| NFR-01 | 분량 | wf-design 본문 순감(목표 ≤ 2,200어절), wf-doc ≤ 2,350, wf-implement 무변경(K3) |
| NFR-02 | 지연 | 제품 경로 편집 1회의 훅 추가 지연 중앙값 ≤ 300ms(Python 판정 포함, 10회 측정). `.wf-gate.json`이 없는 저장소의 `docs/` 경로는 Python을 부르지 않는다 |
| NFR-03 | 하네스 중립 | 판정은 B층 Python(표준 라이브러리 + git)만, 스킬 본문은 의무만. 훅은 어댑터 |
| NFR-04 | 앵커 불변 | `#적용-제외--경량-경로`, `#8-사용자-승인-관문`, `#승인-기록` 앵커 유지 |
| NFR-05 | 린트·테스트 | `lint_skill.py`·`lint_worklog.py` 0 오류, `유지` 4행 통과(TST-01·02 확장분 같은 SHA 2회) |
| NFR-06 | 완료 기록 불변 | 완료 작업의 승인 기록은 소급 수정하지 않는다(기존 2형식 모두 FR-02를 만족 — 확인 대상) |

## 인수 조건

| ID | 조건 |
|---|---|
| AC-01 | 판정 스크립트: 미승인 기준선 + 제품 경로 → exit 1(작업 ID·문서·상태), 승인 + 응답 인용 → 0, 상태 `approved`인데 응답 인용 없음 → 1, 링크 없음 → 1, `docs/` 경로 → 0, `docs/work/` 없음 → 0, 열린 작업 없음·`on-hold`만 → 0, 판독 불가 → 2. 선언: `exclude` 일치 → 0, `product`로 지정한 `docs/` 안 경로 → 1, 선언 JSON 손상 → 2(FR-01~03·05) |
| AC-02 | 경량 표지 작업: 변경 5개 이하·일반 파일 → 0, 6개째 → 1, 게이트 설정·의존성 선언·`.wf-gate.json` → 1, 테스트 아닌 새 파일 → 1, 테스트 새 파일 → 0(FR-04) |
| AC-03 | 이 저장소의 완료 작업 기준선(불릿·표 두 형식)이 FR-02로 승인 판정된다(NFR-06) |
| AC-04 | 훅: exit 1 → `ask`와 이유, exit 0 → 무출력, exit 2·Python 부재 → `ask`(gate=error), 선언 없는 저장소의 `docs/` 경로·`docs/work/` 없음 → Python 미호출 무출력, 선언이 있으면 `docs/` 경로도 판정 호출, 입력 파싱 실패 → 무출력(TST-01 T47~) |
| AC-05 | `install-hooks.ps1`가 PreToolUse에 승인 게이트를 멱등 등록하고 기존 항목을 보존한다(T 확장) |
| AC-06 | NFR-02 지연 측정 기록. 설치 후 이 작업(승인됨)의 제품 파일 편집에 확인이 뜨지 않음을 실세션에서 관찰. 미승인 시 확인은 AC-04(실제 판정 1건 포함)로 검증하고, 실세션 관찰은 다음 정식 작업 착수 시 후속으로 기록. `bypassPermissions` 도달 여부는 사용자 관찰 시 기록(미수행 허용) |
| AC-07 | wf-design §1·§8이 요약·링크로 줄고 두 references에 FR-06·07·08이 있으며, 앵커 유지, 본문 ≤ 2,200어절(FR-06~08, NFR-01·04) |
| AC-08 | templates.md ADR 절에 FR-09 문장, 승인 기록 절에 FR-08 문장이 있다 |
| AC-09 | C층 v5(DCR-019 반영), ADR-018·DCR-019 `approved`, 등록부 행, 린트 2종 0 오류, `유지` 4행 통과, closing.md 순서로 종결 |

## 설계

| ID | 이름 | 내용 |
|---|---|---|
| DES-01 | B층 판정 `approval_gate.py` | `python approval_gate.py <저장소 루트> <대상 경로>` → exit 0 통과(무출력), 1 확인 필요(`<작업 ID>: <사유>` 행), 2 내부 오류. 순서: 대상이 루트 밖 → 0 / 제품 코드 판정(DES-09) 아님 → 0 / `docs/work/` 없음 → 0 / 열린 작업 기록(`lint_worklog.worklog_state`, `CLOSED` 제외) 각각: 머리말 `기준선` 값이 `N/A — 경량 경로`로 시작하면 DES-02, 아니면 값 안의 Markdown 링크(작업 폴더 기준 상대 경로)를 모두 따라가 머리말 `상태` ∈ {`approved`, `completed`}이고 `## 승인 기록` 절에 `응답`과 따옴표 인용(`"…"` 또는 `“…”`)이 있는 행이 있는지 본다. 링크 0개·문서 없음·조건 미달 → 사유 기록 / 사유가 하나라도 있으면 1. 표준 라이브러리 + git, `lint_worklog` 헬퍼 재사용 |
| DES-02 | 경량 기계 조건 | (a) `git status --porcelain --untracked-files=all`의 경로 중 제품 코드 ∪ {대상} 개수 ≤ 5. (b) 대상이 `.wf-gate.json`, 게이트 설정(`.claude/settings*.json`) 또는 의존성 선언(`requirements*.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `package.json`, `package-lock.json`, `go.mod`, `Cargo.toml`, `*.csproj`, `pom.xml`, `build.gradle*`)이 아님. (c) 대상이 없는 파일이면 경로에 `test`/`tests` 디렉터리가 있거나 파일명이 `test_*`·`*_test.*`·`*.test.*`·`*Tests.*`. git이 없으면 (a)는 대상 1개로 센다. 위반 사유: `경량 경로 기계 조건 위반 (a|b|c)` |
| DES-03 | 어댑터 `wf-approval-gate.ps1` | PreToolUse(matcher `Edit\|Write\|MultiEdit\|NotebookEdit`), DES-06과 같은 입력 처리. `<cwd>/docs/work/` 없음, 또는 `<cwd>/.wf-gate.json`이 없고 대상이 `<cwd>/docs/` 아래면 Python을 부르지 않고 무출력. 그 외 `$env:CLAUDE_WF_GATE_SCRIPT` 또는 `$PSScriptRoot\..\..\skills\wf-doc\scripts\approval_gate.py`를 `python <judge> <cwd> <대상>`로 5초 제한 호출 → exit 1: `ask`(메시지 + 판정 출력), 2·타임아웃·Python 부재: `ask`(메시지 + `gate=error (...)`), 0: 무출력. `deny` 없음(ADR-018). 바깥 catch 무출력 |
| DES-04 | 메시지·설치 | `messages/approval-gate.md` 1행: `[llm_workflow 승인 게이트] 기준선이 승인되지 않은 작업이 열려 있다. wf-design §8 — 승인 이외의 응답에서는 구현을 시작하지 않는다. 대상:`. `install-hooks.ps1` `$desired`에 PreToolUse 항목 추가(같은 matcher의 두 번째 항목) |
| DES-05 | 경량 경로 references | 새 `skills/wf-design/references/lightweight-path.md`: 1. 판단형 3조건·예(이관) 2. 기계 조건(DES-02 문장판) — 상한이지 허가 아님 3. 생략하지 않는 것(이관) 4. 기록을 남기면 경량 표지, 승인 게이트가 표지와 기계 조건을 읽음 5. 의심·도중 이탈 시 정식 경로(이관). 본문 §1 절은 제목 유지 + 2문장(요건 요약, 의심 시 정식 경로) + 링크 |
| DES-06 | 승인 요청 references | 새 `skills/wf-design/references/approval-request.md`: 1. 한 화면 요약 구성(결정·위험·남은 질문·산출물 링크)과 30줄 목표 2. 현행 필수 항목은 요약 또는 링크로 충족 3. 규모별 — 경량 경로 없음, 합본 req-design은 결정 표 중심 4. 파일 보존 시 `approval` 유형(이관) 5. 승인 기록에 사용자 응답 인용(FR-08), 승인 게이트가 이를 읽음. 본문 §8 첫 두 문단 → 1문장(구성·분량은 references, 승인 여부를 명시적으로 물음). §8 승인 기록 1항에 "사용자 응답을 인용해" |
| DES-07 | 템플릿 | templates.md ADR 절 끝 규칙 문장 앞에 FR-09 1문장, 승인 기록 절에 FR-08 1문장. wf-doc §2.8 경량 표지 문장에 "승인 게이트가 읽는다" 링크는 어절 순증 0일 때만 |
| DES-09 | 제품 코드 선언 `.wf-gate.json` | 루트의 선택 파일 `{"product": [glob…], "exclude": [glob…]}`(루트 기준 상대 경로, `fnmatch`, `/` 구분). 판정: `exclude` 일치 → 제품 아님 / `product` 일치 → 제품 / 그 외 `docs/` 밖이면 제품. 파일 없음 → 기본값. JSON 손상·형식 오류 → exit 2(fail-to-ask). 위치를 `docs/` 밖에 둔 이유: 게이트 대상이라 승인 없이 예외를 늘릴 수 없게 한다. 경량 조건 (b)의 민감 파일에 포함 |
| DES-08 | C층 v5 | DCR-019: FR-08(승인 게이트), FR-05 v5 무동작 조건, NFR-01 예외 확장, AC-10~12, DES-08(`wf-approval-gate.ps1`), DES-04 6개 항목, B층 계약 행, 실패 흐름, 검증 전략, RISK-08~10 |

### 검증 전략

- AC-01~03: `test_approval_gate.py`(tmp 저장소 + git init, TDD Red 먼저), AC-03은 이 저장소 실제 작업 폴더 대상 1건.
- AC-04·05: `run-tests.ps1` T47~ — `CLAUDE_WF_GATE_SCRIPT`로 exit 0/1/2를 내는 스텁 판정, 실제 판정 1건, Python 부재(존재하지 않는 경로).
- AC-06: 훅 호출 10회 중앙값 측정, 설치 후 실세션 통과 관찰. 세션 `cwd`가 이 저장소로 고정되고 이 작업은 승인 상태이므로 미승인 확인의 실세션 관찰은 다음 작업의 설계 단계로 넘긴다.
- AC-07·08: `lint_skill.py`(K3·K4·K5), grep.
- AC-09: 린트, `유지` 전량, `git diff --name-only`.

## 가정과 미해결 질문

| ID | 질문 | 권장 | 이유 |
|---|---|---|---|
| Q-01 | 제품 코드 정의 — (A) `docs/` 밖 전부 (B) (A) + 저장소별 glob 선언 덮어쓰기 | 권장 (A) → **(B)** 사용자 채택 — DES-09(`.wf-gate.json`, `docs/` 밖) | 05는 (A)+(B)를 권했으나 덮어쓸 대상이 아직 없다(결정 사다리 1단계). 생성 문서 폴더 같은 예외가 생기면 그때 선언을 추가 |
| Q-02 | 승인 판정에 응답 인용 요구(Q-D6 (b)) — (A) 상태 + 응답 인용 (B) 상태만 | **(A)** — 사용자 채택 | 에이전트가 `approved`를 직접 적는 것이 이 게이트의 가장 큰 구멍. 완전히 막지 못하고 "기록된 승인"으로 바꾼다. 완료 작업 두 형식 모두 이미 만족(AC-03) |
| Q-03 | 경량 기계 조건 (a)의 파일 수 상한 — (A) 2 (B) 3 (C) 5 | 권장 (A) → **(C) 5** 사용자 채택 | 05의 출발값(9월 편집안 "≤2"). 근거 수치가 없어 코드 저장소 실측으로 조정(05 D-06) |
| 결정됨 | 확인/차단 방식(Q-D3) | `ask`만, `deny` 보류 | ADR-014 결정 1 — 미도달이 확인된 모드가 없다. `bypassPermissions` 관찰은 사용자 수행 |
| 결정됨 | 셸 편집 종료 시 그물(Q-D6 (a)) | 넣지 않음 | 05 권장, 관찰된 경로 없음 |

## 위험

| ID | 위험 | 영향 | 완화 |
|---|---|---|---|
| RISK-01 | 자기 승인 — 에이전트가 상태와 응답 인용을 직접 쓴다 | 게이트 무력화 | 완전 차단 불가. 기록이 남아 사후 감사 가능, 승인 기록은 사람이 보는 승인 요청 직후에만 쓰는 규칙(DES-06) |
| RISK-02 | 기록 없이 정식 경로 대상 작업을 함 | 게이트 미발화 | 훅으로 막을 수 없음 — wf-design §1 규칙에 의존(05 Q-D5 남는 구멍) |
| RISK-03 | 매 편집 지연 | 체감 지연 | `docs/` 경로 선필터, NFR-02 측정. 초과 시 PS 판정 대안(ADR-018 대안 B)으로 DCR |
| RISK-04 | 열린 작업이 둘 이상이면 승인된 작업의 편집도 확인 | 확인 소음 | 보수적 기본값으로 감수, 이유에 미승인 작업 ID를 표시 |
| RISK-05 | 권한 자동 승인 모드에서 `ask` 미도달 | 게이트 무력화 | 사용자 관찰 후 그 모드만 `deny`(별도 DCR). C층 RISK-06과 같은 항목 |
| RISK-06 | 전역 훅이라 다른 저장소의 `docs/work/` 관례가 다르면 오판 | 확인 소음 | 링크 없는 `기준선`은 미승인으로 보아 확인(보수적), 메시지에 포인터 |
| RISK-08 | 선언 파일로 제품 범위를 줄여 게이트 회피 | 게이트 무력화 | 선언을 `docs/` 밖에 둬 그 편집 자체가 게이트 대상, 경량 조건 (b) 민감 파일 |
| RISK-07 | 이관으로 본문 규칙이 references로 숨어 읽히지 않음 | 경량 경로 오남용 | 본문에 요건 요약과 "의심 시 정식 경로" 유지, 게이트가 기계 조건을 강제 |

## 추적성

| 요구사항 | 설계 | 인수 조건 | 계획 |
|---|---|---|---|
| FR-01~03·05 | DES-01, DES-03, DES-04, DES-09 | AC-01, AC-03, AC-04 | 승인 후 plan.md |
| FR-04 | DES-02 | AC-02 | 승인 후 plan.md |
| FR-06 | DES-05 | AC-07 | 승인 후 plan.md |
| FR-07·08 | DES-06, DES-07 | AC-07, AC-08 | 승인 후 plan.md |
| FR-09 | DES-07 | AC-08 | 승인 후 plan.md |
| NFR-01~06 | DES-01~08 | AC-05~09 | 승인 후 plan.md |

## 승인 기록

- 2026-10-26 — 사용자가 대화형 승인 관문에서 이 문서를 기준선 v1로 **승인**. 응답: Q-01 "docs/ 밖 + glob 선언", Q-02 "상태 + 응답 인용", Q-03 "5개", "승인". Q-01 (B)는 DES-09로 반영(선언 파일을 `docs/` 밖에 두는 위치는 우회 방지를 위한 설계 결정), Q-03은 FR-04·DES-02·AC-02에 5로 반영. [ADR-018](./ADR-018-승인-게이트-판정.md)·[DCR-019](./DCR-019-C층-승인-게이트-훅-추가.md) 동시 승인.

## 인계

- 다음 단계 또는 워크플로우: wf-implement 계획 수립
- 시작 조건: 충족 — v1·ADR-018·DCR-019 승인(2026-10-26)
- 입력 문서와 기준선: 위 문서 연결
- 완료된 항목: §4.1 조사, 요구사항·설계·위험·추적표, ADR-018·DCR-019 초안, §4.5 일관성 검토
- 미완료 항목: 계획, 구현·검증
- 차단 요인: 없음
- 다음 행동: wf-implement 계획 수립

## 변경 이력

| 날짜 | 변경 내용 | 근거 | 상태 전이 | 작성·승인 |
|---|---|---|---|---|
| 2026-10-26 | 최초 작성 — 조사, FR-01~09, NFR-01~06, AC-01~09, DES-01~08, Q-01~03, RISK-01~07, ADR-018·DCR-019 초안 | 사용자 선택(05 확인, 사이클 B 먼저, 이 세션) | draft → awaiting-approval | Claude(작성) |
| 2026-10-26 | 승인 — Q-01 (B)·Q-02 (A)·Q-03 5 채택, DES-09·RISK-08 추가, FR-01·03·04·NFR-02·AC-01·02·04·DES-01~03 반영, 승인 기록 | 사용자 승인 관문 응답 | awaiting-approval → approved, v1 | 사용자(승인) |

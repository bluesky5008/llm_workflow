# REQ-DESIGN-hook-friction: 회귀 보호 훅·규정의 사용자 판정 강요 완화 — 요구사항·설계

> 문서 유형: `requirements, design`
> 작업 ID: `20261122-hook-friction`
> 상태: `approved`
> 기준선: `v1` (승인일 2026-11-22)
> 작성일: 2026-11-22
> 최종 갱신: 2026-11-22
> 관련 문서: [WORK-20261122-hook-friction: 작업 기록](./work-log.md), [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md), [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md), [DESIGN-llm-workflow](../../design.md), [REQ-llm-workflow](../../requirements.md), [ADR-014](../20261025-regression-guard/ADR-014-회귀-보호-훅-강제-방식.md), [REQ-DESIGN-regression-guard](../20261025-regression-guard/req-design.md), [검증 시점·실행 집합·대장 전이](../../../skills/wf-implement/references/verification-depth.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 회귀 보호의 두 훅(PreToolUse 가드 DES-06, Stop 게이트 DES-07)과 이를 둘러싼 스킬 규정이 순수 테스트 추가처럼 위험하지 않은 변경에도 사용자 판정을 강요하는 문제를 줄인다. 저장소 밖에서 만든 선행 변경 `46600de`(기록·대장 SHA 미갱신)를 이 작업에 편입한다.
- 현재 결론 또는 상태: 승인(2026-11-22) — 기준선 v1. 질문 Q-01~05 답(전부 권장안), 요구사항 FR-01~08·NFR-01~05, AC-01~08, DES-01~09, RISK-01~11, 추적표, [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md)·[DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md), §4.5, 적대 검토 2라운드(1라운드 17건 수용·16 해소·1 일부 남음 → 수정, 2라운드 신규 6건 작성자 수정·재확인 없음).
- 다음 행동: [인계](#인계).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | related | [DESIGN-llm-workflow](../../design.md) | DES-02·04·06·07·09, 계약, 흐름, 위험 | 변경 대상(C층 v5) — [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md) |
| input | related | [REQ-llm-workflow](../../requirements.md) | FR-06·07, NFR-01, AC-07·08 | 변경 대상 — DCR-026 |
| input | related | [ADR-014](../20261025-regression-guard/ADR-014-회귀-보호-훅-강제-방식.md) | 결정 1·3 | 정밀화(대체 아님) — ADR-025 |
| input | related | [ADR-012](../20261018-context-signal-v2/ADR-012-컨텍스트-신호-usage-파싱.md) | 임계 기본값·usage 판독 | 선행 변경의 사후 기록 — DCR-026 |
| input | related | [REQ-DESIGN-regression-guard](../20261025-regression-guard/req-design.md) | DES-04(판정 스크립트), DES-08(대장 판독 규칙) | `regression_guard.py`의 정본 — 판정 추가, 판독 규칙 무변경 |
| input | related | [검증 시점·실행 집합·대장 전이](../../../skills/wf-implement/references/verification-depth.md) | §3, §6 | 사용자 판정 규정 — 변경 대상 |
| input | related | [wf-implement](../../../skills/wf-implement/SKILL.md) | 주의 ④, §3.3 | 진행 중 기존 테스트 수정 금지 — 변경 대상 |
| output | decision | [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md) | document | 판정 단위·반복 억제·판정 범위 |
| output | change | [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md) | document | C층 v5 → v6 |
| output | implementation | [WORK-20261122-hook-friction](./work-log.md) | document | 승인 후 plan.md |

## 문제와 목적

사용자 보고(2026-11-22): 워크플로우를 쓰는 중 원하지 않는 상황에서 사용자 선택을 강요받는 일이 늘고 있다. 빈도는 C(편집 시 회귀 보호)·D(종료 시 회귀 보호)가 가장 많고 B(승인 게이트)는 적다. 그리고 그 선택은 훅 확인창보다 **Claude의 일반 질문**으로 더 많이 온다.

목적은 사람이 실제로 판단해야 하는 경우(기존 단언의 삭제·약화, 기대값 변경, 테스트 비활성화·삭제)에만 사용자 판정을 받고, 나머지는 기록으로 처리하는 것이다. 회귀 보호의 목적(테스트를 고쳐 통과시키는 것을 막는다)은 유지한다.

## 현재 상태 조사

### 확인된 사실

- 착수 HEAD `46600de`(= `origin/main`), 워킹트리 clean. 열린 작업 없음(보류 1건 `20260814-multiuser-workflow`). 다음 ADR·DCR 번호 025. C층 기준선 v5([design.md](../../design.md)).
- **보호 단위가 파일·폴더다.** 대장 `테스트 파일` 열은 TST-01 = `setup/hooks/tests/run-tests.ps1`(파일 하나에 훅 테스트 59건), TST-02 = `skills/wf-doc/scripts/tests/*.py`(폴더 전체). 같은 파일·폴더에 테스트를 **추가만** 해도 보호 대상 변경이 된다.
- **가드(DES-06)** [wf-test-guard.ps1:27-39](../../../setup/hooks/wf-test-guard.ps1): 대상 경로가 `유지` 행 glob에 맞으면 무조건 `ask`. 편집 내용(추가인지 수정인지)과 대상 파일의 존재 여부(새 파일 생성)를 보지 않는다. PowerShell `-like`의 `*`는 `/`도 맞추므로 하위 폴더까지 보호된다. 편집 호출마다 처음부터 판정하고 상태를 남기지 않는다.
- **종료 게이트(DES-07)** [regression_guard.py:93-126](../../../skills/wf-doc/scripts/regression_guard.py): 행의 마지막 성공 SHA 이후(커밋 + 워킹트리)의 `git diff --name-only`로 파일 단위 판정 — 추가만 한 변경도 위반. 위반은 **열린** 작업 기록의 `### 테스트 대장 변경`에 행 ID가 있을 때만 해소된다(`recorded_ids`, 129-142). 매 Stop마다 다시 판정하며 `stop_hook_active`로 연속 차단만 막는다.
- **착수 시점에 실제 차단 중이었다:** `python skills/wf-doc/scripts/regression_guard.py .` → exit 1, `TST-01: 테스트 파일 변경 setup/hooks/tests/run-tests.ps1`, `TST-02: … test_approval_gate.py`, `TST-02: … test_regression_guard.py`. 원인은 `46600de`(대장 SHA `ac32578` 이후 보호 파일 3개 변경, 열린 작업 기록 없음). 이 작업 기록의 `### 테스트 대장 변경`에 TST-01·02를 적은 뒤 exit 0.
- `46600de`의 보호 파일 변경 3건은 모두 **순수 추가**다(`git diff --stat`: run-tests.ps1 +41, test_approval_gate.py +40, test_regression_guard.py +9, 삭제 줄 0). 착수 시 Python 3.12에서 훅 테스트 59/59, `skills/wf-doc/scripts/tests`·`skills/wf-tree/scripts/tests` 통과(2026-11-22 세션 기록).
- `46600de`는 테스트 외에도 C층 동작을 바꿨다 — 컨텍스트 임계값 기본값 130000/20000 → 400000/100000(코드 주석 「2026-11-11 user decision」, [ADR-012](../20261018-context-signal-v2/ADR-012-컨텍스트-신호-usage-파싱.md)·design.md 설정값은 130k/20k), usage 2단 중첩(`iterations[{cache_creation{}}]`) 판독, 대장 칸 `\|` 처리, 승인 게이트의 상태(첫 백틱 값)·응답 인용(「」, "사용자" 줄) 판독 완화. 설계 문서·ADR·[approval-request §4](../../../skills/wf-design/references/approval-request.md#4-승인-기록의-응답-인용)에는 반영되지 않았다.
- **사용자 판정을 요구하는 규정:**
  - [wf-implement 주의 ④](../../../skills/wf-implement/SKILL.md#주의--자주-틀리는-것) "대장 `유지` 행의 테스트를 수정·제외해 통과시키지 않는다".
  - [wf-implement §3.3](../../../skills/wf-implement/SKILL.md#33-구현) "진행 중에는 등록·격리 외의 전이와 기존 테스트의 수정·제외·삭제를 하지 않는다" — 순수 추가가 "수정"인지 정하지 않는다.
  - [verification-depth §6](../../../skills/wf-implement/references/verification-depth.md#6-명세테스트-충돌): `유지` 행이 실패하고 의미를 바꿔야 통과하면 사용자 판정 (a)/(b).
  - 훅 메시지: [test-guard.md](../../../setup/hooks/messages/test-guard.md) "멈추고 … 사용자 판정을 받아라", [stop-gate.md](../../../setup/hooks/messages/stop-gate.md) "되돌리거나, 정당한 변경이면 … 기록하라" — 정당성 판단 기준을 주지 않는다.
- [경량 경로 §4](../../../skills/wf-design/references/lightweight-path.md#4-승인-게이트와의-관계): "기록을 남기지 않는 경량 작업"이 허용된다. 그 경우 종료 게이트 위반을 기록할 작업 기록이 없다.
- 본문 어절(`lint_skill.py`): wf-implement 2,816/2,850(여유 34), wf-design 2,192/2,300. 오류 0, 경고 6.
- Claude Code 도구 입력: Edit `{file_path, old_string, new_string, replace_all}`, MultiEdit `{file_path, edits:[{old_string, new_string, replace_all}]}`, Write `{file_path, content}`, NotebookEdit `{notebook_path, …}`. PostToolUse는 도구가 실제로 실행된 뒤에만 발화한다(거절·실패한 편집에는 오지 않는다).
- 상태 파일 `%TEMP%\claude-wf\<session_id>.json`은 DES-02가 객체 전체를 덮어쓴다(`Write-WfState`, [wf-common.ps1:102-111](../../../setup/hooks/wf-common.ps1)). 같은 파일에 다른 필드를 두면 PostToolUse 동시 발화 때 서로 지운다.
- B(승인 게이트) 판정은 현재 저장소에서 README·스킬·훅 경로 모두 exit 0(열린 작업 없음).
- 재사용 후보 자산: `Get-WfKeptTestFiles`(대장 판독), `ConvertTo-WfKey`(경로 정규화), `Read-WfState`/상태 디렉터리, `Write-WfPermission`/`Write-WfJson`, `run-tests.ps1`의 `New-GuardRepo`·`Invoke-Guard`·`Invoke-StopGate` 픽스처, `test_regression_guard.py`의 tmp git 픽스처, `install-hooks.ps1`의 `New-WfEntry`·자기 항목 식별(`\setup\hooks\wf-*.ps1`).

### 해석

- C·D의 질문 대부분은 **순수 추가를 파일 단위 보호가 위험 변경으로 분류**해서 생긴다. TDD(Red 먼저)는 기존 테스트 파일에 테스트를 더하는 일이 잦으므로 워크플로우 자신의 규정과 훅이 충돌한다.
- Claude의 일반 질문으로 나타나는 경로는 둘이다. (1) Stop 차단 사유는 Claude에게 전달되고 "정당한 변경이면 기록"의 정당성 판단 기준이 없어 사용자에게 묻는다. (2) 가드 확인 뒤에도 주의 ④·§3.3의 "수정" 범위가 모호해 Claude가 보수적으로 묻는다.
- 같은 사유의 반복은 판정이 상태를 남기지 않아서다(가드: 편집마다, 게이트: Stop마다).
- 순수 추가도 테스트를 무력화할 수 있다(예: `@pytest.mark.skip` 줄 삽입, 테스트 본문 앞 값 없는 `return` 삽입). 순수 추가를 통과시키려면 추가된 줄의 비활성화 패턴을 따로 봐야 한다. 줄을 주석으로 바꾸는 것은 삭제 + 추가라 순수 추가가 아니다.

### 가정

- A-01 B(승인 게이트)는 범위 밖 — 사용자 보고상 빈도가 낮다. 단 선행 변경(`46600de`)의 승인 게이트 판독 완화는 사후 기록한다(Q-05).
- A-02 `deny`는 도입하지 않는다(ADR-014 결정 1 유지).
- A-03 재정비 관문의 「변경 없어도 재정비 기록 1행」은 완료 보고 관문과 같은 응답이라 별도 질문을 만들지 않는다 — 범위 밖.
- A-04 PreToolUse `ask`의 `permissionDecisionReason`은 사용자에게만 보이고 Claude에게는 전달되지 않는다(Claude Code 동작, 미검증 — 구현 첫 TASK에서 확인). 맞든 틀리든 이 설계는 성립한다 — 메시지와 규정을 함께 고친다(FR-06).
- A-05 비활성화 패턴은 휴리스틱이다. 목록 밖의 무력화 삽입은 완료 보고의 diff 검토와 대장 `보호 스코프` 열의 테스트 수 대조로 잡는다(RISK-01).

## 질문

질문 단계 점검: 범위 — Q-05(선행 변경 편입 범위). 인수 조건 — 해당 없음(판정 결과는 훅 테스트·pytest로 관찰). 실패 시 기대 동작 — Q-04(기록할 곳이 없을 때). 보안 — Q-01(순수 추가 판정이 무력화 삽입을 놓칠 위험). 데이터 — Q-02(세션 상태 파일 신설). 공개 인터페이스(훅 동작·메시지) — Q-01·Q-02·Q-03. 호환성(기존 대장·작업 기록) — 해당 없음(대장 열·상태값 무변경).

| ID | 질문 | 선택지 | 권장안 | 근거 | 답 |
|---|---|---|---|---|---|
| Q-01 | 순수 추가를 위반에서 뺄 것인가 | (A) 뺀다 — 가드: 새 파일 생성이거나 Edit의 `new_string`이 `old_string`을 그대로 포함하고 추가 부분에 비활성화 패턴(`skip`·`xfail`·`-Skip` 등)이 없으면 묻지 않음. 게이트: 보호 파일 diff에 삭제 줄이 없고 추가 줄에 비활성화 패턴이 없으면 위반 아님 (B) 판정은 그대로, 규정 문구만 고침 | (A) | 영향: DES-06·07 판정, `regression_guard.py`, 훅·pytest 테스트. (B)는 훅 확인창·Stop 차단이 그대로 남아 TDD마다 발생 | "전부 권장안" — 사용자, 2026-11-22 |
| Q-02 | 같은 세션의 반복 판정을 억제할 것인가 | (A) 억제 — 가드: PostToolUse에서 실제로 편집된(=사용자가 허락한) 보호 파일을 세션 상태에 남기고 같은 세션의 같은 파일은 다시 묻지 않음. 게이트: 같은 세션에서 이미 차단한 위반 집합과 같으면 다시 막지 않고 새 위반만 막음 (B) 억제 없음 | (A) | 영향: 새 PostToolUse 훅 항목(DES-04 등록), 세션 상태 파일(`%TEMP%\claude-wf`, DES-02와 같은 위치), DES-06·07. 거절된 편집은 PostToolUse가 오지 않아 기록되지 않음 | "전부 권장안" — 사용자, 2026-11-22 |
| Q-03 | 사용자 판정을 받는 경우를 좁힐 것인가 | (A) 좁힌다 — 즉시 사용자 판정은 기존 단언 삭제·약화·기대값 변경·테스트 비활성화(§6 충돌)만. 그 밖의 보호 파일 변경은 `### 테스트 대장 변경`에 기록하고 진행, 확인은 완료 보고 관문의 일괄 응답. 주의 ④·§3.3에 「순수 추가는 수정이 아니다」 명시, 훅 메시지를 판단 기준 중심으로 교체 (B) 규정 유지 | (A) | 영향: wf-implement 주의 ④·§3.3, verification-depth §2·§6, messages 2개, wf-implement 본문 어절(K3 상한) | "전부 권장안" — 사용자, 2026-11-22 |
| Q-04 | 기록할 작업 기록이 없을 때(기록 없는 경량 작업, 저장소 밖 커밋) 남은 위반을 어떻게 할 것인가 | (A) 계속 차단 — 순수 추가는 Q-01로 빠지고, 남은 위반(삭제·변경)은 정당한 신호이므로 차단하되 Q-02로 세션당 1회 (B) 열린 작업 기록이 없으면 차단 대신 사용자 알림만 | (A) | 영향: DES-07, 경량 경로 §4 문구. (B)는 작업 기록 없이 단언을 지우는 경로가 무방비 | "전부 권장안" — 사용자, 2026-11-22 |
| Q-05 | 선행 변경 `46600de`를 어떻게 편입할 것인가 | (A) 이 작업의 DCR에 함께 반영 — 임계값 기본값(ADR-012 정밀화)·usage 중첩 판독·`\|` 처리·승인 인용 판독을 설계·ADR에 사후 기록하고, 대장 SHA 갱신과 `### 테스트 대장 변경` 기록을 이 작업에서 수행 (B) 대장 SHA·기록만 이 작업에서 하고 설계 문서 반영은 별도 작업 | (A) | 영향: DCR 범위(C층 DES-02·08·09, B층 `approval_gate.py`), approval-request §4 문구, 대장 TST-01·02 | "전부 권장안" — 사용자, 2026-11-22 |

## 범위

- 포함: B층 판정(`regression_guard.py`)의 내용 단위 판정·지문·지문 단위 해소, 공유 비활성화 패턴 파일, C층 DES-06 가드의 순수 추가 판정·세션 기억(PreToolUse + PostToolUse), DES-07 게이트의 세션 반복 억제, DES-04 등록 7개, 훅 메시지 2개, verification-depth §9 신설과 §2·§6·주의 ④·§3.3 개정, 경량 경로 §4 1문장, 테스트(TST-01·02 추가), [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md), [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md)(REQ·DESIGN v5 → v6, 선행 변경 사후 기록 포함), approval-request §4·REQ-DESIGN-regression-guard DES-08 문구, 대장 TST-01·02 SHA 갱신.
- 범위 밖: B(승인 게이트) 판정 완화(A-01 — 선행 변경 기록만), `deny` 도입(A-02), 재정비 관문 기록 규칙(A-03), 대장 열·상태값 변경, 테스트 실행을 통한 판정, 대장 행의 테스트 단위 분할.

## 요구사항

이 절에서 「가드」는 C층 DES-06(`wf-test-guard.ps1`), 「게이트」는 C층 DES-07(`wf-stop-gate.ps1`), 「B층 판정」은 `regression_guard.py`를 뜻한다. `DES-NN`만 쓰면 이 문서의 [설계](#설계) 행이다.

### 기능 요구사항

| ID | 이름 | 내용 |
|---|---|---|
| FR-01 | 순수 추가 정의 | **순수 추가**는 보호 파일의 변경 전 줄이 변경 후 줄에 모두 같은 순서로 그대로 남고(줄 단위 부분열), 새로 생긴 줄 어디에도 공유 **비활성화 패턴**(FR-02)이 없는 변경이다. 줄 안의 문자를 고치면(주석 처리, `or True` 덧붙임, 줄 쪼개기) 그 줄이 남지 않으므로 순수 추가가 아니다. 새 파일 생성은 모든 줄이 새 줄이며 같은 패턴 검사를 받는다. 파일 삭제·이름 변경은 원래 파일의 줄이 모두 사라지므로 순수 추가가 아니다. 순수 추가는 「수정」이 아니며 회귀 보호의 위반이 아니다 |
| FR-02 | 비활성화 패턴 | 테스트를 끄거나 무조건 통과시키는 **구문**의 정규식 목록을 B층 데이터 파일 한 곳에 둔다(대소문자 무시, 줄 단위). 일반 낱말(`skips`, `Select-Object -Skip`)에 맞지 않도록 구문 단위로 쓴다. 최소 목록: `pytest\.mark\.(skip\|xfail)`, `pytest\.(skip\|xfail)\(`, `unittest\.skip`, `\.skipTest\(`, `^\s*@skip`, `\bIt\b.*\s-Skip\b`, `Set-ItResult`, `\.only\(`, `\bx(it\|describe)\(`, 값 없는 `return`(`^\s*return\s*;?\s*$`), `^\s*if\s*\(?\s*(False\|\$false)\s*\)?\s*[:{]?\s*$`. B층 판정과 가드는 같은 파일을 읽는다 |
| FR-03 | 가드의 순수 추가 통과 | 가드는 대상이 `유지` 행 테스트 파일이고 도구가 Edit·MultiEdit·Write일 때, 현재 파일 내용에 편집을 메모리에서 적용한 결과가 FR-01의 순수 추가이면 묻지 않는다. 적용 규칙: Edit = `old_string`의 첫 위치(`replace_all`이면 모든 위치)를 `new_string`으로 치환, MultiEdit = `edits`를 순서대로 같은 방식으로 적용, Write = `content`로 교체, 대상 파일이 없으면 변경 전 내용은 빈 내용. `old_string`을 찾지 못하거나 판정 중 예외가 나면 순수 추가가 아닌 것으로 본다(fail-to-ask, NFR-04). NotebookEdit와 Claude 게이트 설정 파일에는 이 통과를 적용하지 않는다(항상 `ask`) |
| FR-04 | 가드의 세션 기억 | 가드가 테스트 파일로 `ask`를 낼 때 (경로, 도구 이름 + `tool_input`의 해시)를 세션 가드 상태 `asked`에 남긴다. PostToolUse(도구가 실제로 실행됨 = 사용자 허락)의 (경로, 해시)가 `asked`의 항목과 **같을 때만** 그 경로를 `approved`로 옮긴다. 같은 세션에서 `approved` 경로는 다시 묻지 않는다. 거절된 편집은 PostToolUse가 오지 않으므로, 이후 다른 편집(순수 추가 포함)의 PostToolUse로는 승인되지 않는다. NotebookEdit와 설정 파일은 `asked`·`approved`에 넣지 않는다(항상 `ask`). 세션이 바뀌면 기억은 없다 |
| FR-05 | B층 내용 단위 판정 | (a) 테스트 파일 변경은 내용으로 판정한다 — 마지막 성공 SHA 대비(커밋 + 워킹트리, 이름 변경 감지 끔) 보호 파일의 diff에 삭제 줄이 있거나 추가 줄이 FR-02에 맞으면 위반, 순수 추가면 위반 아님. 미추적 파일(`git ls-files --others --exclude-standard`) 중 보호 파일은 전 줄을 추가 줄로 보고 같은 판정을 한다. 이진 파일·판독 불가 diff는 그 파일의 위반으로 본다. (b) 대장 축소 판정(삭제·상태 변경·`테스트 파일` 값 변경)은 무변경. (c) 테스트 파일 위반마다 **지문**(삭제 줄과 패턴에 맞은 추가 줄의 내용만으로 만든 해시 8자 — 줄 번호·다른 순수 추가와 무관)을 출력한다. 같은 파일에 새 삭제가 생기면 지문이 바뀐다. (d) 해소: 테스트 파일 위반은 열린 작업 기록 `### 테스트 대장 변경`의 같은 행에 행 ID와 그 **지문**이 함께 있어야 해소된다. 대장 축소 위반은 기존대로 행 ID만으로 해소된다. (e) 판정 스크립트 자체의 오류(대장 판독 실패, 패턴 파일 없음, git 실행 불가)는 exit 2(게이트는 통과 — 기존 C층 NFR-01) |
| FR-06 | 게이트의 세션 반복 억제 | 게이트는 판정이 위반을 내면 위반마다 키(행 ID·파일·지문)를 만들고, 같은 세션에서 이미 차단한 키 집합에 **없는 키가 하나라도** 있을 때만 차단한 뒤 그 키들을 집합에 더한다. 모든 키가 이미 차단한 것이면(일부가 해소된 부분집합 포함) 차단하지 않는다. `stop_hook_active` 통과는 그대로 |
| FR-07 | 사용자 판정 범위 | 보호 테스트(대장 `유지` 행의 테스트 파일) 변경을 셋으로 나눈다. (1) **순수 추가**(FR-01) — 수정이 아니다. 기록·승인 불요, 새 테스트는 TASK `completed` 때 대장 등록(기존 규칙). (2) **단언 보존 변경** — 기존 단언마다 같거나 더 강한 단언이 남는 변경(기능 변경에 따른 호출·픽스처·이름 조정, 단언 강화). 진행 중 허용, `### 테스트 대장 변경`에 `유지 → 유지` · 분류 `단언 보존 변경 — 사유` · 증거(수정 전후 같은 제품 SHA 통과 또는 단언 대조) · 게이트가 보고한 지문을 적고 진행, 확인은 완료 보고 관문의 일괄 응답. (3) **단언 약화** — 단언 삭제·약화, 기대값 변경, 테스트 비활성화·삭제. 진행 중 금지, §6 충돌 출구로 즉시 사용자 판정. 단 승인된 DCR이 바꾼 동작에 따른 기대값 변경은 §6 판정 (b)가 이미 내려진 것으로 보고 `Breaking`으로 기록한다(선례: [WORK-20261026-approval-gate](../20261026-approval-gate/work-log.md) T45·T46). 판단이 서지 않으면 (3)으로 본다. 냄새 제거 목적의 `리팩터`는 기존대로 독립 재정비 작업 한정. 기록한 작업을 닫을 때는 기록한 행의 테스트를 실행해 마지막 성공 SHA를 갱신한다(경량 경로 작업 기록 포함 — 닫힌 기록은 해소에 쓰이지 않으므로) |
| FR-08 | 선행 변경 편입 | `46600de`의 C층·B층 동작 변경(임계 기본값 400000/100000, usage 임의 깊이 중첩 판독, 대장 칸 분할의 GFM `\|`, 승인 게이트의 상태 첫 백틱 값·응답 인용 「」·"사용자" 줄)을 REQ·DESIGN v6에 반영하고, 대장 판독 규칙의 정본인 [REQ-DESIGN-regression-guard DES-08](../20261025-regression-guard/req-design.md#설계)과 approval-request §4의 문장을 코드와 맞춘다. 대장 TST-01·02의 마지막 성공 SHA를 이 작업의 `completed` 전이에서 갱신한다 |

### 비기능 요구사항

| ID | 이름 | 내용 |
|---|---|---|
| NFR-01 | 본문 어절 | wf-implement 본문 ≤ 2,850어절(`lint_skill.py` K3 오류 0). 본문 변경은 주의 ④ 문구와 §3.3 금지문 수정(합계 순증 ≤ 25어절)뿐이며 판정 규칙 본체는 verification-depth §9 |
| NFR-02 | 대장·판독 호환 | 대장 열·상태값 무변경. 대장 판독 규칙은 `46600de`의 `\|` 이스케이프 외 무변경(FR-08로 정본 문구 보완). 대장 축소 위반의 해소는 기존 기록 그대로. 테스트 파일 위반의 해소에 지문이 필요해지는 것은 계약 변경이다. 이 저장소의 열린 기록은 이 작업뿐이고(그 기록의 TST-01·02는 순수 추가라 새 판정에서 위반이 아니다), 훅은 전역 설치라 다른 저장소의 열린 기록에 행 ID만 적힌 테스트 파일 위반은 순수 추가가 아니면 키마다 세션당 1회 차단되며 지문을 더하면 해소된다(메시지가 안내 — DES-07) |
| NFR-03 | 지연 | 가드의 순수 추가 판정은 PowerShell 안에서 하고 Python을 부르지 않는다. 훅 `timeout: 10`초 안. B층 판정의 추가 비용은 보호 파일당 `git diff` 1회 |
| NFR-04 | 실패 정책 | 가드: 대장 판독 오류·순수 추가 판정 예외 → `ask`(fail-to-ask 유지). 가드 상태 파일 읽기·쓰기 실패 → 기억 없음으로 진행(묻는 쪽). 게이트: 판정 스크립트의 부재·exit 2·타임아웃 → 통과(기존). 가드 상태 읽기·쓰기 실패 → 억제 없이 차단. PostToolUse 기록 실패 → 무출력. 가드 상태 파일은 잠금 없이 읽고-고치고-쓴다 — 동시 발화로 갱신을 잃으면 다시 묻거나 다시 차단하는 쪽(안전)이다 |
| NFR-05 | 하네스 중립 | 판정 규칙(순수 추가·비활성화 패턴·지문·해소)은 B층(Python 표준 라이브러리 + git)과 B층 데이터 파일이 정본. 가드는 같은 데이터 파일을 읽어 사전 판정만 한다 |

## 인수 조건

| ID | 조건 |
|---|---|
| AC-01 | (가드 순수 추가) 대장 `유지` 행 테스트 파일에 대해: 줄 경계에 줄을 더하는 Edit → 무출력; 기존 줄을 주석 처리(`old="assert a"`→`new="# assert a"`)·약화(`old="== 1"`→`new="== 1 or True"`)·쪼개는 Edit → `ask`; 더한 줄에 `@pytest.mark.skip`이 있는 Edit → `ask`; 없는 파일 Write(패턴 없음) → 무출력, 패턴 있는 내용 → `ask`; 기존 줄을 모두 순서대로 유지한 Write → 무출력, 한 줄을 지운 Write → `ask`; 모든 항목을 적용한 결과가 순수 추가인 MultiEdit → 무출력, 아니면 `ask`; `old_string`이 파일에 없는 Edit → `ask`; NotebookEdit → `ask`; 게이트 설정 파일 → 순수 추가여도 `ask`; 기존 보호 파일의 정상 낱말(`'T28 threshold skips …'`, `Select-Object -Skip 2`)이 든 줄 추가 → 무출력 |
| AC-02 | (가드 기억) `ask`가 난 테스트 파일 편집과 같은 (경로, 해시)의 PostToolUse가 오면 이후 같은 세션의 비순수 편집은 무출력; 다른 `session_id`는 `ask`; `ask` 뒤 PostToolUse 없이(거절) 같은 파일에 순수 추가 편집과 그 PostToolUse가 와도 이후 비순수 편집은 `ask`; 설정 파일·NotebookEdit는 PostToolUse 뒤에도 `ask` |
| AC-03 | (B층 판정) tmp git 픽스처에서 마지막 성공 SHA 이후 `유지` 테스트 파일에: 줄만 추가(커밋·워킹트리 각각) → exit 0; 줄 삭제 → exit 1이고 출력 행 끝에 지문 8자; 추가 줄에 `pytest.mark.skip` → exit 1; 값 없는 `return` 추가 → exit 1; 다른 파일에 순수 추가만 더하거나 위반 줄 위에 줄을 끼워 hunk가 밀려도 지문 불변; 같은 파일의 다른 삭제 → 다른 지문; glob 안에서 `git mv` + 줄 삭제 → exit 1(원래 경로 삭제); 패턴 줄이 든 미추적 새 보호 파일 → exit 1, 패턴 없는 미추적 새 파일 → exit 0; 지문 없이 행 ID만 기록 → exit 1, 행 ID + 지문 기록 → exit 0; 대장 `유지` 행 삭제 + 행 ID 기록 → exit 0(기존 동작); 패턴 파일 없음 → exit 2 |
| AC-04 | (게이트 억제) 같은 세션에서 같은 키 집합으로 두 번째 Stop(`stop_hook_active` 거짓) → 무출력; 키 일부만 남은 부분집합 → 무출력; 새 키(행 추가 또는 지문 변경)가 있으면 → 차단; 다른 세션 → 차단 |
| AC-05 | (패턴 공유) 비활성화 패턴 파일이 하나이고 B층 pytest와 훅 테스트가 같은 표본 줄(맞음 4·안 맞음 4, 안 맞음에 `skips`·`Select-Object -Skip 2` 포함)에 같은 결과를 낸다. 이 작업이 TST-01·02에 더하는 모든 테스트(AC-01·03·05)의 패턴 표본·픽스처 줄은 테스트 소스 안에서 실행 시 조합해, 테스트 파일 자체에는 패턴에 맞는 줄이 생기지 않는다(이 작업의 추가가 순수 추가로 판정됨) |
| AC-06 | (규정) verification-depth에 `## 9. 보호 테스트 변경의 판정` 절이 FR-07의 세 분류·기록 형식(지문 포함)·승인된 DCR의 `Breaking`·「판단이 서지 않으면 단언 약화」·기록할 작업 기록이 없으면 경량 경로 작업 기록을 만들고 닫을 때 SHA를 갱신한다는 문장을 담는다. §6 첫 문단·§2 「통과시키려고 테스트를 수정·제외·삭제」 문장·wf-implement 주의 ④와 §3.3 금지문이 §9와 모순 없이 §9를 가리킨다. 메시지 `test-guard.md`·`stop-gate.md`가 판단 기준(순수 추가 통과·단언 보존은 지문과 함께 기록·단언 약화만 사용자 판정)을 담는다. wf-implement 본문 ≤ 2,850어절, `lint_skill.py` 오류 0 |
| AC-07 | (선행 변경·설계) REQ·DESIGN 기준선 v6에 DCR-026 변경 항목이 반영되고(설정값 400000/100000, usage 판독, `\|`, 승인 판독, DES-04 7개, C층 DES-06·07, 가드 상태 파일, B층 출력 지문·해소 규칙), REQ-DESIGN-regression-guard DES-08에 `\|` 규칙과 변경 이력 1행, approval-request §4가 「」와 "사용자" 줄 인용을 명시한다 |
| AC-08 | (회귀·통합) `유지` 4행(TST-01·02·04·05) 통과, 설치 재실행 시 PostToolUse 2개(C층 DES-02, 가드 기록) 포함 7개 등록·중복 없음, T18·T19·T21의 PostToolUse 기대값 1→2는 `Breaking`(DCR-026 승인)으로 기록, 이 문서 `lint_design.py` exit 0, 작업 기록 린트 오류 0, `completed` 전이 후 HEAD에서 `regression_guard.py .` exit 0 |

## 설계

| ID | 이름 | 내용 |
|---|---|---|
| DES-01 | B층 내용 판정 | `regression_guard.py`: 후보 파일은 `git diff --no-renames --name-only --relative -z <sha>`(이름 변경을 삭제 + 추가로). 여기에 `git ls-files --others --exclude-standard -z`의 미추적 파일을 더한다(전 줄 추가 줄, 삭제 줄 없음). 보호 행이 있는 추적 파일마다 `git diff --no-renames --unified=0 --no-color --relative <sha> -- <파일>`. 헤더는 **위치로** 가른다 — 첫 `@@` 행 앞은 헤더, 그 뒤의 `-`·`+` 접두 줄이 내용(`+++`·`---` 접두 판별 금지). 헤더에 `Binary files`가 있으면 위반(지문 `bin`). 위반 = 내용 삭제 줄 ≥ 1 또는 패턴에 맞는 추가 줄 ≥ 1. 지문 = (`-`+삭제 줄 내용, `+`+패턴 추가 줄 내용)을 나온 순서로 `\n` 이어 UTF-8 SHA-1 앞 8자. 출력 `TST-NN: 테스트 파일 변경 <파일> [<지문>]`, 대장 축소는 기존 출력 + ` [-]`. 해소 `recorded_ids` → `recorded(root)`가 열린 작업 기록 대장 변경 절의 **줄마다** (행 ID 집합, 8자 16진 토큰 집합)을 돌려주고, 테스트 파일 위반은 같은 줄에 행 ID와 지문이 함께 있을 때, 대장 축소 위반은 행 ID만 있을 때 해소. 패턴은 `load_patterns()`가 DES-02 파일을 읽고 없으면 예외(exit 2) |
| DES-02 | 공유 패턴 파일 | `skills/wf-doc/scripts/test-disable-patterns.txt` — 한 줄에 정규식 하나, `#` 주석·빈 줄 무시, UTF-8. FR-02 최소 목록. Python `re.IGNORECASE`와 .NET `[regex]` `IgnoreCase`에서 같은 의미가 되는 문법만 쓴다(룩비하인드·명명 그룹·인라인 플래그 없음) |
| DES-03 | 가드 순수 추가·기억 | `wf-test-guard.ps1`이 `hook_event_name`으로 분기. **PreToolUse:** 기존 판정으로 hits를 만든 뒤, hits에 `settings`가 있거나 도구가 NotebookEdit면 기존대로 `ask`(기억·순수 추가 없음). hits가 테스트 행만이면 (1) 가드 상태 `approved`에 경로가 있으면 무출력 (2) `Test-WfPureAddition`이 참이면 무출력 (3) 아니면 `asked`에 (경로, `Get-WfToolInputHash`)를 더하고 `ask`. **PostToolUse:** 대상의 (경로, 해시)가 `asked`에 있으면 그 항목을 지우고 경로를 `approved`에 더함, 그 밖은 무출력. 경로 키는 `ConvertTo-WfKey` 상대 경로 |
| DES-04 | 공용 함수 | `wf-common.ps1`에 추가: `Get-WfGuardState`/`Set-WfGuardState`(`%TEMP%\claude-wf\<session_id>.guard.json` — `{asked:[{path,hash}], approved:[path], stopKeys:[key]}`; C층 DES-02의 `<sid>.json`과 분리해 서로 덮어쓰지 않게 한다. 잠금 없음 — NFR-04), `Get-WfDisablePatterns`(DES-02 파일을 `$PSScriptRoot\..\..\skills\wf-doc\scripts\`에서 읽음), `Get-WfToolInputHash`(`tool_name` + `ConvertTo-Json -Compress -Depth 10 tool_input`의 SHA-1), `Test-WfPureAddition`(FR-03 적용 규칙으로 변경 후 내용을 만들고, CRLF → LF 정규화 뒤 변경 전 줄이 변경 후 줄의 부분열인지 두 포인터로 확인, 부분열 밖 줄에 패턴 검사) |
| DES-05 | 게이트 억제 | `wf-stop-gate.ps1`: 판정 exit 1이면 출력 행마다 키 = `<행 ID>\|<파일>\|<지문>`(행 끝 `[…]`을 지문으로, 없으면 `-`). 가드 상태 `stopKeys`에 없는 키가 하나라도 있으면 키들을 `stopKeys`에 더하고 `block`, 모두 있으면 무출력. 상태 읽기·쓰기 실패는 억제 없이 `block` |
| DES-06 | 설치 | `install-hooks.ps1` `$desired.PostToolUse`에 `New-WfEntry 'Edit\|Write\|MultiEdit\|NotebookEdit' wf-test-guard.ps1` 추가(C층 DES-02 다음). 총 7개. 자기 항목 식별·멱등은 기존 그대로. 기존 훅 테스트 T18·T19·T21의 PostToolUse 기대값 1 → 2는 승인된 DCR-026에 따른 `Breaking` 수정(§6 판정 (b) 승인됨, FR-07) |
| DES-07 | 메시지 | `test-guard.md`: 「기존 줄을 그대로 두고 줄만 더하는 편집은 이 확인 없이 진행된다. 이 편집은 기존 줄을 바꾸거나 테스트를 끄는 구문을 더한다 — 단언 보존 변경이면 허용 후 `### 테스트 대장 변경`에 기록, 단언 약화면 거절하고 verification-depth §6」 취지. `stop-gate.md`: 「위반은 기존 줄 삭제·변경 또는 테스트를 끄는 구문 추가다. verification-depth §9로 분류해 단언 보존 변경이면 행 ID와 지문을 기록하고 끝내고, 단언 약화면 되돌리거나 §6으로 사용자 판정. 기록할 열린 작업 기록이 없으면 경량 경로 작업 기록을 만든다」 취지. ASCII 아닌 문구는 메시지 파일에만(C층 DES-05 원칙) |
| DES-08 | 규정 | verification-depth `## 9. 보호 테스트 변경의 판정`(FR-07 표, 기록 예 — `TST-NN · 유지 → 유지 · 단언 보존 변경 — 사유, 지문 [xxxxxxxx] · …`, 승인된 DCR의 `Breaking`, 기록 없는 경우와 닫을 때 SHA 갱신). §6 첫 문단 끝에 「분류는 §9」. §2 표 아래 「`유지` 행을 통과시키려고 테스트를 수정·제외·삭제하는 것은」을 「`유지` 행을 통과시키려고 단언을 약화하거나 테스트를 제외·삭제하는 것은(§9 (3))」로, `리팩터` 단락의 「기능 작업 진행 중의 기존 테스트 수정 금지(§3.3)」를 「진행 중의 단언 약화 금지(§3.3·§9)」로. wf-implement 주의 ④ 「테스트를 수정·제외해 통과시키지 않는다」→「단언을 약화하거나 테스트를 제외해 통과시키지 않는다([§9](references/verification-depth.md#9-보호-테스트-변경의-판정))」, §3.3 금지문 「기존 테스트의 수정·제외·삭제를 하지 않는다」→「기존 단언의 약화·테스트 제외·삭제를 하지 않는다 — 순수 추가와 단언 보존 변경은 §9」. 경량 경로 §4 끝에 「보호 테스트 변경을 기록해야 하면 작업 기록을 남긴다(§9)」 1문장. templates `### 테스트 대장 변경` 예시에 단언 보존 변경 행 1개 |
| DES-09 | 기준선 반영 | [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md)대로 `docs/requirements.md`(FR-06·07·NFR-01·AC-07·08 문구, v6)·`docs/design.md`(C층 DES-02 설정값·usage 판독, DES-04 7개, DES-06·07·09, 가드 상태 파일, B층 계약 출력 지문·해소, 흐름, 위험, 대안과 결정 ADR-025, v6), [REQ-DESIGN-regression-guard](../20261025-regression-guard/req-design.md) DES-08 `\|` 문구와 변경 이력 1행, approval-request §4 |

| ID | 의존 | 피의존 | 소유 데이터 | 출처 |
|---|---|---|---|---|
| DES-01 | DES-02 | DES-05 | — | 확장(skills/wf-doc/scripts/regression_guard.py) |
| DES-02 | — | DES-01, DES-04 | 비활성화 패턴 목록 | 신규 — B층·C층이 같은 패턴을 읽어야 하는데 공유할 기존 데이터 파일이 없음(skills/wf-doc/scripts/test-disable-patterns.txt) |
| DES-03 | DES-04, DES-07 | DES-06 | — | 확장(setup/hooks/wf-test-guard.ps1) |
| DES-04 | DES-02 | DES-03, DES-05 | 가드 상태 파일 | 확장(setup/hooks/wf-common.ps1) |
| DES-05 | DES-01, DES-04, DES-07 | DES-06 | — | 확장(setup/hooks/wf-stop-gate.ps1) |
| DES-06 | DES-03, DES-05 | — | `~/.claude/settings.json` 훅 항목 | 확장(setup/hooks/install-hooks.ps1, setup/hooks/tests/run-tests.ps1) |
| DES-07 | — | DES-03, DES-05 | 메시지 문구 | 확장(setup/hooks/messages/) |
| DES-08 | — | — | 보호 테스트 변경 분류 규정 | 확장(skills/wf-implement/references/verification-depth.md, skills/wf-implement/SKILL.md, skills/wf-design/references/lightweight-path.md, skills/wf-doc/references/templates.md) |
| DES-09 | — | — | — | 확장(docs/requirements.md, docs/design.md, docs/work/20261025-regression-guard/req-design.md, skills/wf-design/references/approval-request.md) |

결정: [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md) — 판정 단위를 파일에서 변경 내용으로(순수 추가 면제 + 비활성화 패턴), 지문 단위 해소, 세션 반복 억제, 사용자 판정 범위의 3분류. [ADR-014](../20261025-regression-guard/ADR-014-회귀-보호-훅-강제-방식.md) 결정 1·3의 정밀화(대체 아님). C층 기준선 변경은 [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md).

## 위험

| ID | 위험 | 대응 |
|---|---|---|
| RISK-01 | 비활성화 패턴 밖의 무력화 삽입(조건부 skip, 환경 변수로 끄기, 값을 돌려주는 조기 `return`)이 순수 추가로 통과 | 패턴은 구문 단위 최소 목록으로 시작하고 데이터 파일 한 곳에서 늘린다(DES-02). 완료 보고에서 보호 파일 diff를 보이고 대장 `보호 스코프` 열의 테스트 수(「총 N」)를 실행 결과와 대조한다. 이전에는 모든 편집이 사람 확인이었으므로 감수 단점으로 ADR-025에 기록 |
| RISK-02 | 가드 기억 뒤 같은 파일의 약화 편집이 확인 없이 통과 | 게이트가 Stop에서 내용으로 다시 판정한다. 해소는 지문 단위라(FR-05 (d)) 기록된 변경 뒤의 새 삭제는 새 지문으로 위반이 되고, 억제도 새 키라 적용되지 않는다(FR-06) |
| RISK-03 | 게이트 억제로 Claude가 차단을 무시하면 그 세션에서는 다시 막지 않음 | 억제는 이미 차단한 키에만. 다음 세션에서 다시 차단. `completed` 전이에서 `regression_guard` exit 0이 필요(AC-08) |
| RISK-04 | PostToolUse 항목 추가로 모든 편집에 PowerShell 기동 1회 추가(~250ms) | 기록 분기는 파일 읽기 1회. 측정해 작업 기록에 남긴다(NFR-03). 필요하면 후속으로 PreToolUse 2개 통합 |
| RISK-05 | A-04(`ask` 사유의 Claude 비전달) 미검증 | 첫 TASK에서 관찰. 어느 쪽이든 FR-07 규정과 메시지를 함께 고치므로 설계는 유지 |
| RISK-06 | 줄 부분열 판정이 같은 내용 줄의 위치 이동을 놓침 | 두 포인터 매칭은 순서를 보존하므로 줄이 사라지면 반드시 실패한다. 같은 내용 줄의 이동은 단언 의미가 같다 — 감수. B층은 git diff가 이동을 삭제 + 추가로 보이므로 위반(안전) |
| RISK-07 | 선행 변경 `46600de`는 워크플로우 밖에서 만들어져 TDD Red 증거가 없음 | 착수 시 59/59·pytest 통과를 증거로 기록하고, 작업 기록 `설계와 달라진 점`에 Red 미보유를 남긴다 |
| RISK-08 | 지문 출력·해소 규칙 변경을 다른 소비자가 파싱하거나 기존 기록에 기대 | 출력 소비자는 게이트뿐(B층 계약). 행 앞부분 `TST-NN: <사유> <파일>`은 유지하고 끝에 ` [지문]`만 붙인다. 이 저장소의 열린 기록은 이 작업뿐, 다른 저장소의 행 ID만 적힌 기록은 키마다 세션당 1회 차단 후 지문 추가로 해소(NFR-02) |
| RISK-09 | 줄바꿈만 바뀐 파일(CRLF ↔ LF)이 모든 줄 삭제·추가로 보여 위반 | 가드는 CRLF → LF 정규화 후 비교(DES-04). B층은 git의 정규화(`core.autocrlf`·`.gitattributes`)에 맡기고, 남는 경우는 위반 쪽(안전) — 지문 기록 1건으로 해소 |
| RISK-10 | 지문 기록을 Claude가 작성하므로, 단언 약화를 단언 보존 변경으로 잘못 분류해 기록하면 게이트가 통과 | 게이트는 기록 확인이지 승인이 아니다(C층 RISK-08과 같은 결). 완료 보고에서 대장 변경 표와 diff를 함께 보이고 일괄 확인. 분류 기준과 「판단이 서지 않으면 (3)」을 규정에 둔다(FR-07) |
| RISK-11 | 경량 경로 작업 기록을 열면 승인 게이트가 그 작업의 기계 조건을 판정(경량 경로 §4) — 제품 코드 5파일 초과·새 비테스트 파일에서 확인이 생김 | 기존 설계된 동작이다. 기록이 필요한 정도의 보호 테스트 변경이면 경량 경로 조건 판정을 받는 것이 맞다 — 감수 |

## 추적성

| 요구사항 | 설계 | 인수 조건 |
|---|---|---|
| FR-01 | DES-01, DES-04 | AC-01, AC-03 |
| FR-02 | DES-02 | AC-05 |
| FR-03 | DES-03, DES-04 | AC-01 |
| FR-04 | DES-03, DES-04, DES-06 | AC-02, AC-08 |
| FR-05 | DES-01 | AC-03 |
| FR-06 | DES-05 | AC-04 |
| FR-07 | DES-06, DES-07, DES-08 | AC-06, AC-08 |
| FR-08 | DES-09 | AC-07, AC-08 |
| NFR-01 | DES-08 | AC-06 |
| NFR-02 | DES-01, DES-09 | AC-03, AC-07, AC-08 |
| NFR-03 | DES-03, DES-04 | AC-01 |
| NFR-04 | DES-03, DES-05 | AC-01, AC-03, AC-04 |
| NFR-05 | DES-01, DES-02 | AC-05 |

## 적대 검토

검토자: 새 맥락 서브에이전트(general-purpose, 읽기 전용 지시, 문서 경로·검토 규칙·대조 자료만 전달). 대상: 이 문서·ADR-025·DCR-026. 1라운드 17건(높음 4·중간 5·낮음 8) 전부 수용, 근거 없는 지적 0. 2라운드: 해소 16·남음 1(8번 일부 — 18로 수정), 신규 6건(낮음 5·제안 1) 전부 작성자 수정 — 최대 2라운드라 재확인 없음.

| 번호 | 라운드 | 심각도 | 지적 | 근거 | 작성자 응답 | 최종 |
|---|---|---|---|---|---|---|
| 1 | 1 | 높음 | Edit 판정이 문자열 포함만 봐서 줄을 바꾸는 편집(주석 처리, `or True`)이 통과 — FR-01·해석과 모순 | 이전 판 FR-01·FR-03 (b)·AC-01, 해석 절 | 수용 — FR-01을 줄 단위 부분열로 정의, FR-03을 「메모리에서 편집 적용 후 같은 판정」으로 통일, AC-01에 주석·약화·쪼개기 케이스 || 해소(2라운드) |
| 2 | 1 | 높음 | 이름 변경 감지 때문에 glob 안 `git mv` + 단언 삭제가 순수 추가로 보임 — 현행보다 퇴행 | 검토자 실측, regression_guard.py:106-110, 이전 판 DES-01 | 수용 — DES-01 `--no-renames`, FR-01 삭제·이름 변경은 순수 추가 아님, AC-03 `git mv` 케이스 || 해소(2라운드) |
| 3 | 1 | 높음 | 행 ID 단위 해소가 무변경이라 한 번 기록하면 그 행의 이후 약화가 지문과 무관하게 걸러짐 — RISK-02 대응이 사실과 다름 | regression_guard.py:129-142·158, 이전 판 FR-05 (c)·FR-07 (2)·RISK-02 | 수용 — FR-05 (d) 테스트 파일 위반은 행 ID + 지문으로만 해소, FR-07 (2) 지문 기록, DES-01 `recorded()`, RISK-02·08·10, NFR-02 계약 변경 명시 || 해소(2라운드) |
| 4 | 1 | 높음 | 거절 뒤 순수 추가 편집의 PostToolUse로 `asked` 경로가 `approved`가 되어 거절 우회 | 이전 판 FR-04·DES-03·AC-02, ADR-025 이유 | 수용 — FR-04 (경로, 도구 입력 해시) 일치 시에만 승인, DES-03·04 `Get-WfToolInputHash`, AC-02 거절 케이스 || 해소(2라운드) |
| 5 | 1 | 중간 | 판정 불가 시 위반(ADR 결정 1·FR-05)과 exit 2 통과(NFR-04·DES-01)가 모순 | ADR-025:49, 이전 판 FR-05 (a)·NFR-04·DES-01, regression_guard.py:155-157 | 수용 — FR-05 (a) 파일 단위 판독 불가는 위반, (e) 스크립트 자체 오류는 exit 2 통과로 구분, ADR 결정 1 정정 || 해소(2라운드) |
| 6 | 1 | 중간 | 단언 보존 변경 허용이 주의 ④와 §2 「통과시키려고 수정·제외·삭제」 문장과 모순 | 이전 판 FR-07 (2)·DES-08, SKILL.md:46, verification-depth.md:32 | 수용 — DES-08에 주의 ④·§2 문장 개정 추가, NFR-01 순증 한도 25, AC-06 || 해소(2라운드) |
| 7 | 1 | 중간 | PostToolUse 추가로 T18·T19·T21 기대값 1→2가 필요한데 새 FR-07 (3)에 걸리고 처리 경로 없음 | run-tests.ps1:465·470·489, 이전 판 DES-06·FR-07 (3), DCR-026 검증 방법 | 수용 — FR-07 (3)에 승인된 DCR의 `Breaking` 예외(선례 T45·T46), DES-06·AC-08·DCR 검증에 명시 || 해소(2라운드) |
| 8 | 1 | 중간 | `skip` 패턴이 정상 낱말(`skips`, `-Skip 2`)에 맞고, 이 작업의 표본 줄 테스트도 반드시 걸림 | run-tests.ps1:232·360·551, 이전 판 FR-02·AC-01·03·05 | 수용 — FR-02 구문 단위 패턴으로 축소, AC-01 정상 낱말 케이스, AC-05 표본 줄은 실행 시 조합 || 남음(일부) — 실행 시 조합 규칙이 AC-05에만 → 18에서 작성자 수정 |
| 9 | 1 | 중간 | 지문이 diff 전체 해시라 순수 추가·줄 번호 이동에도 바뀌고, 문자열 동일 비교라 부분집합도 재차단 — FR-06과 불일치 | 이전 판 FR-06·DES-01·DES-05·AC-04 | 수용 — 지문을 삭제 줄·패턴 줄 내용만으로(FR-05 (c)), 억제는 키 집합 포함 판정(FR-06·DES-05·AC-04) || 해소(2라운드) |
| 10 | 1 | 낮음 | `+++` 헤더 미제외, 접두 판별 시 `--`로 시작하는 삭제 줄 오인 | 이전 판 DES-01 | 수용 — DES-01 헤더는 첫 `@@` 앞 위치로 판별 || 해소(2라운드) |
| 11 | 1 | 낮음 | 대장 `크기` 열은 `medium`·`small`이라 테스트 수 대조 근거가 아님 | docs/test-register.md 대장 표, 이전 판 RISK-01, ADR-025 | 수용 — `보호 스코프` 열의 「총 N」으로 정정(RISK-01·ADR-025) || 해소(2라운드) |
| 12 | 1 | 낮음 | `46600de`가 판독 규칙(`\|`)을 바꿨는데 NFR-02는 무변경이라 하고 정본 DES-08 갱신 대상 없음 | regression_guard.py:38-41, REQ-DESIGN-regression-guard DES-08, 이전 판 NFR-02·FR-08 | 수용 — NFR-02 정정, FR-08·DES-09·AC-07에 REQ-DESIGN-regression-guard DES-08 문구·이력 || 해소(2라운드) |
| 13 | 1 | 낮음 | NotebookEdit도 `approved` 확인을 먼저 거쳐 무출력이 될 수 있음 | 이전 판 FR-03·FR-04·DES-03 | 수용 — FR-04·DES-03 NotebookEdit·설정 파일은 기억 제외, AC-02 || 해소(2라운드) |
| 14 | 1 | 낮음 | 새 파일 생성 판정이 가드(무조건 통과)와 B층(패턴 검사)에서 다름 | 이전 판 FR-01·FR-03 (a)·FR-05 (a) | 수용 — FR-01·FR-03 새 파일도 패턴 검사, AC-01 || 해소(2라운드) |
| 15 | 1 | 낮음 | 지역 DES ID와 C층 DES ID가 섞여 추적 검증 불가 | 이전 판 FR-03·NFR-03·NFR-04·DES-07, design.md:78-86 | 수용 — 요구사항 절 머리에 용어 정의(가드·게이트·B층 판정), C층 ID는 「C층 DES-NN」으로 표기 || 해소(2라운드) |
| 16 | 1 | 낮음 | 새 가드 상태 파일도 읽고-고치고-쓰기 경합이 있는데 미기재 | 이전 판 DES-03·04·05 | 수용 — NFR-04·DES-04에 잠금 없음과 유실 시 안전 쪽 명시 || 해소(2라운드) |
| 17 | 1 | 낮음 | 경량 기록으로 해소해도 닫으면 다시 위반, SHA 갱신 절차 없음. 승인 게이트 부작용 미기재 | regression_guard.py:132-134, lightweight-path.md:35, ADR-025 결정 4 | 수용 — FR-07·AC-06 닫을 때 SHA 갱신, RISK-11 승인 게이트 부작용 || 해소(2라운드) |
| 18 | 2 | 낮음 | AC-01·AC-03 픽스처의 패턴 줄이 이 작업의 TST-01·02 테스트 소스에 리터럴로 들어가 스스로 가드 `ask`·게이트 위반이 됨 — 실행 시 조합 규칙이 AC-05에만 | AC-01, AC-03, AC-05, FR-02 | 수용 — AC-05를 「이 작업이 TST-01·02에 더하는 모든 테스트(AC-01·03·05)의 패턴 표본·픽스처 줄은 실행 시 조합」으로 확장 | 작성자 수정(재확인 없음) |
| 19 | 2 | 낮음 | DCR 영향 범위 「기존 기록은 그대로 해소에 쓰인다」가 FR-05 (d)·ADR 감수 단점과 모순 | DCR-026 영향 범위, FR-05 (d), ADR-025 결과 | 수용 — DCR 영향 범위를 「대장 축소 위반은 그대로, 테스트 파일 위반은 지문 필요」로 정정 | 작성자 수정(재확인 없음) |
| 20 | 2 | 낮음 | 지문 해소 계약 변경의 영향을 이 저장소로만 한정 — 훅은 전역이라 다른 저장소의 열린 기록도 영향 | NFR-02, RISK-08, ADR-025 결과, DCR-026 영향 범위 | 수용 — NFR-02·RISK-08·ADR·DCR에 전역 영향(행 ID만 적힌 다른 저장소 기록은 테스트 파일 위반이 키마다 세션당 1회 차단, 지문 추가로 해소, 메시지가 안내) 명시 | 작성자 수정(재확인 없음) |
| 21 | 2 | 낮음 | DCR 변경 항목 DESIGN DES-07 행이 단일 `stopKey` 비교로 남음 | DCR-026 변경 항목, DES-04·05 | 수용 — `stopKeys` 집합 포함 판정으로 정정 | 작성자 수정(재확인 없음) |
| 22 | 2 | 제안 | DCR 제안 설계 3의 정본 범위 DES-01~06에 메시지(DES-07)·기준선 반영(DES-09) 누락 가능 | DCR-026 제안 설계 3, DES-07, DES-09 | 수용 — DES-01~09로 정정 | 작성자 수정(재확인 없음) |
| 23 | 2 | 낮음 | `git diff <sha>`는 미추적 파일을 포함하지 않아 커밋 전 새 테스트 파일(패턴 포함)이 B층 판정에 안 보임 — FR-05 (a) 「커밋 + 워킹트리」와 가드 판정이 어긋남 | FR-01, FR-05 (a), DES-01, regression_guard.py:106 | 수용 — FR-05 (a)·DES-01에 `git ls-files --others --exclude-standard`의 보호 파일을 전 줄 추가로 판정(패턴 검사), AC-03 미추적 패턴 파일 케이스 | 작성자 수정(재확인 없음) |

## 승인 기록

- 2026-11-22 22:43 — 사용자가 대화형 승인 관문에서 이 문서를 기준선 v1로 **승인**. 응답: "승인합니다". Q-01~05 답 그대로(FR·DES 변경 없음). 적대 검토 2라운드 신규 6건의 작성자 수정(재확인 없음)과 8번 일부 남음의 수정을 공개한 상태로 승인. [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md)·[DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md) 동시 승인.

## 인계

- 다음 단계 또는 워크플로우: wf-implement §3.1·§3.2 — 계획 수립
- 시작 조건: 충족(승인 v1, 적대 검토 2라운드 완료)
- 입력 문서와 기준선: 이 문서, [ADR-025](./ADR-025-회귀-보호-판정-단위와-반복-억제.md), [DCR-026](./DCR-026-C층-회귀-보호-판정-완화와-선행-변경-편입.md)
- 완료된 항목: §4.1 조사, 질문 Q-01~05 답, 요구사항·AC·설계·위험·추적표, ADR-025·DCR-026 초안, §4.5, 적대 검토 2라운드, 승인(v1)
- 미완료 항목: 계획·구현·검증·통합
- 차단 요인: 없음
- 다음 행동: wf-implement 시작 조건 확인 후 plan.md 작성.

## 변경 이력

| 날짜 | 변경 | 근거 | 상태 | 작성 |
|---|---|---|---|---|
| 2026-11-22 | 최초 작성 — §4.1 조사 결과와 질문 Q-01~05 | 사용자 요청 「훅 발생 기능 조정, wf-design 시작」(2026-11-22) | → draft | Claude(작성) |
| 2026-11-22 | 질문 Q-01~05 답 반영(전부 권장안), FR-01~08·NFR-01~05, AC-01~08, DES-01~09, RISK-01~08, 추적표, ADR-025·DCR-026 초안 | 사용자 답 "전부 권장안"(2026-11-22) | draft 유지 | Claude(작성) |
| 2026-11-22 | 적대 검토 1라운드 반영 — 17건 전부 수용. FR-01~08·NFR-01~04 개정, AC-01~08 보강, DES-01·03~09 개정, RISK-01·02·06·08 개정, RISK-10·11 신설, 추적표 | 적대 검토 1라운드 | draft 유지 | Claude(작성) |
| 2026-11-22 | 적대 검토 2라운드 — 판정 기록(해소 16, 8번 일부 남음), 신규 6건 작성자 수정(FR-05 (a)·DES-01 미추적 파일, AC-03·05, NFR-02·RISK-08 전역 영향) | 적대 검토 2라운드 | draft → awaiting-approval | Claude(작성) |
| 2026-11-22 | 사용자 승인 — 기준선 v1, ADR-025·DCR-026 동시 승인 | 사용자 응답 "승인합니다" | awaiting-approval → approved | 사용자(승인) |

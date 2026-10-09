# WORK-20261009-skill-diet: 작업 기록 — 스킬 다이어트·정리

> 문서 유형: `work-log, verification, completion`
> 작업 ID: `20261009-skill-diet`
> 상태: `completed`
> 기준선: `v1` — [REQ-DESIGN-skill-diet](./req-design.md) 승인일 2026-10-09
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [ST-llm-workflow](../../status.md), [REQ-DESIGN-skill-diet](./req-design.md), [ADR-010](./ADR-010-스킬-문서-계층-규칙.md), [ADR-011](./ADR-011-wf-tree-축소.md), [WORK-20261009-test-lifecycle](../20261009-test-lifecycle/work-log.md), [조사 결과 적용 분석](../../research/20261009-research-application/application_analysis.md)

## 요약

- 목적: 사이클 4(분석 §5 후보 B) — 스킬 본문의 세부를 references·scripts로 내리고, 경고 절과 스킬 린트를 두고, wf-tree를 축소하는 wf-design·wf-implement 진행을 기록한다.
- 현재 결론 또는 상태: 완료(2026-10-09 20:19) — TASK-01~09 전부, AC-01~12 12/12. 본문 합 10,446 → 8,665어절(−17%), 린트 2종 0 오류, TST-01 22 · TST-02 49 · TST-05 13 통과. 커밋 `a38ed25` 푸시, 대장 SHA 갱신 완료.
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | related | [ST-llm-workflow](../../status.md) | 작업 목록 | 이 작업의 행 |
| input | related | [WORK-20261009-test-lifecycle](../20261009-test-lifecycle/work-log.md) | 후속 작업 | 선행 사이클 3(완료·동결, 역방향 링크 없음) |
| input | baseline | [REQ-DESIGN-skill-diet](./req-design.md) | document | 기준선 v1(2026-10-09). FR-01~11, AC-01~12 |
| input | plan | [PLAN-20261009-skill-diet](./plan.md) | TASK-01~09 | 진행 상태의 정본 |
| output | decision | [ADR-010](./ADR-010-스킬-문서-계층-규칙.md), [ADR-011](./ADR-011-wf-tree-축소.md) | document | `approved`(2026-10-09). 등록부 행 |
| input | related | [조사 결과 적용 분석](../../research/20261009-research-application/application_analysis.md) | §5, §6 | 사이클 편성 입력(불변 기록, 역방향 링크 없음) |
| output | related | [REGISTER-llm-workflow](../../test-register.md) | TST-04, TST-05 | 이 작업이 등록한 행. TST-02 비고 갱신 |

## 기준선과 현재 계획

- 기준선: [REQ-DESIGN-skill-diet](./req-design.md) v1(2026-10-09), [ADR-010](./ADR-010-스킬-문서-계층-규칙.md)·[ADR-011](./ADR-011-wf-tree-축소.md)
- 계획: [PLAN-20261009-skill-diet](./plan.md)(completed)

## 수행 기록

### 2026-10-09 — 착수와 wf-design §4.1~4.5

- 발견 사항: 분석 §6의 round1 재확인 — S12 근거는 LoopsBench 의존 간선 F1 0.71, S6·S10은 묶음 A, S15 보류 유지. 이관 후보 실측: wf-implement 373·wf-doc ≈1,050·wf-tree ≈930어절. 들어오는 앵커 38종. junction은 스킬 폴더별이라 `skills/scripts/`는 설치 불가.
- 결정과 이유: 본문 상한을 분석 제안이 아니라 실측 기반(2,850/2,350/1,200/2,300)으로 — 2,400은 R1 문장을 깎아야 해 의미 불변과 충돌(Q-01). 경계표는 R3로 references(Q-02). 분기 템플릿 비게이트 7행은 삭제(Q-04). ADR-010·011 발행.
- 검증: 어절·절 단위 측정 스크립트(`PYTHONIOENCODING=utf-8`), 앵커 grep 전수, 린트 `python skills/wf-doc/scripts/lint_worklog.py` 0 오류 — `0962f3c` + 미커밋.
- 결과: 완료 — 2026-10-09 19:40

### 2026-10-09 — 승인과 계획 수립

- 발견 사항: §3.1 재확인 — HEAD `0962f3c`, 대장 `유지` 행 SHA `7395a99` ≠ HEAD라 전량 재실행 TST-01 22/22·TST-02 33/33. 타인 미커밋 변경 없음.
- 결정과 이유: TASK 9개, references → 본문 → 스크립트(TDD) → 통합 순 — 트리거 링크 대상이 먼저 있어야 하고 린트 K7은 본문 4개가 끝나야 통과. 트리는 현행 규칙으로 손 렌더 1회, TASK-09에서 render.py로 재생성(FR-10).
- 검증: 린트 `python skills/wf-doc/scripts/lint_worklog.py` 0 오류 — `0962f3c` + 미커밋.
- 결과: 완료 — 2026-10-09 19:42

### 2026-10-09 — TASK-01

- 결정과 이유: 경계표 2개는 `boundaries.md` 한 파일에, 머리말·식별자 목록·추적표·인계 블록은 `templates.md`의 새 절 4개에 — 골격은 템플릿 파일이 정본이라 흩어 두지 않음. 하이퍼링크 세부 7개와 표 어휘는 `linking.md`.
- 검증: `python -m pytest skills/wf-doc/scripts/tests -q` 33 passed, `wc -l` 36·21행 — `0962f3c`+dirty.
- 결과: 완료 — 2026-10-09 19:44

### 2026-10-09 — TASK-02

- 발견 사항: 1차 재배치 후 2,454어절로 상한(2,350) 초과 — 설계의 추정(≈2,290)이 콜아웃·트리거 분량을 낮게 봄. 사라진 행 28건 중 references에 없는 것은 경로 조정된 표 행·합쳐 쓴 문장뿐.
- 결정과 이유: 상한 충족을 위해 §2.3 날짜·작업 ID 형식 노트 2개, 완료 문서의 `다음 행동` 노트, §2.5 정보 표지 코드블록을 templates.md로 추가 이동하고 상태 구분 불릿 2개를 합침 — 전부 형식 세칙(R2)이라 §4.1 경미 변경. 예시용 자리표시자 링크(`<작업-ID>`, `경로`)는 린트 K4가 건너뛰어야 함(TASK-08 메모).
- 검증: 어절 2,337 ≤ 2,350, 가드 39 ≥ 35, pytest 33 passed, wf-doc 링크 118건 중 깨짐 0(자리표시자 2건 제외) — `0962f3c`+dirty.
- 결과: 완료 — 2026-10-09 19:46

### 2026-10-09 — TASK-03

- 발견 사항: §3.5 문항은 실제 19개(조사 절의 "20문항"은 끝 문장 "리뷰에서 발견한 문제는 수정…"을 포함해 센 값). 경계표 "12행"은 머리·구분선 포함 표 줄 수이며 데이터 행은 10개. 이동 10행 + 19문항 / 삭제 0.
- 결정과 이유: 표 링크는 references 위치에 맞춰 상대 경로만 조정(`../SKILL.md#…`, `../../wf-design/…`). review-checklist.md의 "결정 사다리(2.4)"·"냄새 체크리스트"에 본문 §2.4·verification-depth §4 링크를 붙임 — 파일이 단독으로 읽히므로 참조 대상이 필요(형식 추가, 의미 불변). 정본 콜아웃은 "이 절" → "이 표"로만 바꿔 이동.
- 검증: 원문 표 행 10·문항 19 전부 grep 일치, `wc -l` 18·34행 ≤ 120 — `0962f3c`+dirty.
- 결과: 완료 — 2026-10-09 19:52

### 2026-10-09 — TASK-04

- 발견 사항: 1차 재배치 후 2,854어절로 상한 4어절 초과 — 초과분은 신설 트리거의 영역 열거. 들어오는 앵커 20종 중 미존재 `#37-자문-요청-crp`는 연구 초안의 미래 절 참조(HEAD에도 없음)라 무관.
- 결정과 이유: 트리거에서 영역 열거 삭제(표가 보여 줌). 경계 규칙 6항·§2.3 끝 문장은 가드 어미를 유지한 채 정본(주의 절 ①) 링크만 붙임. 주의 절 ②③④는 원문 가드를 지우지 않는 절 링크 요약 — 가드 문구는 이관 금지(ADR-010 R1).
- 검증: 어절 2,840 ≤ 2,850, 가드 26 ≥ 24, 절 번호·H2/H3 제목 불변(주의 절만 추가), 나가는 링크 3파일 깨짐 0, 들어오는 앵커 전수 유효 — `0962f3c`+dirty.
- 결과: 완료 — 2026-10-09 19:54

### 2026-10-09 — TASK-05

- 발견 사항: wf-design §6.2 결정 등록부 예시 행의 링크(`./work/20260809-session-store/ADR-001-…`)는 존재하지 않는 예시 경로 — 기준선에도 있던 것. lint_skill K4가 예시·자리표시자 링크를 구분해야 함(TASK-08 메모, TASK-02 메모와 같은 부류).
- 결정과 이유: 경계 규칙 5항은 `대신하지 않는다` 가드를 남기고 정본 링크를 붙임. 주의 절 ①은 정본 링크, ②③은 §8·§1 원문을 남긴 절 링크 요약(TASK-04와 같은 방식). 콜아웃 2곳의 표 링크를 wf-doc·wf-implement `references/boundaries.md`로.
- 검증: 어절 2,288 ≤ 2,300(순증 27 ≤ 40), 가드 19 ≥ 18, 나가는 링크 깨짐 0(예시 행 1건 제외) — `0962f3c`+dirty.
- 결과: 완료 — 2026-10-09 19:55

### 2026-10-09 — TASK-06

- 발견 사항: §7 "깊이를 제한하지 않는 대신" 문구는 ADR-011 깊이 상한과 모순이라 rendering.md에서 "깊이 상한 안에서도"로 고침. 테스트 fixture 2건이 `## 작업 목록` 밖에 TASK를 붙여 파싱되지 않던 것을 교정. write 교체가 절 길이를 변경 후에 재던 결함을 Red에서 발견·수정.
- 결정과 이유: render.py는 lint_worklog 헬퍼를 import하지 않고 자체 파서(약 30행)를 둠 — 스킬 폴더별 junction이라 wf-tree 단독 설치 시 wf-doc 경로를 보장할 수 없음(RISK-06과 같은 결합 회피). 상태 문구·롤업·depends·완료 시점 순서는 rendering.md에 먼저 적고 그 표기로 골든 작성(RISK-03).
- 검증: Red — 수집 오류(모듈 없음)로 13건 전부 실패 → Green 13 passed(계획 12 + exit 코드 1). 실제 plan.md·status.md 렌더 확인, 깊이 3 입력에 W 경고·exit 0. references 57·51행 — `0962f3c`+dirty.
- 결과: 완료 — 2026-10-09 20:05

### 2026-10-09 — TASK-07

- 발견 사항: 이동 — 예시 트리·유형 표 15행·§7 표기·완료 시점·대형 트리 4항·§9 문항 9개(references 2파일). 삭제 — 분기 템플릿 비게이트 7행(목록은 ADR-011), 매체 표 2행은 한 문장으로 합침. 어절 1,200으로 상한과 같음(여유 0).
- 결정과 이유: 헌장 경계 규칙 2항·목적·description의 "분기 템플릿 제안"을 "필수 게이트의 누락을 막는다"로 — 제안 기능이 사라졌으므로 유지하면 거짓 문장. 주의 절 ①은 ASCII에 화살표가 없어 "`depends:`는 기다리는 쪽에 적는다(UML과 반대)"로 표현. §4 표의 **필수 게이트** 굵은 표기는 제목이 이미 필수 게이트라 생략.
- 검증: 어절 1,200 ≤ 1,200, 가드 20 ≥ 20, 절 번호·앵커 5종 유지, 나가는 링크 3파일 깨짐 0, description에 "분기 템플릿" 0회 — `0962f3c`+dirty.
- 결과: 완료 — 2026-10-09 20:06

### 2026-10-09 — TASK-08

- 발견 사항: 실제 4스킬 린트 경고 6 — K3 95% 초과 4건(상한이 실측 기반이라 설계상 예정된 경고), K6 wf-doc §2.1 유형표 26행(R1 공유 어휘, 이관 금지 목록)·wf-tree 헌장 표. 예시·자리표시자 링크는 전부 펜스 안이라 K4가 `outside_fences`로 자연히 건너뜀(TASK-02·05 메모 해소).
- 결정과 이유: import는 `Finding`·`anchors_of`·`headings`·`outside_fences`·`read_lines` 5개로 한정(RISK-06). K6 표 행은 펜스 밖 연속 `|` 행 묶음으로 셈. README에 계층 규칙 1문단(ADR-010 포인터·린트 명령·render.py)과 wf-tree 행 문구 갱신.
- 검증: Red — 수집 오류로 16건 전부 실패 → Green 16 passed(K1~K7 쌍 14 + 탐색 + exit). 폴더 전체 49 passed(기존 33 무변경). `lint_skill.py` 인자 없음 exit 0 — `0962f3c`+dirty.
- 결과: 완료 — 2026-10-09 20:09

### 2026-10-09 — TASK-09

- 발견 사항: K6가 떨어진 표 둘을 합쳐 셈(wf-tree 5+5행) — 실제 실행에서 발견, 회귀 테스트 후 수정. PLAN_TREE_TASKS.md의 앵커 1건은 기준선 이전부터 깨진 기존 문제(범위 밖). 수행 기록의 완료 시점이 실제 시계보다 앞서 적혀 있어(추정 기입) 파일 수정 시각으로 전부 교정.
- 결정과 이유: 재정비 관문 변경 없음 — `lint_worklog.py` 무변경(Breaking 0), 새 동작은 TST-04·05가 보호(Missing 0). TST-02 명령은 그대로 두고 비고에 49건 합류를 적음. `유지` 행 SHA는 선례대로 미커밋 상태로 기록, 커밋 후 갱신은 후속 작업.
- 검증: AC-01~12 12/12([검증 결과](#검증-결과)), review-checklist.md 전 항목 확인, 트리 `render.py --write --view all` 재생성 — `0962f3c`+dirty.
- 결과: 완료 — 2026-10-09 20:19

## 설계와 달라진 점

- TASK-03(§4.1 경미): review-checklist.md의 "결정 사다리(2.4)"·"냄새 체크리스트"에 링크 추가(단독 파일이라 참조 대상 필요). §3.5 문항은 19개 — AC-01의 "20문항"은 조사 오산(끝 문장 포함)이며 문항 전부 이동으로 판정.
- TASK-06(추가): node-templates.md 유형 표 `migrate` 행에 ★ 추가 — 본문 "★ 게이트 유형은 approve·release·migrate"와 일치.
- TASK-07(§4.1 경미): 헌장 경계 규칙 2항·목적 문장·description을 게이트 중심으로 고침(분기 템플릿 제안 기능 삭제의 귀결, ADR-011 ⑥ 확장). 매체 표 2행 → 한 문장. 주의 절 ①을 ASCII 표기에 맞게 표현.
- TASK-06(§4.1 경미): rendering.md 접기 절 첫 문장 "깊이를 제한하지 않는 대신" → "깊이 상한 안에서도"(ADR-011 ④의 귀결). render.py는 헬퍼 import 대신 자체 파서(설치 독립성). pytest 13(계획 12 + exit 코드).
- TASK-04(§4.1 경미): 주의 절 ②③④는 원문 이동이 아니라 원문을 남긴 채 절 링크를 단 요약(가드 문구 이관 금지와 양립). review-checklist.md의 두 참조(결정 사다리·냄새 체크리스트)에 링크 추가. 이유: 의미 불변·가드 수 유지.
- TASK-02(§4.1 경미): DES-03 목록 외에 §2.3 형식 노트 2개·완료 문서 `다음 행동` 노트·§2.5 정보 표지 코드블록을 `templates.md`(공통 머리말 노트, 신설 `## 정보 표지`)로 추가 이동. 상태 구분 불릿 2개 합침. 이유: 상한 2,350 충족, 전부 표현 세칙이라 의미 불변.

## 검증 결과

### 범위와 환경

- 대상 기준선 또는 구현: REQ-DESIGN-skill-diet v1 — TASK-01~09 구현, 워킹트리 `0962f3c`+미커밋
- 실행 환경: Windows 11, PowerShell 5.1, Python 3.13.1, pytest 9.1.1
- 제외 항목: TST-03(격리, 환경 원인 — 이 작업과 무관). 참조 준수율·토큰 효과(범위 밖, RISK-07)

### 결과 요약

- 총계: 12 (성공 12 / 실패 0 / 미수행 0) — 인수 조건 AC-01~12. 자동 테스트 TST-01 22/22 · TST-02 49/49 · TST-05 13/13
- 기준: `0962f3c` · 워킹트리 dirty(이 작업의 변경만)
- 명령: 묶음마다 1줄
  - `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1`(TST-01)
  - `python -m pytest skills/wf-doc/scripts/tests -q`(TST-02, TST-04 포함) · `python -m pytest skills/wf-tree/scripts/tests -q`(TST-05)
  - `python skills/wf-doc/scripts/lint_skill.py` · `python skills/wf-doc/scripts/lint_worklog.py`
  - 어절·가드 측정 스크립트(조사 절 함수, `PYTHONIOENCODING=utf-8`) · 링크 전수 검사 스크립트(69파일)
- 커버리지: N/A — pytest-cov 미설치, 변경의 대부분이 산문
- 산출물: 없음

### 인수 조건별 결과

| 검증 ID | 인수 조건 | 방법·명령 | 결과 | 분류 | 증거 |
|---|---|---|---|---|---|
| VER-01 | AC-01 | 통독·grep, 앵커 스크립트 | 성공 | — | boundaries.md 표 10행+콜아웃, review-checklist 19문항("20"은 조사 오산), 경계 절 표 0·규칙 6항·트리거, §3.5 트리거. wf-implement 들어오는 앵커 17종 유효 — `0962f3c`+dirty |
| VER-02 | AC-02 | 통독·grep, `git diff` | 성공 | — | references 3파일, 본문 코드 펜스 0, 핵심 5규칙·트리거. templates.md diff에 H2 삭제 없음(합본 H2 8개 유지), `lint_worklog.py` 무변경 — `0962f3c`+dirty |
| VER-03 | AC-03 | 통독·grep | 성공 | — | §3 표 0·게이트 3종 문장, §4 3행, §2 깊이 상한, §7 트리거·손 렌더 규정, §9 트리거, references 2파일, description "분기 템플릿" 0회 — `0962f3c`+dirty |
| VER-04 | AC-04 | `python -m pytest skills/wf-tree/scripts/tests -q`, `python skills/wf-tree/scripts/render.py docs/work/20261009-skill-diet/plan.md [--write]` | 성공 | — | 13 passed; TASK-01~09 전부 표시·depends·완료 시점; `--write`로 이 plan.md 트리 교체; 깊이 3 입력에 `W 깊이 상한 초과` exit 0 — `0962f3c`+dirty |
| VER-05 | AC-05 | grep | 성공 | — | wf-implement §3.2 "`depends:` 후보" 1회, node-templates.md 자체 검토 같은 문항 1회 — `0962f3c`+dirty |
| VER-06 | AC-06 | 통독·grep | 성공 | — | 4스킬 `## 주의 — 자주 틀리는 것`이 경계 절 바로 뒤(H2 #3·#3·#2·#2), 내용 DES-07. "실행 승인" 정본 wf-implement 주의 ① 1곳, 나머지 4곳은 링크 — `0962f3c`+dirty |
| VER-07 | AC-07 | `python skills/wf-doc/scripts/lint_skill.py`, `python -m pytest skills/wf-doc/scripts/tests -q` | 성공 | — | 인자 없음 4파일 exit 0(경고 6: K3 95% 4·K6 wf-doc R1 표 2); lint_skill pytest 16 passed(폴더 49); README 실행 기준 문단 — `0962f3c`+dirty |
| VER-08 | AC-08 | 어절·가드 측정 스크립트(`PYTHONIOENCODING=utf-8`) | 성공 | — | wf-implement 2,840/26 · wf-doc 2,337/38 · wf-tree 1,200/20 · wf-design 2,288/19(어절/가드) — 상한·가드 전부 충족, 합 8,665 ≤ 8,700 — `0962f3c`+dirty |
| VER-09 | AC-09 | HEAD 대비 사라진 행 대조 스크립트 | 성공 | — | references에 없는 행은 ADR-011 삭제 7행, 정본 요약 3문장(설계와 달라진 점), 경로·링크만 바뀐 행, 합쳐 쓴 문장만 — `0962f3c`+dirty |
| VER-10 | AC-10 | K4·L6·전수 링크 스크립트, `git diff --stat docs/work` | 성공 | — | K4 0·L6 0, 69파일 깨짐 0(기존 planning 문서 1건·디렉터리 링크 3건 제외), 완료 기록·선행 ADR·DCR diff 없음 — `0962f3c`+dirty |
| VER-11 | AC-11 | TST-01·02·05 명령, 대장 확인 | 성공 | — | 22/22 · 49/49(기존 33 포함) · 13/13. 대장 TST-04·05 `유지`, SHA `0962f3c`(+미커밋) — 20:13 |
| VER-12 | AC-12 | grep, `wc -l` | 성공 | — | decisions.md ADR-010·011 `approved`. 신설 references 36·21·18·34·57·51행 ≤ 120 — `0962f3c`+dirty |

### 실패와 미수행 분석

없음.

### 테스트 대장 변경

- 등록: TST-04(`python -m pytest skills/wf-doc/scripts/tests/test_lint_skill.py -q`, 16) · TST-05(`python -m pytest skills/wf-tree/scripts/tests -q`, 13) `유지` — 같은 SHA 2회 통과(Green + `completed` 전이 + 통합 재확인).
- 재정비 관문(통합): Breaking 0 · Stale 0 · Missing 0 — 폐기·병합 후보 0. TST-02 명령 불변, 비고에 49건 합류 기록. 대장과 재정비 기록에 반영됨.

## 완료 보고

### 완료 상태

- 결과: 완료
- 완료 판단 근거: TASK-01~09 `completed`, AC-01~12 12/12, 린트 2종 0 오류, TST-01·02·05 통과, 자체 리뷰 전 항목 확인(발견 결함 K6 수정·재검증). wf-implement §5 조건 전부 충족

### 주요 변경

- 스킬 본문 4종 재배치: 합 10,446 → 8,665어절(−17%), 가드 수 비감소. 경계 소유권 표 3개·§3.5 문항·wf-doc 코드블록·하이퍼링크 세부·wf-tree 유형 표·렌더 세칙·자체 검토를 references(신설 6파일)로 이동, 각 자리에 트리거 문장
- 4스킬에 `## 주의 — 자주 틀리는 것` 신설, "설계 승인은 실행 승인이 아니다" 정본 1곳(wf-implement)
- wf-tree 축소: 필수 게이트 3종만, 깊이 상한 2, `scripts/render.py`(pytest 13), 비게이트 분기 템플릿 7행 삭제(ADR-011)
- `skills/wf-doc/scripts/lint_skill.py`(K1~K7, pytest 16), README 실행 기준에 계층 규칙·린트·render 문단

### 통합 상태

- 커밋 `a38ed25`(조사 분석은 `6026739`)로 `origin/main`에 푸시(2026-10-09, 사용자 요청). `유지` 행 4개를 clean 커밋에서 재실행(20:27, 22/22·49/49·16/16·13/13)해 대장 SHA 갱신

### 남은 위험과 제한

- 본문이 상한에 0~14어절 여유로 붙어 있어 K3 95% 경고가 상시 발생한다 — 상한은 성장 감시용, 묶음 A·C가 문장을 더하면 경량 경로로 상한 조정(ADR-010)
- references 참조 준수율·토큰 효과는 이 저장소에서 관측 불가(RISK-07)
- `docs/planning/PLAN_TREE_TASKS.md`의 `templates.md#포트폴리오-portfolio` 앵커는 기준선 이전부터 깨져 있음(반영됨 문서, 범위 밖)
- 이 작업 기록은 L9 크기 경고(>12KB) 상태 — 검증 표 12행이 원인, 오류 아님

### 후속 작업

- (완료) `유지` 행 4개 clean 재실행과 대장 SHA 갱신 — `a38ed25`, 20:27
- 참조 준수율 측정과 롤백 판단 — 분석 §5 후보 D(코드 저장소 사이클)
- 린트 2종의 Stop 훅 게이트 집행 — 묶음 A
- render.py 활성 경로 뷰를 `resume.md` 훅에 주입할지 — 묶음 A(ADR-011 후속)

## 인계

- 다음 단계 또는 워크플로우: 없음
- 완료된 항목: TASK-01~09, AC-01~12, ADR-010·011 적용, TST-04·05 등록
- 미완료 항목: 없음
- 다음 행동: 없음

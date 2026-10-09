# WORK-20261009-plan-relocation: 작업 기록 — 계획 문서 재배치

> 문서 유형: `work-log, verification, completion`
> 작업 ID: `20261009-plan-relocation`
> 상태: `completed`
> 기준선: `v1` ([REQ-DESIGN-plan-relocation](./req-design.md), 2026-10-09 승인)
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [REQ-DESIGN-plan-relocation: 요구사항·설계](./req-design.md), [PLAN-20261009-plan-relocation: 구현 계획](./plan.md), [ADR-004: TASK 식별자의 작업 범위 발행](./ADR-004-TASK-식별자-작업-범위.md), [wf-tree 존치 판정(조사)](../../research/20260919-aidlc-research/wf-tree_verdict.md)

## 요약

- 목적: 사이클 1 "계획 문서 재배치"(요구 1·2·3)의 wf-design 진행 상태와 재개 지점을 기록한다.
- 현재 결론 또는 상태: **완료**(2026-10-09 14:08) — TASK-01~07 완료, AC-01~09 전 항목 성공, 로컬 작업 사본에 통합(미커밋). 상세는 [완료 보고](#완료-보고).
- 다음 행동: [인계](#인계) 절의 "다음 행동".

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-plan-relocation](./req-design.md) | FR-01~10, AC-01~09, DES-01~10 | 기준선 v1(2026-10-09) |
| input | implementation | [PLAN-20261009-plan-relocation: 구현 계획](./plan.md) | TASK-01~07, VER-01~09 | 이 작업의 계획(자기 적용) |
| input | decision | [ADR-004: TASK 식별자의 작업 범위 발행](./ADR-004-TASK-식별자-작업-범위.md) | document | approved(2026-10-09) |
| input | related | [wf-tree 존치 판정](../../research/20260919-aidlc-research/wf-tree_verdict.md) | §0, §3 | 조사 입력 |
| input | related | [WORK-20260814-multiuser-workflow](../20260814-multiuser-workflow/work-log.md) | Q-04 | 보류된 다인 토론. 이 작업이 plan.md 구조를 1인용 관점에서 먼저 결정 |

## 기준선과 현재 계획

- 기준선: [REQ-DESIGN-plan-relocation v1](./req-design.md)(2026-10-09 승인), [ADR-004](./ADR-004-TASK-식별자-작업-범위.md)
- 계획: [PLAN-20261009-plan-relocation](./plan.md) — TASK-01~07, 트리 사용(최초 작성 시 1회 생성). 진행 상태는 계획의 작업 목록이 정본

## 현재 상태

- 진행 중인 작업: 없음
- 마지막 완료 작업: TASK-07 검증·자체 리뷰·통합(2026-10-09 14:08)
- 차단 요인: 없음

## 수행 기록

### 2026-10-09 — 사이클 편성과 wf-design 착수

- 수행 내용: 사용자 요구 8개를 조사 기록과 대조해 사이클 3개로 편성(1: 계획 문서 재배치, 2: 작업 기록 다이어트·아카이빙·린트, 3: 검증 기록과 테스트 수명주기). 사용자 승인. 사이클 1을 wf-design으로 착수. 현재 상태 조사(변경 대상 절, plan.md 참조 10곳, 훅 의존성 없음, 스냅숏 실측 1.5KB) 수행 후 요구·설계 초안 작성.
- 변경 파일: `docs/work/20261009-plan-relocation/req-design.md`(신설), 이 파일(신설)
- 발견 사항: 훅·설정은 plan.md를 읽지 않는다. 조사 기록의 스냅숏 비용 "8~9KB"는 과장(실측 약 1.5KB). main의 다음 ADR 번호는 004이며 보관 브랜치의 ADR-004와 번호가 겹친다.
- 결정과 이유: 산출물은 작업 폴더의 통합 req-design 문서(선례 따름). TASK 번호 범위·plan.md 처리·생성 시점·ADR-003 관계·분기 템플릿 범위는 사용자 결정으로 남김(Q-01~Q-05).
- 실행한 검증: 없음(문서 초안 단계)
- 결과: 초안 완료, 승인 전

같은 세션의 부수 작업(이 작업 범위 밖): 원격 9월 커밋 3개를 `archive/202609-cycles`로 이관하고 main을 c4cde3f 위에서 재시작(커밋 dbbb68b). 조사 산출물 15편을 `docs/research/20260919-aidlc-research/`로 보존. 테스트 조사 정리 `docs/research/20261009-test-lifecycle/testing_research_digest.md` 작성(미커밋). `20260814-multiuser-workflow`를 `on-hold`로 전환(미커밋).

### 2026-10-09 — Q-01~Q-05 결정, 요구·설계 확정, 승인 요청 (재개 세션)

- 수행 내용: 인계 절에 따라 ADR-003 본문을 읽고 Q-04 권장안(부분 수정)을 정한 뒤 Q-01~Q-05를 권장안과 함께 사용자에게 제시. 사용자가 다섯 항목 모두 권장안을 선택. 결정을 req-design에 반영해 요구사항(FR-01~10, NFR-01~03)·인수 조건(AC-01~09)·설계(DES-01~10)·위험(RISK-01~04)·추적표(FR→DES→AC)를 확정. ADR-004 초안을 `proposed`로 작성하고 `docs/decisions.md`에 등록. wf-design §4.5 일관성 검토 수행 후 req-design을 `awaiting-approval`로 올리고 승인 관문에 요청.
- 변경 파일: [req-design.md](./req-design.md)(확정, `awaiting-approval`), [ADR-004](./ADR-004-TASK-식별자-작업-범위.md)(신설, `proposed`), `docs/decisions.md`(ADR-004 행 추가), 이 파일
- 발견 사항: ADR-003의 결정은 트리거 배치(wf-implement §3.2 단일 관문)이며 이번 작업은 관문에서 하는 일(재생성 → 온디맨드)과 ADR-003이 안전망으로 지목한 완료 조건만 바꾼다. 따라서 대체가 아닌 부분 수정(DES-09).
- 결정과 이유: Q-01 작업 범위 TASK 번호(ADR-004) — plan이 작업 폴더로 내려가면 전역 번호의 근거 문서가 사라짐. Q-02 status.md 대체 — wf-doc에 status 유형이 이미 있음. Q-03 인계 시 뷰 미포함 — 인계 절 "다음 행동"이 같은 역할. Q-04 부분 수정 — 배치 결정은 불변. Q-05 제외 — 요구 1~3 범위 밖.
- 실행한 검증: §4.5 체크리스트(핵심 요구사항 전부 DES에 연결, AC 전부 검증 방법 있음, 범위 밖 항목 제외 절에 명시, 실패·복구는 git revert, 호환성 영향은 NFR-02와 동결 스냅숏 가정). 새 문서 2개와 decisions.md의 상대 링크 존재 검사 — 깨진 링크 0건(백틱 안 예시 문자열 2건은 링크가 아님).
- 결과: 승인 요청 상태 → 같은 세션에서 사용자 "승인". req-design `approved`·v1, ADR-004 `approved`, decisions.md 갱신

### 2026-10-09 — 계획 수립 (wf-implement §3.1·3.2)

- 수행 내용: §3.1 재확인 — 스킬 설치본(`~/.claude/skills/wf-*`)은 저장소 `skills/`로의 심볼릭 링크라 편집이 즉시 적용됨. 기준선 이후 저장소 변경은 이 작업 폴더·`docs/decisions.md`뿐. 미커밋 변경(조사 정리, 다인 토론 보류 전환, `docs/paper/`)은 이 작업과 무관하며 보존. [plan.md](./plan.md)를 새 규칙으로 작성(FR-09 자기 적용): 작업 폴더, `PLAN-<작업-ID>`, TASK-01~07, ASCII 트리 1회 생성(생성 일시 표기), 스냅숏 없음.
- 변경 파일: `plan.md`(신설), 이 파일
- 발견 사항: 완료 문서 14개와 `docs/requirements.md`·`design.md`가 `docs/plan.md`를 링크한다. TASK-05에서 링크 수리 범위를 정한다. wf-tree 어절 측정: `wc -w` 2,268(파일 전체), 본문 `split()` 1,992, description 405자(Python `len`). 기준선 조사의 "2,077어절·913자"와 방법이 달라 변경 전·후를 같은 명령으로 측정한다(VER-08).
- 결정과 이유: TDD 사이클은 적용 불가(Markdown 규칙 문서, 자동 테스트 체계 없음) → wf-implement §3.3 규정에 따라 TASK-07의 후행 검증으로 대체. 작업 7개·의존 있음 → 트리 사용.
- 실행한 검증: 없음(계획 단계)
- 결과: 계획 수립 완료, TASK-01 착수

### 2026-10-09 — TASK-01 wf-tree 축소와 온디맨드 생성 시점

- 수행 내용: description·§1 트리거 문구를 "최초 작성 1회, 이후 요청 시"로. §5 단일 소스 원칙을 생성 일시 표시(`<!-- generated: YYYY-MM-DD HH:MM -->`)와 "트리는 목록보다 오래될 수 있음"으로 고치고 완료 스냅숏 예외 문단을 동결 기록 한 줄로 대체. §5 저장 위치: 포트폴리오는 진행 중 작업만(행 추가·제거는 wf-implement §7 소유), 작업 트리는 `docs/work/<작업-ID>/plan.md`. §7 매체 표 2종(Mermaid 행·표기 규칙·색상표·예시 다이어그램 삭제, ASCII 표기 한 문단으로 통합), §갱신 시점 → §생성 시점(최초 1회·요청 시, 상태 갱신은 목록만), 대형 트리 대응 3항(Mermaid 분할) 삭제. §8 이후 갱신 문구, §9 체크리스트(생성 일시 항목으로 교체, 노드 30 분할 항목 삭제).
- 변경 파일: `skills/wf-tree/SKILL.md`
- 발견 사항: 본문 어절 1,992 → 1,844, description 405 → 409자(Python `len`, 같은 방법). 남은 "Mermaid"·"snapshot" 언급 2곳은 금지·동결 기록 설명(역사 언급)이며 규정이 아니다.
- 결정과 이유: DES-08은 §9의 `generated` 표시 항목 삭제를 말하지만 DES-02가 생성 일시 표시를 요구하므로 삭제 대신 "생성 일시가 있는가"로 교체했다(wf-implement §4.1 경미한 변경 — 설계를 더 명확히 하는 보완).
- 실행한 검증: `grep -n -i "mermaid|snapshot|스냅숏|갱신될 때마다|재생성"` — 규정 0건, 역사 언급 2건, 생성 시점 참조 3건. 정밀 판정은 TASK-07.
- 결과: 완료(2026-10-09 13:58)

### 2026-10-09 — TASK-02·03·04 wf-implement·wf-doc·wf-design

- 수행 내용: **TASK-02** wf-implement §3.2 마지막 문장을 "진행 상태 갱신은 작업 목록만, 트리는 wf-tree 생성 시점에만"으로(단일 관문 §3.2의 채택 기준·최초 생성 문구는 그대로 — ADR-003 배치 유지). §5 완료 조건의 트리 동기화·스냅숏 2항 삭제. §7 첫 문단·파일 레이아웃을 `docs/status.md` + `docs/work/<작업-ID>/plan.md·work-log.md`로, 완료 사이클 축약·스냅숏 항목을 "포트폴리오 행의 추가·제거"(DES-05 시점 규칙)와 "계획 파일의 수명" 2항으로 대체. **TASK-03** wf-doc SKILL §2.6 문서 ID `PLAN-<작업-ID>`, TASK·VER 작업 범위 규칙 1항(ADR-004), 추적표 예시 경로. templates.md: 필수 연결표 `plan` 행, plan 템플릿 문서 ID·저장 위치·generated 노트(생성 시점 링크)·축약형 노트 삭제, work-log 스냅숏 노트 삭제, status 저장 위치 문구·작업 목록 열(`완료` → `계획·기록`·`다음 행동`)·노트. **TASK-04** wf-design §6 한 문장.
- 변경 파일: `skills/wf-implement/SKILL.md`, `skills/wf-doc/SKILL.md`, `skills/wf-doc/references/templates.md`, `skills/wf-design/SKILL.md`, `skills/wf-tree/SKILL.md`(완료 시점 원천 문구 1곳 — status `완료` 열 삭제의 연쇄)
- 발견 사항: status 템플릿의 `완료` 열은 진행 중 작업만 싣는 포트폴리오에서 항상 공란이므로 삭제하고, wf-tree 완료 시점 표기의 원천을 plan `완료:` 필드만으로 좁혔다.
- 결정과 이유: `완료` 열 삭제와 `계획·기록`·`다음 행동` 열 추가는 DES-05(작업 ID·상태·plan/work-log 링크·다음 행동)의 번역이다. 스킬에서 docs/의 ADR-004를 링크하지 않고 규칙만 적었다 — 스킬 본문은 저장소 밖 설치를 전제로 이식성을 유지한다(README "실행 기준").
- 실행한 검증: 편집 후 grep — wf-implement에 `plan.md` 언급은 새 레이아웃·수명 규칙 2곳뿐, `스냅숏`·`mermaid`·`재생성` 0건. wf-doc·wf-design에 `docs/plan.md`·`snapshot`·`mermaid` 0건. 정밀 판정은 TASK-07.
- 결과: 완료(2026-10-09 14:00)

### 2026-10-09 — TASK-05 docs/plan.md → docs/status.md 전환, TASK-06 ADR-003 표기

- 수행 내용: **TASK-05** `git rm docs/plan.md`(이력 보존). `docs/status.md`(`ST-llm-workflow`) 신설 — 작업 목록에 진행 중 2행(이 작업 `in-progress`, 다인 토론 `on-hold`), ASCII 트리 1회 생성(생성 일시 표기), 승인 기록은 v1 승인 관문이 겸함. 역방향 링크: 이 작업 plan.md와 다인 토론 work-log의 문서 연결에 status 행 추가(링크만). README "실행 기준" 절 끝에 진행 중·완료 작업의 위치 안내 한 문단. 들어오는 링크 수리 53곳: 완료 작업 폴더 11개 파일의 `../../plan.md[#앵커]` → `./work-log.md[#수행-기록|#계획-트리]`, `docs/requirements.md`·`design.md` 추적표의 `./plan.md#작업-목록` → `./work/20260809-claude-hooks/work-log.md#수행-기록`(그 TASK들이 속한 사이클). 치환 전 대상 work-log에 해당 절이 있는지 단언으로 확인. **TASK-06** ADR-003 `## 대체 관계`에 관련(부분 수정) 1항, `## 변경 이력`에 1행 추가(`git diff` +2행). `docs/decisions.md` ADR-003 행 대체·관련 열에 부분 수정 링크.
- 변경 파일: `docs/plan.md`(삭제), `docs/status.md`(신설), `README.md`, `docs/requirements.md`, `docs/design.md`, 완료 작업 폴더 11개 파일(링크 경로만), `docs/work/20260814-multiuser-workflow/work-log.md`(링크 1행), `docs/work/20260814-wf-tree-triggers/ADR-003-트리거-단일-관문.md`, `docs/decisions.md`, 이 폴더 `plan.md`
- 발견 사항: 완료 문서의 링크 텍스트 "[PLAN-llm-workflow: 구현 계획]"은 NFR-02(내용 불변)에 따라 그대로 두고 경로만 바꿨다. 각 사이클의 TASK 상세는 해당 work-log 수행 기록(`### 날짜 — TASK-NN`)이 정본이므로 의미상 가장 가까운 대상이다. 과거 plan.md의 축약 목록·트리는 `git show c4cde3f:docs/plan.md`로 열람 가능.
- 결정과 이유: (1) 링크 대상을 status.md가 아니라 각 work-log로 — status.md는 완료 작업을 싣지 않아 대상이 없다. (2) 다인 토론 work-log(on-hold)에 역방향 링크 1행 추가 — wf-doc §2.6 "역방향 링크만 추가는 문서 명확화"에 해당. (3) status 트리는 이후 상태 변화에도 재생성하지 않는다(온디맨드 규칙 자기 적용).
- 롤백 절차(필수 게이트): 커밋 전 `git checkout -- docs/plan.md docs/requirements.md docs/design.md README.md docs/decisions.md docs/work && rm docs/status.md`. 커밋 후 해당 커밋 `git revert`. 스킬 변경도 같은 커밋이라 함께 되돌아간다.
- 실행한 검증: 치환 후 `docs/` 전체에서 `](…plan.md` 링크 잔존 0건(이 작업 폴더 제외). 정밀 판정(AC-05·07·09)은 TASK-07.
- 결과: 완료(2026-10-09 14:01)

### 2026-10-09 — TASK-07 검증·자체 리뷰·통합

- 수행 내용: VER-01~09 실행(아래 [검증 결과](#검증-결과)). 1차 검사에서 발견한 결함 3종을 수정 후 재검사: (1) `docs/requirements.md`·`design.md` 추적표의 수리 링크 앵커가 claude-hooks work-log의 실제 절 이름(`## 진행 기록`)과 달랐음 → 10곳 교정. (2) req-design DES-09 셀의 예시 유사 링크 `(…)`와 조사 절의 옛 앵커 `#갱신-시점`, 다인 토론 work-log의 같은 앵커 2곳 → 실제 링크·`#생성-시점`으로 교정. (3) wf-tree description이 바이트 기준 913으로 AC-08(900 이하) 미달 → 어구 2개를 줄여 883바이트. wf-implement §3.5 자체 리뷰: 스킬 diff 전수 통독 — 승인 설계와 일치, 범위 밖 변경 없음, 소유권 경계(wf-tree 헌장·wf-implement §3.2 단일 관문) 유지, 완료 문서는 링크 경로만 변경, `docs/paper/`·조사 문서 등 무관 미커밋 변경 보존. 개요 문서 2편·루트 SKILL.md에 옛 규칙 언급 0건.
- 변경 파일: `docs/requirements.md`, `docs/design.md`(앵커 교정), `req-design.md`, `docs/work/20260814-multiuser-workflow/work-log.md`(앵커 2곳), `skills/wf-tree/SKILL.md`(description), `plan.md`·`docs/status.md`(완료 처리), 이 파일
- 발견 사항: 기준선 조사의 "2,077어절·913자"는 각각 `wc -w`(파일 전체)와 description UTF-8 바이트였다. 같은 방법으로 2,077 → 1,938, 913 → 883. 저장소에 기존 깨진 링크 4건이 있다(`docs/research/20260919-aidlc-research/` 3건, `docs/planning/PLAN_TREE_TASKS.md` 1건) — 이 작업이 닿지 않은 파일의 기존 실패라 수정하지 않고 보고한다(wf-implement §2.2).
- 결정과 이유: 완료 보고 종결과 같은 변경에서 `docs/status.md`의 이 작업 행을 제거(FR-06·wf-implement §7 자기 적용). status·plan의 트리는 재생성하지 않았다 — 온디맨드 규칙의 첫 적용이며 생성 일시 표시가 신선도를 알린다.
- 실행한 검증: 아래 표
- 결과: 완료(2026-10-09 14:08)

## 설계와 달라진 점

경미한 변경 2건(wf-implement §4.1, 기준선 의미 불변):

1. DES-08의 "wf-tree §9 `generated` 표시 항목 삭제"를 삭제 대신 "생성 일시(`<!-- generated: … -->`)가 있는가"로 교체 — DES-02의 생성 일시 표시 요구와 정합.
2. status 템플릿의 `완료` 열을 삭제하고 `계획·기록`·`다음 행동` 열을 추가(DES-05 번역). 연쇄로 wf-tree 완료 시점 표기의 원천에서 status `완료` 열을 제외.

## 검증 결과

### 검증 범위와 환경

- 대상 기준선 또는 구현: [REQ-DESIGN-plan-relocation v1](./req-design.md) FR-01~10·NFR-01~03 구현(스킬 4종, docs 마이그레이션, ADR 정합, 자기 적용)
- 실행 환경: Windows 11, Git Bash, Python 3(저장소 루트에서 실행), git 작업 사본(HEAD dbbb68b)
- 제외 항목: TDD 사이클(자동 테스트 체계 없는 Markdown 규칙 문서 — §3.3 규정에 따라 후행 검증으로 대체)

### 결과 요약

- 성공: VER-01~09 (9/9)
- 실패: 없음
- 미수행: 없음

### 인수 조건별 결과

| 검증 ID | 인수 조건 | 방법·명령 | 결과 | 증거 |
|---|---|---|---|---|
| VER-01 | [AC-01](./req-design.md#인수-조건) | `grep -rin mermaid skills/` | 성공 | 1건 — wf-tree §7 "다이어그램 언어(Mermaid 등)…사용하지 않는다"(금지 문장, 역사 언급). 표기 규칙·예시·색상표 0건 |
| VER-02 | [AC-02](./req-design.md#인수-조건) | `grep -rn "갱신될 때마다\|자동으로 재생성\|같은 변경에서.*재생성\|트리 표현을 재생성" skills/`; `grep -n "^### 생성 시점" skills/wf-tree/SKILL.md` | 성공 | 자동 재생성 규정 0건. `### 생성 시점` 존재(최초 작성 1회·요청 시) |
| VER-03 | [AC-03](./req-design.md#인수-조건) | `grep -rn "스냅숏\|snapshot" skills/`; 4개 work-log의 `## 계획 트리` 절을 `git show HEAD:…`와 바이트 비교(Python) | 성공 | skills 언급 2건은 "남기지 않는다"·"새 스냅숏은 만들지 않는다"(금지·동결 설명). 의무 규정·완료 조건 0건. 4개 스냅숏 절 전부 unchanged, `<!-- snapshot` 표시 유지 |
| VER-04 | [AC-04](./req-design.md#인수-조건) | templates.md 319~325행, wf-implement 344~352행 통독 | 성공 | `PLAN-<작업-ID>`·저장 위치 `docs/work/<작업-ID>/plan.md`, 레이아웃 `status.md + plan.md·work-log.md` |
| VER-05 | [AC-05](./req-design.md#인수-조건) | `test ! -e docs/plan.md && test -e docs/status.md`; 작업 목록 행 grep | 성공 | 검증 시점 행 2개(이 작업 in-progress, 다인 토론 on-hold), 완료 행 0. 완료 보고 종결로 이 작업 행 제거 → on-hold 1행 |
| VER-06 | [AC-06](./req-design.md#인수-조건) | plan.md 존재·`### TASK-` 첫 항목·mermaid 펜스·`<!-- snapshot` 개수 | 성공 | TASK-01 시작, mermaid 펜스 0, 스냅숏 표시 0, `<!-- generated: 2026-10-09 13:55 …>` 1회 생성 |
| VER-07 | [AC-07](./req-design.md#인수-조건) | 상대 링크 전수 검사 스크립트(Python: skills·docs·README·개요 2편·루트 SKILL.md, 펜스·인라인 코드 제외, 파일 존재 + GitHub 슬러그 앵커 존재) | 성공 | 57파일 795링크. 이 작업이 닿은 파일의 깨진 링크 0. 기존 실패 4건은 미변경 파일(research 3·planning 1) — 범위 밖, [후속 작업](#후속-작업) |
| VER-08 | [AC-08](./req-design.md#인수-조건) | `git show HEAD:skills/wf-tree/SKILL.md`와 현재본을 같은 Python 함수로 측정(`len(s.split())`, description UTF-8 바이트) | 성공 | 어절 2,077 → 1,938(본문만 1,992 → 1,850), description 913 → 883바이트(397자) |
| VER-09 | [AC-09](./req-design.md#인수-조건) | `grep -n "ADR-003\|ADR-004" docs/decisions.md`; `git diff --numstat` ADR-003 | 성공 | ADR-004 행 approved, ADR-003 행 대체·관련 열에 부분 수정 링크. ADR-003 diff `2 0`(대체 관계 1항·변경 이력 1행 추가뿐) |

### 실패와 미수행 분석

없음. 1차 검사의 결함 3종(앵커 10곳, 유사 링크·옛 앵커 4곳, description 길이)은 같은 TASK에서 수정 후 재검사로 해소.

### 비기능 검증

- NFR-01: VER-08 — wf-tree 축소 확인.
- NFR-02: VER-03(스냅숏 절 불변)·VER-09(ADR-003 추가 2곳뿐). 완료 문서 11개의 diff는 링크 경로 치환뿐.
- NFR-03: VER-02 — 목록 정본·트리 파생 원칙이 wf-tree §5·§생성 시점, wf-implement §3.2에 명시.

### 남은 위험

[완료 보고](#남은-위험과-제한) 참조.

### 재검증 조건

스킬 4종·`docs/status.md`·템플릿을 다시 고치면 VER-01·02·03·07을 재실행한다. 링크 검사 스크립트는 이 기록의 VER-07 설명대로 재작성 가능(저장소에 두지 않음).

## 완료 보고

### 완료 상태

- 결과: 완료
- 완료 판단 근거: wf-implement §5(이 작업으로 개정된 조건) — TASK-01~07 완료, 구현이 기준선 v1과 일치(경미한 변경 2건 기록), AC-01~09 검증 결과 기록(9/9 성공), 자체 리뷰 중대 문제 없음, 코드·문서·설정 통합(로컬), 남은 위험 공개.

### 완료한 내용

- 계획 트리에서 Mermaid·자동 재생성·완료 스냅숏 의무를 제거하고 온디맨드 생성 시점(최초 작성 1회·요청 시)을 도입(FR-01·02·03).
- 구현 계획을 작업 폴더 `docs/work/<작업-ID>/plan.md`(`PLAN-<작업-ID>`, 작업 범위 TASK 번호 — ADR-004)로 이동(FR-04·05).
- `docs/plan.md`를 삭제하고 진행 중 작업만 담는 포트폴리오 `docs/status.md`로 대체, 들어오는 링크 53곳 수리, README 안내(FR-06·07·08).
- 이 작업의 계획을 새 규칙으로 작성·운용(FR-09). ADR-004 발행·등록, ADR-003 부분 수정 표기(FR-10).

### 주요 변경

- `skills/wf-tree/SKILL.md` — §7 매체·Mermaid 전부 삭제, §생성 시점 신설, §5·§8·§9·§1·description. 어절 2,077 → 1,938.
- `skills/wf-implement/SKILL.md` — §3.2 재생성 문구, §5 완료 조건 2항 삭제, §7 레이아웃·포트폴리오 행 규칙·계획 파일 수명.
- `skills/wf-doc/SKILL.md`·`references/templates.md` — `PLAN-<작업-ID>`, TASK·VER 작업 범위 규칙, plan·work-log·status 템플릿, 필수 연결표.
- `skills/wf-design/SKILL.md` — §6 한 문장.
- `docs/plan.md` 삭제, `docs/status.md` 신설, `README.md` 한 문단, `docs/requirements.md`·`design.md`·완료 작업 폴더 11개 파일·다인 토론 work-log(링크만), `docs/decisions.md`, ADR-003(2곳 추가).
- 이 폴더: `req-design.md`(v1), `ADR-004-…md`, `plan.md`, 이 파일.

### 설계와 달라진 점

위 [설계와 달라진 점](#설계와-달라진-점) 2건(경미).

### 인수 조건 충족 여부

AC-01~09 전부 충족 — [인수 조건별 결과](#인수-조건별-결과).

### 검증 결과와 증거

[검증 결과](#검증-결과) 절. 실행 명령과 핵심 출력은 표의 방법·증거 열.

### 통합 상태

로컬 작업 사본에 일관 반영 완료(미커밋). 스킬 설치본(`~/.claude/skills/wf-*`)은 저장소 `skills/`로의 심볼릭 링크라 별도 배포 불요. 커밋·push는 사용자 요청 범위(wf-implement §2.3). 같은 작업 사본의 무관한 미커밋 변경: `docs/research/20261009-test-lifecycle/`, `docs/paper/`(미추적), 다인 토론 work-log의 보류 전환 — 커밋 범위는 사용자가 정한다.

### 남은 위험과 제한

- RISK-02(트리 묵음): `docs/status.md`의 트리는 생성 시점 상태로 남아 제거된 이 작업 노드를 아직 보인다. 생성 일시 표시가 이를 알리며, 재생성은 요청 시.
- 완료 문서의 링크 텍스트 "[PLAN-llm-workflow: 구현 계획]"이 이제 각 사이클 work-log를 가리킨다(NFR-02로 텍스트 불변). 과거 plan.md 원문은 `git show c4cde3f:docs/plan.md`.
- 기존 깨진 링크 4건(`docs/research/20260919-aidlc-research/s1-s3_papers_deep_dive.md` 앵커 2, `S21_CRP_edit_draft.md` 파일 1, `docs/planning/PLAN_TREE_TASKS.md` 앵커 1) — 이 작업과 무관, 미수정.
- 산문 규칙이라 자동 회귀 검증이 없다. 다음 작업의 계획 수립이 새 규칙의 자연 관찰 지점.

### 후속 작업

- 커밋(사용자 요청 시): 이 작업 폴더 4개 파일 + 스킬 4종 + docs 변경 + README. 무관 변경의 포함 여부는 사용자 결정.
- 사이클 2: 작업 기록 다이어트·아카이빙·린트(요구 4~6). 사이클 3: 검증 기록과 테스트 수명주기.
- 기존 깨진 링크 4건 수리 — 경량 경로.
- 다인 토론(`20260814-multiuser-workflow`) 재개 시 Q-04를 이 작업 결과(작업별 plan, status 포트폴리오, 온디맨드 트리) 전제로 재검토.

### 인계

아래 [인계](#인계) 절.

## 미완료 항목

없음(이 작업 범위). 미커밋 상태 — 커밋은 사용자 요청 시.

## 재개 지점

- 다음 작업: 없음 — 작업 완료. 커밋 요청이 오면 `git status`로 범위를 확인하고 이 작업 관련 파일만 또는 사용자 지정 범위로 커밋
- 먼저 확인할 사항: `git status --short`(이 작업 파일 + 무관 미커밋 3종)
- 필요한 명령 또는 파일: [plan.md](./plan.md), 이 문서의 [완료 보고](#완료-보고)

## 인계

- 다음 단계 또는 워크플로우: 없음 — 작업 완료(2026-10-09 14:08). 후속은 [후속 작업](#후속-작업)
- 시작 조건: 해당 없음
- 입력 문서와 기준선: [REQ-DESIGN-plan-relocation v1](./req-design.md), [ADR-004](./ADR-004-TASK-식별자-작업-범위.md), [PLAN-20261009-plan-relocation](./plan.md)
- 완료된 항목: wf-design 전체, 계획 수립, TASK-01~07, AC-01~09 검증, 자체 리뷰, 로컬 통합, 완료 보고
- 미완료 항목: 없음(커밋은 사용자 요청 범위)
- 차단 요인: 없음
- 다음 행동: 사용자가 커밋을 요청하면 커밋 범위를 확인해 커밋한다. 그렇지 않으면 사이클 2를 wf-design으로 착수한다.
- 재개 프롬프트: 작업 20261009-plan-relocation 재개 — docs/work/20261009-plan-relocation/work-log.md의 인계 절을 읽고 "다음 행동"부터 진행하라.

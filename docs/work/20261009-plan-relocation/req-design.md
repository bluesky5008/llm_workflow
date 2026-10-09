# REQ-DESIGN-plan-relocation: 계획 문서 재배치 — 요구사항·설계

> 문서 유형: `requirements, design`
> 작업 ID: `20261009-plan-relocation`
> 상태: `approved`
> 기준선: `v1` (승인일 2026-10-09)
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [wf-tree SKILL](../../../skills/wf-tree/SKILL.md), [wf-implement SKILL](../../../skills/wf-implement/SKILL.md), [wf-doc SKILL](../../../skills/wf-doc/SKILL.md), [wf-doc 템플릿](../../../skills/wf-doc/references/templates.md), [wf-design SKILL](../../../skills/wf-design/SKILL.md), [wf-tree 존치 판정(조사)](../../research/20260919-aidlc-research/wf-tree_verdict.md), [ADR-004: TASK 식별자의 작업 범위 발행](./ADR-004-TASK-식별자-작업-범위.md), [ADR-003: 계획 트리 트리거의 단일 관문 배치](../20260814-wf-tree-triggers/ADR-003-트리거-단일-관문.md), [WORK-20261009-plan-relocation: 작업 기록](./work-log.md)

## 요약

- 목적: 계획 문서의 비용을 줄이고 재개 지점을 작업 폴더로 모은다. (1) 계획 트리에서 Mermaid와 자동 재생성·완료 스냅숏 의무를 없애고, (2) 작업별 구현 계획을 작업 폴더로 내리고, (3) `docs/` 바로 아래의 저장소 관통 계획 문서는 진행 중 작업만 담는 포트폴리오(`docs/status.md`)로 바꾼다.
- 현재 결론 또는 상태: 기준선 v1 승인(2026-10-09) — Q-01~Q-05 전부 권장안, ADR-004 승인. 구현 완료(2026-10-09 14:05, AC-01~09 전 항목 성공 — [작업 기록](./work-log.md#완료-보고)).
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | N/A | document | 이 작업의 루트 문서. 변경 대상이 스킬 규칙이며 C층 훅 기준선(`docs/requirements.md`·`design.md`)과 시스템이 다르다(선례: [tree-completion-time](../20260817-tree-completion-time/req-design.md)) |
| input | related | [wf-tree 존치 판정](../../research/20260919-aidlc-research/wf-tree_verdict.md) | §0 기능별 판정, §3 권고 | 조사 입력. Mermaid·자동 재생성·스냅숏 제외 권고 |
| input | related | [wf-tree §5·§7·§8·§9](../../../skills/wf-tree/SKILL.md#5-데이터-모델과-식별자), [wf-implement §3.2·§5·§7](../../../skills/wf-implement/SKILL.md#32-계획-수립), [wf-doc plan·work-log·status 템플릿](../../../skills/wf-doc/references/templates.md#구현-계획-plan), [wf-doc 추적 식별자](../../../skills/wf-doc/SKILL.md#추적-식별자), [wf-design §6](../../../skills/wf-design/SKILL.md#6-산출물) | 변경 대상 절 | 조사(2026-10-09)에서 확인한 현행 규칙 |
| input | related | [ADR-003: 계획 트리 트리거의 단일 관문 배치](../20260814-wf-tree-triggers/ADR-003-트리거-단일-관문.md) | 결정, 결과와 감수할 단점 | 부분 수정 대상(DES-09). 배치 결정은 유지, 관문에서의 재생성 의무와 완료 조건 안전망만 변경 |
| output | decision | [ADR-004: TASK 식별자의 작업 범위 발행](./ADR-004-TASK-식별자-작업-범위.md) | FR-05, DES-06 | Q-01 결정의 장기 식별자 정책. 이 문서 v1과 함께 승인(2026-10-09) |
| output | implementation | [PLAN-20261009-plan-relocation: 구현 계획](./plan.md), [WORK-20261009-plan-relocation: 작업 기록](./work-log.md) | TASK-01~07, VER-01~09 | 계획(자기 적용)과 수행·검증 기록 |

**산출물 위치에 대한 결정:** 선행 스킬 변경 작업들과 동일하게 작업 폴더의 통합 문서로 둔다. 승인 관문에서 사용자 확인을 받는다.

## 문제와 목적

사용자의 사용 경험(2026-10-09): 계획 문서 `docs/plan.md`가 사이클마다 Mermaid와 ASCII 트리를 재생성하고 완료 사이클의 축약 목록을 누적해 비대해졌다. 작업별 계획은 작업 폴더에 있어야 재개 시 한 폴더만 읽으면 되는데, 지금은 저장소 관통 문서 하나에 모든 사이클의 TASK가 전역 번호로 쌓인다.

조사 기록 [wf-tree 존치 판정](../../research/20260919-aidlc-research/wf-tree_verdict.md)의 결론이 같은 방향이다. 계획 구조화(`상위:`·`depends:`)와 진행 상태 추적은 근거가 강하지만, Mermaid 매체는 ASCII와 정보가 같고 에이전트 쪽 효과 근거가 없으며, 상태 갱신마다의 자동 재생성과 완료 스냅숏 의무는 비용 근거만 있다(Skills Harmful의 Heavy Implementation Pipeline 패턴, FH 계획 논문·Learning When to Plan의 "매 단계 갱신" 비용).

## 현재 상태 조사 (wf-design §4.1)

### 사실

- **wf-tree §7 렌더링**: 매체를 Markdown 목록(원천)·ASCII·Mermaid 3종으로 규정. Mermaid 표기 규칙, classDef 색상표(4색 hex), 예시 다이어그램을 본문에 둔다. §갱신 시점(현 [§생성 시점](../../../skills/wf-tree/SKILL.md#생성-시점)): "진행 상태가 갱신될 때마다 같은 변경에서 트리 표현을 자동으로 재생성한다". 대형 트리 대응 3항: 포트폴리오 뷰와 작업별 상세 뷰를 별도 Mermaid로, 노드 30 초과 시 분할.
- **wf-tree §5 저장 위치**: 포트폴리오는 `docs/status.md`(status 유형, `ST-<슬러그>`), 작업 내부 트리는 `docs/plan.md`의 `## 계획 트리` 절. §5 단일 소스 원칙에 완료 스냅숏 예외(`<!-- snapshot -->`) 규정. §9 자체 검토에 `generated` 표시·노드 30 분할·`status.md` 실재 확인 항목.
- **wf-tree §1·description**: "wf-implement 계획 수립이 트리 사용을 결정한 계획을 수립·갱신할 때 TASK 작성·상태 갱신과 같은 변경에서 트리를 생성·재생성한다". description은 913자(조사 기록의 린트 경고 임계 900자 초과).
- **wf-implement §3.2**: 트리 사용 기준(작업 3개 이상, 분해·OR·의존, 포트폴리오 소속). `completed` 전이 시 완료 시점 기입과 트리 재생성을 같은 변경에서. **§7**: "구현 계획은 저장소 전체를 관통하는 현행 문서로 `docs/plan.md`에 두고, 작업 폴더에는 작업 기록만". 완료 사이클 축약 규정, 완료 사이클 트리 스냅숏 의무(ASCII 상세와 mermaid를 work-log에 백업한 뒤에만 축약 가능). **§5 완료 조건**에 "트리가 작업 목록과 동기화", "완료 시점의 트리 스냅숏이 작업 기록에 남았다" 2항.
- **wf-doc 템플릿**: plan 문서 ID 권장값 `PLAN-<프로젝트-슬러그>`(저장소 현행 문서), `## 계획 트리` generated 절, 축약형 노트. work-log 템플릿 노트에 `## 계획 트리` 스냅숏 절 규정. status 템플릿 저장 위치 문구 "저장소 관통 문서(`requirements.md`·`design.md`·`plan.md`)와 같은 위치". 문서 유형별 필수 연결표에 `plan`·`work-log`·`status` 행. **wf-doc SKILL §2.6**: 문서 ID 목록에 `PLAN-<프로젝트-슬러그>`, 추적표 예시가 `[TASK-01](./plan.md)`.
- **wf-design §6**: "`docs/plan.md`와 작업 폴더의 `work-log.md`는 wf-implement 작업 기록과 저장 위치가 소유한다" 한 문장.
- **ADR-003**(2026-08-14, approved): 결정은 "계획 트리의 채택 결정·최초 생성·재생성 트리거를 wf-implement §3.2 한 곳에만 배치". 결과 절의 안전망이 "wf-implement §5 완료 조건의 동기화 확인(FR-03)". 대체 관계 없음.
- **docs/plan.md 현황**(c4cde3f): 155행, 11.4KB. 머리말 작업 ID는 마지막 사이클 하나(`20260817-tree-completion-time`). 완료 사이클 6개를 축약 목록으로, 현재 사이클 TASK-25~29를 상세로. `## 계획 트리`에 포트폴리오 성격의 ASCII(완료 사이클 7개 롤업)와 현재 사이클 Mermaid. TASK 번호는 저장소 전역 일련번호(01~29).
- **완료 스냅숏 실측**: work-log의 `## 계획 트리` 스냅숏 절은 약 30행·1.5KB(`20260817-tree-completion-time`). 조사 기록의 "8~9KB/사이클"은 파일 전체 크기로 보이며 과장이다. 스냅숏을 가진 work-log는 4개(동결 기록).
- **훅 의존성**: `setup/hooks/wf-common.ps1`은 `docs/work/*/work-log.md` 머리말의 상태만 읽는다. `plan.md`·`status.md`를 읽는 훅·설정은 없다. `setup/CLAUDE.global.md`, README, 개요 문서 2편에도 `plan.md` 언급 없음.
- **plan.md 참조 전수**(skills·setup·README·개요): wf-design §6(1), wf-doc SKILL(2), wf-doc 템플릿(2), wf-implement §7(3), wf-tree §5(2). 총 10곳.
- **등록부**: `docs/decisions.md`의 마지막 번호는 ADR-003(2026-08-14). 보관 브랜치 `archive/202609-cycles`는 ADR-004·ADR-005·DCR-006을 발행했으나 main 이력에는 없다.

### 해석

- 요구 1·2·3은 서로 맞물린다. Mermaid만 빼면 ASCII 자동 재생성과 스냅숏 의무가 남아 비용의 대부분이 유지된다. 계획을 작업 폴더로 내리면 `docs/plan.md`의 남는 역할은 "진행 중 작업의 목록과 트리"뿐이며, 이는 wf-doc에 이미 있는 `status` 유형의 정의와 같다. 따라서 `docs/plan.md`를 `docs/status.md`로 대체하는 것이 새 유형을 만들지 않는 최소 변경이다.
- 작업 폴더로 내려간 plan의 문서 ID는 `PLAN-<작업-ID>`가 자연스럽다(`WORK-<작업-ID>`와 같은 규칙). TASK 번호를 전역으로 유지할 이유는 작업 간 TASK 상호 참조뿐인데, 링크에 작업 경로가 들어가므로 작업 범위 번호로도 유일성이 보장된다.
- ADR-003의 결정(트리거 배치)은 이 작업으로 바뀌지 않는다. 바뀌는 것은 관문에서 하는 일(재생성 → 온디맨드)과 ADR-003이 안전망으로 지목한 완료 조건이다. 따라서 대체가 아니라 부분 수정이며, 변경 내용의 정본은 이 문서(DES-02·DES-03)다.
- 훅과 설정이 plan.md에 의존하지 않으므로 파일 이동·대체는 스킬 문서와 docs/ 문서만의 변경이다.
- 완료된 사이클 7개의 docs/plan.md 내용은 각 work-log가 정본이며, 소급해 작업 폴더에 plan.md를 만들 필요가 없다(완료는 당시 기준선의 사건 기록).

### 가정

- 이 저장소의 사용자는 1인이다. 다인 사용 시의 plan 분할·발효 규칙(보류된 [다인 토론 Q-04](../20260814-multiuser-workflow/work-log.md#미해결-질문))은 이 작업의 결과를 전제로 재개 시 재검토한다.
- 완료 사이클의 동결 스냅숏 4개는 수정하지 않는다(선례: tree-completion-time의 제외 항목).

## 범위

### 포함

- `skills/wf-tree/SKILL.md` — §7 매체·Mermaid 규칙·색상표·예시·대형 트리 대응 3항 제거, §갱신 시점을 온디맨드 생성 시점으로, §5 저장 위치·스냅숏 예외, §1·description, §9 체크리스트
- `skills/wf-implement/SKILL.md` — §3.2 트리 재생성 문구, §5 완료 조건 2항, §7 저장 위치·축약·스냅숏
- `skills/wf-doc/SKILL.md` §2.6 식별자·추적표 예시, `references/templates.md` plan·work-log·status 템플릿과 필수 연결표
- `skills/wf-design/SKILL.md` §6의 plan.md 문구
- `docs/plan.md` → `docs/status.md` 전환(마이그레이션)과 이 작업의 자기 적용(계획을 `docs/work/20261009-plan-relocation/plan.md`에 작성)
- ADR-004 발행·등록, ADR-003 부분 수정 표기(한 줄), `docs/decisions.md` 갱신

### 제외

- wf-tree 분기 템플릿 축소(판정 ⑤)와 렌더링 스크립트화(`render.py`) — 별도 작업(Q-05 결정)
- 세션 인계 시 활성 경로 뷰 자동 생성 — 넣지 않음(Q-03 결정)
- 완료 work-log 4개의 동결 스냅숏 소급 수정
- 완료 사이클의 plan.md 소급 생성, 과거 TASK 번호(01~29)의 재번호
- 작업 기록 다이어트·아카이빙(요구 4~6) — 사이클 2
- 훅 변경 — 의존성 없음

## 기능 요구사항

| ID | 항목 | 내용 |
|---|---|---|
| FR-01 | Mermaid 제거 | 계획·포트폴리오 문서에 Mermaid 생성물을 두지 않는다. 트리 매체는 Markdown 목록(원천)과 ASCII 2종 |
| FR-02 | 온디맨드 렌더링 | 상태 갱신마다의 자동 재생성을 폐지한다. ASCII 트리는 계획 최초 작성 시 1회와 사용자 요청 시에만 생성한다([DES-02](#설계)). 갱신 사이에 트리와 목록이 어긋나도 목록이 정본이므로 결함이 아니다 |
| FR-03 | 완료 스냅숏 의무 폐지 | 완료 사이클의 트리 스냅숏을 work-log에 남기는 의무와 관련 완료 조건을 없앤다. 기존 스냅숏은 동결 기록으로 유지 |
| FR-04 | 작업별 계획 파일 | 구현 계획은 `docs/work/<작업-ID>/plan.md`(문서 ID `PLAN-<작업-ID>`)에 둔다. 작업 내부 트리도 이 파일의 `## 계획 트리` 절 |
| FR-05 | TASK 번호 범위 | TASK 식별자는 작업 범위에서 `TASK-01`부터 발행한다([ADR-004](./ADR-004-TASK-식별자-작업-범위.md)). 작업 간 참조는 경로 포함 링크로. 과거 전역 번호는 기록으로 유지 |
| FR-06 | 진행 중 포트폴리오 | `docs/status.md`는 진행 중(`in-progress`·`awaiting-approval`·`on-hold`·`blocked`) 작업만 담는다. 완료 작업 행은 완료 보고 종결과 같은 변경에서 제거하고, 이력은 작업 폴더와 git이 정본 |
| FR-07 | 마이그레이션 | 기존 `docs/plan.md`를 제거(git 이력 보존)하고 `docs/status.md`를 신설한다. 완료 사이클 축약 목록·트리는 옮기지 않는다 |
| FR-08 | 참조 무결성 | plan.md를 가리키는 스킬·템플릿·예시 10곳을 새 구조로 갱신하고 깨진 링크가 없다 |
| FR-09 | 자기 적용 | 이 작업의 계획을 새 규칙으로 작성한다(작업 폴더 plan.md, 작업 범위 TASK 번호, ASCII만, 스냅숏 없음) |
| FR-10 | ADR 정합 | ADR-004를 발행·등록하고, ADR-003에는 부분 수정 사실을 한 줄로 표기한다. 등록부의 두 행이 파일과 일치한다 |

## 비기능 요구사항

| ID | 항목 | 내용 |
|---|---|---|
| NFR-01 | wf-tree 축소 | wf-tree 본문 어절 수가 감소한다(현재 2,077어절, description 913자) |
| NFR-02 | 완료 문서 보존 | 완료 작업의 문서(work-log 7개, req-design 6개, ADR-003)의 내용은 바꾸지 않는다. 링크 수리와 [DES-09](#설계)의 ADR-003 한 줄 표기만 허용 |
| NFR-03 | 단일 소스 | 목록이 정본, 트리는 파생이라는 원칙은 유지한다 |

## 인수 조건

| ID | 조건 |
|---|---|
| AC-01 | `skills/` 전수 검색에서 Mermaid 렌더링 규정·예시·색상표가 0건(역사 언급 제외) |
| AC-02 | "갱신될 때마다 재생성" 류 자동 재생성 규정이 0건이고 온디맨드 생성 시점(최초 작성 1회, 요청 시) 규정이 wf-tree에 존재 |
| AC-03 | 스냅숏 의무 규정과 완료 조건 2항이 0건, 기존 work-log 4개의 스냅숏 절은 `git diff` 무변경 |
| AC-04 | plan 템플릿의 문서 ID가 `PLAN-<작업-ID>`이고 저장 위치가 작업 폴더이며, wf-implement §7 파일 레이아웃이 `docs/work/<작업-ID>/plan.md`를 보인다 |
| AC-05 | `docs/plan.md`가 없고 `docs/status.md`가 존재하며, 작업 목록에 완료 작업 행이 없고 진행 중 작업(이 작업, 보류 중인 다인 토론)만 있다 |
| AC-06 | 이 작업의 계획이 `docs/work/20261009-plan-relocation/plan.md`에 있고 TASK-01부터 시작하며 Mermaid·스냅숏이 없다 |
| AC-07 | skills·docs의 상대 링크 전수 검사에서 깨진 링크 0건 |
| AC-08 | wf-tree 어절 수가 2,077 미만, description 900자 이하 |
| AC-09 | `docs/decisions.md`에 ADR-004 행(approved)이 있고 ADR-003 행의 대체·관련 열에 이 문서가 링크되며, ADR-003 파일의 `git diff`가 대체 관계 1항·변경 이력 1행 추가뿐이다 |

## 설계

| ID | 설계 요소 | 내용 |
|---|---|---|
| DES-01 | wf-tree §7 축소 | 매체 표를 2종으로. Mermaid 표기 규칙·색상표·예시 다이어그램·대형 트리 대응 3항 삭제. ASCII 표기(`[✓]`·`[▶]`·`[ ]`, 완료 시점 우측 끝, 롤업 배지)는 유지 |
| DES-02 | 온디맨드 생성 시점 | §갱신 시점을 "생성 시점"으로 교체: (a) 계획(작업 plan·포트폴리오 status) 최초 작성 시 1회, (b) 사용자 요청 시. 상태 갱신은 목록 필드만 바꾼다. 요청 시 생성은 전체 트리 또는 활성 경로 뷰 중 사용자가 지정한 것. 트리가 목록보다 오래됐을 수 있음을 `## 계획 트리` 절 첫 줄에 생성 일시로 표시 |
| DES-03 | 스냅숏 폐지 | wf-implement §7 스냅숏 항목·§5 완료 조건 2항·wf-doc work-log 템플릿 노트·wf-tree §5 스냅숏 예외를 삭제. 기존 `<!-- snapshot -->` 절의 해석은 wf-tree §5에 "과거 규칙의 동결 기록" 한 줄로만 남긴다 |
| DES-04 | 작업별 plan | wf-implement §7 레이아웃을 `docs/work/<작업-ID>/plan.md + work-log.md`로. wf-doc 문서 ID `PLAN-<작업-ID>`, 추적표 예시 경로 `./work/<작업-ID>/plan.md`. work-log `## 기준선과 현재 계획`이 같은 폴더 plan.md를 링크. 필수 연결표 `plan` 행의 "작업 기록"은 같은 폴더 |
| DES-05 | status.md 역할 | `docs/status.md`(`ST-llm-workflow`)를 저장소 관통 포트폴리오로. 작업 목록 표에 진행 중 작업만(작업 ID·상태·plan/work-log 링크·다음 행동). `## 계획 트리`는 작업 노드만의 ASCII(온디맨드, DES-02). 행 추가 = 작업 시작(wf-design 착수 또는 경량 경로 작업 ID 발행), 행 제거 = 완료 보고 종결, 둘 다 같은 변경에서. wf-tree §8의 포트폴리오 최초 생성 승인은 이 작업의 승인 관문이 겸한다 |
| DES-06 | 식별자 규칙 | wf-doc §2.6에 "TASK-NN은 작업 범위 식별자이며 다른 작업의 TASK는 경로 포함 링크로 가리킨다" 추가. `PLAN-<프로젝트-슬러그>`를 `PLAN-<작업-ID>`로. 정책의 근거는 [ADR-004](./ADR-004-TASK-식별자-작업-범위.md) |
| DES-07 | 마이그레이션 | `docs/plan.md`를 `git rm`(이력 보존), `docs/status.md` 신설. 완료 사이클 7개는 status에 싣지 않는다. 롤백은 git revert. 완료 사이클의 조망은 `docs/work/` 목록과 `git log`가 대체(README에 한 줄 안내) |
| DES-08 | 문구 정리 | wf-design §6의 plan.md 문구, wf-doc status 템플릿 저장 위치 문구, wf-tree §1·description·§9(generated 표시·노드 30 분할 항목 삭제, status.md 실재 확인 유지) |
| DES-09 | ADR-003 부분 수정 표기 | ADR-003은 `approved` 유지, 대체 ADR 없음. ADR-003 `## 대체 관계`에 "관련: [REQ-DESIGN-plan-relocation](./req-design.md) DES-02·DES-03이 관문에서의 재생성 의무와 완료 조건 안전망을 변경(2026-10-09). 배치 결정은 유지" 1항, `## 변경 이력`에 1행 추가. `docs/decisions.md` ADR-003 행의 대체·관련 열에 같은 링크. NFR-02의 명시적 예외 |
| DES-10 | ADR-004 발행 | [ADR-004](./ADR-004-TASK-식별자-작업-범위.md)를 이 문서와 함께 `proposed` → 승인 시 `approved`. 번호는 main 이력 기준(등록부 마지막 ADR-003의 다음). 보관 브랜치의 ADR-004와 번호가 겹치는 사실을 ADR 본문에 기록 |

### 검증 전략

- AC-01~04·08: 스킬 파일 grep과 어절·문자 수 측정(실행 명령과 결과를 작업 기록에 남긴다).
- AC-03·09: `git diff --stat`과 대상 파일 diff.
- AC-05·06: 파일 존재·부재 확인과 문서 머리말·작업 목록 검사.
- AC-07: skills·docs 상대 링크 전수 검사 스크립트(선례: tree-completion-time 검증 방법 재사용).

## 가정과 미해결 질문

| ID | 질문 | 해소 조건 | 결정(2026-10-09) |
|---|---|---|---|
| Q-01 | TASK 번호를 작업 범위(`TASK-01`부터)로 바꿀 것인가, 전역 일련번호를 유지할 것인가? | 사용자 결정 | **작업 범위.** [ADR-004](./ADR-004-TASK-식별자-작업-범위.md) |
| Q-02 | `docs/plan.md`를 삭제하고 `docs/status.md`로 대체할 것인가, 파일명을 유지하고 내용만 바꿀 것인가? | 사용자 결정 | **status.md로 대체.** wf-doc에 status 유형과 `ST-` 식별자가 이미 있다 |
| Q-03 | 온디맨드 생성 시점에 "세션 인계 시 활성 경로 뷰 1회"를 넣을 것인가? | 사용자 결정 | **넣지 않음.** 인계 절의 "다음 행동"이 같은 역할. 요청 시 생성으로 충분 |
| Q-04 | ADR-003을 대체·수정하는가? | ADR-003 본문 확인 후 사용자 결정 | **부분 수정, 대체 ADR 없음.** 배치 결정은 유지되고 관문에서 하는 일만 바뀐다(DES-09) |
| Q-05 | wf-tree 분기 템플릿 축소와 렌더링 스크립트화를 포함할 것인가? | 사용자 결정 | **제외.** 별도 작업 |

## 위험

| ID | 위험 | 영향 | 완화 |
|---|---|---|---|
| RISK-01 | 10곳의 plan.md 참조 중 누락 | 깨진 링크·옛 규칙 잔존 | AC-07 링크 전수 검사와 AC-01·02·04 grep |
| RISK-02 | 온디맨드 전환 후 트리가 오래 묵어 재개 시 혼란 | 트리를 믿고 잘못된 재개 | 목록이 정본 원칙 유지, 트리 절 첫 줄에 생성 일시(DES-02), 인계 절의 "다음 행동"이 재개 지점 |
| RISK-03 | 완료 사이클 기록이 status에서 사라져 조망 상실 | 과거 사이클 찾기 비용 | `docs/work/` 목록과 `git log`가 대체, README 한 줄 안내(DES-07) |
| RISK-04 | ADR-004 번호가 보관 브랜치와 겹침 | 브랜치 간 참조 혼동 | main 이력 기준 발행을 ADR 본문과 등록부에 명시(DES-10). 보관 브랜치는 병합 대상이 아님 |

## 추적성

| 요구사항 | 설계 | 작업 | 검증 |
|---|---|---|---|
| FR-01 | DES-01 | [TASK-01](./plan.md#작업-목록) | AC-01 — [VER-01](./work-log.md#검증-결과) 성공 |
| FR-02 | DES-02, DES-08 | [TASK-01, TASK-02](./plan.md#작업-목록) | AC-02 — [VER-02](./work-log.md#검증-결과) 성공 |
| FR-03 | DES-03 | [TASK-01, TASK-02, TASK-03](./plan.md#작업-목록) | AC-03 — [VER-03](./work-log.md#검증-결과) 성공 |
| FR-04 | DES-04 | [TASK-02, TASK-03](./plan.md#작업-목록) | AC-04 — [VER-04](./work-log.md#검증-결과) 성공 |
| FR-05 | DES-06, DES-10 | [TASK-03](./plan.md#작업-목록) | AC-06, AC-09 — [VER-06, VER-09](./work-log.md#검증-결과) 성공 |
| FR-06 | DES-05 | [TASK-02, TASK-05](./plan.md#작업-목록) | AC-05 — [VER-05](./work-log.md#검증-결과) 성공 |
| FR-07 | DES-07 | [TASK-05](./plan.md#작업-목록) | AC-05 — [VER-05](./work-log.md#검증-결과) 성공 |
| FR-08 | DES-04, DES-08 | [TASK-03, TASK-04, TASK-05](./plan.md#작업-목록) | AC-07 — [VER-07](./work-log.md#검증-결과) 성공 |
| FR-09 | DES-04, DES-06 | 계획 수립, [TASK-07](./plan.md#작업-목록) | AC-06 — [VER-06](./work-log.md#검증-결과) 성공 |
| FR-10 | DES-09, DES-10 | [TASK-06](./plan.md#작업-목록) | AC-09 — [VER-09](./work-log.md#검증-결과) 성공 |
| NFR-01 | DES-01, DES-08 | [TASK-01](./plan.md#작업-목록) | AC-08 — [VER-08](./work-log.md#검증-결과) 성공 |
| NFR-02 | DES-03, DES-09 | [TASK-05, TASK-06](./plan.md#작업-목록) | AC-03, AC-09 — [VER-03, VER-09](./work-log.md#검증-결과) 성공 |
| NFR-03 | DES-02 | [TASK-01, TASK-02](./plan.md#작업-목록) | AC-02 — [VER-02](./work-log.md#검증-결과) 성공 |

## 승인 기록

| 기준선 | 일자 | 결과 | 근거 |
|---|---|---|---|
| v1 | 2026-10-09 | 승인 | 대화형 승인 관문에서 사용자 응답 "승인" — Q-01~Q-05 결정(전부 권장안), ADR-004, 산출물 위치(작업 폴더 통합 문서), `docs/status.md` 포트폴리오 최초 생성(wf-tree §8 승인 겸함) 포함 |

## 인계

- 다음 단계 또는 워크플로우: 없음 — 작업 완료(wf-implement 구현·검증 종료, 2026-10-09 14:05). 후속은 사이클 2(작업 기록 다이어트·아카이빙·린트)
- 시작 조건: 충족 — 이 문서 v1 승인(2026-10-09)
- 입력 문서와 기준선: 이 문서 v1, [ADR-004](./ADR-004-TASK-식별자-작업-범위.md)(approved)
- 완료된 항목: 현재 상태 조사, 요구사항·설계, Q-01~Q-05 확정, ADR-004, 기준선 v1 승인, 구현·검증 전체([TASK-01~07](./plan.md#작업-목록), AC-01~09 성공 — [작업 기록](./work-log.md))
- 미완료 항목: 없음
- 차단 요인: 없음

## 변경 이력

| 날짜 | 사건 | 근거 |
|---|---|---|
| 2026-10-09 | 초안 작성(§4.1 조사 완료, 요구·설계 초안, Q-01~05) | 2026-10-09 세션. 컨텍스트 임계 훅 신호로 인계 |
| 2026-10-09 | Q-01~Q-05 결정 반영(전부 권장안), FR-10·NFR 표·AC-09·DES-09·10·RISK-04·추적표 추가, §4.5 검토 후 `awaiting-approval` | 사용자 결정(대화형 질문 응답), ADR-003 본문 확인 |
| 2026-10-09 | 기준선 v1 승인, `approved`. 승인 기록·인계 절 추가 | 대화형 승인 관문 사용자 응답 "승인" |

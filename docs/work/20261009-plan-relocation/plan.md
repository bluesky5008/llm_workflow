# PLAN-20261009-plan-relocation: 구현 계획 — 계획 문서 재배치

> 문서 유형: `plan`
> 작업 ID: `20261009-plan-relocation`
> 상태: `completed`
> 기준선: `v1` ([REQ-DESIGN-plan-relocation](./req-design.md), 2026-10-09 승인)
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [REQ-DESIGN-plan-relocation: 요구사항·설계](./req-design.md), [ADR-004: TASK 식별자의 작업 범위 발행](./ADR-004-TASK-식별자-작업-범위.md), [WORK-20261009-plan-relocation: 작업 기록](./work-log.md)

## 요약

- 목적: 기준선 v1(FR-01~10, DES-01~10)을 스킬 문서 4종·docs 마이그레이션·ADR 정합의 작업 7개로 번역하고 AC-01~09로 검증한다.
- 현재 결론 또는 상태: **완료** — TASK-01~07 전부 완료(2026-10-09 14:05), AC-01~09 전 항목 성공. 검증 상세는 [작업 기록](./work-log.md#검증-결과).
- 다음 행동: 없음 — 커밋은 사용자 요청 시. 계획 트리는 재생성하지 않았다(온디맨드 규칙 자기 적용, 목록이 정본).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-plan-relocation](./req-design.md) | FR-01~10, NFR-01~03, AC-01~09, DES-01~10 | 승인 기준선 v1 |
| input | decision | [ADR-004: TASK 식별자의 작업 범위 발행](./ADR-004-TASK-식별자-작업-범위.md) | document | 이 계획의 TASK 번호가 01부터 시작하는 근거(자기 적용) |
| output | implementation | [WORK-20261009-plan-relocation: 작업 기록](./work-log.md) | document | 수행 기록·검증 결과(verification 합침)의 정본 |
| input | related | [ST-llm-workflow: 포트폴리오](../../status.md) | document | 이 작업이 등재된 포트폴리오(TASK-05에서 신설) |

## 기준선

- 관련 요구사항: [FR-01~10, NFR-01~03, AC-01~09](./req-design.md#기능-요구사항)
- 관련 설계: [DES-01~10](./req-design.md#설계)
- 관련 ADR·DCR: [ADR-004](./ADR-004-TASK-식별자-작업-범위.md); [ADR-003](../20260814-wf-tree-triggers/ADR-003-트리거-단일-관문.md)은 부분 수정 대상(DES-09)

## 작업 정의

- 목표: 스킬 4종에서 Mermaid·자동 재생성·스냅숏 의무를 제거하고 계획을 작업 폴더로 내리는 규칙으로 바꾼 뒤, `docs/plan.md`를 `docs/status.md`로 전환하고 ADR을 정합시킨다.
- 범위·범위 밖·가정·위험: [기준선 문서](./req-design.md#범위) 참조.
- 트리 사용 결정: **사용** — 작업 7개(3개 이상), TASK-05→02·03, TASK-06→04, TASK-07→전체 의존.
- TDD 적용: 변경 대상이 전부 Markdown 규칙 문서이며 저장소에 자동 테스트 체계가 없다. [wf-implement §3.3](../../../skills/wf-implement/SKILL.md#33-구현)의 "사이클을 적용할 수 없는 변경"으로 분류하고, 각 TASK의 검증은 TASK-07의 후행 검증(grep·링크 전수 검사·어절 측정·git diff)으로 대체한다. 이유는 작업 기록에 남긴다.
- 자기 적용(FR-09): 이 문서가 새 규칙의 첫 적용이다 — 작업 폴더 위치, `PLAN-<작업-ID>`, TASK-01부터, ASCII 트리 1회 생성, 스냅숏 없음.

## 계획 트리

<!-- generated: 2026-10-09 13:55 — 계획 최초 작성 시 1회 생성. 이후 목록이 정본이며 트리는 요청 시에만 재생성 -->

```text
[작업] 20261009-plan-relocation — 계획 문서 재배치 ................ in-progress (0/7)
├─ [ ] 구현: wf-tree — ASCII만, 온디맨드 생성, 스냅숏 예외·대형 트리 3항 삭제 (TASK-01)
├─ [ ] 구현: wf-implement — §3.2 재생성 문구, §5 완료 조건 2항, §7 레이아웃·스냅숏 (TASK-02)
├─ [ ] 구현: wf-doc — §2.6 식별자·추적표, plan·work-log·status 템플릿, 필수 연결표 (TASK-03)
├─ [ ] 구현: wf-design §6 — plan.md 문구 (TASK-04)
├─ [ ] 전환: docs/plan.md → docs/status.md, README 안내 (TASK-05) .......... depends: TASK-02, TASK-03
│   ├─ [ ] 롤백 준비: git revert 경로 기록 (필수)
│   └─ [ ] 검증: AC-05 → TASK-07 (필수)
├─ [ ] 문서화: ADR-003 부분 수정 표기, decisions.md 관련 열 (TASK-06) ...... depends: TASK-04
└─ [ ] 검증: AC-01~09 판정, 자체 리뷰, 통합 (TASK-07) ...................... depends: TASK-01~06
```

## 작업 목록

### TASK-01: wf-tree 축소와 온디맨드 생성 시점

- 상태: completed
- 완료: 2026-10-09 13:58
- 상위: 없음
- 목표: `skills/wf-tree/SKILL.md`에서 Mermaid 매체·표기 규칙·색상표·예시 다이어그램·대형 트리 대응 3항을 삭제하고, §갱신 시점을 "생성 시점"(최초 작성 1회, 요청 시)으로 교체하며, §5 스냅숏 예외를 동결 기록 한 줄로 줄이고 저장 위치를 작업 폴더 plan.md로 바꾼다. §1·description·§9를 맞춘다.
- 관련 요구사항과 설계: FR-01·02·03, NFR-01·03 / DES-01·02·03·08
- 변경 대상: `skills/wf-tree/SKILL.md`
- 의존성: 없음
- 위험: 어절 수 감소 목표(NFR-01)와 ASCII 규칙 보존(DES-01)의 균형 — 삭제는 Mermaid·자동 재생성·대형 트리 3항·분할 항목에 한정
- 검증 방법: TASK-07 VER-01·02·08(grep 0건, 생성 시점 규정 존재, 어절·description 측정)
- 완료 조건: AC-01·02·08의 wf-tree 부분이 충족되고 트리 구조·노드 유형·분기 템플릿·상태 롤업·ASCII 완료 시점 규칙은 변경 없음

### TASK-02: wf-implement 계획 저장 위치와 완료 조건

- 상태: completed
- 완료: 2026-10-09 14:00
- 상위: 없음
- 목표: §3.2의 "같은 변경에서 트리 재생성" 문구를 온디맨드 규칙으로, §5 완료 조건의 트리 동기화·스냅숏 2항을 삭제, §7 파일 레이아웃을 `docs/work/<작업-ID>/plan.md + work-log.md`로 바꾸고 완료 사이클 축약·스냅숏 항목을 삭제한다. 포트폴리오(`docs/status.md`) 행 추가·제거 시점(DES-05)을 §7에 둔다.
- 관련 요구사항과 설계: FR-02·03·04·06 / DES-02·03·04·05
- 변경 대상: `skills/wf-implement/SKILL.md`
- 의존성: 없음
- 위험: ADR-003의 단일 관문(§3.2) 배치는 유지해야 한다 — 채택 기준·최초 생성 문구는 남기고 재생성 의무만 바꾼다
- 검증 방법: TASK-07 VER-02·03·04
- 완료 조건: §3.2·§5·§7에 plan.md 저장소 관통 문구·스냅숏 의무·자동 재생성이 없고 새 레이아웃과 status 행 규칙이 있다

### TASK-03: wf-doc 식별자 규칙과 템플릿

- 상태: completed
- 완료: 2026-10-09 14:00
- 상위: 없음
- 목표: SKILL §2.6 문서 ID 목록의 `PLAN-<프로젝트-슬러그>`를 `PLAN-<작업-ID>`로, 추적표 예시 경로를 `./work/<작업-ID>/plan.md`로, TASK 작업 범위·경로 포함 링크 규칙(ADR-004) 한 줄 추가. templates.md의 plan 템플릿(문서 ID·저장 위치·축약형 노트·generated 노트), work-log 템플릿 스냅숏 노트 삭제, status 템플릿 저장 위치 문구, 필수 연결표 `plan` 행.
- 관련 요구사항과 설계: FR-03·04·05·08 / DES-03·04·06
- 변경 대상: `skills/wf-doc/SKILL.md`, `skills/wf-doc/references/templates.md`
- 의존성: 없음
- 위험: 완료 문서들이 `PLAN-llm-workflow`·`../../plan.md`를 링크한다(NFR-02: 내용 불변). TASK-05에서 plan.md를 제거하면 그 링크가 깨지므로 링크 수리 범위를 TASK-05에서 정한다
- 검증 방법: TASK-07 VER-03·04·07
- 완료 조건: AC-04의 템플릿 부분 충족, `mermaid`·`snapshot` 문구가 templates.md에 없음

### TASK-04: wf-design §6 문구

- 상태: completed
- 완료: 2026-10-09 14:00
- 상위: 없음
- 목표: §6의 "`docs/plan.md`와 작업 폴더의 `work-log.md`는 …" 문장을 "작업 폴더의 `plan.md`·`work-log.md`와 `docs/status.md`는 …"로 바꾼다.
- 관련 요구사항과 설계: FR-08 / DES-08
- 변경 대상: `skills/wf-design/SKILL.md`
- 의존성: 없음
- 위험: 없음(한 문장)
- 검증 방법: TASK-07 VER-07(grep `docs/plan.md` 0건)
- 완료 조건: wf-design에 `docs/plan.md` 언급 0건

### TASK-05: docs/plan.md → docs/status.md 전환

- 상태: completed
- 완료: 2026-10-09 14:01
- 상위: 없음
- 목표: `git rm docs/plan.md`, `docs/status.md`(`ST-llm-workflow`, 진행 중 작업만: 이 작업 `in-progress`, 다인 토론 `on-hold`) 신설, README 개요 절에 "완료 사이클은 `docs/work/`와 git 이력" 한 줄. 완료 문서의 `../../plan.md` 링크 수리(NFR-02 허용 범위).
- 관련 요구사항과 설계: FR-06·07·08, NFR-02 / DES-05·07
- 변경 대상: `docs/plan.md`(삭제), `docs/status.md`(신설), `README.md`, 완료 문서의 plan.md 링크(수리만)
- 의존성: TASK-02, TASK-03(status 템플릿·레이아웃 규칙이 먼저 확정)
- 위험: 완료 문서 링크 수리가 내용 변경으로 번지지 않도록 링크 대상만 바꾼다. 롤백: `git revert`(삭제·신설 모두 한 커밋에 담는다)
- 검증 방법: TASK-07 VER-05·07
- 완료 조건: AC-05 충족, 링크 수리 diff가 경로 치환뿐, 롤백 절차가 작업 기록에 있다

### TASK-06: ADR-003 부분 수정 표기와 등록부

- 상태: completed
- 완료: 2026-10-09 14:01
- 상위: 없음
- 목표: ADR-003 `## 대체 관계`에 관련 1항, `## 변경 이력`에 1행 추가. `docs/decisions.md` ADR-003 행의 대체·관련 열에 REQ-DESIGN-plan-relocation 링크 추가.
- 관련 요구사항과 설계: FR-10, NFR-02 / DES-09
- 변경 대상: `docs/work/20260814-wf-tree-triggers/ADR-003-트리거-단일-관문.md`, `docs/decisions.md`
- 의존성: TASK-04(스킬 문구 확정 후 ADR 문구 작성)
- 위험: NFR-02 예외는 2곳 추가뿐 — 기존 문장은 수정하지 않는다
- 검증 방법: TASK-07 VER-09(git diff 2곳 추가뿐)
- 완료 조건: AC-09 충족

### TASK-07: 검증·자체 리뷰·통합

- 상태: completed
- 완료: 2026-10-09 14:05
- 상위: 없음
- 목표: AC-01~09를 VER-01~09로 판정(명령·결과를 작업 기록에), wf-implement §3.5 자체 리뷰, 통합 상태 기록, 완료 보고. 계획 트리는 재생성하지 않는다(온디맨드 규칙의 자기 적용 — 목록 상태가 정본).
- 관련 요구사항과 설계: AC-01~09 전부 / DES 전부
- 변경 대상: `work-log.md`(검증 결과·완료 보고), 이 문서(상태 갱신)
- 의존성: TASK-01~06
- 위험: 어절 수 측정 방법이 기준선 조사와 다를 수 있다 — 변경 전·후를 같은 명령으로 측정해 기록한다
- 검증 방법: 링크 전수 검사 스크립트, grep, 어절·문자 측정, git diff
- 완료 조건: wf-implement §5 완료 조건(이 작업으로 바뀐 조건 적용) 충족

## 검증 계획

| VER | AC | 방법 |
|---|---|---|
| VER-01 | AC-01 | `grep -rin mermaid skills/` 0건(역사 언급 제외 판정 기록) |
| VER-02 | AC-02 | `grep -rn "갱신될 때마다\|같은 변경에서.*재생성" skills/` 0건, wf-tree 생성 시점 절 존재 |
| VER-03 | AC-03 | `grep -rn "스냅숏\|snapshot" skills/` 0건, `git diff --stat` 에 완료 work-log 4개 없음 |
| VER-04 | AC-04 | templates.md plan 절·wf-implement §7 레이아웃 통독 |
| VER-05 | AC-05 | `test ! -e docs/plan.md && test -e docs/status.md`, 작업 목록 행 검사 |
| VER-06 | AC-06 | 이 문서 존재·TASK-01 시작·`mermaid`/`snapshot` 0건 |
| VER-07 | AC-07 | 상대 링크 전수 검사 스크립트(skills·docs, 앵커 제외) 0건 |
| VER-08 | AC-08 | 변경 전·후 같은 명령으로 wf-tree 본문 어절·description 문자 수 측정 |
| VER-09 | AC-09 | decisions.md 행 검사, ADR-003 `git diff` 추가 2곳뿐 |

## 마이그레이션과 롤백

- 마이그레이션: TASK-05 — `docs/plan.md` 삭제와 `docs/status.md` 신설을 같은 변경에 담는다. 완료 사이클 7개의 내용은 옮기지 않는다(정본은 각 work-log).
- 롤백: 커밋 전에는 `git checkout -- docs/plan.md && rm docs/status.md`, 커밋 후에는 해당 커밋 `git revert`. 스킬 변경도 같은 커밋이므로 함께 되돌아간다.

## 인계

- 다음 단계 또는 워크플로우: 없음 — 작업 완료. 커밋·push는 사용자 요청 범위
- 시작 조건: 충족 — 기준선 v1(2026-10-09)
- 입력 문서와 기준선: [REQ-DESIGN-plan-relocation v1](./req-design.md), [ADR-004](./ADR-004-TASK-식별자-작업-범위.md)
- 완료된 항목: TASK-01~07
- 미완료 항목: 없음
- 차단 요인: 없음
- 다음 행동: [작업 기록](./work-log.md#완료-보고)의 완료 보고 참조

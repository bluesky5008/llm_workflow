# REQ-DESIGN-skill-diet: 스킬 다이어트·정리 — 요구사항·설계

> 문서 유형: `requirements, design`
> 작업 ID: `20261009-skill-diet`
> 상태: `approved`
> 기준선: `v1` (승인일 2026-10-09)
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [WORK-20261009-skill-diet: 작업 기록](./work-log.md), [조사 결과 적용 분석](../../research/20261009-research-application/application_analysis.md), [묶음 A — 스킬 다이어트 설계](../../research/20260919-aidlc-research/bundleA_skill_diet.md), [wf-tree 존치 판단](../../research/20260919-aidlc-research/wf-tree_verdict.md), [ADR-010: 스킬 문서의 계층 규칙](./ADR-010-스킬-문서-계층-규칙.md), [ADR-011: wf-tree 축소](./ADR-011-wf-tree-축소.md), [REQ-DESIGN-test-lifecycle](../20261009-test-lifecycle/req-design.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 사이클 4(분석 §5 후보 B) — 스킬 본문에서 절차 세부·표·템플릿·체크리스트를 references/scripts로 내리고(S4), 산재한 경고를 전용 절로 모으고(S5), wf-tree를 필수 게이트·스크립트 렌더링으로 축소하며(AI-16 잔여·S12), 재도입을 막는 스킬 린트(S13)를 둔다. 다른 묶음(A·C)의 본문 추가가 들어갈 어절 예산을 만드는 전제 사이클이다.
- 현재 결론 또는 상태: 기준선 v1 승인(2026-10-09) — Q-01~Q-04 전부 권장안(A). 본문 상한은 실측 기반 2,850/2,350/1,200/2,300. ADR-010(계층 규칙·린트)·ADR-011(wf-tree 축소) `approved`.
- 다음 행동: wf-implement 계획 수립 — 진행은 [작업 기록](./work-log.md).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | N/A | document | 이 작업의 루트 문서. 변경 대상이 스킬 본문의 구조이며 C층 훅 기준선과 시스템이 다르다(선례: [test-lifecycle](../20261009-test-lifecycle/req-design.md)) |
| input | related | [조사 결과 적용 분석](../../research/20261009-research-application/application_analysis.md) | §2.3, §3.2, §3.5, §5 후보 B, §6 | 사이클 편성의 입력. 불변 조사 기록이라 역방향 링크 없음 |
| input | related | [묶음 A — 스킬 다이어트 설계](../../research/20260919-aidlc-research/bundleA_skill_diet.md) | §0, §2.2, §3, §4, §5 | 판정 규칙 R1~R5·트리거 문장·경고 절 초안·린트 항목. 불변 기록, 역방향 링크 없음 |
| input | related | [wf-tree 존치 판단](../../research/20260919-aidlc-research/wf-tree_verdict.md) | §0, §3 | 기능별 존치·제외 판정. 불변 기록, 역방향 링크 없음 |
| input | related | [1차 대조](../../research/20260919-aidlc-research/llm_workflow_vs_papers_round1.md) | §2.3, §4 S12 | S12의 원문 근거(LoopsBench 의존 간선 F1 0.71). 불변 기록 |
| input | related | [REQ-DESIGN-test-lifecycle](../20261009-test-lifecycle/req-design.md) | NFR-02, DES-08 | 어절 상한·상쇄 방식의 선례. 완료·동결 문서라 역방향 링크 없음 |
| input | related | [ADR-006: 작업 기록 린트의 B층 배치](../20261009-worklog-diet/ADR-006-작업-기록-린트-B층.md) | 후속 작업 | "스킬 본문 린트 — 같은 scripts/ 관례 재사용"의 이행. 승인 문서라 역방향 링크 없음 |
| output | decision | [ADR-010: 스킬 문서의 계층 규칙](./ADR-010-스킬-문서-계층-규칙.md) | FR-01, FR-08, NFR-02, DES-01, DES-06 | 본문·references·scripts 분리 규칙과 린트 집행. `approved`(2026-10-09) |
| output | decision | [ADR-011: wf-tree 축소](./ADR-011-wf-tree-축소.md) | FR-04, FR-05, DES-04, DES-05 | 분기 템플릿 축소·노드 유형 이관·렌더 스크립트·깊이 상한. `approved`(2026-10-09) |
| output | implementation | [WORK-20261009-skill-diet: 작업 기록](./work-log.md) | document | 진행 기록. 구현 계획(`plan.md`)은 승인 후 wf-implement가 작성 |
| bidirectional | related | [ST-llm-workflow](../../status.md) | 작업 목록 | 포트폴리오 행 |

**산출물 위치에 대한 결정:** 선행 스킬 변경 작업들과 동일하게 작업 폴더의 통합 req-design 문서로 둔다. 승인 관문에서 사용자 확인을 받는다.

## 문제와 목적

9월 조사(round1 §2.2, 묶음 A §2.2)는 스킬 4종의 결함을 "길이"가 아니라 **위임되지 않은 세부(UD)**·**묻힌 경고(BG)**·**스크립트 부재(MUS)**로 판정했다. 10월 분석(§0-3, §3.2)은 wf-implement+wf-doc 본문 합이 사이클 3 상한(6,348)에 닿아 **본문에 문장을 더하는 모든 후속 항목(묶음 A·C)이 상쇄 없이는 들어갈 수 없음**을 확인했고, 사이클 순서를 9월 계획(A → B)에서 B → A로 뒤집었다. 사용자는 2026-10-09 후보 B를 선택했다.

이 사이클은 규칙을 더하지 않는다. 본문에 있는 것을 세 층으로 재배치하고(본문 = 판단 규칙·가드·라우팅·경고, references = 절차 세부·표·템플릿·체크리스트, scripts = 결정 없이 재현 가능한 작업), 재배치가 "삭제"가 되지 않도록 강제 트리거 문장과 린트로 고정한다. 예외는 wf-tree의 분기 템플릿 비게이트 행(삭제, 근거 [판정 보고서 ⑤](../../research/20260919-aidlc-research/wf-tree_verdict.md))과 S12 의존 복원 문장(추가, 약 25어절)뿐이다.

## 현재 상태 조사 (wf-design §4.1)

### 사실

- **기준선**: main `0962f3c`(2026-10-09, 사이클 3 완료 직후). 워킹트리는 미추적 조사 폴더 2개 외 clean. 어절(frontmatter 제외, `len(text.split())`): wf-implement 3,114 · wf-doc 3,221 · wf-tree 1,850 · wf-design 2,261(합 10,446). references: templates 2,740 · verification-depth 880 · design-change 1,184 · reverse-engineering 1,318 · worklog-style 588. 분석 문서의 수치와 일치.
- **절 단위 실측(이관 후보)** — 묶음 A §3.2 분류표는 8월 절 구조 기준이라 다시 쟀다.

| 스킬 | 절 | 어절 | 형태 | 판정(R1~R5) |
|---|---|---|---|---|
| wf-implement | wf-design과의 역할 경계 — 소유권 표 | 215(12행) | 표 | R3 — "판단이 필요하면 그 표를 읽고" 트리거가 이미 있음 → references |
| wf-implement | §3.5 자체 리뷰 문항 | 158(20문항) | 목록 | R2 → references |
| wf-implement | §2.4 결정 사다리, §3.2~3.4·3.6 골격, §7 저장 위치·불변식·인계 | 314 / 223·276·192·113 / 456 | 산문 | R1 — 본문 유지(묶음 A §3.2와 동일) |
| wf-doc | wf-design·wf-implement 경계 소유권 표 2개 | 205+201(12·11행) | 표 | R3 → references |
| wf-doc | §2.3 머리말 골격 코드블록 | 180 | 코드 | R2 → templates.md |
| wf-doc | §2.6 문서 연결 예시·식별자 목록 2개·추적표 코드블록 | 257+13 | 코드 | R2 → templates.md(문서 연결 예시는 templates에 이미 중복 존재) |
| wf-doc | §2.6 하이퍼링크 강제 규칙 12불릿 | 259 | 목록 | 분리 — 핵심 5개 본문, 세부 7개 references |
| wf-doc | §2.7 인계 블록·재개 프롬프트 코드블록 | 108 | 코드 | R2 → templates.md |
| wf-doc | §2.1 유형표(124), §2.4 상태표(108), §1·§3·§4 | — | 표·목록 | R1 — 공유 어휘·판단 규칙, 본문 유지 |
| wf-tree | §3 노드 유형 표 | 218(17행) | 표 | R2 → references |
| wf-tree | §4 분기 템플릿 표 | 199(12행) | 표 | 필수 게이트 3행 본문 유지, 비게이트 7행 삭제 |
| wf-tree | §7 매체·표기·완료 시점 세칙 + 대형 트리 대응 | 267+75 | 산문 | R4 → scripts/render.py + references |
| wf-tree | §9 자체 검토 9문항 | 102 | 목록 | R2 → references |
| wf-tree | §2 예시 트리 코드블록 | 70 | 코드 | R2 → references |
| wf-tree | §7 생성 시점, §5 단일 소스·저장 위치, §6, §8 | 60 / 173 / 84 / 183 | 산문 | R1 — 본문 유지 |

- **가드 문구**(`…지 않는다`·`생략하지`·`간주하지`·`대신하지` 포함 행): wf-design 18 · wf-implement 24 · wf-doc 35 · wf-tree 20. Rationalization Loophole 비해당(묶음 A §0-2)이 현재 기준선에서도 성립한다.
- **경고의 산재**(BG): `> **정본:**` 콜아웃 8곳(경계 절). "설계 승인은 실행 승인이 아니다"가 wf-design 경계 규칙 5항, wf-implement 경계 규칙 6항, wf-implement §2.3 끝 문장의 3곳에 반복. 전용 경고 절은 4스킬 모두 없음.
- **description 길이**: wf-design 301 · wf-implement 180 · wf-doc 362 · wf-tree 397자. 묶음 A가 지적한 wf-tree 913자는 사이클 1에서 이미 줄었다. 임계 1,024자 이내.
- **들어오는 앵커**(docs/·setup/·README·루트 SKILL.md·CLAUDE.global.md → skills/): 38종. 상위는 `wf-implement#7-작업-기록과-저장-위치`(12), `#33-구현`(8), `wf-design#6-산출물`(8), `#32-계획-수립`(6), `templates#구현-계획-plan`(5), `#24-최소-구현-원칙--ponytail-full-모드`(4), `wf-doc#추적-식별자`(4), `wf-tree#생성-시점`(3), `#5-데이터-모델과-식별자`(3), `#단일-소스-원칙`(2), `#7-렌더링`(2), `wf-implement#wf-design과의-역할-경계`(2). 완료 작업 기록은 동결(NFR-01)이므로 이 앵커들은 바뀌면 안 된다. 스킬 간 교차 앵커 58종 중 이관의 영향을 받는 것: `wf-doc#wf-design과의-경계`(2)·`#wf-implement와의-경계`(1)·`#추적-식별자`(4)·`#23-공통-머리말-작성`(2)·`#27-인계와-재개-지점-작성`(4)·`wf-tree#7-렌더링`(1)·`#생성-시점`(3) — 모두 H2/H3 제목을 유지하면 유효하다.
- **절 번호 참조**: CLAUDE.global.md·루트 SKILL.md가 "§2.4"·"§3.3", 훅 메시지 `resume.md`가 "§3.1"을 텍스트로 언급한다. 번호를 바꾸면 깨진다.
- **B층 선례**: `skills/wf-doc/scripts/lint_worklog.py`(ADR-006) — 표준 라이브러리, 헬퍼 `read_lines`·`outside_fences`·`headings`·`slug`·`anchors_of`·`section`, `Finding(path, line, level, code, msg)`, 출력 `경로:행: E|W Lx 메시지`, 오류 시 exit 1, 상한은 상단 상수. pytest 33(TST-02). ADR-006 후속 작업에 "스킬 본문 린트 — 같은 scripts/ 관례 재사용"이 명시돼 있다.
- **설치 구조**: `~/.claude/skills/wf-*`는 `skills/wf-*` 폴더별 junction(dir /AL 확인). 스킬 폴더 밖(`skills/scripts/`)의 파일은 설치되지 않으므로 9월 계획의 `skills/scripts/lint.py` 위치는 쓸 수 없다. 작업 중의 스킬 변경은 다른 저장소 세션에 즉시 노출된다.
- **사이클 1·2·3이 이미 처리한 것**: 트리 자동 재생성·완료 스냅숏·Mermaid 제거(wf-tree §7은 "Markdown 목록 + ASCII, 온디맨드"), `plan.md` 분리, 합본 work-log H2 8개 고정과 린트, `references/verification-depth.md`(트리거 문장 "표를 참조하지 않은 생략은 유효하지 않다"의 선례).
- **round1 재확인(분석 §6)**: S12의 근거는 LoopsBench 대조표 "Plan state(의존 누락) — `depends:` 표현은 있으나 복원을 강제·검증하는 절차 없음(부분)", 수치 의존 간선 F1 0.71. S6·S10은 묶음 A 항목, S15는 보류 유지 — 이 사이클 범위 밖.
- **테스트 자산**: TST-01 훅 러너 22 · TST-02 린트 pytest 33(`유지`, SHA `7395a99`), TST-03 pptx(`격리`). 콘솔 cp949 환경에서 Python 출력은 `PYTHONIOENCODING=utf-8` 또는 `sys.stdout.reconfigure`가 필요(린트 선례 있음).

### 해석

- 다이어트의 판정 축은 UD이므로 **"무엇이 판단 규칙이고 무엇이 세부인가"**가 기준이며 길이는 결과다. 경계 소유권 표는 묶음 A §0이 "판단 규칙이라 UD 아님"이라 했지만, 본문이 이미 "판단이 필요하면 그 표를 읽고"로 라우팅하고 있어 **R3(온디맨드 참조)** 성격이다. 번호 매긴 경계 적용 규칙(항상 적용)은 본문에 남긴다(Q-02).
- 실측 결과 분석 §5의 목표 어절(wf-implement 2,400)은 §2.4 결정 사다리·§3.2·§7 같은 R1 내용을 깎아야 도달한다. R1 삭제는 이 사이클의 목적(의미 불변)과 충돌하므로 **상한은 실측 기반**으로 둔다(Q-01). wf-doc 2,400은 실측(≈2,290)보다 느슨하고, wf-tree 1,000은 게이트·트리거·주의 절을 두면 미달(≈1,140)이다.
- 이관의 실패 모드는 "references가 읽히지 않음"(묶음 A §1.5-1)이다. 대응은 ① 이관마다 조건+명령형 트리거 문장, ② 린트가 링크되지 않는 references를 경고, ③ 준수율 관측은 코드 저장소 사이클(분석 §5 후보 D)로 — 이 저장소의 산문 작업으로는 측정이 안 된다.
- wf-tree의 비게이트 분기 템플릿은 wf-implement §3.3·§3.5·§4.2가 이미 규정한 것의 중복 표현이라 references로 옮길 가치도 없다(판정 보고서 ⑤). 삭제하되 삭제 목록을 ADR-011에 남긴다(Q-04).
- 렌더 스크립트가 의미 있으려면 트리의 모든 노드가 목록 항목이어야 한다. 현행 트리에 손으로 덧붙인 자식(예: "테스트: … (선행)")은 분기 템플릿 제안이 목록 없이 그려진 것이며, 단일 소스 원칙과 어긋난다. 스크립트 도입 후 트리는 `상위:` 필드가 있는 목록 항목만 그린다.
- 린트의 상한 초과는 경고가 아니라 **오류**여야 한다. 종단 분석(묶음 A §2.3)의 유일한 검증 개입 지점이 "도입 시점 차단"이기 때문이다. 상한값은 린트 상수이고 변경은 wf-design 경량 경로(ADR-006 방식).

### 가정

- 이 저장소의 사용자는 1인이며, 작업 중 다른 저장소에서 스킬을 로드하는 세션을 동시에 열지 않는다(junction 즉시 반영의 위험을 운영으로 회피).
- Python 3.13·pytest가 있다. 없는 환경의 대체(손 렌더·수동 검토)는 ADR-006과 같은 방식으로 규정한다.
- 묶음 A(강제 게이트)·C(자문 요청)의 본문 추가 추정 약 220어절(분석 §3.2)은 이 사이클이 만드는 예산(합 ≈1,800어절 감소) 안에 든다. 정확한 값은 그 사이클의 wf-design이 다시 잰다.
- 참조 준수율·토큰 감소의 효과 측정은 이 사이클의 인수 조건이 아니다(산문 저장소 한계, 분석 §4). 이 사이클은 구조·의미 불변·링크 무결·린트를 검증한다.

## 범위

### 포함

- `skills/wf-implement/` — 경계 소유권 표 → `references/boundaries.md`(신설), §3.5 문항 → `references/review-checklist.md`(신설), §3.2에 의존 복원 문장(S12), `## 주의` 절 신설, 트리거 문장
- `skills/wf-doc/` — 경계 소유권 표 2개 → `references/boundaries.md`(신설), §2.3·§2.6·§2.7 코드블록 → `references/templates.md`(공통 머리말·추적 식별자 목록·추적표·인계 블록 절 추가), 하이퍼링크 세부 규칙 → `references/linking.md`(신설), `## 주의` 절, 트리거 문장, 신설 `scripts/lint_skill.py` + `scripts/tests/test_lint_skill.py`
- `skills/wf-tree/` — §3 노드 유형 표·§9 자체 검토·§2 예시 → `references/node-templates.md`(신설), §7 렌더 세칙 → `references/rendering.md`(신설) + `scripts/render.py` + `scripts/tests/test_render.py`(신설), §4를 필수 게이트 3종으로 축소, 깊이 상한, `## 주의` 절, description 갱신
- `skills/wf-design/SKILL.md` — `## 주의` 절(산재 문장 이동), 경계 정본 콜아웃의 링크 갱신. 그 외 무변경
- `README.md` 실행 기준 절 — 계층 규칙(ADR-010) 포인터와 스킬 린트 실행 명령 1문단
- `docs/test-register.md` — TST-04(lint_skill pytest)·TST-05(render pytest) 등록
- [ADR-010](./ADR-010-스킬-문서-계층-규칙.md)·[ADR-011](./ADR-011-wf-tree-축소.md) 발행·등록, `docs/decisions.md`, `docs/status.md`
- 자기 적용 — 이 작업의 `plan.md` 계획 트리를 `render.py`로 재생성하고, 완료 시 스킬 린트 0 오류

### 제외

- 묶음 A 항목 전부(S9 Stop 훅·S20·S18·S19·S10·S3 잔여·S16·S6) — 다음 사이클. S6·S10의 round1 근거는 조사 절에 적어 두었다
- S21 자문 요청(묶음 C), S14 역공학 보강, S15 known failure modes(보류 유지), S17
- 스킬 린트 실행 자체의 테스트 대장 등록 — "테스트가 아닌 게이트를 대장에 두는가"는 묶음 A의 게이트 원천 질문(분석 §3.1)과 함께 결정. 이 사이클은 린트의 **pytest**만 등록하고 린트 실행 의무는 README에 둔다
- 린트 결과를 훅으로 집행(C층) — 묶음 A
- `lint_worklog.py` 검사 항목 변경 — 무변경(헬퍼 import만). `templates.md` 합본 work-log 절·H2 8개 무변경
- 완료된 작업 기록·선행 ADR·DCR의 소급 편집 — 동결(NFR-01). 들어오는 앵커 38종은 제목을 유지해 깨지지 않게 한다
- 참조 준수율·토큰 감소·규칙 준수율의 효과 측정 — 코드 저장소 사이클(분석 §5 후보 D)
- CLAUDE.global.md·루트 SKILL.md·`setup/hooks/` — 무변경(절 번호 유지로 호환)
- wf-design SKILL.md 본문의 다이어트 — references 위임이 끝나 있어 주의 절·링크 갱신만

## 기능 요구사항

| ID | 항목 | 내용 |
|---|---|---|
| FR-01 | 계층 규칙 | 스킬 문서는 세 층으로 나눈다 — 본문(SKILL.md): 항상 따르는 판단 규칙·소유권·금지·가드·라우팅·경고; references/: 특정 절차 실행 시에만 필요한 세부(템플릿·표기 세칙·체크리스트·표·예시); scripts/: 결정 없이 기계적으로 재현 가능한 작업. 판정 규칙 R1~R5와 이관 금지 목록(경계 적용 규칙, 가드 문구 전부, §2.3 자율·비가역 목록, §4 경미/중대 분기, 완료 조건, 경량 경로 조건, wf-tree 단일 소스 원칙·필수 게이트)은 [ADR-010](./ADR-010-스킬-문서-계층-규칙.md)이 정본이다. 이관한 내용에는 본문에 조건+명령형 트리거 문장을 남기고, "읽지 않은 행위는 수행하지 않은 것으로 간주한다"는 어법을 쓴다. 절차 세부·표기 세칙·템플릿은 이후 references에만 추가한다 |
| FR-02 | wf-implement 이관 | 경계 소유권 표(12행)를 `references/boundaries.md`로 옮기고 정본 콜아웃을 함께 옮긴다. 본문 경계 절에는 한 문단 요약·경계 적용 규칙 6항·반환 흐름과 트리거("소유권 판단이 필요하면 references/boundaries.md의 표를 읽는다")를 남긴다. §3.5 문항 20개를 `references/review-checklist.md`로 옮기고 본문에는 트리거("자체 리뷰를 시작할 때 이 파일을 읽고 전 항목을 확인한다. 읽지 않은 자체 리뷰는 수행하지 않은 것으로 간주한다")와 "발견한 문제는 수정하고 영향받는 검증을 다시 수행한다"를 남긴다. H2/H3 제목·번호는 바꾸지 않는다 |
| FR-03 | wf-doc 이관 | 경계 소유권 표 2개를 `references/boundaries.md`로(정본 콜아웃 포함, H3 제목 `wf-design과의 경계`·`wf-implement와의 경계`는 본문에 유지하고 적용 규칙 목록만 남김). §2.3 머리말 골격, §2.6 식별자 목록 2개·추적표 골격, §2.7 인계 블록·재개 프롬프트 형식을 `references/templates.md`의 새 절(공통 머리말 · 추적 식별자 목록 · 추적표 · 인계 블록)로 옮기고 목차에 추가한다. §2.6 문서 연결 예시 코드블록은 templates의 공통 문서 연결 절과 중복이라 삭제하고 링크로 대체한다. 하이퍼링크 강제 규칙은 핵심 5개(모든 참조는 링크 · 문서 연결 절 필수 · 역방향 링크 동시 추가 · 가상 링크 금지 · 루트·불변 문서 예외)를 본문에 두고 나머지 7개를 `references/linking.md`로 옮긴다. 각 이관 자리에 트리거 문장을 둔다. `#추적-식별자`·`#23-공통-머리말-작성`·`#27-인계와-재개-지점-작성` 앵커는 유지한다 |
| FR-04 | wf-tree 축소 | §3 노드 유형 표를 `references/node-templates.md`로 옮기고 본문에는 "노드 유형은 references 표를 따르며 새 유형을 만들지 않는다"와 ★ 게이트 유형(`approve`·`release`·`migrate`)만 남긴다. §4 분기 템플릿은 필수 게이트 3종(`release` → 부모 `approve` 필수, `migrate` → 롤백 준비 + `verify` 필수, 포트폴리오 최초 생성 → `approve` 필수)만 남기고 비게이트 7행은 삭제한다(제목 `## 4. 필수 게이트`). §9 자체 검토 문항과 §2 예시 트리를 references로 옮기고 §9에는 트리거를 남긴다. 작업 내부 트리의 분해 깊이는 상한을 두며(Q-03, 제안: 작업 → TASK → 하위 항목의 2단계) 초과가 필요하면 TASK를 분할한다. description의 "분기 템플릿으로 누락 항목 제안"을 게이트 3종으로 고친다 — [ADR-011](./ADR-011-wf-tree-축소.md) |
| FR-05 | 렌더 스크립트 | `skills/wf-tree/scripts/render.py`가 `plan.md`(`## 작업 목록`의 `### TASK-NN: 제목`과 `상태`·`완료`·`상위`·`의존성` 필드) 또는 `status.md`(작업 목록 표)를 읽어 현행 §7 표기(`[✓]`·`[▶]`·`[ ]`, ★ 게이트, `depends:` 우측 주석, 완료 시점, 롤업 `(n/m)`, `⚠ blocked N`, 완료 서브트리 접기)로 ASCII 트리를 출력한다. 뷰 옵션 전체·활성 경로·남은 항목·특정 가지, `--write`로 `## 계획 트리` 절의 펜스와 `<!-- generated: YYYY-MM-DD HH:MM -->`를 교체한다. 깊이 상한 초과·`상위` 대상 없음은 경고한다. 표준 라이브러리만 쓴다. 본문 §7에 트리거("트리를 생성·재생성할 때는 scripts/render.py를 실행한다. 손으로 그리거나 고치지 않는다. Python을 쓸 수 없으면 references/rendering.md의 표기로 손 렌더하고 generated 주석에 그 사실을 적는다")를 둔다. 스크립트가 정하지 못하는 규칙(매체 선택 이유·표기 어휘의 의미·뷰의 용도)은 `references/rendering.md`에 둔다 |
| FR-06 | 의존 복원 자기 검토(S12) | wf-implement §3.2 "작업 간 의존성" 항목에 "수정 파일이 겹치거나 심볼을 참조하는 작업 쌍은 `depends:` 후보로 검출해 기록하거나 제외 이유를 적는다"는 한 문장을 추가하고, wf-tree 자체 검토(references)에 같은 문항을 둔다 |
| FR-07 | 경고 절(S5) | 4스킬에 경계 절 다음·§1 앞에 `## 주의 — 자주 틀리는 것` 절을 두고 산재한 경고를 모은다. 내용은 DES-07. "설계 승인은 실행 승인이 아니다"의 정본은 wf-implement 주의 절 1곳이며, wf-design 경계 규칙 5항·wf-implement 경계 규칙 6항은 한 문장으로 줄이고 정본을 링크한다. 신규 문장은 스킬당 2개 이내(순증 ≤ 50어절) |
| FR-08 | 스킬 린트(S13) | `skills/wf-doc/scripts/lint_skill.py`가 `skills/*/SKILL.md`(인자 없음: 저장소의 전부, 인자: 지정 파일)를 검사한다. K1 frontmatter `name` ≤ 64자·`description` ≤ 1,024자(E), 900자 초과(W). K2 description의 XML 태그·경로의 백슬래시(E). K3 본문 어절 > 스킬별 상한(E), 상한의 95% 초과(W) — 상한은 상단 상수(Q-01 값, 목록에 없는 스킬은 5,000). K4 SKILL.md와 references/*.md의 상대 링크 대상 파일·앵커 부재(E). K5 어디서도 링크되지 않는 references/*.md(W). K6 본문의 표 ≥ 10행 또는 코드블록 ≥ 12행(W "references 이관 검토"). K7 `## 주의` 절 부재(E), 가드 문구 패턴 0회(W). 출력·exit 규약은 `lint_worklog.py`와 같고 헬퍼는 import로 재사용한다. pytest는 K1~K7마다 실패·통과 입력을 둔다(≥ 14). README에 실행 명령과 시점(SKILL.md·references 변경 커밋 전)을 적는다 |
| FR-09 | 앵커·링크 보존 | 들어오는 앵커 38종(조사 절)이 가리키는 H2/H3 제목과 번호를 바꾸지 않는다. 이관으로 바뀌는 교차 링크(정본 콜아웃 4곳 등)는 같은 변경에서 갱신한다. 완료 작업 기록·선행 ADR·DCR은 수정하지 않는다 |
| FR-10 | 자기 적용 | 이 작업의 `plan.md` 계획 트리는 최초 작성 시 현행 규칙으로 1회 생성하고, `render.py` TASK 완료 후 스크립트로 재생성해 결과를 작업 기록에 남긴다. 완료 전 `lint_skill.py`·`lint_worklog.py` 0 오류. TST-04·05를 같은 SHA 2회 통과로 `유지` 등록 |
| FR-11 | ADR 발행·등록 | ADR-010·011을 `proposed`로 발행하고 승인 시 `approved`. 번호는 main 등록부 마지막(ADR-009)의 다음 |

## 비기능 요구사항

| ID | 항목 | 내용 |
|---|---|---|
| NFR-01 | 완료 기록 불변 | 완료된 작업 기록·선행 req-design·ADR·DCR의 내용을 소급 수정하지 않는다. 역방향 링크 행 추가도 이 사이클은 하지 않는다 |
| NFR-02 | 본문 어절 상한 | 작업 완료 시 본문 어절(같은 측정 방법)이 wf-implement ≤ 2,850 · wf-doc ≤ 2,350 · wf-tree ≤ 1,200 · wf-design ≤ 2,300(Q-01). 합 ≤ 8,700(현재 10,446, −17%). 린트 K3가 같은 값으로 집행한다 |
| NFR-03 | 의미 불변 | 본문에서 사라지는 문장은 references로 옮겨지거나(이동) 삭제 목록과 사유가 ADR-011·작업 기록 `## 설계와 달라진 점`에 있다(삭제). 가드 문구 행 수는 스킬마다 작업 전 값(18/24/35/20) 이상이다. 새 규칙은 FR-06의 한 문장과 FR-07의 주의 절 신규 문장뿐이다 |
| NFR-04 | 링크 무결 | 스킬·references·docs/의 상대 링크와 앵커가 전부 유효하다(lint_skill K4, lint_worklog L6, docs/ 전수 grep). 들어오는 앵커 38종 유지 |
| NFR-05 | 기존 테스트 무변경 통과 | TST-01 22/22, TST-02 33/33. `lint_worklog.py`와 그 pytest는 변경하지 않는다 |
| NFR-06 | 도구 비의존 | 스크립트 2종은 Python 3 표준 라이브러리만 쓴다. Python 부재 시 손 렌더·수동 검토로 대체하고 그 사실을 기록한다(ADR-006 방식). 훅·하네스 변경 없음 |
| NFR-07 | references 분량 | 신설 references 파일은 각 120행 이내. `templates.md` 증가분은 이관한 코드블록 분량 + 절 제목·노트 이내 |
| NFR-08 | 콘솔 인코딩 | 스크립트 출력은 cp949 콘솔에서 `UnicodeEncodeError` 없이 동작한다(`sys.stdout.reconfigure` 선례) |

## 인수 조건

| ID | 조건 |
|---|---|
| AC-01 | wf-implement `references/boundaries.md`에 12행 소유권 표와 정본 콜아웃이 있고, 본문 경계 절에 표가 없으며 트리거 문장과 적용 규칙 6항이 있다. `references/review-checklist.md`에 20문항이 있고 §3.5에 트리거 문장이 있다(FR-02). §2.4·§3.1·§3.3·§3.5·§7 등 들어오는 앵커 38종이 모두 유효하다(FR-09) |
| AC-02 | wf-doc `references/boundaries.md`에 표 2개, `references/templates.md`에 공통 머리말·추적 식별자 목록·추적표·인계 블록 절과 목차 항목, `references/linking.md`에 세부 규칙 7개가 있고, 본문 §2.3·§2.6·§2.7에 해당 코드블록이 없으며 핵심 5개 규칙과 트리거 문장이 있다(FR-03). 합본 work-log 템플릿의 H2 8개와 `lint_worklog.py`는 `git diff`에서 무변경이다(NFR-05) |
| AC-03 | wf-tree 본문 §3에 노드 유형 표가 없고 게이트 3종 문장이 있으며, §4가 필수 게이트 3행만 담고, §2에 깊이 상한 문장이, §7에 render.py 트리거와 손 렌더 대체 규정이, §9에 트리거가 있다. `references/node-templates.md`(유형 표·자체 검토 문항·예시)와 `references/rendering.md`가 있다. description에 "분기 템플릿" 제안 문구가 없다(FR-04) |
| AC-04 | `python skills/wf-tree/scripts/render.py docs/work/20261009-skill-diet/plan.md`가 목록의 TASK 전부를 `[✓]`·`[▶]`·`[ ]`와 `depends:`·완료 시점으로 출력하고, `--write`가 `## 계획 트리` 절의 펜스와 generated 일시를 교체하며, 깊이 상한 초과 입력에 경고를 낸다. pytest ≥ 10 통과(FR-05) |
| AC-05 | wf-implement §3.2에 의존 후보 검출 문장이, `references/node-templates.md` 자체 검토에 같은 문항이 있다(FR-06) |
| AC-06 | 4스킬에 `## 주의 — 자주 틀리는 것` 절이 경계 절 다음에 있고 내용이 DES-07과 같다. "설계 승인은 실행 승인이 아니다" 정본이 wf-implement 주의 절 1곳이고 다른 2곳은 링크다(FR-07) |
| AC-07 | `python skills/wf-doc/scripts/lint_skill.py`가 인자 없이 4스킬을 검사해 exit 0이고, K1~K7 각각의 실패 입력에서 해당 코드를 내는 pytest ≥ 14가 통과한다. README 실행 기준에 명령과 시점이 있다(FR-08) |
| AC-08 | 어절 측정(조사 절과 같은 함수)이 wf-implement ≤ 2,850 · wf-doc ≤ 2,350 · wf-tree ≤ 1,200 · wf-design ≤ 2,300이고, 가드 문구 행 수가 18/24/35/20 이상이다(NFR-02·03) |
| AC-09 | 삭제한 문장 목록(wf-tree 분기 템플릿 7행, 중복 문서 연결 예시, 정본 요약으로 줄인 반복 문장)이 ADR-011 또는 작업 기록 `## 설계와 달라진 점`에 있고, 그 외 본문에서 사라진 문장은 references에서 grep으로 찾을 수 있다(NFR-03) |
| AC-10 | `lint_skill.py` K4·`lint_worklog.py` L6이 0 오류이고, docs/·README·setup/에서 skills/로 향하는 링크를 grep해 깨진 앵커가 0이다(NFR-04). 완료 기록·선행 ADR·DCR의 `git diff`가 무변경이다(NFR-01) |
| AC-11 | TST-01 22/22, TST-02 33/33 통과. 대장에 TST-04(`python -m pytest skills/wf-doc/scripts/tests -q`의 lint_skill 부분 또는 분리 명령)·TST-05(`python -m pytest skills/wf-tree/scripts/tests -q`)가 `유지`로 있고 마지막 성공 SHA가 있다(NFR-05, FR-10) |
| AC-12 | `docs/decisions.md`에 ADR-010·011 행이 `approved`로 있다(FR-11). 신설 references 각 120행 이내, `wc -l`(NFR-07) |

## 설계

| ID | 설계 요소 | 내용 |
|---|---|---|
| DES-01 | 계층 규칙과 집행 | [ADR-010](./ADR-010-스킬-문서-계층-규칙.md): 세 층의 정의, R1~R5, 이관 금지 목록, 트리거 문장 의무, 본문 상한과 린트 집행, "세부는 references에만 추가" 규칙. README 실행 기준에 ADR 포인터 1문단 + 린트 명령. 스킬 본문에는 이 규칙을 적지 않는다(스킬 사용자가 아니라 스킬 유지자의 규칙) |
| DES-02 | wf-implement 구조(후) | `SKILL.md`(절 번호 불변) + `references/{verification-depth, boundaries, review-checklist}.md`. 경계 절: 한 문단 요약 → 적용 규칙 6항 → 반환 흐름 → 트리거. §3.5: 트리거 2문장 + 문제 수정 문장. §3.2: S12 문장. `## 주의` 절은 wf-doc 경계 절 뒤·§1 앞 |
| DES-03 | wf-doc 구조(후) | `SKILL.md` + `references/{templates, boundaries, linking, worklog-style}.md` + `scripts/{lint_worklog, lint_skill}.py`. templates.md 목차에 공통 머리말(§2.3 코드블록)·추적 식별자 목록(§2.6 코드블록 2개)·추적표(§2.6 골격)·인계 블록(§2.7 코드블록 2개) 절 추가. 본문 §2.6 `#### 추적 식별자`는 제목·규칙 불릿 유지. linking.md: 승인 문서 역링크 처리·불변 문서 단방향·합본 앵커·이동 시 검색·`관련 문서`와 `문서 연결` 정합·대상 항목 표기·관계 어휘 설명 |
| DES-04 | wf-tree 구조(후) | `SKILL.md` 절: 헌장과 역할 경계 · 주의 · 1 적용 시점 · 2 트리 모델(깊이 상한 포함, 예시 제거) · 3 노드 유형(포인터 + ★ 3종) · 4 필수 게이트(3행 표) · 5 데이터 모델과 식별자 · 6 상태와 롤업 · 7 렌더링(매체 1문단 · 생성 시점 · 스크립트 트리거 · 손 렌더 대체) · 8 포트폴리오 · 9 자체 검토(트리거). `references/node-templates.md`(유형 표 15행 + 기존 생태계 매핑, 자체 검토 10문항 — 기존 9 + S12, 예시 트리), `references/rendering.md`(표기 어휘와 의미, 완료 시점 파생 규칙, 뷰 4종, 접기 규칙, 손 렌더 시 준수 표기), `scripts/render.py`, `scripts/tests/test_render.py` — [ADR-011](./ADR-011-wf-tree-축소.md) |
| DES-05 | render.py 계약 | 입력: 파일 경로 1개. `plan.md`는 `## 작업 목록` 아래 `### TASK-NN: 제목` 블록의 `상태`·`완료`·`상위`·`의존성` 필드(`없음` 허용), `status.md`는 `## 작업 목록` 표의 작업 ID·제목·상태·의존 열. 루트 라인은 문서 제목의 작업 ID·제목과 롤업 `(완료/전체)`. 자식은 `상위` 체인으로 중첩, 같은 부모 안에서는 목록 순서. ★은 제목이 `승인:`·`릴리스:`·`전환:`으로 시작하는 항목. 옵션 `--view all|active|remaining|branch=TASK-NN`(기본 active: 루트→진행 중 경로만 전체 깊이, 나머지 깊이 1 요약), `--write`(`## 계획 트리` 절의 첫 펜스와 generated 주석 교체, 절이 없으면 `## 작업 목록` 앞에 삽입), `--depth N`(상한, 기본 2). 경고: 상위 대상 없음·순환·깊이 초과·상태 어휘 오류(W, exit 0), 파일·절 없음(E, exit 1). 표준 라이브러리, stdout utf-8. pytest: 파싱 2·중첩 2·접기 1·뷰 2·depends 1·완료 시점 1·write 1·경고 2 |
| DES-06 | lint_skill.py 계약 | 대상 결정: 인자 없음 → 저장소 루트(`skills/` 탐색, 상위 3단계) 아래 `skills/*/SKILL.md` 전부. 검사 K1~K7(FR-08), 상한 상수 `MAX_BODY_WORDS = {"wf-implement": 2850, "wf-doc": 2350, "wf-tree": 1200, "wf-design": 2300}`·`DEFAULT_MAX = 5000`·`WARN_RATIO = 0.95`·`MAX_TABLE_ROWS = 10`·`MAX_CODE_LINES = 12`·`GUARD_RE`. 어절은 frontmatter 제외 `len(text.split())`. 앵커 검사는 `lint_worklog.anchors_of`·`slug` import. `Finding` 출력 형식·exit 규약 동일. pytest는 임시 디렉터리에 가짜 스킬 폴더를 만들어 K코드별 실패·통과 쌍 |
| DES-07 | 주의 절 내용 | **wf-implement**: ① 설계 승인은 실행 승인이 아니다 — push·병합·배포·삭제는 별도 승인(§2.3). 이 문장이 정본 ② 실행하지 못한 검증을 성공으로 보고하지 않는다(§2.5) ③ 문서 상태 `completed`와 작업 완료는 다르다 ④ 대장 `유지` 행의 테스트를 수정·제외해 통과시키지 않는다(§3.3) ⑤ references를 읽지 않은 자체 리뷰·검증 생략은 수행하지 않은 것이다. **wf-doc**: ① 하이퍼링크 규칙을 하나라도 어긴 문서는 완료로 표시하지 않는다 ② 템플릿을 채운 사실이 승인·완료를 만들지 않는다 ③ `TBD`를 지우려고 내용을 지어내지 않는다 — 책임자·해소 조건을 남긴다 ④ 승인·검증·완료를 대신 선언하지 않는다. **wf-tree**: ① `depends:` 점선의 화살표 머리는 대기자 쪽 — UML과 반대 ② 부모-자식은 분해이지 순서가 아니다 ③ 롤업은 표시 전용이며 상태 필드를 바꾸지 않는다 ④ 트리를 손으로 고치지 않는다 — 목록을 고치고 재생성한다. **wf-design**: ① 설계 승인은 실행 승인이 아니다(정본 링크) ② 승인 이외의 응답에서 구현을 시작하지 않고 `approved`를 적지 않는다 ③ 프로토타입은 제품 구현이 아니다. 각 항목은 기존 문장의 이동이며 신규는 wf-implement ⑤·wf-tree ④뿐 |
| DES-08 | S12 문장 | wf-implement §3.2 목록의 "작업 간 의존성" 항목을 "작업 간 의존성 — 수정 파일이 겹치거나 심볼을 참조하는 작업 쌍은 `depends:` 후보로 검출해 기록하거나 제외 이유를 적는다"로 확장. node-templates.md 자체 검토에 "파일 겹침·심볼 참조로 검출한 `depends:` 후보가 목록에 반영되었거나 제외 이유가 있는가" |
| DES-09 | 트리거 문장 목록 | 이관 1건당 1문장, 조건+명령+불이행 효과. wf-implement 경계·§3.5(FR-02), wf-doc §2.3·§2.6·§2.7·경계(FR-03), wf-tree §3·§7·§9(FR-04·05). 어법은 §3.4의 선례("표를 참조하지 않은 생략은 이유를 적어도 유효하지 않다")를 따른다 |
| DES-10 | 앵커 보존 전략 | 유지 목록 = 조사 절의 38종 + 교차 58종의 H2/H3 제목. 갱신 대상 = 정본 콜아웃 4곳(wf-design 2, wf-implement 1, wf-doc 2의 표 링크)·templates.md에서 본문 코드블록을 가리키던 링크·README. 검증 = lint_skill K4 + `grep -rhoE "skills/.*#"` 전수 대조 |
| DES-11 | 측정·자기 적용 | 어절 측정 함수는 사이클 3과 동일(조사 절). 작업 전 값은 이 문서에 고정. 이관 대조는 TASK별 수행 기록 `발견 사항`에 "이동 N문장 / 삭제 N문장(사유 위치)"로 요약하고 삭제 목록은 ADR-011·`## 설계와 달라진 점`에. 계획 트리는 FR-10 |
| DES-12 | ADR | ADR-010(계층 규칙·린트 집행)·ADR-011(wf-tree 축소: 게이트 3종·유형 이관·렌더 스크립트·깊이 상한). ADR-003(트리거 단일 관문)·ADR-006(B층 배치)은 유지되며 관련 관계만 기록 |

제외한 설계 항목: 보안·개인정보·데이터 마이그레이션은 변경 대상이 산문 규칙·문서·표준 라이브러리 스크립트라 적용되지 않는다(N/A). 롤백은 `git revert`로 충분하며 신설 파일은 되돌리면 사라진다. junction 즉시 반영은 가정 1항으로 회피한다.

### 검증 전략

- AC-01·02·03·05·06·09·12: 변경 후 해당 절 통독과 grep. 산문·템플릿이라 TDD 부적용 — 사유를 작업 기록에 남기고 후행 검증으로 대체
- AC-04·07: 스크립트 2종은 TDD 적용(실패하는 pytest 먼저). `python -m pytest skills/wf-tree/scripts/tests -q`, `python -m pytest skills/wf-doc/scripts/tests -q`, 스크립트 직접 실행
- AC-08·10·11: 어절 측정 스크립트, `lint_skill.py`·`lint_worklog.py` exit code, 링크 전수 grep, `git diff --stat`, TST-01·02 실행

## 가정과 미해결 질문

| ID | 질문 | 권장 | 근거 | 결정(2026-10-09) |
|---|---|---|---|---|
| Q-01 | 본문 어절 상한 — (A) 실측 기반 wf-implement 2,850 · wf-doc 2,350 · wf-tree 1,200 · wf-design 2,300, (B) 분석 §5 제안 2,400 · 2,400 · 1,000 · (없음) | **(A)** | 실측(조사 절 표): wf-implement 이관 가능분은 경계표 215 + §3.5 158 = 373이고 트리거·주의·S12로 약 110이 돌아와 ≈2,850. 2,400은 §2.4 사다리(314)·§3.2(223)·§7(456) 같은 R1 내용을 깎아야 하며 의미 불변(NFR-03)과 충돌. wf-tree는 게이트 표·트리거·주의·깊이 상한으로 ≈1,140이라 1,000 미달. wf-doc은 ≈2,290으로 어느 쪽이든 충족. (A)의 합 8,700은 현재 대비 −17%이고 묶음 A·C 추가분(≈220)을 수용 | **(A)** — 상한은 린트 상수, 이후 조정은 경량 경로 |
| Q-02 | 경계 소유권 표 3개의 이관 — (A) 전부 references로 옮기고 정본 콜아웃도 이동, 본문에는 적용 규칙·트리거, (B) 본문 유지(묶음 A §0 "판단 규칙이라 UD 아님") | **(A)** | 본문이 이미 "판단이 필요하면 그 표를 읽고"로 온디맨드 참조를 지시한다(R3). 표 3개 621어절은 이 사이클 예산의 1/3이다. 정본 콜아웃 4곳의 링크 갱신으로 정본 위치는 명확히 남는다 | **(A)** |
| Q-03 | wf-tree 작업 내부 트리의 깊이 상한 — (A) 2단계(작업 → TASK → 하위 항목), (B) 3단계, (C) 상한 없음(현행) | **(A)** | 판정 보고서 §3 "분해 깊이 상한(예: 작업 내부 2단계)", Horizon Gap의 과분해 경고. 저장소 plan.md 3개의 실제 깊이는 전부 2 이내. 초과가 필요하면 TASK 분할이 wf-implement §3.2 "독립적으로 구현·검증할 수 있는 크기"와 일치 | **(A)** 2단계 — render.py `--depth` 기본값 2 |
| Q-04 | 분기 템플릿 비게이트 7행 — (A) 삭제(판정 보고서 ⑤ — wf-implement 규정의 중복 표현), (B) references로 이동해 제안 기능 유지 | **(A)** | `implement`→`test`+`review`, 버그 수정→재현 테스트, 공개 계약→`document`+`verify`, 신뢰 경계→보안 `test`, 기준선 충돌→`change`, `design`→`review`+`approve`, 대안 경쟁→`decide`는 전부 wf-implement §2.4·§3.3·§3.5·§4.2·wf-design §3.3·§4.5·§8이 이미 규정. 트리에만 있는 제안은 목록 없는 노드를 만들어 단일 소스 원칙과 충돌(조사 절 해석). 삭제 목록은 ADR-011에 보존 | **(A)** |

가정은 조사 절 참조. 낮은 위험이라 질문으로 올리지 않은 것: 린트 상한 초과를 오류(E)로 두는 것(종단 분석 근거), 린트 위치 `skills/wf-doc/scripts/`(ADR-006 후속 작업 명시·junction 제약), ★ 게이트 노드의 제목 접두 규약.

## 위험

| ID | 위험 | 영향 | 완화 |
|---|---|---|---|
| RISK-01 | 이관이 삭제가 됨 — references를 읽지 않음 | 규칙 준수율 저하 | 트리거 문장(DES-09) + 린트 K5 + 주의 절 ⑤. 준수율 관측과 롤백 판단(절반 미만이면 본문 복귀)은 후보 D 사이클 |
| RISK-02 | 앵커 깨짐 — 제목 변경·절 이동 | 완료 기록·훅 메시지·CLAUDE.global의 참조 무효 | 유지 목록 고정(DES-10), K4·L6·전수 grep, 절 번호 불변 |
| RISK-03 | render.py가 현행 트리 표기를 재현하지 못함 | 트리 품질 저하·손 렌더 복귀 | 현행 §7 표기를 rendering.md에 먼저 옮기고 그 표기로 pytest 골든 작성(TDD). 손 렌더 대체 규정은 예외 경로 |
| RISK-04 | 상한을 맞추려 R1 문장을 깎음 | 규칙 손실 | NFR-03 가드 수 비감소·삭제 목록 의무, 상한은 실측 기반(Q-01 A). 미달 시 상한 조정(경량 경로)을 삭제보다 우선 |
| RISK-05 | junction 즉시 반영 — 작업 중 반쯤 바뀐 스킬이 다른 세션에 로드 | 다른 저장소 작업의 규칙 혼선 | 가정 1항(동시 세션 없음), TASK 단위로 일관 상태 유지, 커밋은 완료 후 |
| RISK-06 | lint_skill이 lint_worklog 헬퍼에 결합 | 한쪽 변경이 다른 쪽을 깨뜨림 | import 대상을 파서 헬퍼 6개로 한정, 양쪽 pytest가 대장 `유지` |
| RISK-07 | 산문 저장소라 효과(토큰·준수율)가 관측되지 않음 | 다이어트의 가치 미실증 | 범위에서 명시적으로 제외, 후보 D에서 측정(분석 §4) |

## 추적성

| 요구사항 | 설계 | 검증 | 작업 |
|---|---|---|---|
| FR-01 | DES-01, DES-09 | AC-07, AC-09 | [TASK-01~08](./plan.md#작업-목록) |
| FR-02 | DES-02, DES-09, DES-10 | AC-01 | [TASK-03, TASK-04](./plan.md#작업-목록) |
| FR-03 | DES-03, DES-09, DES-10 | AC-02 | [TASK-01, TASK-02](./plan.md#작업-목록) |
| FR-04 | DES-04, DES-09 | AC-03 | [TASK-06, TASK-07](./plan.md#작업-목록) |
| FR-05 | DES-04, DES-05 | AC-04 | [TASK-06](./plan.md#작업-목록) |
| FR-06 | DES-08 | AC-05 | [TASK-04, TASK-06](./plan.md#작업-목록) |
| FR-07 | DES-07 | AC-06 | [TASK-02, TASK-04, TASK-05, TASK-07](./plan.md#작업-목록) |
| FR-08 | DES-06 | AC-07 | [TASK-08](./plan.md#작업-목록) |
| FR-09 | DES-10 | AC-01, AC-10 | [TASK-02, TASK-04, TASK-05, TASK-07, TASK-09](./plan.md#작업-목록) |
| FR-10 | DES-11 | AC-04, AC-11 | [TASK-09](./plan.md#작업-목록) |
| FR-11 | DES-12 | AC-12 | [TASK-09](./plan.md#작업-목록) |
| NFR-01 | DES-10 | AC-10 | [TASK-09](./plan.md#작업-목록) |
| NFR-02 | DES-01, DES-06, DES-11 | AC-08 | [TASK-02, TASK-04, TASK-05, TASK-07, TASK-09](./plan.md#작업-목록) |
| NFR-03 | DES-07, DES-11 | AC-08, AC-09 | [TASK-02, TASK-04, TASK-05, TASK-07, TASK-09](./plan.md#작업-목록) |
| NFR-04 | DES-10 | AC-10 | [TASK-08, TASK-09](./plan.md#작업-목록) |
| NFR-05 | DES-03, DES-06 | AC-02, AC-11 | [TASK-08, TASK-09](./plan.md#작업-목록) |
| NFR-06 | DES-05, DES-06 | AC-04, AC-07 | [TASK-06, TASK-08](./plan.md#작업-목록) |
| NFR-07 | DES-02, DES-03, DES-04 | AC-12 | [TASK-01, TASK-03, TASK-06](./plan.md#작업-목록) |
| NFR-08 | DES-05, DES-06 | AC-04, AC-07 | [TASK-06, TASK-08](./plan.md#작업-목록) |

작업 열은 [PLAN-20261009-skill-diet 작업 목록](./plan.md#작업-목록)의 TASK다(2026-10-09 기입, 선례: [test-lifecycle 추적표](../20261009-test-lifecycle/req-design.md#추적성)).

## 승인 기록

| 기준선 | 일자 | 결과 | 근거 |
|---|---|---|---|
| v1 | 2026-10-09 | 승인 | 대화형 승인 관문에서 사용자 응답 "승인" — Q-01~Q-04 권장안(A), ADR-010·011, 산출물 위치(작업 폴더 통합 문서) 포함 |

## 인계

- 다음 단계 또는 워크플로우: wf-implement(계획 수립, [wf-implement §1](../../../skills/wf-implement/SKILL.md#1-시작-조건)) — 진행 상태는 [작업 기록](./work-log.md)
- 시작 조건: 충족 — 이 문서 v1 승인(2026-10-09)
- 입력 문서와 기준선: 이 문서 v1, [ADR-010](./ADR-010-스킬-문서-계층-규칙.md)·[ADR-011](./ADR-011-wf-tree-축소.md)(approved)
- 완료된 항목: §4.1 조사, 요구사항·설계·위험·추적표, ADR 2건, §4.5 일관성 검토, Q-01~04 확정, 기준선 v1 승인
- 미완료 항목: 없음
- 차단 요인: 없음

## 변경 이력

| 날짜 | 변경 | 근거 | 상태 또는 기준선 | 작성자·승인자 |
|---|---|---|---|---|
| 2026-10-09 | 최초 작성 — 조사(절 단위 실측, 앵커 38종, 가드 수, round1 S12 근거), 범위, FR-01~11, NFR-01~08, AC-01~12, DES-01~12, Q-01~04, RISK-01~07, 추적표. ADR-010·011 초안과 함께 §4.5 검토 후 승인 요청 | 사용자 후보 B 선택(2026-10-09), 분석 §5, 묶음 A §3~§5, wf-tree 판정 §3 | draft → awaiting-approval | Claude(작성) |
| 2026-10-09 | 기준선 v1 승인. Q-01~Q-04 권장안(A) 확정, ADR-010·011 승인 | 대화형 승인 관문 사용자 응답 "승인" | awaiting-approval → approved, v1 | 사용자(승인) |
| 2026-10-09 | 추적표 작업 열 기입(TASK-01~09). 기준선 의미 변경 없음 | wf-implement §3.2 계획 수립·§3.6 통합 | approved 유지 | Claude(작성) |

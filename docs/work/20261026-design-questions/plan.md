# PLAN-20261026-design-questions: 구현 계획 — 설계 질문 단계와 근거 강제 적대 검토

> 문서 유형: `plan`
> 작업 ID: `20261026-design-questions`
> 상태: `in-progress`
> 기준선: [REQ-DESIGN-design-questions](./req-design.md) `v1` (승인일 2026-10-26)
> 작성일: 2026-10-26
> 최종 갱신: 2026-10-26
> 관련 문서: [WORK-20261026-design-questions: 작업 기록](./work-log.md), [ADR-020](./ADR-020-설계-질문과-적대-검토.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 승인된 v1(FR-01~13, DES-01~08)을 5개 TASK로 구현하고, 종결은 closing.md 순서를 따른다.
- 현재 결론 또는 상태: TASK-01~04 완료(4/5).
- 다음 행동: TASK-05.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-design-questions](./req-design.md) | FR-01~13, AC-01~07, DES-01~08 | v1 |
| input | decision | [ADR-020](./ADR-020-설계-질문과-적대-검토.md) | document | approved |
| output | implementation | [WORK-20261026-design-questions](./work-log.md) | 수행 기록 | TASK별 결과 |

## 기준선

- 관련 요구사항: FR-01~13, NFR-01~06
- 관련 설계: DES-01~08
- 관련 ADR·DCR: [ADR-020](./ADR-020-설계-질문과-적대-검토.md). DCR 없음(DES-08)

## 작업 정의

- 목표: 질문 단계·적대 검토 references 신설, wf-design 본문·references·templates·verification-depth의 연결 문장, 어절 순증 0.
- 범위: req-design [포함](./req-design.md#포함). 범위 밖: [제외](./req-design.md#제외).
- 가정: §3.1 재확인(2026-10-26 08:28) — HEAD `0410724`+미커밋(문서만), `유지` 4행 통과(TST-01 56, TST-02 86(TST-04 16 포함), TST-05 15).
- 위험: 모든 변경이 문서라 Red는 grep 기대 문구 부재로 대신한다(req-design 검증 전략). 어절 상쇄 실패 시 RISK-06.

## 계획 트리

<!-- generated: 2026-10-26 08:33 — scripts/render.py --view all -->

```text
[작업] 20261026-design-questions — 설계 질문 단계와 근거 강제 적대 검토 ... in-progress (4/5)
├─ [✓] templates.md — 질문 표·적대 검토 절·등록부 형식·인계 질문 행 (DES-03) (TASK-01) ... 2026-10-26 08:31
├─ [✓] interview.md·adversarial-review.md 신설 (DES-02·06) (TASK-02) ..................... depends: TASK-01  2026-10-26 08:32
├─ [✓] wf-design 본문·approval-request·design-change (DES-01·04·07) (TASK-03) ............ depends: TASK-01  2026-10-26 08:32
├─ [✓] verification-depth §6 링크 (DES-05) (TASK-04) ..................................... depends: TASK-03  2026-10-26 08:33
└─ [ ] 통합과 종결 (TASK-05) ............................................................. depends: TASK-01~04
```

## 작업 목록

### TASK-01: templates.md — 질문 표·적대 검토 절·등록부 형식·인계 질문 행 (DES-03)

- 상태: completed
- 완료: 2026-10-26 08:31
- 상위: 없음
- 목표: (a) 요구사항 노트 질문 표 골격 6열과 `답`·사실 질문 규칙 (b) 설계·DCR 템플릿 `## 적대 검토` 절 골격 7열 (c) 결정 등록부 형식 예 절(목차 행) (d) 인계 노트 질문 한 줄 형식
- 관련 요구사항과 설계: FR-05·06·07·12, DES-03, AC-02·03·04·05
- 변경 대상: `skills/wf-doc/references/templates.md`
- 의존성: 없음
- 위험: wf-doc 본문은 무변경(어절 2,337)
- 검증 방법: Red — grep `| ID | 질문 | 선택지 | 권장안 | 근거 | 답 |`·`## 적대 검토`·`차단 요인: Q-` 부재 확인. Green 후 grep, `lint_skill.py`
- 완료 조건: AC-02, AC-03·04·05의 templates 항목

### TASK-02: interview.md·adversarial-review.md 신설 (DES-02·06)

- 상태: completed
- 완료: 2026-10-26 08:32
- 상위: 없음
- 목표: DES-02 7부, DES-06 9부
- 관련 요구사항과 설계: FR-01~04·08~11·13, DES-02·06, AC-01·04
- 변경 대상: `skills/wf-design/references/interview.md`, `skills/wf-design/references/adversarial-review.md`(신설)
- 의존성: TASK-01(templates 앵커 링크)
- 위험: 본문 링크 전까지 K5 고아 — TASK-03과 같은 검증 시점
- 검증 방법: Red — 파일 부재. Green 후 grep(필수 문구), K4
- 완료 조건: AC-01·04의 references 항목

### TASK-03: wf-design 본문·approval-request·design-change (DES-01·04·07)

- 상태: completed
- 완료: 2026-10-26 08:32
- 상위: 없음
- 목표: 본문 §2 교체·§4.1·§4.5 1문장·§6.2 예시 이관 링크, approval-request §1 1행, design-change §2 시작 조건·문단·§3G 1줄·§5 1행
- 관련 요구사항과 설계: FR-01·07·08·12, DES-01·04·07, AC-01·03·04·05·07
- 변경 대상: `skills/wf-design/SKILL.md`, `skills/wf-design/references/approval-request.md`, `skills/wf-design/references/design-change.md`
- 의존성: TASK-01·02(링크 대상)
- 위험: NFR-01 ≤ 2,189, NFR-04 앵커 — RISK-06
- 검증 방법: Red — grep `interview.md`·`adversarial-review.md` 본문 부재. Green 후 `lint_skill.py` K3·K4·K5, 앵커 grep, 하네스 명칭 부재 grep
- 완료 조건: AC-01·03·04·05·07의 wf-design 항목

### TASK-04: verification-depth §6 링크 (DES-05)

- 상태: completed
- 완료: 2026-10-26 08:33
- 상위: 없음
- 목표: §6 표 아래 1줄 — 테스트 전 인수 조건이 둘 이상으로 읽히면 design-change §2
- 관련 요구사항과 설계: FR-07, DES-05, AC-03
- 변경 대상: `skills/wf-implement/references/verification-depth.md`
- 의존성: TASK-03(design-change §2 문구)
- 위험: wf-implement 본문 무변경(AC-03)
- 검증 방법: Red — grep `design-change.md#2-변경-시작-조건` 부재. Green 후 grep, K4, `git diff --stat 0410724 -- skills/wf-implement/SKILL.md` 비어 있음
- 완료 조건: AC-03

### TASK-05: 통합과 종결

- 상태: pending
- 상위: 없음
- 목표: 린트 2종, `유지` 전량, 재정비 관문(테스트 무변경), 자체 리뷰, 설치본 동기화 확인, 완료 보고 관문, closing.md 종결. 뮤테이션은 코드 파일 변경 없음으로 대상 없음
- 관련 요구사항과 설계: NFR-01~06, AC-05·07
- 변경 대상: `docs/test-register.md`, 이 작업 문서, `docs/status.md`, 05 머리말(필요 시)
- 의존성: TASK-01~04
- 위험: 없음 — 설치본 `~/.claude/skills/wf-*`는 저장소 심볼릭 링크(08:33 확인)라 동기화 불필요
- 검증 방법: 린트 2종, `유지` 전량, `git diff --name-only <구현 SHA>`
- 완료 조건: AC-05·07

## 인계

- 다음 단계 또는 워크플로우: TASK-05
- 시작 조건: 충족 — v1·ADR-020 승인(2026-10-26)
- 입력 문서와 기준선: 위 문서 연결
- 완료된 항목: 계획, TASK-01~04
- 미완료 항목: TASK-05
- 차단 요인: 없음
- 다음 행동: TASK-05

## 변경 이력

| 날짜 | 변경 내용 | 근거 | 상태 전이 | 작성·승인 |
|---|---|---|---|---|
| 2026-10-26 | 최초 작성 — TASK-01~05 | REQ-DESIGN-design-questions v1 | → in-progress | Claude(작성) |
| 2026-10-26 | TASK-01~04 completed | 작업 기록 수행 기록 | in-progress 유지 | Claude(작성) |

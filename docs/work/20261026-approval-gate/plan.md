# PLAN-20261026-approval-gate: 구현 계획 — 승인 게이트와 경량 경로 기계 조건

> 문서 유형: `plan`
> 작업 ID: `20261026-approval-gate`
> 상태: `completed`
> 기준선: [REQ-DESIGN-approval-gate](./req-design.md) `v1` (승인일 2026-10-26)
> 작성일: 2026-10-26
> 최종 갱신: 2026-10-26
> 관련 문서: [WORK-20261026-approval-gate: 작업 기록](./work-log.md), [ADR-018](./ADR-018-승인-게이트-판정.md), [DCR-019](./DCR-019-C층-승인-게이트-훅-추가.md), [ST-llm-workflow](../../status.md)

## 요약

- 목적: 승인된 v1(FR-01~09, DES-01~09)을 6개 TASK로 구현하고, 종결은 closing.md 순서를 따른다.
- 현재 결론 또는 상태: TASK-01~06 완료(6/6).
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-approval-gate](./req-design.md) | FR-01~09, AC-01~09, DES-01~09 | v1 |
| input | decision | [ADR-018](./ADR-018-승인-게이트-판정.md) | document | approved |
| input | change | [DCR-019](./DCR-019-C층-승인-게이트-훅-추가.md) | document | approved, C층 v5 |
| output | implementation | [WORK-20261026-approval-gate](./work-log.md) | 수행 기록 | TASK별 결과 |

## 기준선

- 관련 요구사항: FR-01~09, NFR-01~06
- 관련 설계: DES-01~09
- 관련 ADR·DCR: [ADR-018](./ADR-018-승인-게이트-판정.md), [DCR-019](./DCR-019-C층-승인-게이트-훅-추가.md), [ADR-014](../20261025-regression-guard/ADR-014-회귀-보호-훅-강제-방식.md)(결정 재사용)

## 작업 정의

- 목표: B층 판정·PS 어댑터·설치, wf-design 이관과 템플릿 문장, C층 v5.
- 범위: req-design [포함](./req-design.md#포함). 범위 밖: [제외](./req-design.md#제외).
- 가정: §3.1 재확인(2026-10-26 00:56) — HEAD `7ec8c02`+미커밋(문서만), `유지` 4행 통과(TST-01 47, TST-02 68, TST-04 16, TST-05 13+2=15). 사용자 미추적 06·07은 건드리지 않고 커밋 제외, 05는 종결 시 포함 여부 확인.
- 위험: TST-01 `run-tests.ps1`·`~/.claude/settings.json` 편집은 기존 가드가 확인을 묻는다(정상) — 테스트 파일 변경은 작업 기록 `### 테스트 대장 변경`에 적어 종료 판정을 통과시킨다.

## 계획 트리

<!-- generated: 2026-10-26 01:20 — scripts/render.py --view all -->

```text
[작업] 20261026-approval-gate — 승인 게이트와 경량 경로 기계 조건 ... completed (6/6)
├─ [✓] B층 판정 approval_gate.py (DES-01·02·09) (TASK-01) ... 2026-10-26 01:01
├─ [✓] PS 어댑터·메시지·훅 테스트 (DES-03·04) (TASK-02) ..... depends: TASK-01  2026-10-26 01:05
├─ [✓] 설치 등록·지연 측정·실세션 관찰 (DES-04) (TASK-03) ... depends: TASK-02  2026-10-26 01:07
├─ [✓] wf-design 이관과 템플릿 문장 (DES-05~07) (TASK-04) ... 2026-10-26 01:09
├─ [✓] C층 v5 반영 (DES-08) (TASK-05) ....................... depends: TASK-03  2026-10-26 01:14
└─ [✓] 통합과 종결 (TASK-06) ................................ depends: TASK-01~05  2026-10-26 01:20
```

## 작업 목록

### TASK-01: B층 판정 approval_gate.py (DES-01·02·09)

- 상태: completed
- 완료: 2026-10-26 01:01
- 상위: 없음
- 목표: `python approval_gate.py <루트> <대상>` exit 0/1/2. 제품 코드 판정(기본 `docs/` 밖, `.wf-gate.json` `exclude` 우선·`product` 추가), 열린 작업의 `기준선` 링크 문서 상태 ∈ {approved, completed} + `## 승인 기록` 응답 인용, 경량 표지 기계 조건(≤ 5, 민감 파일, 새 파일은 테스트). `lint_worklog` 헬퍼 재사용
- 관련 요구사항과 설계: FR-01~05, DES-01·02·09, AC-01~03
- 변경 대상: `skills/wf-doc/scripts/approval_gate.py`(신설), `skills/wf-doc/scripts/tests/test_approval_gate.py`(신설, TST-02 합류)
- 의존성: 없음
- 위험: 승인 기록 2형식 판독(AC-03) — 이 저장소 실제 작업 폴더 1건으로 확인
- 검증 방법: Red — 테스트 먼저(모듈 없음 → 수집 오류, 이후 케이스별 실패). Green 후 TST-02 전량
- 완료 조건: AC-01~03

### TASK-02: PS 어댑터·메시지·훅 테스트 (DES-03·04)

- 상태: completed
- 완료: 2026-10-26 01:05
- 상위: 없음
- 목표: `setup/hooks/wf-approval-gate.ps1`(선필터 → `CLAUDE_WF_GATE_SCRIPT` 또는 기본 경로 판정 5초 호출 → `ask`/무출력, `deny` 없음), `messages/approval-gate.md`, `run-tests.ps1` T47~(스텁 판정 exit 0/1/2, Python 부재, 선필터 2종, 선언 있으면 docs 경로 호출, 실제 판정 1건, 입력 파싱 실패)
- 관련 요구사항과 설계: FR-01·03·05, DES-03·04, AC-04
- 변경 대상: `setup/hooks/wf-approval-gate.ps1`·`messages/approval-gate.md`(신설), `setup/hooks/tests/run-tests.ps1`(TST-01 보호 — 가드 확인)
- 의존성: TASK-01(실제 판정 1건)
- 위험: 테스트 파일 편집 확인·종료 판정 — 작업 기록 대장 변경 절에 TST-01 기록
- 검증 방법: Red — T47~ 먼저(스크립트 없음 → 실패). Green 후 TST-01 전량
- 완료 조건: AC-04

### TASK-03: 설치 등록·지연 측정·실세션 관찰 (DES-04)

- 상태: completed
- 완료: 2026-10-26 01:07
- 상위: 없음
- 목표: `install-hooks.ps1` `$desired`에 PreToolUse 승인 게이트, 설치 테스트(T 확장: 등록·멱등), `setup_claude.ps1` 재실행(사용자 확인 — 전역 설정 변경), 제품 경로 훅 10회 지연 중앙값, 설치 후 이 작업의 제품 파일 편집 통과 관찰
- 관련 요구사항과 설계: DES-04, NFR-02, AC-05·06
- 변경 대상: `setup/hooks/install-hooks.ps1`, `setup/hooks/tests/run-tests.ps1`, `~/.claude/settings.json`(설치 결과, 저장소 밖)
- 의존성: TASK-02(같은 테스트 파일)
- 위험: NFR-02 초과 시 ADR-018 대안 B — 중대 변경으로 보고
- 검증 방법: Red — 설치 테스트 먼저. 측정 스크립트는 scratchpad
- 완료 조건: AC-05·06

### TASK-04: wf-design 이관과 템플릿 문장 (DES-05~07)

- 상태: completed
- 완료: 2026-10-26 01:09
- 상위: 없음
- 목표: `references/lightweight-path.md`·`approval-request.md` 신설, 본문 §1 경량 경로 절(제목 유지) 2문장 + 링크, §8 첫 두 문단 → 1문장, 승인 기록 1항 "사용자 응답을 인용해", templates.md ADR 절·승인 기록 절 1문장씩
- 관련 요구사항과 설계: FR-06~09, DES-05~07, AC-07·08
- 변경 대상: `skills/wf-design/SKILL.md`, `skills/wf-design/references/`(2개 신설), `skills/wf-doc/references/templates.md`, (어절 0이면) `skills/wf-doc/SKILL.md` §2.8
- 의존성: 없음
- 위험: NFR-04 앵커 — `lint_skill.py` K4
- 검증 방법: 문서 변경(`Red: 해당 없음`). `lint_skill.py`(K3 ≤ 2,200·K4·K5), grep
- 완료 조건: AC-07·08

### TASK-05: C층 v5 반영 (DES-08)

- 상태: completed
- 완료: 2026-10-26 01:14
- 상위: 없음
- 목표: DCR-019 변경 항목대로 `docs/requirements.md`·`docs/design.md` v5(FR-05·08, NFR-01, AC-10~12, DES-04·08, 계약·흐름·검증·위험·대안), README 훅 목록
- 관련 요구사항과 설계: DES-08, AC-09
- 변경 대상: `docs/requirements.md`, `docs/design.md`, `README.md`
- 의존성: TASK-03(실제 동작과 일치)
- 위험: 없음
- 검증 방법: 문서 변경(`Red: 해당 없음`). DCR-019 변경 항목 표와 대조, `lint_worklog.py`
- 완료 조건: AC-09의 C층 항목

### TASK-06: 통합과 종결

- 상태: completed
- 완료: 2026-10-26 01:20
- 상위: 없음
- 목표: 전체 스위트 + `유지` 전량, 변경 범위 뮤테이션(`approval_gate.py`·`wf-approval-gate.ps1` — 수동 1~3개), 재정비 관문, 자체 리뷰, 완료 보고 관문, closing.md 종결
- 관련 요구사항과 설계: NFR-01~06, AC-09
- 변경 대상: `docs/test-register.md`, 이 작업 문서, `docs/status.md`
- 의존성: TASK-01~05
- 위험: 뮤턴트 잔류 — 해시 대조
- 검증 방법: 린트 2종, `유지` 전량, `git diff --name-only <구현 SHA>`
- 완료 조건: AC-09

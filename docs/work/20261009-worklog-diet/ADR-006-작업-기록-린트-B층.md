# ADR-006: 작업 기록 린트의 B층 배치 — skills/ 아래 Python 표준 라이브러리 스크립트

> 문서 유형: `adr`
> 작업 ID: `20261009-worklog-diet`
> 상태: `approved`
> 기준선: `v1` ([REQ-DESIGN-worklog-diet](./req-design.md) 기준선에 포함, 승인일 2026-10-09)
> 작성일: 2026-10-09
> 최종 갱신: 2026-10-09
> 관련 문서: [REQ-DESIGN-worklog-diet: 요구사항·설계](./req-design.md), [WORK-20261009-worklog-diet: 작업 기록](./work-log.md), [REQ-llm-workflow 범위(B층 보류 항목)](../../requirements.md#범위), [README 실행 기준](../../../README.md#실행-기준--스킬이-정본입니다)

## 요약

- 결정: 작업 기록 린트는 **B층(저장소 스크립트, 하네스 무관)** 으로 `skills/wf-doc/scripts/lint_worklog.py`에 두고 Python 3 표준 라이브러리만 사용한다. 실행은 수동이며 실행 시점은 wf-implement §7이 규정한다. 훅(C층) 연동은 이 결정의 범위 밖이다.
- 핵심 이유: `skills/`는 junction·symlink로 설치되므로 이 워크플로우를 쓰는 모든 저장소에서 같은 스크립트가 실행된다. 표준 라이브러리만 쓰면 설치 의존성이 없고, Python은 PowerShell과 달리 OS에 묶이지 않는다.
- 주요 단점: Python이 없는 환경에서는 린트를 실행할 수 없다. 이때는 wf-doc §4 수동 검토로 대체하고 미실행을 기록한다.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-worklog-diet](./req-design.md) | FR-05, FR-06, NFR-03 | 결정이 구체화하는 요구사항 |
| input | related | [REQ-llm-workflow](../../requirements.md#범위) | 범위 제외 "B층 독립 스크립트" | 보류돼 있던 B층을 이 결정이 처음 도입. 해당 문서의 기준선 의미는 바꾸지 않음(별도 작업으로 하라는 보류 조건의 이행) |
| output | decision | [REQ-DESIGN-worklog-diet](./req-design.md) | DES-05, DES-07 | 린트 스크립트 설계의 근거 |

## 배경

저장소의 계층 구분: A층은 스킬 본문의 의무와 상태 어휘(하네스 중립), C층은 `setup/hooks/`의 Claude Code 훅(하네스 종속), B층은 "저장소 스크립트 — 재개 가능성 린트 등 결정적 검사"로 역할만 정의되고 미착수였다([REQ-llm-workflow 범위](../../requirements.md#범위), `docs/paper/` 초안). 사용자 요구 5(산문 교정 방안)는 조사 기록의 결론 — 산문 규칙은 반복 실패를 막지 못하므로 기계적 검사로 승격 — 과 함께 B층의 첫 실제 필요다.

저장소에는 Python 선례(`docs/presentation/make_pptx.py` + pytest, 조사 폴더의 측정 스크립트)와 PowerShell 선례(`setup/hooks/*.ps1` + 자체 테스트 러너)가 있다. 사용자 환경은 Windows이며 Python 3.13·pytest가 설치돼 있다.

## 영향을 받는 요구사항과 제약

- [FR-05·FR-06](./req-design.md#기능-요구사항), [NFR-03](./req-design.md#비기능-요구사항) — 린트의 검사 항목·결정성·이식성.
- [README 실행 기준](../../../README.md#실행-기준--스킬이-정본입니다) — 스킬 본문은 하네스 기능을 전제하지 않는다. 스크립트 호출은 하네스가 아니라 실행 환경(Python)에만 의존하므로 이 원칙과 양립한다.
- [wf-implement §2.4 결정 사다리](../../../skills/wf-implement/SKILL.md#24-최소-구현-원칙--ponytail-full-모드) — 표준 라이브러리 우선(3단계), 새 의존성 금지.

## 고려한 대안

| 대안 | 장점 | 단점·위험 | 전환 비용 |
|---|---|---|---|
| A. PowerShell 스크립트를 `setup/hooks/`에 두고 훅 테스트 러너에 합류 | 기존 러너·인코딩 처리 재사용 | Windows·PS 5.1 종속. `setup/`은 하네스 어댑터 층이라 B층 역할과 다름. 다른 OS 사용자는 실행 불가 | 낮음 |
| B. 저장소 로컬 `tools/lint_worklog.py` | 저장소 안에서 자유로운 위치 | junction 밖이라 이 워크플로우를 설치한 다른 저장소에서 쓸 수 없다. 각 저장소에 복사해야 함 | 낮음, 그러나 이식 불가 |
| C. `skills/wf-doc/scripts/lint_worklog.py`, Python 표준 라이브러리 (채택) | 스킬과 함께 설치·갱신(`git pull`). 문서 형식 소유자(wf-doc) 옆에 검사기가 있어 소유권이 분명. OS 무관 | Python 필요. 스킬 폴더에 코드가 들어가 스킬 로드 시 노출(단, SKILL.md만 로드되므로 컨텍스트 비용 없음) | 신규 파일 2개, wf-doc §4 1항 교체 |
| D. 처음부터 Stop 훅으로 집행(C층) | 강제력 최대 | 하네스 종속, 훅 기준선(REQ-llm-workflow) 변경과 테스트가 필요. 검사 규칙이 안정되기 전의 강제는 회피 행동을 낳는다(RISK-02) | 높음. 후속 작업으로 분리 |

## 결정

대안 C를 채택한다. 파일은 `skills/wf-doc/scripts/lint_worklog.py`와 `skills/wf-doc/scripts/tests/test_lint_worklog.py`(pytest). 표준 라이브러리 외 의존성은 두지 않는다. 실행 명령은 저장소 루트에서 `python skills/wf-doc/scripts/lint_worklog.py [경로...]`이며, 스킬이 설치된 다른 저장소에서는 설치 경로(`~/.claude/skills/wf-doc/scripts/lint_worklog.py`)로 같은 방식으로 실행한다. 상한값은 스크립트 상단 상수로 두고, 변경은 wf-design 경량 경로로 처리한다.

실행 시점과 의무(TASK 완료 기록 후, 세션 인계 전, 완료 보고 종결 전; 0 오류가 완료 조건)는 [wf-implement §7](../../../skills/wf-implement/SKILL.md#7-작업-기록과-저장-위치)이 소유한다. 훅으로 자동 실행하는 것은 별도 작업(C층 DCR)으로 남긴다.

## 이유

- 이식성: 사용자는 이 워크플로우를 여러 저장소에 적용한다. junction 안에 있어야 한 번의 `git pull`로 모든 저장소의 검사기가 갱신된다.
- 소유권: 검사 대상이 문서 형식(절·필드·링크)이므로 형식 소유자인 wf-doc 옆에 두는 것이 경계표와 맞는다. 검사의 의미(어떤 필드가 필수인가)는 wf-implement·wf-doc이 규정하고 스크립트는 그것을 실행한다.
- 결정 사다리: 표준 라이브러리로 충분한 작업(정규식·파일 탐색)에 의존성을 추가하지 않는다.

## 결과와 감수할 단점

- Python 부재 환경에서는 수동 검토로 대체하고 작업 기록에 미실행을 남긴다(DES-03). 린트를 "실행하지 못했는데 통과"로 기록하지 않는다.
- `skills/wf-doc/` 아래에 `references/`·`agents/`에 더해 `scripts/`가 생긴다. SKILL.md 본문에는 호출 문장만 두고 검사 세부는 스크립트와 `references/worklog-style.md`에 둔다(NFR-04).
- 린트 규칙과 템플릿이 어긋나면 린트가 틀린 것이다. 템플릿(wf-doc)이 정본이며 스크립트를 템플릿에 맞춘다.

## 후속 작업

- 훅(C층) 연동 — 린트 규칙이 두 사이클 이상 안정된 뒤 별도 작업으로 검토.
- 스킬 본문 린트(조사 AI-13) — 같은 `scripts/` 관례를 재사용할 수 있다. 별도 작업.

## 대체 관계

- 대체 대상 ADR: 없음
- 대체 ADR: 없음
- 번호에 관한 주의: 보관 브랜치 `archive/202609-cycles`에는 ADR-006이 없고 DCR-006이 있다. 이 문서는 main 이력의 [결정 등록부](../../decisions.md) 기준 다음 번호이며 보관 브랜치는 병합 대상이 아니다.

## 승인 기록

- 2026-10-09 — [REQ-DESIGN-worklog-diet v1](./req-design.md#승인-기록) 승인과 함께 사용자 승인.

## 변경 이력

| 날짜 | 변경 | 근거 | 상태 또는 기준선 | 작성자·승인자 |
|---|---|---|---|---|
| 2026-10-09 | 최초 작성 | 사용자 요구 5, 조사(묶음 A §2.3·§5, 묶음 B §(a)) | proposed | Claude(작성) |
| 2026-10-09 | 기준선 v1과 함께 승인 | 사용자 승인(대화형 관문) | proposed → approved | 사용자(승인) |

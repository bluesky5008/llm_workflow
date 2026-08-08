# 루트 진입 스킬(SKILL.md) 작업 정의

> 상태: 반영됨
> 작성일: 2026-08-08

> **이 문서는 기획 기록입니다.** 정본은 [루트 SKILL.md](../../SKILL.md)와 각 스킬 문서이며, 내용이 다르면 정본을 따릅니다.

## 요약

동적 스킬 로드가 보장되지 않는 에이전트를 위해, 저장소 루트에 워크플로우 전체를 하나의 스킬로 포장하는 얇은 진입 스킬(SKILL.md)을 추가한다. 네 스킬의 내용을 병합하지 않고, frontmatter와 명령형 라우팅 규칙만 담아 상황별로 읽을 정본 문서를 지정한다.

## 관련 문서

- [Human–AI Development Workflow](../../README.md)
- [루트 SKILL.md](../../SKILL.md) — 이 기획의 산출물
- [wf-design](../../skills/wf-design/SKILL.md), [wf-implement](../../skills/wf-implement/SKILL.md), [wf-doc](../../skills/wf-doc/SKILL.md), [wf-tree](../../skills/wf-tree/SKILL.md)
- 진입 규칙 선례: [setup/CLAUDE.global.md](../../setup/CLAUDE.global.md), [setup/AGENTS.codex.md](../../setup/AGENTS.codex.md)
- 선례 패턴: [TDD 반영 작업 정의](./TDD_TASKS.md) — 기획 문서 → 사용자 검토·승인 → 반영 → 링크 검증 경로

## 배경과 판단

- 문제: 스킬 자동 로드가 없는 에이전트는 skills/ 하위 4개 스킬의 동적 발동을 보장할 수 없다.
- 기존 해법: 항상 로드되는 짧은 진입 규칙 + 필요할 때 파일을 읽게 하는 방식([AGENTS.codex.md](../../setup/AGENTS.codex.md) 패턴). 루트 SKILL.md는 이 패턴의 에이전트 중립 일반화다.
- 내용 병합(단일 대형 스킬)은 기각한다: 점진적 로드 상실(스킬 4개 + references 약 2,000줄 상시 로드), description 트리거 정밀도 하락, 정본/요약 경계 구조 해체.
- README·01·02는 진입 문서를 대체할 수 없다: 에이전트의 발견·로드 규약에 걸리지 않고, 스스로 "절차를 규정하지 않는다"고 선언한 사람용 안내 계층이다. 루트 SKILL.md는 이 세 문서의 대체가 아니라 에이전트용 실행 계층의 추가다.

## 설계

- 위치: 저장소 루트 `SKILL.md` — SKILL.md를 가진 폴더를 스킬 하나로 취급하는 규약에 따라 저장소 전체를 스킬 하나로 설치할 수 있다.
- 구성: frontmatter(name, description) + 라우팅 규칙(상대 경로 링크) + 항상 적용되는 원칙. 규칙 본문은 복제하지 않고 정본을 링크한다.
- 진입 규칙 3종([CLAUDE.global.md](../../setup/CLAUDE.global.md), [AGENTS.codex.md](../../setup/AGENTS.codex.md), [루트 SKILL.md](../../SKILL.md))은 같은 규칙 세트를 매체별 표현으로 유지한다. 규칙을 추가·변경할 때 세 파일을 함께 갱신한다.
- [setup/setup_claude.ps1](../../setup/setup_claude.ps1)은 변경하지 않는다. skills/ 하위 폴더만 junction하므로 루트 SKILL.md는 Claude Code에 설치되지 않고, 4개 스킬과의 이중 발동이 없다.
- README·01·02는 이동·개조하지 않고 사람용 안내 계층으로 유지한다.

## 결정 기록

| 질문 | 결정 (2026-08-08, 사용자) |
|---|---|
| 워크플로우를 하나의 스킬로 만드는 방식 | 내용 병합 대신 **얇은 라우터 SKILL.md 추가** 승인 |
| 루트 3개 md(README·01·02)의 처리 | 진입 문서로 개조하지 않고 사람용 안내 계층으로 유지 |
| 스킬 이름 | `llm-workflow` — 저장소 이름과 일치 (권장안 적용) |

## 완료 조건

- 루트 SKILL.md가 frontmatter + 라우팅 + 공통 원칙만 담고 규칙 본문을 복제하지 않는다.
- 진입 규칙 3종의 규칙 세트가 서로 어긋나지 않는다.
- README가 루트 SKILL.md의 존재와 용도를 안내한다.
- 저장소 전체 로컬 링크·앵커가 기계 검증을 통과했다.

이 문서는 루트 진입 스킬의 범위와 결정을 정리한 기획 기록이다. 정본은 [루트 SKILL.md](../../SKILL.md)다.

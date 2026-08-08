# Human–AI Development Workflow

> 상태: 초안 0.4

사용자가 AI에게 코딩 작업을 맡길 때 사용하는 개발 워크플로우입니다.

개발 작업은 다음 두 단계로 나뉩니다.

```text
작업 요청
   ↓
요구사항 정의 + SW 설계
   ↓
사용자 승인
   ↓
계획 수립 + 구현 + 검증·리뷰 + 통합
   ↓
완료
```

첫 번째 워크플로우는 **무엇을 왜 어떤 구조로 만들지** 결정합니다.

두 번째 워크플로우는 승인된 결정을 기준으로 **어떻게 만들고 완료를 증명할지** 수행합니다.

두 워크플로우 사이에는 사용자의 승인 관문이 있습니다. 승인되지 않은 요구사항과 설계를 구현 기준으로 사용하지 않습니다.

## 실행 기준 — 스킬이 정본입니다

세 개의 스킬이 이 워크플로우의 **실행 기준(정본)** 입니다. 다른 문서나 사본과 내용이 다르면 스킬을 따릅니다.

| 스킬 | 소유하는 것 |
|---|---|
| [skills/wf-design](./skills/wf-design/SKILL.md) | 요구사항·설계의 의미, ADR/DCR 판단, 승인과 기준선의 효력 |
| [skills/wf-implement](./skills/wf-implement/SKILL.md) | 승인된 기준선의 구현, 테스트 실행과 증거, 리뷰와 통합 |
| [skills/wf-doc](./skills/wf-doc/SKILL.md) | 기록할 Markdown 구조, 상태 표기, 식별자, 하이퍼링크, 추적표와 인계 형식 |

wf-doc은 별도의 실행 단계가 아니라 두 워크플로우 전체에 적용되는 문서 계층입니다. 문서의 현재 상태, 기준선, 문서간 양방향 하이퍼링크, 추적 관계, 검증 증거와 다음 인계 지점을 같은 방식으로 기록합니다.

동작·인터페이스·데이터·보안에 영향이 없는 작은 작업은 1단계 산출물을 생략할 수 있습니다. 조건은 [적용 제외 — 경량 경로](./skills/wf-design/SKILL.md#적용-제외--경량-경로)를 따릅니다.

설치된 ponytail 스킬과 wf-implement의 내용이 다르면 wf-implement의 규정을 우선합니다.

## 개요 문서

- [01. 요구사항 정의 + SW 설계](./01_REQUIREMENTS_AND_DESIGN.md)
- [02. 계획 수립 + 구현 + 검증·리뷰 + 통합](./02_IMPLEMENTATION_AND_INTEGRATION.md)

두 문서는 각 단계의 목적과 형태를 설명하는 **개요**이며 절차를 규정하지 않습니다. 규범적인 내용은 스킬에만 두고, 개요 문서는 정본을 링크합니다. 워크플로우 규칙을 바꿀 때는 스킬을 고치고 개요 문서의 설명이 여전히 맞는지 확인합니다.

## Claude Code 설치

**Windows** — 저장소를 클론한 뒤 한 번 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_claude.ps1
```

스크립트는 `~/.claude/skills/`에 junction을 만들고 [CLAUDE.global.md](./CLAUDE.global.md)의 워크플로우 규칙을 `~/.claude/CLAUDE.md`에 설치합니다. 재실행해도 안전하며(이미 올바른 junction은 건너뛰고, 다른 곳을 가리키면 다시 연결합니다), junction 방식이므로 `git pull`만 하면 스킬이 최신화됩니다. 설치 후 새 세션에서 `/wf-design` 또는 `/wf-doc`으로 확인합니다.

**macOS / Linux** — symlink로 연결하고 규칙을 복사합니다.

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/wf-design" ~/.claude/skills/wf-design
ln -s "$(pwd)/skills/wf-implement" ~/.claude/skills/wf-implement
ln -s "$(pwd)/skills/wf-doc" ~/.claude/skills/wf-doc
cat CLAUDE.global.md >> ~/.claude/CLAUDE.md
```

## OpenAI Codex CLI 설치

저장소를 클론한 뒤 한 번 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_codex.ps1
```

스크립트는 [AGENTS.codex.md](./AGENTS.codex.md)의 진입 규칙(이 저장소의 절대 경로로 치환됨)을 `~/.codex/AGENTS.md`에 설치하고, 수동 호출용 custom prompt(`/wf-design`, `/wf-implement`, `/wf-doc`)를 `~/.codex/prompts/`에 만듭니다.

- Codex에는 스킬 자동 로드가 없으므로 항상 로드되는 것은 짧은 진입 규칙뿐이고, 상세 절차는 규칙이 가리키는 이 저장소의 SKILL.md를 세션 중에 읽는 방식입니다.
- 규칙이 저장소 안의 파일을 절대 경로로 참조하므로 **설치 후 저장소를 이동·삭제하면 안 됩니다.** 이동했다면 스크립트를 다시 실행합니다.

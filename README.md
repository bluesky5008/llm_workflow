# Human–AI Development Workflow

> 상태: 초안 0.3

사용자가 AI에게 코딩 작업을 맡길 때 사용하는 개발 워크플로우입니다.

개발 작업은 다음 두 단계로 나뉩니다.

1. [요구사항 정의 + SW 설계](./01_REQUIREMENTS_AND_DESIGN.md)
2. [계획 수립 + 구현 + 검증·리뷰 + 통합](./02_IMPLEMENTATION_AND_INTEGRATION.md)

이 두 문서가 실행 기준입니다. 요약본이나 다른 사본과 내용이 다르면 이 두 문서를 따릅니다.

## Claude Code Skill

두 문서는 [skills/wf-design](./skills/wf-design/SKILL.md)과 [skills/wf-implement](./skills/wf-implement/SKILL.md)로 스킬화되어 있습니다. `~/.claude/skills/`에 복사하거나 junction으로 연결하면 전역에서 사용할 수 있습니다.

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\wf-design" -Target "<repo>\skills\wf-design"
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\wf-implement" -Target "<repo>\skills\wf-implement"
```

- 스킬 내용은 이 저장소의 01/02 문서에서 파생됩니다. 문서를 수정하면 스킬도 함께 갱신합니다.
- 설치된 ponytail 스킬과 wf-implement의 내용이 다르면 wf-implement의 규정을 우선합니다.

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

동작·인터페이스·데이터·보안에 영향이 없는 작은 작업은 1단계 산출물을 생략할 수 있습니다. 조건은 [적용 제외 — 경량 경로](./01_REQUIREMENTS_AND_DESIGN.md#적용-제외--경량-경로)를 따릅니다.

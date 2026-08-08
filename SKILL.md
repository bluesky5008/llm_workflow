---
name: llm-workflow
description: Human–AI 개발 워크플로우의 진입 스킬. 코딩 작업을 요구사항 정의·SW 설계(wf-design) → 사용자 승인 → 계획·구현·검증·통합(wf-implement) 순서로 진행하고, 문서 공통 포맷(wf-doc)과 작업 계획 트리(wf-tree)를 함께 적용한다. 이 저장소의 워크플로우를 하나의 스킬로 사용하는 에이전트는 이 파일을 읽고 상황에 맞는 하위 스킬 문서로 이동한다.
---

# Human–AI Development Workflow — 진입 스킬

이 파일은 워크플로우 전체를 하나의 스킬로 포장하는 얇은 진입점(라우터)이다. 규칙의 정본은 아래 각 스킬 문서이며, 이 파일은 규칙을 복제하지 않고 상황별로 읽을 문서만 지정한다.

## 라우팅 규칙

- 코딩 작업은 wf-design(요구사항 정의 + SW 설계) → 사용자 승인 → wf-implement(계획 + 구현 + 검증 + 통합) 순서를 따른다.
- 요구사항·설계를 시작할 때 [skills/wf-design/SKILL.md](skills/wf-design/SKILL.md)를 읽고 그 절차를 따른다. 구현 중 승인된 설계의 변경(DCR)과 레거시 코드 역공학도 이 스킬의 참조 절차를 사용한다.
- 승인된 기준선을 구현할 때 [skills/wf-implement/SKILL.md](skills/wf-implement/SKILL.md)를 읽고 그 절차를 따른다.
- 두 워크플로우의 문서를 만들거나 갱신할 때 [skills/wf-doc/SKILL.md](skills/wf-doc/SKILL.md)의 공통 포맷을 함께 적용한다.
- 작업 계획을 트리로 수립·시각화·갱신하거나 작업 포트폴리오를 관리할 때 [skills/wf-tree/SKILL.md](skills/wf-tree/SKILL.md)의 규칙을 따른다.

## 항상 적용되는 원칙

- 동작·공개 인터페이스·데이터 모델·보안에 영향이 없는 국소적이고 되돌리기 쉬운 작은 작업은 wf-design을 생략할 수 있다(경량 경로). 판단이 애매하면 정식 경로를 따른다.
- 코드 작성은 wf-implement의 최소 구현 원칙(ponytail full 모드, §2.4)을 따른다. 다른 코딩 지침과 내용이 다르면 wf-implement의 규정을 우선한다.
- 테스트는 wf-implement의 TDD 규정(실패하는 테스트 먼저, §3.3)을 따른다. 버그 수정은 경량 경로에서도 재현 테스트를 먼저 작성한다.

사람용 개요와 설치 방법은 [README.md](README.md)를 본다.

# 개발 워크플로우

- 코딩 작업은 Workflow 1(요구사항 정의 + SW 설계) → 사용자 승인 → Workflow 2(계획 + 구현 + 검증 + 통합) 순서를 따른다.
- Workflow 1을 시작할 때 다음 파일을 읽고 그 절차를 따른다: `{{REPO}}\skills\wf-design\SKILL.md`
- Workflow 2를 시작할 때 다음 파일을 읽고 그 절차를 따른다: `{{REPO}}\skills\wf-implement\SKILL.md`
- 동작·공개 인터페이스·데이터 모델·보안에 영향이 없는 국소적이고 되돌리기 쉬운 작은 작업은 Workflow 1을 생략할 수 있다(경량 경로). 판단이 애매하면 정식 경로를 따른다.
- 코드 작성은 wf-implement의 최소 구현 원칙(ponytail full 모드, §2.4)을 따른다. 다른 코딩 지침과 내용이 다르면 wf-implement의 규정을 우선한다.

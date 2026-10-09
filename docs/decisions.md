# 결정 등록부

ADR·DCR 전역 목록. 개별 파일이 정본이며 이 표는 조망용이다. 번호는 저장소 전역 일련번호다.

| ID | 유형 | 제목 | 상태 | 날짜 | 위치 | 대체·관련 |
|---|---|---|---|---|---|---|
| ADR-001 | adr | 컨텍스트 사용량 신호 선택 | approved | 2026-08-09 | [work/20260809-claude-hooks/ADR-001-…](./work/20260809-claude-hooks/ADR-001-컨텍스트-신호-선택.md) | — |
| DCR-002 | dcr | 발표 자료 디자인 적용(범위·요구사항 변경) | approved | 2026-08-09 | [work/20260809-dev-briefing/DCR-002-…](./work/20260809-dev-briefing/DCR-002-디자인-적용.md) | [REQ-DESIGN-dev-briefing](./work/20260809-dev-briefing/req-design.md) v1 → v2 |
| ADR-003 | adr | 계획 트리 트리거의 단일 관문 배치 | approved | 2026-08-14 | [work/20260814-wf-tree-triggers/ADR-003-…](./work/20260814-wf-tree-triggers/ADR-003-트리거-단일-관문.md) | [REQ-DESIGN-wf-tree-triggers](./work/20260814-wf-tree-triggers/req-design.md); 부분 수정: [REQ-DESIGN-plan-relocation](./work/20261009-plan-relocation/req-design.md) DES-02·03 (2026-10-09, 배치 결정 유지) |
| ADR-004 | adr | TASK 식별자의 작업 범위 발행 | approved | 2026-10-09 | [work/20261009-plan-relocation/ADR-004-…](./work/20261009-plan-relocation/ADR-004-TASK-식별자-작업-범위.md) | [REQ-DESIGN-plan-relocation](./work/20261009-plan-relocation/req-design.md) v1. 번호는 main 이력 기준 — 보관 브랜치 `archive/202609-cycles`의 ADR-004와 무관 |
| ADR-005 | adr | 작업 기록의 수명주기 — 상태 전이 시 축약과 제자리 동결 | approved | 2026-10-09 | [work/20261009-worklog-diet/ADR-005-…](./work/20261009-worklog-diet/ADR-005-작업-기록-수명주기.md) | [REQ-DESIGN-worklog-diet](./work/20261009-worklog-diet/req-design.md) FR-04. 번호는 main 이력 기준 — 보관 브랜치 `archive/202609-cycles`의 ADR-005와 무관 |
| ADR-006 | adr | 작업 기록 린트의 B층 배치 — skills/ 아래 Python 표준 라이브러리 스크립트 | approved | 2026-10-09 | [work/20261009-worklog-diet/ADR-006-…](./work/20261009-worklog-diet/ADR-006-작업-기록-린트-B층.md) | [REQ-DESIGN-worklog-diet](./work/20261009-worklog-diet/req-design.md) FR-06 |
| DCR-007 | dcr | 세션 핸드오프 훅의 닫힘 상태에 on-hold 추가 | completed | 2026-10-09 | [work/20261009-worklog-diet/DCR-007-…](./work/20261009-worklog-diet/DCR-007-훅-닫힘-상태-on-hold.md) | [REQ-llm-workflow](./requirements.md)·[DESIGN-llm-workflow](./design.md) v1 → v2(2026-10-09). [REQ-DESIGN-worklog-diet](./work/20261009-worklog-diet/req-design.md) Q-02 |
| ADR-007 | adr | 검증 결과의 3튜플 앵커 | approved | 2026-10-09 | [work/20261009-test-lifecycle/ADR-007-…](./work/20261009-test-lifecycle/ADR-007-검증-결과-3튜플-앵커.md) | [REQ-DESIGN-test-lifecycle](./work/20261009-test-lifecycle/req-design.md) FR-01. 보관 브랜치 `archive/202609-cycles`의 ADR-004(같은 결정)를 main 번호로 재발행 |
| ADR-008 | adr | 테스트 대장의 저장소 관통 배치 | approved | 2026-10-09 | [work/20261009-test-lifecycle/ADR-008-…](./work/20261009-test-lifecycle/ADR-008-테스트-대장-저장소-관통.md) | [REQ-DESIGN-test-lifecycle](./work/20261009-test-lifecycle/req-design.md) FR-04, Q-01 |
| ADR-009 | adr | 테스트 재정비 관문 | approved | 2026-10-09 | [work/20261009-test-lifecycle/ADR-009-…](./work/20261009-test-lifecycle/ADR-009-테스트-재정비-관문.md) | [REQ-DESIGN-test-lifecycle](./work/20261009-test-lifecycle/req-design.md) FR-05·07, Q-04 |
| ADR-010 | adr | 스킬 문서의 계층 규칙 — 본문·references·scripts 분리와 린트 집행 | approved | 2026-10-09 | [work/20261009-skill-diet/ADR-010-…](./work/20261009-skill-diet/ADR-010-스킬-문서-계층-규칙.md) | [REQ-DESIGN-skill-diet](./work/20261009-skill-diet/req-design.md) FR-01·08. [ADR-006](./work/20261009-worklog-diet/ADR-006-작업-기록-린트-B층.md) 관례 재사용 |
| ADR-011 | adr | wf-tree 축소 — 필수 게이트 3종, 노드 유형 이관, 렌더 스크립트, 깊이 상한 | approved | 2026-10-09 | [work/20261009-skill-diet/ADR-011-…](./work/20261009-skill-diet/ADR-011-wf-tree-축소.md) | [REQ-DESIGN-skill-diet](./work/20261009-skill-diet/req-design.md) FR-04·05, Q-03·04. [ADR-003](./work/20260814-wf-tree-triggers/ADR-003-트리거-단일-관문.md) 유지 |

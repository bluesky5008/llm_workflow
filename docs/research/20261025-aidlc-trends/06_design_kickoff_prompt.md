# 설계 개선 착수 프롬프트 — 테스트 사이클 완료 후 사용

> 상태: 참고 자료(조사 트랙). 테스트 사이클 1·2 완료 후 새 세션에 아래 블록을 그대로 붙여 넣는다.
> 입력: [대조 문서 §1·§4·§5](./00_trends_vs_workflow.md), [설계 노트](./01_design_notes.md), [테스트 액션 아이템](./04_test_action_items.md)(형식 선례).
> 작성 2026-10-25.

```text
llm_workflow 저장소의 v2 설계 개선을 시작하자.
테스트 개선(docs/research/20261025-aidlc-trends/04_test_action_items.md의 사이클 1·2)은 끝난 상태다.

[0. 착수 전 확인]
- docs/status.md와 열린 작업 기록을 먼저 확인하라.
  테스트 사이클(20261025-regression-guard 및 후속)이 완료 상태가 아니면 착수하지 말고 보고하라.
- 테스트 사이클에서 새로 생긴 것을 확인하라: 훅 5종, 대장 스키마, 충돌 출구 §6, Red 필드.
  설계 개선은 이 위에 쌓는다. 특히 승인 게이트 훅(S28)은 DCR-015의 훅 구조와 메시지·실패 정책을 재사용한다.

[1. 입력]
- docs/research/20261025-aidlc-trends/00_trends_vs_workflow.md
  - §1: 설계 증거, AWS AI-DLC v2, 현행 wf-design 대조표
  - §4: S22~S28, S11·S21·S8·S6 재판정
  - §5: 권고 순서
- docs/research/20261025-aidlc-trends/01_design_notes.md (출처·수치 원자료)
- skills/wf-design/SKILL.md, references/design-change.md, references/reverse-engineering.md
- docs/research/20261010-v2-research/02_unapplied_items_papers.md (S11·S21·S6·S8의 이전 판정)

[2. 최신성 재확인 — 짧게]
- 2026-10-25 이후 나온 것만 확인하라.
  - Thoughtworks Radar Vol 35(10-28 공개 예정이었음)의 spec-driven·AI 설계 항목
  - awslabs/aidlc-workflows 최신 릴리스의 변경점
  - 01_design_notes.md 핵심 수치의 출처 상태(철회·개정): R2ABench 관계 F1 0.13, SlopCodeBench, Adversarial Review 2608.18167, UnderSpecBench
- 바뀐 것만 추가 노트로 남기고, 바뀌지 않았으면 "변경 없음"으로 기록하라.

[3. 산출물 1 — 설계 한정 액션 아이템]
04_test_action_items.md와 같은 형식으로
docs/research/20261025-aidlc-trends/05_design_action_items.md를 작성하라.
(조사 트랙 문서이므로 스킬·docs 정본은 편집하지 않는다.)
- 각 항목에 다음을 적는다: ID(D-01~), 수정 위치, 내용, 근거 수치, 검증 방법, 매핑(S번호), 이 저장소에서 측정 가능한지 / 코드 저장소에서만 가능한지.
- 사이클 편성 초안. 기본안은 아래와 같고, 다르게 편성하려면 이유를 적어라.
  - 사이클 A — 질문 장치: S21 CRP 확대(설계 인터뷰 S23과 통합) + S11 근거 강제 적대 검토(새 맥락, 지적마다 ID·파일 인용, 최대 2라운드, 할당량 금지)
  - 사이클 B — 강제: S28 승인 게이트 훅(설계 상태 approved 전 제품 코드 쓰기 확인·차단, 경량 경로 통과) + S26 승인 요청 분량 예산·한 화면 요약 + S25 ADR 작성 시 직전 ADR 3~5개 참조
  - 사이클 C — 코드 저장소 실측: S22 기존 자산 대조(설계 요소별 재사용/신규 사유) + S24 컴포넌트·의존 목록 기계 검사(대칭·순환·고아·요구사항 누락 린트) + S27 설계 침식 점검
  - 기타: S6 경량 경로 기계 조건(AI-DLC Bugfix·Express 프로필 참조), S8 폐기 확정
- 사용자 결정 사항 표를 붙여라(질문 · 권장안 · 근거).
  최소한 다음은 포함한다:
  - 인터뷰 단계의 의무 범위(정식 경로 전체 vs 조건부)
  - 적대 검토의 실행 주체(서브에이전트 vs 별도 세션)
  - S28의 확인/차단 방식(DCR-015의 Q-01 결정을 따를지)

[4. 산출물 2 — 첫 사이클 착수]
액션 아이템을 내가 확인한 뒤, 첫 사이클을 wf-design 정식 경로로 착수하라.
선례는 docs/work/20261025-regression-guard/ 구조를 따른다:
- req-design: 스킬 규칙 변경
- DCR: C층 훅 기준선(REQ·DESIGN-llm-workflow)을 바꾸는 경우만
- ADR: 결정이 있을 때
- 작업 기록, status.md 행, decisions.md 행

[5. 제약]
- 스킬 본문 어절 상한(lint_skill K3)을 지킨다: wf-design 2,300 · wf-implement 2,850 · wf-doc 2,350. 늘어나는 규칙은 references로 보내고 본문에는 트리거·링크만 둔다(ADR-010).
- 스킬 본문은 하네스 중립을 유지한다. 훅은 setup/hooks/ 어댑터로만 둔다.
- 새 규칙을 늘리기보다 기존 규칙(§4.1 조사, §4.5 일관성 검토, §8 승인 관문)을 강화·강제하는 쪽을 우선한다.
- 효과 측정이 이 저장소에서 불가능한 항목은 "코드 저장소 실측 필요"로 표시한다(v2 결정 D-02).
- 근거는 출처가 확인된 수치만 쓴다. 2차 출처·미확인은 표시한다.
- 승인 전에는 스킬·훅을 구현하지 않는다. 커밋·push는 내가 지시할 때만 한다.
```

# Workflow 1 — 요구사항 정의 + SW 설계 (개요)

> 상태: 초안 0.4
>
> 목적: 사용자의 요청을 구현 가능한 요구사항과 승인 가능한 SW 설계로 구체화한다.

> **이 문서는 개요입니다.** 실행 기준(정본)은 [skills/wf-design/SKILL.md](./skills/wf-design/SKILL.md)이며, 내용이 다르면 스킬을 따릅니다. 이 문서는 워크플로우의 목적과 형태를 설명할 뿐 절차를 규정하지 않습니다.

## 이 단계가 결정하는 것

Workflow 1은 **무엇을 왜 어떤 계약과 구조로 만들지** 결정하고 사용자 승인을 받아 기준선을 발행한다. 승인된 기준선 안에서 어떤 작업과 코드로 구현할지는 [Workflow 2](./02_IMPLEMENTATION_AND_INTEGRATION.md)가 소유한다.

- 해결할 문제, 범위와 범위 밖 항목
- 기능·비기능 요구사항과 측정 가능한 인수 조건
- 시스템 구조, 데이터와 인터페이스 계약, 정상·실패 흐름, 품질 속성
- 되돌리기 어려운 기술 결정(ADR)
- 승인된 기준선과 그 효력

이 단계에서는 원칙적으로 제품 코드를 변경하지 않는다. 저장소 조사, 문서 작성, 읽기 전용 분석과 범위를 명시한 실현 가능성 프로토타입만 수행한다.

## 진행 형태

```text
현재 상태 조사 → 요구사항 정의 → SW 설계 → 설계 결정 기록(ADR) → 일관성 검토 → 사용자 승인 관문
```

승인 관문에서 사용자는 **승인 / 수정 요청 / 거부 / 보류** 중 하나로 응답한다. 승인되지 않은 요구사항과 설계를 구현 기준으로 사용하지 않는다.

## 산출물

요구사항 명세, SW 설계 문서, 미해결 질문과 가정, 위험 목록, 필요한 ADR·DCR과 설계 변경 기록, 요구사항–설계–검증 추적 정보를 `docs/work/<작업-ID>/` 아래에 남긴다.

산출물의 필요 여부·저장 위치·충분성은 wf-design이 결정하고, Markdown 골격·식별자·하이퍼링크·상태 표기는 [skills/wf-doc](./skills/wf-doc/SKILL.md)이 정한다.

## 경량 경로

동작·공개 인터페이스·데이터 모델·보안 정책에 영향이 없고, 국소적이며 되돌리기 쉽고, 새 설계 결정이 필요 없는 작업은 이 단계의 산출물 작성을 생략할 수 있다. 조건과 예외는 [wf-design의 적용 제외 — 경량 경로](./skills/wf-design/SKILL.md#적용-제외--경량-경로)를 따른다.

## 승인된 설계 변경 (DCR)

구현 중 승인된 설계나 요구사항을 바꿔야 하는 상황이 되면 Workflow 2가 영향받는 구현을 보류하고 증거와 초안을 인계하며, Workflow 1이 변경을 분류하고 재승인과 새 기준선을 결정한다. 절차 정본은 [wf-design/references/design-change.md](./skills/wf-design/references/design-change.md)이다.

## 상세 절차

| 내용 | 정본 위치 |
|---|---|
| 적용 시점, 기본 원칙, 진행 절차, 완료 조건, 승인 관문 | [wf-design/SKILL.md](./skills/wf-design/SKILL.md) |
| DCR 시작 조건, 변경 분류, 영향 분석, 재승인 | [wf-design/references/design-change.md](./skills/wf-design/references/design-change.md) |
| 코드 역공학: 증거 관리, 현행 요구사항·설계 복원, 신뢰도 분류 | [wf-design/references/reverse-engineering.md](./skills/wf-design/references/reverse-engineering.md) |
| 문서 머리말, 상태값, 식별자, 하이퍼링크, 추적표, 인계 형식 | [wf-doc/SKILL.md](./skills/wf-doc/SKILL.md) |
| 문서 유형별 필수 절과 템플릿 | [wf-doc/references/templates.md](./skills/wf-doc/references/templates.md) |

다음 단계: [Workflow 2 — 계획 수립 + 구현 + 검증·리뷰 + 통합](./02_IMPLEMENTATION_AND_INTEGRATION.md)

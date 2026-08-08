# Workflow 2 — 계획 수립 + 구현 + 검증·리뷰 + 통합 (개요)

> 상태: 초안 0.4
>
> 목적: 승인된 요구사항과 설계를 구현하고, 완료 여부를 검증하여 안전하게 통합한다.

> **이 문서는 개요입니다.** 실행 기준(정본)은 [skills/wf-implement/SKILL.md](./skills/wf-implement/SKILL.md)이며, 내용이 다르면 스킬을 따릅니다. 이 문서는 워크플로우의 목적과 형태를 설명할 뿐 절차를 규정하지 않습니다.

## 이 단계가 결정하는 것

Workflow 2는 [Workflow 1](./01_REQUIREMENTS_AND_DESIGN.md)이 발행한 **승인된 기준선 안에서 어떤 작업과 코드로 구현하고 완료를 어떻게 증명할지** 소유한다.

- 작업 분할, 순서, 의존성과 변경 대상 파일
- 코드·테스트·설정 변경
- 구체적인 테스트 선택·실행과 증거 기록
- 자체 리뷰, 통합, 완료·부분 완료·차단 판단

요구사항, 인수 조건, 공개 인터페이스, 데이터 모델, 보안 정책, 주요 컴포넌트 책임을 바꿔야 하면 영향받는 구현을 보류하고 Workflow 1로 반환한다. 판단이 애매하면 중대한 변경으로 취급한다.

## 진행 형태

```text
현재 상태 재확인 → 계획 수립 → 구현 → 검증 → 자체 리뷰 → 통합 → 최종 결과 보고
```

승인된 기준선 안의 되돌릴 수 있는 로컬 변경은 별도 승인 없이 진행한다. push, PR 생성·병합, 패키지 게시, 배포, 외부 전송, 되돌리기 어려운 마이그레이션은 사용자가 명시적으로 요청하거나 승인한 경우에만 수행한다. **설계 승인은 이런 외부·비가역 작업의 실행 승인이 아니다.**

## 최소 구현 원칙

코드 작성은 [ponytail](https://github.com/DietrichGebert/ponytail) 스킬의 `full` 모드를 기준으로 하며, 만들 필요 → 기존 재사용 → 표준 라이브러리 → 플랫폼 기능 → 기존 의존성 → 한 줄 → 최소 코드 순의 결정 사다리를 따른다. 신뢰 경계의 입력 검증, 데이터 손실을 막는 오류 처리, 보안과 접근성은 최소화 대상이 아니다.

ponytail 스킬이 설치되어 있고 지침이 다르면 [wf-implement §2.4](./skills/wf-implement/SKILL.md#24-최소-구현-원칙--ponytail-full-모드)를 우선한다.

## 완료의 증거

"완료"는 코드가 작성되었다는 뜻이 아니다. 완료 여부는 인수 조건과 검증 결과로 판단하며, 실행하지 못한 검증은 성공한 것으로 간주하지 않는다. 조건을 충족하지 못하면 "완료"가 아니라 "부분 완료" 또는 "차단됨"으로 보고한다.

## 작업 기록

계획의 진행 상태와 검증 결과는 대화가 아니라 `docs/work/<작업-ID>/`에 갱신하며, 세션이 중단된 뒤 재개할 때 가장 먼저 읽는 재개 지점으로 사용한다. 파일 구성은 [wf-implement §7](./skills/wf-implement/SKILL.md#7-작업-기록과-저장-위치)이 정한다.

## 상세 절차

| 내용 | 정본 위치 |
|---|---|
| 시작 조건, 기본 원칙, 진행 절차, 변경 관리, 완료 조건 | [wf-implement/SKILL.md](./skills/wf-implement/SKILL.md) |
| wf-design과의 역할 경계와 반환 흐름 | [wf-implement/SKILL.md](./skills/wf-implement/SKILL.md#wf-design과의-역할-경계) |
| 설계 변경(DCR) 분류와 재승인 | [wf-design/references/design-change.md](./skills/wf-design/references/design-change.md) |
| 계획·작업 기록·검증·완료 보고의 Markdown 골격 | [wf-doc/references/templates.md](./skills/wf-doc/references/templates.md) |

선행 단계: [Workflow 1 — 요구사항 정의 + SW 설계](./01_REQUIREMENTS_AND_DESIGN.md)

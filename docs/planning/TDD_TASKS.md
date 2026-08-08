# TDD 반영 작업 정의

> 상태: 반영됨
> 작성일: 2026-08-08

> **이 문서는 기획 기록입니다.** 규정 정본은 [skills/wf-implement/SKILL.md](../../skills/wf-implement/SKILL.md)(§2.4·§3.2·§3.3·§3.4)이며, 내용이 다르면 스킬을 따릅니다.

## 요약

개발 워크플로우 스킬 생태계(wf-design, wf-implement, wf-doc, wf-tree)에 TDD(Test-Driven Development)를 반영한다.

핵심 구도: TDD는 wf-implement §2.4의 기존 테스트 기준을 **대체하지 않고 병존**한다. §2.4는 무엇을·얼마나 테스트할지(범위 — "깨지면 실패하는 가장 작은 검증 하나", "자명한 한 줄 변경 면제")를, TDD는 언제·어떤 순서로 작성할지(시점 — 실패하는 테스트 먼저)를 규정한다. 자명한 한 줄 변경은 테스트 자체가 면제이므로 TDD도 자동 면제된다.

## 관련 문서

- [Human–AI Development Workflow](../../README.md)
- [wf-design](../../skills/wf-design/SKILL.md), [wf-implement](../../skills/wf-implement/SKILL.md), [wf-doc](../../skills/wf-doc/SKILL.md), [wf-tree](../../skills/wf-tree/SKILL.md)
- 선례 패턴: [코드 역공학 작업 정의](./CODE_REVERSE_ENGINEERING_TASKS.md), [작업 계획 트리 작업 정의](./PLAN_TREE_TASKS.md) — 기획 문서 → 사용자 검토·승인 → 스킬 반영 → 링크 검증 경로

## 규정 요약

정본은 wf-implement이며, 이 절은 반영된 규정의 요약이다.

- **TDD 사이클([§3.3](../../skills/wf-implement/SKILL.md#33-구현)):** 각 작업 단위는 Red(실패하는 가장 작은 테스트 작성, 의도한 이유의 실패 확인) → Green(결정 사다리를 적용한 최소 구현으로 통과) → Refactor(성공 유지하며 정리) 순서로 구현한다. 적용할 수 없는 변경은 이유를 작업 기록에 남기고 후행 검증으로 대체한다.
- **버그 수정([§3.3](../../skills/wf-implement/SKILL.md#33-구현)):** 원인 수정 전에 버그를 재현하는 실패 테스트를 먼저 작성한다. 자동 재현이 불가능하면 수동 재현 절차와 이유를 기록한다. 경량 경로의 단일 버그 수정에도 적용한다.
- **인수 테스트 선행([§3.2](../../skills/wf-implement/SKILL.md#32-계획-수립)):** 자동화 가능한 인수 조건은 어느 작업에서 실패하는 인수 테스트로 먼저 전환할지 계획에서 식별한다. 추적은 기존 `AC-NN` ↔ `VER-NN`을 재사용한다.
- **특성화 테스트([§3.3](../../skills/wf-implement/SKILL.md#33-구현)):** 테스트가 없는 기존 코드의 동작을 변경하기 전에 현재 동작을 고정하는 특성화 테스트를 변경 범위에 비례해 작성한다. 역공학 작업에서는 [역공학 산출물](../../skills/wf-design/references/reverse-engineering.md)의 검증 가능한 기대 동작을 입력으로 사용한다.
- **증거([§3.4](../../skills/wf-implement/SKILL.md#34-검증)):** TDD 테스트는 최초 실패 실행과 성공 실행을 모두 증거로 기록한다(실패→성공 전환). 결과 값은 기존 어휘(성공·실패·미수행)만 사용하고, 구현 전의 의도된 실패는 증거·비고에 기록한다.
- **ponytail 정합([§2.4](../../skills/wf-implement/SKILL.md#24-최소-구현-원칙--ponytail-full-모드)):** §2.4 기준이 요구하는 테스트의 작성은 결정 사다리 1단계(YAGNI)의 기각 대상이 아니다. Green 단계의 최소 구현은 결정 사다리와 같은 방향이다.

## 소유권

| 영역 | 소유 |
|---|---|
| TDD 사이클, 버그 재현 테스트, 특성화 테스트, TDD 증거 규칙 | [wf-implement](../../skills/wf-implement/SKILL.md) — 정본 |
| 인수 조건의 의미와 자동 테스트로 전환 가능한 형태 | [wf-design §4.2](../../skills/wf-design/SKILL.md#42-요구사항-정의) |
| `test` 노드의 선행 표기·배치, 분기 템플릿 제안 | [wf-tree](../../skills/wf-tree/SKILL.md) — 제안하되 결정하지 않는다 |
| 검증 증거의 표기 위치와 결과 상태 어휘 | [wf-doc](../../skills/wf-doc/SKILL.md) — 새 상태값·식별자 없음 |

기존 경계표(정본)의 의미는 바뀌지 않았다. "구체적인 테스트 선택·실행"은 이미 wf-implement 소유이며, TDD는 그 방법의 시점 규정이다.

## 반영 지점

| 파일 | 변경 |
|---|---|
| [wf-implement/SKILL.md](../../skills/wf-implement/SKILL.md) | §2.4 테스트 우선 관계, §3.2 선행 테스트·인수 테스트 전환 계획, §3.3 TDD 사이클·버그 재현·특성화, §3.4 실패→성공 증거, §3.5 리뷰 항목 |
| [wf-design/SKILL.md](../../skills/wf-design/SKILL.md) | §4.2 자동 인수 테스트로 전환 가능한 인수 조건 형태 |
| [wf-design/references/reverse-engineering.md](../../skills/wf-design/references/reverse-engineering.md) | §8 특성화 테스트 소유권 포인터와 인계 입력 |
| [wf-tree/SKILL.md](../../skills/wf-tree/SKILL.md) | `test` 노드 설명, `implement` 분기 템플릿 선행 표시, 버그 수정 트리거 행, test 자식 첫 배치 규칙, 예시 갱신 |
| [wf-doc/references/templates.md](../../skills/wf-doc/references/templates.md) | 검증 결과 절에 TDD 증거 포인터(새 열·상태값 없음) |
| [02_IMPLEMENTATION_AND_INTEGRATION.md](../../02_IMPLEMENTATION_AND_INTEGRATION.md) | 테스트 우선(TDD) 개요 절 |
| [README.md](../../README.md) | wf-implement 소유 항목에 테스트 우선(TDD) |
| [CLAUDE.global.md](../../setup/CLAUDE.global.md), [AGENTS.codex.md](../../setup/AGENTS.codex.md) | 진입 규칙에 TDD 항목 |

## 결정 기록

기획 단계의 질문은 사용자 결정으로 모두 해소되었다.

| 질문 | 결정 (2026-08-08, 사용자) |
|---|---|
| Q-01 TDD 기본 강도 | **기본 규칙** — 테스트를 남기는 모든 구현 작업에 test-first 기본 적용, 예외는 이유를 작업 기록에 남김 |
| Q-02 인수 테스트 선행 | **비례 적용** — 자동화 가능한 AC만 관련 구현 시작 전 실패하는 인수 테스트로 전환, 나머지는 §3.4 시나리오 검증 유지 |
| Q-03 버그 재현 테스트 | **필수** — 자동 재현 가능하면 재현 테스트 먼저, 불가능하면 수동 재현 절차와 이유 기록. 경량 경로에도 적용 |
| Q-04 특성화 테스트 | **포함** — wf-implement §3.3에 규정, 역공학 절차에는 소유권 포인터만 |
| Q-05 정본 배치 | **SKILL.md 본문 통합** — 상시 적용 규칙이므로 references 분리 없이 본문 편집 |
| Q-06 wf-tree 반영 범위 | **전부** — 분기 템플릿 선행 표시, 버그 수정 트리거 행, 노드 유형 설명, 예시의 test 자식 선행 표시 |
| Q-07 설치 규칙 갱신 | **추가** — CLAUDE.global.md·AGENTS.codex.md에 TDD 항목. 사용자 홈 설치본은 설치 스크립트 재실행 시 갱신됨 |

## 완료 조건

- wf-implement에 TDD 사이클·버그 재현·특성화 테스트·증거 규칙이 반영되었다.
- §2.4 기존 테스트 기준과의 관계(병존: 범위 vs 시점)가 명시되었다.
- 새 상태값·식별자 없이 기존 wf-doc 어휘를 재사용했다.
- 경계표(정본)의 의미가 바뀌지 않았고 상대 요약이 여전히 유효하다.
- 개요 문서와 설치 규칙이 정본과 어긋나지 않게 갱신되었다.
- 저장소 전체 로컬 링크·앵커가 기계 검증을 통과했다.

이 문서는 TDD 반영의 범위와 결정을 정리한 기획 기록이다. 규정 정본은 [wf-implement SKILL.md](../../skills/wf-implement/SKILL.md)다.

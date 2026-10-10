# v2 전환 조사 — 액션 아이템

> 상태: 작업 목록(조사 트랙). wf-design 승인 대상이 아니며 스킬·docs 정본을 편집하지 않는다.
> 목적: v1 베이스라인(사이클 1~4 완료, 커밋 `e937c5a`) 위에서 외부 조사 결과를 적용한 v2로 넘어가기 전에, 미적용 항목의 학술 근거를 정리하고 오늘 기준 유효성을 판정하고 신기술을 탐색한다.
> 입력: [9월 조사 색인](../20260919-aidlc-research/00_research_index_and_remaining.md), [10월 테스트 수명주기 digest §5](../20261009-test-lifecycle/testing_research_digest.md), [10월 9일 적용 분석표](../20261009-research-application/application_analysis.md).
> 작성 2026-10-10.

## 액션 아이템

| ID | 항목 | 산출물 | 상태 | 세션 |
|---|---|---|---|---|
| A0 | v1 베이스라인 긋기 — git tag, README 선언, 적용 분석표를 `e937c5a` 기준으로 재기준화(묶음 B 적용됨 반영, 사이클 4 후속 3건을 묶음 A 입력으로 이동, 어절 예산 재측정) | tag `v1`, README 1문단, [01_rebaseline.md](./01_rebaseline.md) | 완료 | 1 |
| A1 | 미적용 항목 ↔ 근거 논문 대응표 — 항목·묶음·논문 ID·핵심 주장·우리 적용 형태·판정·A2 검증 깊이 | [02_unapplied_items_papers.md](./02_unapplied_items_papers.md) | 완료 | 1 |
| A2 | 근거 논문의 오늘(2026-10-10) 기준 유효성 재검증 — 개정·철회·반박·재현, 핵심 수치의 생존, 실험 모델 세대, 도구(Claude Code 훅) 사양 변화. 설계 방향을 결정한 6편은 정밀, 나머지는 약식 | [03_paper_validity_check.md](./03_paper_validity_check.md) | 완료 | 1 |
| A3 | 미완 조사 회수 — 색인 §3-A 3건(MCP 보안 정밀, 악성 스킬 3편, AI-DLC 2026 운영 모드), §3-C 중 Spec-Driven Development·Agentic AI in SDLC, digest §5 중 검증기 게이밍·tessl 삭제 관문 원문 | `04_recovered_research.md` | 대기 | 2 |
| A4 | 신기술 탐색 — 색인 §3-D 중 코드↔문서 드리프트 탐지·비용·토큰 경제학·한국어 환경 3영역 우선, 2026-08 이후 신규 출판물을 게이트·검증 강제 / 세션 메모리·인계 / 스킬·컨텍스트 파일 품질 / 멀티에이전트 SDLC 거버넌스 4축으로 검색. 후보마다 "기존 S 대체 / 신규 S / 범위 밖" 판정, S22부터 번호 부여 | `05_new_techniques.md` | 대기 | 2 |
| A5 | 종합 — A1~A4를 하나의 적용 분석표로 묶고 v2 사이클 편성 후보(A 강제 게이트, C 자문 요청, D 코드 저장소 실측, 신규)와 권고 순서를 제시. wf-design 입력으로 인계 | `06_v2_application_analysis.md` | 대기 | 3 |

## 사용자 결정 사항 (미결)

| ID | 질문 | 제안 | 결정 |
|---|---|---|---|
| D-01 | 게이트웨이 트랙(색인 §3-B: Zup·캐싱·라우팅·관측성)을 v2 범위에 넣는가 | 제외. 워크플로우와 재료가 겹치지 않아 별도 트랙 | 미결 |
| D-02 | D 코드 저장소 실측을 v2 사이클과 병행하는가 | v2 사이클 중 최소 1개는 코드 저장소에서 수행(효과 측정은 이 저장소에서 불가) | 미결 |
| D-03 | A2 판정 깊이 | 설계 방향을 결정한 6편(TDAD·Skills Harmful·Smells·AI-DLC quality-gate·PROJECTMEM·Systems Problem) 정밀, 나머지 약식 | 세션 1에서 제안대로 수행 |

## 세션 편성

- 세션 1(2026-10-10): A0·A1·A2. 외부 조사는 서브에이전트 3개 병렬(정밀 6편 / 약식 16편 / Claude Code 훅 사양).
- 세션 2: A3·A4. 외부 검색 비중이 높아 서브에이전트 병렬.
- 세션 3: A5. 결과를 wf-design 입력으로 넘기고 v2 첫 사이클의 작업 ID를 발행한다.

## 산출물 위치와 보존 규칙

- 이 폴더 `docs/research/20261010-v2-research/`에 번호 순으로 보존한다. 조사 산출물은 승인 대상이 아니므로 `docs/status.md` 행을 만들지 않는다(선례: [20261009-research-application](../20261009-research-application/application_analysis.md) 보존 커밋 `6026739`).
- 완료 작업 기록·ADR·DCR·스킬 본문은 편집하지 않는다. 스킬 변경은 A5 이후 wf-design 사이클에서만.

# TESTMAP-20260920-enforced-gates: 테스트 맵

> 문서 유형: `test-map`
> 작업 ID: `20260920-enforced-gates`
> 상태: `completed`
> 기준선: `v2` ([REQ-DESIGN-enforced-gates](./req-design.md), 2026-09-21 승인)
> 작성일: 2026-09-20
> 최종 갱신: 2026-09-20
> 관련 문서: [PLAN-llm-workflow: 구현 계획](../../plan.md), [WORK-20260920-enforced-gates: 작업 기록](./work-log.md), [REQ-DESIGN-enforced-gates](./req-design.md)

## 요약

- 목적: 이 작업이 수정·신설하는 파일의 관련 테스트를 식별한다. 사이클 1과 달리 변경 대상의 절반이 **실행 코드(PowerShell 훅)** 이므로 실제 자동 테스트가 매핑되며, 이 저장소에서 `관련 테스트`가 `없음`이 아닌 첫 맵이다.
- 현재 결론 또는 상태: 구현분의 테스트 번호 확정 — T22~T38 신설(하네스 총 38건). 훅 계열 6파일은 단일 하네스, 게이트 정의 2파일은 게이트 명령 자체 실행, 산문 4파일은 관련 테스트 없음.
- 다음 행동: 없음 — DCR-006 승인으로 T36 기대값을 600으로 갱신 완료.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-enforced-gates](./req-design.md) | FR-13, DES-10, AC-10·11 | 맵 생성과 TDD 의무의 근거 |
| output | related | [PLAN-llm-workflow](../../plan.md) | TASK-37~43 `관련 테스트` 필드 | 각 TASK가 이 표의 행을 가리킨다 |
| output | related | [WORK-20260920-enforced-gates](./work-log.md) | 회귀 의무 목록, 검증 | 의무 목록 후보의 원천 |

## 생성 정보

- 생성 방법: 명명 규칙 + 참조 검색 — `setup/hooks/tests/run-tests.ps1`에서 변경 대상 파일명과 `Invoke-Hook` 대상 검색, `docs/presentation/tests/test_make_pptx.py`에 대해서도 동일 검색
- 생성 시점과 기준 커밋: 2026-09-20 23:27 · `2ff74ee` (워킹트리 미커밋 변경은 이 작업의 문서뿐 — 코드 무변경)

## 매핑

| 변경 예정 파일 | 관련 테스트 | 실행 명령 | 근거 | 사전 실행 (SHA · 결과) |
|---|---|---|---|---|
| `setup/hooks/wf-common.ps1` | `run-tests.ps1` 전량 (T01~T21 기존 + T22~T26 파서·트리 키) | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` | 훅 4종이 모두 dot-source 하는 공통 모듈이라 하네스 전량이 관련 테스트 | `2ff74ee`+미커밋 · 38/38 성공 |
| `setup/hooks/wf-stop-gate.ps1` (신설) | `run-tests.ps1` T27~T35, T38 (차단·통과·합집합·인프라·인용·가드·분류·ANSI) | 위와 동일 | 신설 훅 — 기존 훅 3종과 같은 `Invoke-Hook` 패턴 | `2ff74ee`+미커밋 · 38/38 성공 |
| `setup/hooks/messages/stop-gate.md` (신설) | `run-tests.ps1` T27·T34·T35·T38 (차단 사유 본문) | 위와 동일 | 훅이 주입하는 본문이므로 block 출력 검사에 포함 | `2ff74ee`+미커밋 · 38/38 성공 |
| `setup/hooks/install-hooks.ps1` | `run-tests.ps1` T18~T21 기존 + T36~T37 (Stop 등록·timeout 값) | 위와 동일 | T18~T21이 등록 결과 settings.json을 직접 검사 | `2ff74ee`+미커밋 · 38/38 성공 |
| `setup/hooks/messages/resume.md` | `run-tests.ps1` T01 | 위와 동일 | T01이 SessionStart 주입 출력을 검사 (본문 문자열까지는 미검사 — grep 대조 병행) | `2ff74ee`+미커밋 · 38/38 성공 |
| `setup/hooks/messages/post-compact.md` | `run-tests.ps1` T14 | 위와 동일 | T14가 post-compact 주입 출력을 검사 (위와 동일 단서) | `2ff74ee`+미커밋 · 38/38 성공 |
| `setup/setup_claude.ps1` | 없음 | — | `run-tests.ps1`이 이 스크립트를 호출하지 않음 (설치 경로는 `install-hooks.ps1`만 테스트 대상) | — (수동 확인 + grep) |
| `docs/quality-gates.md` (신설) | 없음 (자동 테스트) — 게이트 정의 자체를 실행해 검증 | `gitleaks detect --no-git --source . --no-banner --redact --exit-code 2 --config .gitleaks.toml` | 산문 + 게이트 정의 파일. 정의의 정확성은 정의된 명령을 실제로 돌려야만 확인된다 | AC-09 3건 실측 통과 (정상 0 / 탐지 2 / allowlist 0) |
| `.gitleaks.toml` (신설) | 없음 (자동 테스트) — 위와 동일 명령 | 위와 동일 | allowlist 정확성은 픽스처 스캔으로 확인 (AC-09) | AC-09 (3) allowlist 통과 |
| `skills/wf-implement/SKILL.md` | 없음 | — | 산문 스킬 문서. 하네스가 참조하지 않음 | — (grep 대조, AC-08) |
| `skills/wf-implement/references/verification-depth.md` | 없음 | — | 산문 | — (grep 대조, AC-08) |
| `docs/plan.md`, `docs/work/20260920-enforced-gates/*.md` | 없음 | — | 계획·작업 기록 문서 | — (규칙 대조) |

**사전 실행 기준선.** `2ff74ee` 기준 `run-tests.ps1` 21/21 성공, exit 0 (2026-09-20 23:1x). 기존 실패 없음 — 이 작업에서 발생한 모든 실패는 이 작업이 만든 것이다. 구현 후 최종은 38/38 성공, exit 0 (2026-09-21 00:17).

**저장소의 다른 자동 테스트.** `docs/presentation/tests/test_make_pptx.py`(8건)는 이 작업의 변경 파일을 참조하지 않으므로 관련 테스트가 아니다. 통합(§3.6)의 전체 스위트 1회 실행 의무에는 포함되며, `pytest`·`python-pptx`를 설치해 **8/8 성공**으로 실행했다([작업 기록 검증](./work-log.md#검증)).

## 맵 누락 기록

| 발견 시점 | 실패한 테스트 | 원인 파일 | 누락 원인 |
|---|---|---|---|
| — | — | — | 없음 — 이 작업의 모든 실패는 맵 안의 `run-tests.ps1`에서 발견됐다 |

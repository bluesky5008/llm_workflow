# DCR-015: C층에 회귀 보호 훅 추가 — 보호 테스트 편집 확인과 종료 시 대장 정합 검사

> 문서 유형: `dcr`
> 작업 ID: `20261025-regression-guard`
> 상태: `approved`
> 기준선: `v3 → v4` (승인일 2026-10-25) ([REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md))
> 작성일: 2026-10-25
> 최종 갱신: 2026-10-25
> 관련 문서: [ADR-014: 회귀 보호 훅의 강제 방식](./ADR-014-회귀-보호-훅-강제-방식.md), [REQ-DESIGN-regression-guard](./req-design.md), [REQ-llm-workflow: 요구사항](../../requirements.md), [DESIGN-llm-workflow: 설계](../../design.md), [WORK-20261025-regression-guard: 작업 기록](./work-log.md)

## 요약

- 목적: 세션 핸드오프만 다루던 C층에 회귀 보호 훅 2종을 추가한다 — PreToolUse 보호 테스트 편집 확인, Stop 대장 정합 검사.
- 현재 결론 또는 상태: 제안. 승인 시 REQ·DESIGN-llm-workflow v4.
- 다음 행동: [REQ-DESIGN-regression-guard](./req-design.md) 승인 관문에서 함께 승인 여부.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-llm-workflow](../../requirements.md#기능-요구사항) | 요약·문제와 목적·범위, FR 추가, NFR-01, AC 추가, 추적성 | 변경 대상 요구사항(v3) |
| input | baseline | [DESIGN-llm-workflow](../../design.md#컴포넌트와-책임) | 설계 목표와 제약, 시스템 경계, DES 추가, DES-04, 데이터와 인터페이스, 실패 흐름, 검증 전략 | 변경 대상 설계(v3) |
| input | decision | [ADR-014](./ADR-014-회귀-보호-훅-강제-방식.md) | document | 이 DCR이 싣는 결정 |
| input | related | [REQ-DESIGN-regression-guard](./req-design.md) | FR-03·04 | 이 변경을 요구한 작업 |
| output | related | [WORK-20261025-regression-guard](./work-log.md) | 인계 | 승인·통합 추적 |

## 변경 사유와 증거

- **요구:** 액션 아이템 R-02·R-03([04_test_action_items](../../research/20261025-aidlc-trends/04_test_action_items.md)) — 사용자 지시 "회귀테스트 분야를 먼저", "R1부터 실행하자"(2026-10-25).
- **증거:** [ADR-014 배경](./ADR-014-회귀-보호-훅-강제-방식.md#배경).
- **능력(2026-10-25 공식 훅 문서):** PreToolUse `permissionDecision`(`allow|deny|ask`), `tool_input.file_path`, Stop `decision: block` + `stop_hook_active`, 연속 8회 차단 시 무시.

## 기존 기준선과 설계

- REQ 요약·문제와 목적: "세션 핸드오프의 세 지점을 자동화하는 C층". 범위 포함: 훅 스크립트·설치 로직·README.
- NFR-01: 모든 훅 fail-open.
- DESIGN 출력 계약: `additionalContext` 주입만. 등록: SessionStart 2, PostToolUse 1.

## 제안 설계

1. **DES-06 `wf-test-guard.ps1`** — PreToolUse(matcher `Edit|Write|MultiEdit|NotebookEdit`).
   - 가드: `<cwd>/docs/test-register.md`가 없으면 무출력 exit 0.
   - 대상 경로: `tool_input.file_path`(NotebookEdit는 `notebook_path`). `cwd` 기준 상대 경로로 바꾸고 `\`→`/`, 대소문자 무시.
   - 대장 파싱: `## 대장` 표의 헤더에서 `테스트 파일`·`상태` 열 위치를 찾고, `상태`가 `유지`로 시작하는 행의 `테스트 파일` 값을 `; `로 나눠 `-like` 대조. 한글 토큰은 코드포인트로 구성(ASCII 소스, DES-05).
   - 어댑터 선언 보호 경로(②, `wf-common.ps1` 상수): `~/.claude/settings.json`, `~/.claude/settings.local.json`, `<cwd>/.claude/settings.json`, `<cwd>/.claude/settings.local.json`. 대장 자체(`docs/test-register.md`)는 확인 대상이 아니다(사후 판정 FR-08).
   - 일치: `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"<messages/test-guard.md> (TST-NN)"}}`. 권한 자동 승인 모드 처리는 [ADR-014 결정 1](./ADR-014-회귀-보호-훅-강제-방식.md#결정).
   - 실패: 대장이 있는데 파싱 실패·예외 → `ask`(fail-to-ask, 이유에 `guard=error`). 대장 부재 → 무출력.
2. **DES-07 `wf-stop-gate.ps1`** — Stop. 판정 없는 얇은 래퍼(판정은 하네스 중립 B층 스크립트 `skills/wf-doc/scripts/regression_guard.py`, [REQ-DESIGN-regression-guard DES-04](./req-design.md#설계)).
   - 가드: 대장 부재 → exit 0. `stop_hook_active` 참 → exit 0.
   - 호출: `python <훅 스크립트 기준 저장소의 skills/wf-doc/scripts/regression_guard.py> <cwd>`, timeout 10초. 스크립트 경로는 `$PSScriptRoot` 기준으로 찾는다(대상 저장소에 skills/가 없어도 동작).
   - exit 1 → `{"decision":"block","reason":"<messages/stop-gate.md> <스크립트 출력>"}`. exit 0 → 무출력.
   - 실패: Python 부재·timeout·exit 2·예외 → 무출력 exit 0(fail-open 유지).
3. **DES-04 설치** — `Install-WfHooks`의 desired에 `PreToolUse`(위 매처)·`Stop`(매처 없음) 추가. 자기 항목 식별 규칙(`wf-*.ps1`)은 그대로라 재실행 멱등.
4. **메시지** — `messages/test-guard.md`: "대장 `유지` 테스트의 수정이다. 수정 이유가 테스트 오류인지 요구사항 변경인지 [충돌 출구]에 따라 판정하고, 수정은 재정비 관문 절차로 기록한다." `messages/stop-gate.md`: "`유지` 테스트가 기록 없이 바뀌었다. 되돌리거나 작업 기록 `### 테스트 대장 변경`에 분류·증거와 함께 기록하라." 둘 다 스킬 절을 링크하는 포인터.

## 변경 항목

| 대상 | 변경 전 | 변경 후 | 이유 |
|---|---|---|---|
| REQ 요약·문제와 목적·대상과 시나리오 | 세션 핸드오프 3지점 | + 회귀 보호 2지점(편집 확인, 종료 정합), 시나리오 4·5 | 범위 확장 |
| REQ 범위 포함 | 훅 3종 | 훅 5종 | 범위 확장 |
| REQ FR | FR-01~05 | + FR-06 보호 테스트 편집 확인, FR-07 종료 시 대장 정합 | 제안 설계 1·2 |
| REQ NFR-01 | 모든 훅 fail-open | + 예외 1: FR-06 가드는 대장이 있는데 읽지 못하면 확인 요청([ADR-014](./ADR-014-회귀-보호-훅-강제-방식.md)) | 가드의 실패 결과가 다름 |
| REQ FR-05 | `docs/work/` 없으면 무동작 | + FR-06·07은 `docs/test-register.md` 없으면 무동작 | 가드 기준 |
| REQ AC | AC-01~06 | + AC-07(편집 확인/미등록 통과/파싱 실패 확인), AC-08(종료 차단/기록 시 통과/재진입 통과), AC-09(대장 부재 무동작) | 검증 |
| DESIGN 설계 목표와 제약 | fail-open 단일 원칙, PS 5.1만 의존 | + 가드 예외, 출력 계약 확장(권한 결정·종료 차단), Stop 래퍼의 B층 Python 호출(부재 시 fail-open) | ADR-014 |
| DESIGN 컴포넌트 | DES-01~05 | + DES-06·07, DES-04 등록 2종 추가 | 제안 설계 |
| DESIGN 데이터와 인터페이스 | 출력 `additionalContext` | + `permissionDecision`·`permissionDecisionReason`, `decision`·`reason`. 입력 + `tool_input`, `permission_mode`, `stop_hook_active` | 계약 명시 |
| DESIGN 실패 흐름·검증 전략 | 3훅 | + 2훅의 실패 정책, T29~ 케이스 | 검증 |
| `setup/hooks/wf-test-guard.ps1`·`wf-stop-gate.ps1` | 없음 | 신설 | 구현 |
| `setup/hooks/wf-common.ps1` | — | 대장 파싱(DES-08 규칙)·경로 정규화·Claude 게이트 설정 경로 상수·출력 함수 추가 | 공통화 |
| `setup/hooks/install-hooks.ps1` | 등록 3 | 등록 5 | 설치 |
| `setup/hooks/messages/` | 3파일 | + `test-guard.md`, `stop-gate.md` | 포인터 |
| `setup/hooks/tests/run-tests.ps1` | T01~T28(29) | + T29~(가드·게이트·설치) | 회귀 방지(Red 선행) |
| `README.md` 훅 설명 | 3종 | 5종 + 해제 방법 | 사용자 문서 |

## 영향 범위

- 요구사항: FR-01~05 의미 무변경. NFR-01에 예외 1건.
- 컴포넌트 책임: DES-01~03·05 무변경. DES-04 등록 목록만 확장.
- 인터페이스: 기존 3훅 무변경. 새 훅이 권한 결정을 반환 — 사용자 전역 설치이므로 **대장이 있는 모든 저장소**에서 편집 확인이 생긴다(대장이 없으면 무동작).
- 보안: 에이전트가 자기 게이트를 끄는 경로(Claude 설정 파일 편집)를 같은 장치로 확인. 훅·판정 스크립트는 로컬 파일 읽기·git 읽기만, 네트워크 없음.
- 의존성: Stop 래퍼가 처음으로 Python을 호출한다. 부재 시 종료 검사만 꺼지고(fail-open) 편집 시점 가드는 PS만 쓴다.
- 다른 하네스: 판정이 B층 스크립트이므로 Codex·SEMCo-Work 어댑터는 같은 CLI를 호출하면 된다(이 DCR 범위 밖).
- 성능: PreToolUse는 대장 1개 읽기(수 KB)·정규식. Stop은 Python 기동 + git 2~4회.
- 진행 중인 구현: 없음 — design-change §3.A 해당 없음.

## 고려한 대안

[ADR-014 고려한 대안](./ADR-014-회귀-보호-훅-강제-방식.md#고려한-대안) A~E.

## 구현된 코드의 처리

- 아직 구현 없음(승인 후 wf-implement). 유지: 기존 3훅 전부.

## 마이그레이션과 롤백

- 마이그레이션: `setup_claude.ps1` 재실행으로 등록 추가. 대장에 `테스트 파일` 열이 없는 다른 저장소는 가드가 열을 찾지 못해 `ask`(fail-to-ask)가 되므로, 구현에서 **열 부재는 "보호 대상 없음"(무출력)으로, 표 파싱 오류만 `ask`로** 구분한다.
- 롤백: 커밋 `git revert` 후 `setup_claude.ps1` 재실행, 또는 `~/.claude/settings.json`의 `PreToolUse`·`Stop`에서 `wf-test-guard`·`wf-stop-gate` 항목 삭제.

## 검증 방법

- `powershell -NoProfile -ExecutionPolicy Bypass -File setup/hooks/tests/run-tests.ps1` — 기존 29 + 신규, Windows PS 5.1(사용자 PC).
- 실세션: 이 저장소에서 `유지` 테스트 파일 편집 시도 → 확인 프롬프트, 권한 자동 승인 모드 1회.
- 린트 2종 0 오류.

## 남은 위험

- `ask`의 권한 자동 승인 모드 동작 미확인 — [ADR-014 후속 작업](./ADR-014-회귀-보호-훅-강제-방식.md#후속-작업).
- 기록 행만 쓰는 우회 — 완료 보고 관문 승인에 의존.
- 번호: [결정 등록부](../../decisions.md) 기준 다음 번호 ADR-014·DCR-015.

## 승인 기록

- 2026-10-25 — [REQ-DESIGN-regression-guard](./req-design.md#승인-기록) 승인 관문에서 함께 **승인**(Q-02 3층 구조 반영본). REQ·DESIGN-llm-workflow v3 → v4.

## 변경 이력

| 날짜 | 변경 | 근거 | 상태 또는 기준선 | 작성자·승인자 |
|---|---|---|---|---|
| 2026-10-25 | 최초 작성 | [REQ-DESIGN-regression-guard](./req-design.md) FR-03·04, 훅 문서 확인 | proposed | Claude(작성) |
| 2026-10-25 | 승인 관문 응답 반영 — Claude 게이트 설정 경로 확정(②), Stop 훅을 B층 판정 스크립트의 래퍼로 변경, 의존성·다른 하네스 영향 추가 | 사용자 결정 Q-01~Q-04(3층 구조) | proposed | Claude(작성) |
| 2026-10-25 | 승인, REQ·DESIGN-llm-workflow v4 반영 | 사용자 승인(대화형 관문) | proposed → approved, v3 → v4 | 사용자(승인) |

## 인계

- 다음 단계 또는 워크플로우: 승인 시 wf-design §5 승인 절차(DCR·ADR `approved`, REQ·DESIGN v4, decisions.md) → wf-implement
- 시작 조건: 충족 — 승인(2026-10-25)
- 입력 문서와 기준선: 위 문서 연결
- 완료된 항목: 제안 설계, 변경 항목, 영향 범위
- 미완료 항목: 승인, 구현, 검증
- 차단 요인: 없음
- 다음 행동: wf-implement 계획 수립 — [작업 기록 인계](./work-log.md#인계)

# DESIGN-llm-workflow: Human–AI 개발 워크플로우 설계

> 문서 유형: `design`
> 작업 ID: `20260809-claude-hooks`
> 상태: `approved`
> 기준선: `v1` (승인일 2026-08-09)
> 작성일: 2026-08-09
> 최종 갱신: 2026-08-09
> 관련 문서: [REQ-llm-workflow: 요구사항](./requirements.md), [ADR-001: 컨텍스트 신호 선택](./work/20260809-claude-hooks/ADR-001-컨텍스트-신호-선택.md)

## 요약

- 목적: 세션 핸드오프 C층 — Claude Code 훅 3종과 설치 로직의 설계를 확정한다.
- 현재 결론 또는 상태: 기준선 v1 승인·구현 완료(설계 일탈 없음). 검증은 [추적성](#추적성) 참조.
- 다음 행동: 없음 — 후속 작업은 [작업 기록 완료 보고](./work/20260809-claude-hooks/work-log.md#완료-보고) 참조.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-llm-workflow: 요구사항](./requirements.md) | FR-01~05, AC-01~06 | 이 설계의 입력 요구사항 |
| input | decision | [ADR-001: 컨텍스트 신호 선택](./work/20260809-claude-hooks/ADR-001-컨텍스트-신호-선택.md) | document | DES-02의 신호 결정 |

## 설계 목표와 제약

- **fail-open:** 훅의 어떤 실패도 세션을 막지 않는다. 실패 시 A층(수동 경로)이 그대로 남는다.
- **하네스 중립 보존:** skills/ 본문 무변경. 훅이 주입하는 지시는 스킬이 규정한 절차를 가리키는 포인터일 뿐 새 규범을 만들지 않는다.
- **문서화된 능력만 사용:** 훅 이벤트·필드·출력 계약은 Claude Code 공식 문서에 있는 것만 쓴다(조사 결과 2026-08-09, [hooks 문서](https://code.claude.com/docs/en/hooks.md)).
- **환경:** Windows PowerShell 5.1. 한글 텍스트는 인코딩 안전 경로로만 다룬다.
- **전역 설치:** `~/.claude/settings.json`에 등록되어 모든 저장소에서 발화하므로, 스크립트가 저장소 사용 여부를 스스로 가드한다(FR-05).

## 시스템 경계와 구조

```text
Claude Code (훅 이벤트 발생)
  │ stdin: 입력 JSON (session_id, transcript_path, cwd, source, ...)
  ▼
setup/hooks/*.ps1  (이 저장소가 정본, 절대 경로로 등록됨)
  │ 저장소 가드: <cwd>/docs/work/ 없으면 무출력 종료
  │ 상태 파일: %TEMP%\claude-wf\<session_id>.json
  ▼
stdout: {"hookSpecificOutput":{"hookEventName":"...","additionalContext":"..."}}
  ▼
모델 컨텍스트 (스킬 절차 포인터가 주입됨)
```

- 훅 스크립트와 주입 메시지 파일은 이 저장소 `setup/hooks/`에 두고, `setup_claude.ps1`이 절대 경로로 `~/.claude/settings.json`에 등록한다. `git pull`만으로 스크립트가 최신화된다(기존 skills junction과 같은 원리).
- 컴팩션 직전 개입은 불가능하므로(조사 결과: PreCompact는 주입 불가) 사전(DES-02)·사후(DES-03) 2단으로 감싼다.

## 컴포넌트와 책임

- DES-01: **`wf-session-start.ps1`** — `SessionStart`(matcher `startup|resume|clear`). `<cwd>/docs/work/*/work-log.md`의 공통 머리말 `> 상태:`를 읽어 완료 계열(`completed`, `superseded`, `rejected`, `withdrawn`) 이외의 작업 기록을 찾는다. 있으면 작업 ID·경로 목록과 "재개 절차(인계 절의 '다음 행동')를 먼저 적용하라"는 지시를 `additionalContext`로 주입한다. 동시에 상태 파일에 현재 transcript 크기를 기준점으로 기록한다(DES-02의 입력). 미완료 기록이 없으면 기준점만 기록하고 무주입.
- DES-02: **`wf-context-threshold.ps1`** — `PostToolUse`(matcher `*`). transcript 크기의 성장량(현재 크기 − 기준점)이 임계값을 넘으면 "다음 계획 항목 경계에서 wf-implement 세션 인계를 수행하라"는 지시를 주입한다. 주입 후에는 상태 파일에 경고 시점 크기를 기록하고, 재경고 간격만큼 더 성장하기 전까지 재주입하지 않는다. `UserPromptSubmit`이 아닌 `PostToolUse`를 쓰는 이유: 자동 실행 중에는 사용자 프롬프트 없이 툴 사용만 이어지므로 그 경로에서 발화해야 한다.
- DES-03: **`wf-post-compact.ps1`** — `SessionStart`(matcher `compact`). 컴팩션 직후 "요약은 손실 압축이다. 진행 중 작업 기록의 인계 절과 대조해 상태를 재확인하고, 요약과 문서가 다르면 문서를 정본으로 삼아라"는 지시를 주입하고, 상태 파일의 기준점을 현재 transcript 크기로 재설정한다(컴팩션 후 컨텍스트가 줄었으므로 성장량 계산을 다시 시작).
- DES-04: **`setup_claude.ps1` 훅 설치 로직** — `~/.claude/settings.json`을 JSON으로 읽어 `hooks` 키에 위 3개 항목을 병합한다. 파일·키가 없으면 만들고, 기존의 무관한 설정과 사용자 훅은 보존한다. 자기 항목의 식별은 스크립트 경로 문자열 매칭으로 하며, 재실행 시 중복 등록하지 않고 경로가 다르면(저장소 이동) 갱신한다.
- DES-05: **메시지 파일 분리** — 주입할 한글 텍스트는 `.ps1` 소스에 리터럴로 넣지 않고 `setup/hooks/messages/*.md`(UTF-8)에서 `Get-Content -Encoding UTF8`로 읽는다. 출력 전 `[Console]::OutputEncoding`을 UTF-8로 설정한다. PS 5.1이 BOM 없는 `.ps1`의 한글 리터럴을 오독하는 문제를 원천 회피한다.

## 데이터와 인터페이스

- **훅 등록(설정 계약):** exec form을 사용한다 — `command: "powershell.exe"`, `args: ["-NoProfile","-ExecutionPolicy","Bypass","-File","<저장소>\\setup\\hooks\\<스크립트>.ps1"]`, `timeout: 10`(초). 셸 파싱과 프로필 로드를 배제한다.
- **훅 입력:** 문서화된 공통 필드만 사용 — `session_id`, `transcript_path`, `cwd`, `hook_event_name`, (SessionStart의) `source`. stdin은 UTF-8로 읽는다.
- **훅 출력:** 주입 시 `{"hookSpecificOutput":{"hookEventName":"<이벤트>","additionalContext":"<텍스트>"}}` 한 줄. 무주입 시 출력 없이 exit 0.
- **상태 파일:** `%TEMP%\claude-wf\<session_id>.json` — `{ "baselineBytes": n, "lastWarnedBytes": n|null, "updatedAt": "ISO8601" }`. 없으면 그 자리에서 재생성(기준점=현재 크기). 오래된 파일은 무해하며 청소는 범위 밖.
- **설정값:** 임계값 `CLAUDE_WF_THRESHOLD_KB`(기본 1500), 재경고 간격 `CLAUDE_WF_REWARN_KB`(기본 300) — 환경 변수로 재정의 가능, 기본값은 스크립트 상수. 기본값의 근거: transcript는 컨텍스트보다 빠르게 자라는 보수적 프록시이므로 통상적 자동 컴팩션 발생점보다 먼저 발화하는 쪽으로 잡고, 조기 발화의 비용은 "다음 경계에서"라는 지시 문구로 낮게 유지한다. 구현 중 실측으로 보정할 수 있다.
- **미완료 판정(DES-01):** work-log 머리말의 `> 상태:` 값이 완료 계열이 아니면 미완료. 머리말을 읽을 수 없는 파일은 건너뛴다(오탐 방지).

## 정상·실패·복구 흐름

- **정상:** 이벤트 → 가드 통과 → 판정 → (필요시) 주입 → exit 0.
- **가드(모든 스크립트 공통, FR-05):** `<cwd>/docs/work/`가 없으면 즉시 무출력 exit 0.
- **실패(NFR-01):** 스크립트 전체를 try/catch로 감싸고 catch에서 무출력 exit 0. stdin JSON 파싱 실패, transcript 부재, 상태 파일 손상 모두 동일 — 주입 포기가 유일한 실패 결과이며 A층 수동 경로가 유지된다.
- **타임아웃:** 훅별 `timeout: 10`초. 모든 작업이 파일 stat·소형 JSON 읽기/쓰기이므로 통상 밀리초 단위다(NFR-03).
- **동시성:** PostToolUse가 짧은 간격으로 겹쳐도 상태 파일은 마지막 쓰기 승리로 충분하다(값이 단조 증가 크기이므로 경합 손실의 영향은 재경고 시점이 약간 밀리는 정도).

## 보안과 품질 속성

- 주입 텍스트는 저장소의 작업 ID·경로 목록과 고정 지시문만 포함한다. 비밀 정보·대화 내용을 읽거나 전송하지 않는다.
- 훅 스크립트는 로컬 파일 읽기와 `%TEMP%` 쓰기만 수행하며, 네트워크 접근이 없다.
- 스크립트 정본이 git 저장소에 있으므로 변경이 감사 가능하다. 설치는 사용자가 실행하는 setup 스크립트를 통해서만 일어난다.

## 마이그레이션과 롤백

- 설치: `setup_claude.ps1` 재실행(멱등). 설정 변경은 Claude Code 재시작 없이 반영된다(문서화된 동작).
- 롤백: `~/.claude/settings.json`의 `hooks`에서 이 저장소 경로를 포함한 항목을 제거하면 된다. 임시 비활성은 settings의 `disableAllHooks` 또는 항목 삭제로 가능하다. 제거 절차는 README에 기록한다.
- 데이터 마이그레이션 없음. 상태 파일은 `%TEMP%` 휘발성 데이터다.

## 검증 전략

- **스크립트 단위(TDD 가능):** 견본 stdin JSON을 파이프로 넣어 stdout 계약을 검사하는 Pester 없는 소형 테스트 스크립트(`setup/hooks/tests/`)를 둔다. AC-01(미완료 유/무), AC-02(임계값 초과/미만/재경고 억제), AC-05(가드), AC-04(강제 오류 시 exit 0·무출력)를 커버한다. 구체적 테스트 선택과 Red 실행은 wf-implement 계획이 소유한다.
- **설치 로직:** 임시 디렉터리를 홈으로 위장한 병합 함수 테스트(미설치/기설치/무관 키 보존 — AC-03).
- **실세션 확인:** 이 저장소에서 세션 시작·`/compact` 후 주입 여부를 관찰(AC-01, AC-06).

## 대안과 결정

- [ADR-001: 컨텍스트 사용량 신호 선택](./work/20260809-claude-hooks/ADR-001-컨텍스트-신호-선택.md) — transcript 크기 성장 프록시(기준점 보정) 채택. 대안(statusline 브리지, 모델 자기 판단, 마일스톤 카운트) 비교는 ADR 참조.
- 소결정 (ADR 불요, 근거만 기록):
  - 임계값 검사를 `UserPromptSubmit`이 아닌 `PostToolUse`에 둔다 — 자동 실행 중 발화 필요(DES-02 참조).
  - PreCompact 차단(exit 2)은 사용하지 않는다 — 컴팩션을 막으면 컨텍스트 한계에서 세션이 더 나쁘게 실패한다.
  - 메시지를 파일로 분리한다(DES-05) — 인코딩 안전.

## 가정과 미해결 질문

- 가정: `transcript_path`는 컴팩션 후에도 같은 세션에서 유지되며 파일은 계속 성장한다. 이 가정이 틀려도(새 파일로 교체) DES-03의 기준점 재설정이 크기 0 기준으로 동작하므로 안전하다.
- 가정: 자동 컴팩션도 `SessionStart`(source `compact`)를 발화시킨다(문서의 matcher 목록에 근거). 구현 검증에서 수동 `/compact`로 확인하고, 자동 발화가 다르면 발견 사항으로 기록 후 DCR 여부를 판단한다.

## 위험

- RISK-04: 훅 API의 필드·계약 변경. 완화: 문서화된 필드만 사용, fail-open, 스크립트가 저장소 정본이라 일괄 수정 용이.
- RISK-05: 임계값 프록시의 부정확성으로 조기·지연 발화. 완화: 설정 가능 임계값, 재경고 간격, "다음 경계에서" 지시로 조기 발화 비용 최소화(요구사항 RISK-02와 동일 계열, 설계 수단 확정).

## 추적성

| 요구사항 | 설계 | 작업 | 인수 조건 | 검증 | 결과 |
|---|---|---|---|---|---|
| [FR-01](./requirements.md#기능-요구사항) | DES-01, DES-05 | [TASK-02](./plan.md#작업-목록) | AC-01 | [VER-01, VER-07](./work/20260809-claude-hooks/work-log.md#검증) | 성공 (실세션 관찰 VER-07 미수행) |
| [FR-02](./requirements.md#기능-요구사항) | DES-02, DES-05 | [TASK-03](./plan.md#작업-목록) | AC-02 | [VER-02](./work/20260809-claude-hooks/work-log.md#검증) | 성공 |
| [FR-03](./requirements.md#기능-요구사항) | DES-02, DES-03 | [TASK-03, TASK-04](./plan.md#작업-목록) | AC-02, AC-06 | [VER-02, VER-06](./work/20260809-claude-hooks/work-log.md#검증) | 성공 (실세션 관찰 VER-06 미수행) |
| [FR-04](./requirements.md#기능-요구사항) | DES-04 | [TASK-05](./plan.md#작업-목록) | AC-03 | [VER-03](./work/20260809-claude-hooks/work-log.md#검증) | 성공 |
| [FR-05](./requirements.md#기능-요구사항) | DES-01, DES-02, DES-03 | [TASK-02~04](./plan.md#작업-목록) | AC-05 | [VER-05](./work/20260809-claude-hooks/work-log.md#검증) | 성공 |

## 승인 기록

- 2026-08-09 — 사용자가 대화형 승인 관문에서 [REQ-llm-workflow](./requirements.md)와 함께 기준선 v1로 **승인**. 응답: "승인". [ADR-001](./work/20260809-claude-hooks/ADR-001-컨텍스트-신호-선택.md) 동시 승인.

## 변경 이력

| 날짜 | 변경 | 근거 | 상태 또는 기준선 | 작성자·승인자 |
|---|---|---|---|---|
| 2026-08-09 | 최초 작성(훅 능력 조사 반영) | [REQ-llm-workflow](./requirements.md), 훅 문서 조사 | draft → awaiting-approval | Claude(작성) |
| 2026-08-09 | 승인 관문 통과, 기준선 v1 발행 | 사용자 승인(대화형 관문) | awaiting-approval → approved, v1 | 사용자(승인) |

## 인계

- 다음 단계 또는 워크플로우: 없음 — 구현·통합 완료 ([작업 기록](./work/20260809-claude-hooks/work-log.md) 참조)
- 시작 조건: N/A — 완료
- 입력 문서와 기준선: [REQ-llm-workflow](./requirements.md), 이 문서, [ADR-001](./work/20260809-claude-hooks/ADR-001-컨텍스트-신호-선택.md)
- 완료된 항목: 요구사항 정의, 훅 능력 조사, 설계, ADR, 구현(TASK-01~06), 실설치
- 미완료 항목: 실세션 관찰 [VER-06·VER-07](./work/20260809-claude-hooks/work-log.md#검증)
- 차단 요인: 없음
- 다음 행동: 다음 새 세션에서 실세션 관찰 결과를 작업 기록 검증 표에 갱신

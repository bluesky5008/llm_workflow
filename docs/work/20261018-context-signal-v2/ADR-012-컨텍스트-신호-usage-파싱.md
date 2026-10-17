# ADR-012: 컨텍스트 사용량 신호를 transcript usage 파싱으로 교체

> 문서 유형: `adr`
> 작업 ID: `20261018-context-signal-v2`
> 상태: `approved`
> 기준선: `v3` ([DESIGN-llm-workflow](../../design.md), 승인일 2026-10-18)
> 작성일: 2026-10-18
> 최종 갱신: 2026-10-18
> 관련 문서: [ADR-001: 컨텍스트 신호 선택](../20260809-claude-hooks/ADR-001-컨텍스트-신호-선택.md), [DCR-013: 컨텍스트 신호 v3와 재개 절차 경량화](./DCR-013-컨텍스트-신호-v3-재개-경량화.md), [DESIGN-llm-workflow: 설계](../../design.md), [REQ-llm-workflow: 요구사항](../../requirements.md)

## 요약

- 결정: 임계 훅(DES-02)의 컨텍스트 사용량 신호를 **transcript 꼬리의 마지막 assistant `usage` 블록에서 읽은 실제 컨텍스트 토큰**(`input_tokens + cache_creation_input_tokens + cache_read_input_tokens`)으로 교체한다. 파싱이 불가능할 때만 ADR-001의 바이트 성장 프록시로 폴백한다. 임계값은 토큰 절대값(`CLAUDE_WF_THRESHOLD_TOKENS`, 기본 130000)으로 둔다.
- 핵심 이유: 바이트 프록시는 **작업 유형에 따라 토큰과의 비율이 수 배 달라져** 편집 위주의 큰 작업에서 실제 사용률 30~50%에 조기 발화한다. usage 블록은 모델이 실제로 지고 있는 프롬프트 크기 그 자체라 작업 유형과 무관하다.
- 주요 단점: transcript JSONL의 내부 형식은 공식 계약이 아니다. 형식이 바뀌면 파싱이 실패하고 폴백으로 내려간다(fail-open이라 세션은 막히지 않음).

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | supersedes | [ADR-001: 컨텍스트 신호 선택](../20260809-claude-hooks/ADR-001-컨텍스트-신호-선택.md) | document | 대체 대상. 승인 시 ADR-001을 `superseded`로 전이 |
| input | baseline | [REQ-llm-workflow: 요구사항](../../requirements.md#기능-요구사항) | FR-02, FR-03(a), AC-02, RISK-02, 가정(transcript 프록시), Q-01 | 결정이 해소·갱신하는 요구·질문 |
| output | decision | [DESIGN-llm-workflow: 설계](../../design.md#컴포넌트와-책임) | DES-02, 데이터와 인터페이스(상태 파일·설정값), RISK-05 | 이 결정이 적용되는 설계 요소 |
| output | change | [DCR-013](./DCR-013-컨텍스트-신호-v3-재개-경량화.md) | 변경 항목 | 기준선 변경 요청(이 ADR을 포함) |

## 배경

ADR-001(2026-08-09)은 "훅 입력에 토큰 필드가 없다"는 조사 결과에 따라 transcript 파일 크기의 성장량을 프록시로 채택했고, 실측(1758KB ≈ 11~15 bytes/token)으로 기본값 1500KB를 200K 창의 50~70% 지점으로 보정했다([작업 기록](../20260809-claude-hooks/work-log.md) 발견과 결정).

2026-10-18 사용자 관찰: `/clear` 후 재개 프롬프트로 이어가는 운용에서 **큰 구현 작업일수록 실제 컨텍스트 대비 임계 훅이 이르게 발화**한다. 원인 분석 결과 프록시의 오차가 상수가 아니라 작업 유형의 함수였다.

- 사실: transcript JSONL의 한 줄에는 컨텍스트에 올라가지 않는 데이터가 포함된다 — `Edit`/`Write`의 `toolUseResult.originalFile`(수정 전 파일 전체), `Read`의 내용 이중 기록(`tool_result` + `toolUseResult.file.content`), 이전 턴의 thinking 블록(API가 컨텍스트에서 제거), 콘텐츠 블록마다 반복되는 메시지 봉투.
- 해석: 큰 파일을 여러 번 편집하는 구현 세션은 바이트/토큰 비율이 설계·토론 세션(11~15)보다 훨씬 높다. 같은 1500KB가 구현 세션에서는 훨씬 낮은 사용률을 뜻하므로 숫자 조절로는 해결되지 않는다.
- 사실(2026-10-18 공식 훅 문서 재확인): 훅 공통 입력 필드는 여전히 컨텍스트 사용량을 노출하지 않는다. `SessionStart(resume|fork)`에만 `context_tokens`가 있을 뿐 `PostToolUse`에는 없다. 임계 판정은 여전히 훅 쪽에서 만들어야 한다.
- 사실: transcript의 assistant 줄에는 API 응답의 `message.usage`가 그대로 기록되며, `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`는 그 호출의 프롬프트 크기 — 즉 모델이 당시 지고 있던 컨텍스트 크기다. statusline이 `used_percentage`를 계산하는 데 쓰는 것과 같은 값이다.

## 영향을 받는 요구사항과 제약

- [FR-02, FR-03(a), AC-02](../../requirements.md#기능-요구사항) — 임계값 판정의 입력과 설정 단위(KB → 토큰)
- [NFR-01](../../requirements.md#비기능-요구사항) fail-open — 파싱 실패는 폴백 또는 무주입
- [NFR-03](../../requirements.md#비기능-요구사항) 성능 — 매 툴 사용마다 실행되므로 파일 꼬리만 읽는다(전체 파싱 금지)
- 설계 제약 "문서화된 능력만 사용" — 훅 입력 필드 `transcript_path`는 문서화되어 있으나 **파일 내부 형식은 비문서화**다. 이 제약을 "문서화된 필드로 접근 가능하고, 형식 변화에 fail-open인 것"으로 완화한다(DCR-013 변경 항목).

## 고려한 대안

| 대안 | 장점 | 단점·위험 | 전환 비용 |
|---|---|---|---|
| A. 바이트 프록시 유지 + 임계값 상향(ADR-001 유지) | 변경 0, 환경 변수만 | 비율이 작업 유형마다 달라 어떤 값도 한쪽 작업에는 틀림. 구현 세션에 맞추면 설계 세션에서 지연 발화 | — |
| B. statusline 브리지(statusline 스크립트가 사용량을 파일로 지속, 훅이 읽음) | 정확한 퍼센트, 창 크기 자동 반영 | 사용자 statusline 설정 점유·병합 필요, 이동 부품 2개, statusline이 안 켜진 세션에서는 신호 없음 | 설치 스크립트 확장 + statusline 스크립트 신설 |
| C. 재개 시 `SessionStart(resume)`의 `context_tokens` 활용 | 문서화된 필드 | resume/fork 시점 1회뿐. 사용자의 운용(`/clear` 후 새 세션)에서는 발생하지 않고 PostToolUse에는 없음 | — |
| D. 마일스톤 카운트(ADR-001 대안 D) | 이식 가능 | 컨텍스트와 상관 약함(ADR-001 기각 사유 유지) | — |
| **E. transcript 꼬리의 마지막 usage 파싱 (채택)** | 모델이 실제로 지는 컨텍스트 크기, 작업 유형 무관. 문서화된 필드(`transcript_path`)만으로 접근. 꼬리 1MB 1회 읽기 + 정규식이라 저비용(실측 수십 ms). statusline과 동일 원천 | 파일 내부 형식 비문서화 → 형식 변경 시 파싱 실패. 완화: fail-open 폴백(ADR-001 방식 유지), 계약 테스트가 형식 가정을 고정 | 훅 1개·공통 함수 1개·테스트 7개 |

## 결정

대안 E를 채택한다.

1. `wf-common.ps1`에 `Get-WfContextTokens`를 둔다: transcript 꼬리 1MB를 읽어 끝에서부터 `"type":"assistant"`이고 `"isSidechain":true`가 아닌 줄의 `"usage":{…}`를 찾아 세 입력 토큰 필드를 합산한다. 못 찾으면 `$null`.
2. `wf-context-threshold.ps1`은 토큰을 읽으면 **절대값 임계**로 판정한다 — 기준점 불필요. `CLAUDE_WF_THRESHOLD_TOKENS`(기본 130000), `CLAUDE_WF_REWARN_TOKENS`(기본 20000). 마지막 경고보다 컨텍스트가 작아졌으면(훅 없이 컴팩션) 재경고 억제를 해제한다.
3. 토큰을 못 읽으면 ADR-001의 바이트 성장 판정을 그대로 수행한다(`CLAUDE_WF_THRESHOLD_KB`·`CLAUDE_WF_REWARN_KB` 유지).
4. 주입 메시지 끝에 ASCII 한 줄 `(context_tokens=N threshold=N signal=usage|bytes)`를 붙인다 — 어떤 신호로 왜 울렸는지 사용자와 모델이 즉시 볼 수 있게 한다(DES-05의 한글 분리 원칙 유지).
5. 상태 파일에 `lastWarnedTokens`를 추가한다. 기존 필드는 폴백용으로 유지한다.

기본값 130000의 근거: 200K 창의 65%. ADR-001 보정이 겨냥한 50~70% 구간의 중앙이며, 경고 후 실제 인계는 다음 계획 항목 경계에서 일어나므로 그 사이의 성장 여유를 둔다. 1M 창 모델을 주로 쓰는 환경은 환경 변수로 올린다.

## 이유

- 측정 대상이 프록시가 아니라 **실제 값**이다. 사용자가 느낀 조기 발화는 프록시 오차의 작업 유형 의존성에서 왔고, E는 그 의존성을 제거한다.
- 훅 쪽 변경만으로 끝난다(대안 B처럼 사용자 환경의 다른 설정을 건드리지 않음). 설치 스크립트·등록 계약 무변경.
- 조기 발화의 실제 비용이 ADR-001의 가정("약간 이른 절단일 뿐")보다 크다는 것이 이번 분석의 결론이다 — 인계는 호출당이 아니라 **건당 고정비**(인계 절 작성 + 새 세션의 재읽기 + 재탐색, 수 분)를 내므로, 실제 사용률이 낮을 때 울리면 품질 이득 없이 고정비만 반복된다. 신호의 정확도가 비용에 직결된다.

## 결과와 감수할 단점

- transcript 형식 가정 3개를 계약 테스트(T22~T28)로 고정한다: assistant 줄에 `"usage":{…}`가 있고, 세 토큰 키 이름이 유지되며, 서브에이전트 줄은 `"isSidechain":true`로 구분된다. 어느 하나가 깨지면 폴백으로 내려가고 주입 메시지의 `signal=bytes`로 드러난다.
- 마지막 usage는 직전 호출의 프롬프트 크기다. 그 호출의 출력과 방금 붙은 툴 결과는 반영되지 않아 수천 토큰 과소 추정할 수 있다 → 기본값을 65%로 둔 이유의 일부.
- 큰 툴 결과 줄(수백 KB)이 마지막 assistant 줄을 꼬리 창 밖으로 밀어내면 그 호출에서는 폴백을 쓴다. 꼬리 1MB는 Claude Code의 툴 결과 절단 한도를 감안한 값이며 테스트 T27이 600KB 케이스를 고정한다.
- 인계 고정비 자체는 이 ADR의 범위 밖이다. [DCR-013](./DCR-013-컨텍스트-신호-v3-재개-경량화.md)이 재개 절차 경량화(wf-implement `references/session-resume.md`, wf-doc 인계 블록의 자기완결 규칙)로 함께 다룬다.

## 후속 작업

- 승인 후 2주간 주입 메시지의 `context_tokens`와 실제 체감(이른가/늦은가)을 대조해 기본값 130000을 1회 보정한다. 결과는 작업 기록에 남긴다.
- Claude Code가 훅 입력에 컨텍스트 사용량을 노출하면(문서 변경 감시) 파싱을 그 필드로 교체하는 ADR을 낸다 — 이 ADR의 대안 E는 그때까지의 다리다.

## 대체 관계

- 대체 대상 ADR: [ADR-001: 컨텍스트 사용량 신호 선택](../20260809-claude-hooks/ADR-001-컨텍스트-신호-선택.md) — 바이트 프록시는 폴백으로 격하
- 대체 ADR: 없음

## 승인 기록

- 2026-10-18 — [DCR-013](./DCR-013-컨텍스트-신호-v3-재개-경량화.md) 대화형 재승인 관문에서 사용자 **승인**. 응답: "좋은 제안입니다. 승인하겠습니다." [ADR-001](../20260809-claude-hooks/ADR-001-컨텍스트-신호-선택.md) `superseded` 전이, DESIGN·REQ-llm-workflow 기준선 v3 발행.

## 변경 이력

| 날짜 | 변경 | 근거 | 상태 또는 기준선 | 작성자·승인자 |
|---|---|---|---|---|
| 2026-10-18 | 최초 작성 | 사용자 관찰(큰 작업에서 조기 발화), transcript 구조 분석, 훅 문서 재확인, 프로토타입 테스트 T22~T28 Green | proposed | Claude(작성) |
| 2026-10-18 | 승인, ADR-001 대체, 기준선 v3 | 사용자 승인(대화형 관문, DCR-013) | proposed → approved | 사용자(승인) |

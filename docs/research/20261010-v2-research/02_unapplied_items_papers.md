# A1. 미적용 항목 ↔ 근거 논문 대응표

> 상태: 분석(wf-design 입력 자료). 승인 전 자료이며 편집을 지시하지 않는다.
> 기준: v1 = `e937c5a`. 판정 어휘는 [적용 분석표](../20261009-research-application/application_analysis.md) §2와 같다(재작성 · 그대로 · 보류 · 폐기). 묶음 B는 사이클 4로 전부 적용되어 이 표에 없다([01_rebaseline.md §2](./01_rebaseline.md#2-분석표-2-재판정--사이클-4-반영)).
> 근거 출처는 9월 조사([색인](../20260919-aidlc-research/00_research_index_and_remaining.md), [리딩 리스트](../20260919-aidlc-research/aidlc_reading_list.md), 묶음 A~D, round3, S21 편집안)에서 옮겼다. 핵심 주장의 수치는 9월 조사가 원문에서 재확인한 값이며, 오늘 기준 생존 여부는 [03_paper_validity_check.md](./03_paper_validity_check.md)가 판정한다.
> 작성 2026-10-10.

---

## 1. 묶음 A — 강제 게이트

| 항목 | 근거 출처 | 출처의 핵심 주장(우리가 의존하는 것) | 우리 적용 형태(현재 구조 기준) | 판정 | A2 깊이 |
|---|---|---|---|---|---|
| S9/AI-07 Stop 게이트 훅 | AI-DLC `plugin/hooks/quality-gate.sh`([GitHub thebushidocollective/ai-dlc](https://github.com/thebushidocollective/ai-dlc)) + AI-DLC 2026([ai-dlc.dev/paper](https://ai-dlc.dev/paper); 9월 조사의 han.guru URL은 404 — [03 §1](./03_paper_validity_check.md#1-정밀-6편)) | Stop·SubagentStop에 게이트 결선, intent+unit 게이트의 가산 병합("no gate is silently dropped"), `stop_hook_active`로 one-attempt-only, 래칫("gates can never be removed during construction"). "처방 대신 역압" | `docs/test-register.md` `유지` 행을 게이트 원천으로 Stop 훅이 실행. 린트 2종 포함 여부는 §3.1 질문 | 재작성 | **정밀** |
| S20 불변 보안 설정 | Agent Security is a Systems Problem ([2605.18991](https://arxiv.org/abs/2605.18991)) | 에이전트가 자기 게이트·훅·설정을 약화시킬 수 없어야 한다(시스템 수준 통제) | wf-implement §2.3 비가역 목록에 "자기 강제 설정 변경" 1항 + 게이트 문서 1문단 | 그대로(소량) | **정밀** |
| S18 명령-데이터 분리 | 같은 논문 | 에이전트 입력에서 명령과 데이터의 채널 분리 | `setup/hooks/messages/resume.md`·`post-compact.md`에 1줄(본문 어절 무관) | 그대로(소량) | 정밀(S20과 동일 출처) |
| S19 선택적 재시도 | RSTD ([2605.15425](https://arxiv.org/abs/2605.15425)) | 정적 분해의 재시도 비용 +80.5%, 실행 가능한 제어 흐름 기반 선택적 재시도 −51.7%(vs 모놀리식). "단계 추가는 이득이 아니다" | §3.3 DCR 반환 문단 뒤 1문단: 실패 TASK만 재시도, 전면 재실행 금지 | 그대로(소량) | 약식 |
| S10 호환성 게이트 | Agent Skills Can Be Harmful ([2608.11888](https://arxiv.org/abs/2608.11888)) | 스킬-태스크 비호환(저장소 관례 불일치, AM 19.2%)이 실패 원인 | §3.3 "저장소의 기존 스타일" 항목에 1문장 | 그대로(1문장) | **정밀** |
| S3 잔여 — 검증 깊이 경로 열·예산 신호 | 같은 논문 | 효율 저하 62.6%가 과잉 절차, 그중 과잉 검증 36.8%. 검증 범위를 불확실성·예산에 조건화 | `references/verification-depth.md` §1에 경로(경량/소규모/고위험) 열·"한 열 오른쪽" 승격 조건, `threshold.md`에 "임계값 수신 후 새 전체 검증 금지" | 재작성 | **정밀** |
| S6 경량 경로 관찰 기준 | From Anatomy to Smells ([2607.01456](https://arxiv.org/abs/2607.01456)) | Rationalization Loophole(94%): 판단 여지가 있는 조건은 우회된다 → 기계적 조건으로 | 깊이 표의 경로 판정 열에 기계 조건 2문장(변경 파일 ≤2 등) | 재작성 | **정밀** |
| S16/AI-12 보안 게이트 | Trust but Verify? Security Debt ([2607.12428](https://arxiv.org/abs/2607.12428)) | 4,022 PR 중 39% 취약, 치명 등급의 99.6%가 하드코딩 자격증명, 리뷰가 81.1%를 놓침 | 시크릿 스캔을 대장 행(보호 스코프=저장소 전체)으로 둘지 별도 게이트 파일로 둘지. 효과는 코드 저장소에서 | 재작성 | 약식 |
| S7/AI-11 시도 등록부 + PreToolUse | PROJECTMEM ([2606.12329](https://arxiv.org/abs/2606.12329)) | append-only 사건 로그(issue/attempt/fix/decision) + 실패한 수정의 반복·취약 파일 편집 전 사전 경고(precheck). 세션당 토큰 50%+ 절감 | work-log `## 검증 결과` 아래 H3 표(새 H2 불가, 린트 L2) + PreToolUse 훅 grep. 또는 대장처럼 저장소 관통 파일 | 재작성 | **정밀** |
| S15 known failure modes | Codified Context ([2602.20478](https://arxiv.org/abs/2602.20478)) | 라우터(핫 메모리)에 반복 실수 목록을 둔다 | S7이 데이터를 모은 뒤 루트 SKILL.md에 | 보류 | 약식 |
| (후속) 린트 2종 Stop 집행 | 선례 ADR-006·ADR-010 — 논문 없음 | — | S9와 같은 훅. "테스트가 아닌 게이트" 원천 질문 | 신규 | — |
| (후속) `render.py` 활성 경로 뷰 훅 주입 | ADR-011 후속 — 간접 근거 OpenDev([2603.05344](https://arxiv.org/abs/2603.05344)) 이벤트 기반 리마인더 | 지시 소실 방지를 이벤트로 | `resume.md` 메시지에 활성 경로 삽입 | 신규 | — |

## 2. 묶음 C — 자문 요청(CRP)

| 항목 | 근거 출처 | 핵심 주장 | 우리 적용 형태 | 판정 | A2 깊이 |
|---|---|---|---|---|---|
| S21/AI-15 자문 요청 | Ask Early, Ask Late, Ask Right ([2605.07937](https://arxiv.org/abs/2605.07937)) · Ask or Assume? ([2603.26233](https://arxiv.org/abs/2603.26233)) · Ambig-SWE ([2502.13069](https://arxiv.org/abs/2502.13069)) · Agentic Abstention ([2606.28733](https://arxiv.org/abs/2606.28733)) · Knowing When to Ask for Help ([2608.24087](https://arxiv.org/abs/2608.24087)) | 질문은 초반 창에서 해야 효과(어떤 프론티어 모델도 최적 창에서 묻지 않음, Gemini 3 Flash 0%) · 과잉 질문은 해결률 하락·비용 2배 · 모델은 유도 없이는 비상호작용이 기본 · 적시 기권 재현율 40% 미만 · "확신에 찬 오답"이 실패 모드 | 규칙 본문 `references/consultation.md`, §3.7 트리거 2~3문장, templates `consultation` 유형, 등록부 CRP 계열, 미해소 CRP는 인계 `차단 요인`에(L7 고정). CRP 상한 3건·판정 시점=항목 시작 | 재작성(분량) | 약식 |

편집안은 "6편"이라 하나 링크로 확인되는 것은 위 5편이다. 6번째는 A3에서 편집안 §1을 재독해 확인한다.

## 3. 독립 항목

| 항목 | 근거 출처 | 핵심 주장 | 우리 적용 형태 | 판정 | A2 깊이 |
|---|---|---|---|---|---|
| S14/AI-14 역공학 보강 | Reversa ([2605.18684](https://arxiv.org/abs/2605.18684)) | Scout→Archaeologist→Detective→Architect→Writer→Reviewer 6역할, 산출물에 confirmed/inferred/gap 신뢰도 태깅, 코드 추적성 | `references/reverse-engineering.md` §5·§8(references라 어절 무관). 역공학 작업 발생 시 | 그대로 | 약식 |
| S8 TASK 모드 필드 | AI-DLC 2026 ([ai-dlc.dev/paper](https://ai-dlc.dev/paper)) | HITL / OHOTL / AHOTL 세 운영 모드 | plan.md TASK 필드. **모드 전환 트리거가 원문에서 확인되지 않아** 보류 | 보류 | 정밀(S9 출처와 함께) |
| S11 Adversarial Spec Review | AI-DLC(Mob Elaboration) vs E2EDevBench ([2511.04064](https://arxiv.org/abs/2511.04064)) | E2EDevBench: 설계 중간층 추가가 역효과(DDT<DT<Single) | wf-design §4.5 확장 — 역효과 근거로 보류 | 보류 | 약식 |
| S17 외부 스킬·룰·MCP 도입 게이트 | Your AI, My Shell ([2509.22040](https://arxiv.org/abs/2509.22040)) + 색인 §3-A 미조사 4편 | 스킬·룰·MCP 3채널의 과정 보안. MCP 채널은 미실험 | 스캔 규칙 — A3(§3-A) 후 | 보류 → A3 | 약식 |

## 4. 팀 배포(9월 묶음 C 원본) — 분석표가 재독하지 않은 묶음

| 항목 | 근거 출처 | 핵심 주장 | 우리 적용 형태 | 판정 | A2 깊이 |
|---|---|---|---|---|---|
| 팀 배포 3단계 | A Few Pages of Markdown ([2608.25241](https://arxiv.org/abs/2608.25241), ASE '26) · Shared Organizational Memory ([2608.00122](https://arxiv.org/abs/2608.00122)) · Early Adoption ([2607.14037](https://arxiv.org/abs/2607.14037)) | 무엇을 커밋하고 무엇을 팀 자산으로 승격하고 리뷰를 어떻게 설계할지 | [다인 토론](../../work/20260814-multiuser-workflow/work-log.md)(on-hold) 재개 입력 | 별도 트랙 | 약식 |

## 5. 설계 노선의 배경 근거(항목이 아니라 방향을 정한 논문)

| 출처 | 우리 설계에서의 역할 | A2 깊이 |
|---|---|---|
| TDAD ([2603.17973](https://arxiv.org/abs/2603.17973)) | "컨텍스트 제공 > 절차 처방": 의존 그래프 제공은 회귀 6.08→1.82%, 'TDD 하라' 지시만은 9.94%로 악화. 사이클 3 대장·보호 스코프 설계와 S1 테스트 맵 폐기의 근거 | **정밀** |
| LoopsBench ([2608.00267](https://arxiv.org/abs/2608.00267)) | 회귀는 모든 루프에서 발생, 병목은 계획·코드·테스트 상태 유지 규율 → 대장·관문·상시 재개 불변식 | 약식 |
| Agentic Harness Engineering ([2604.25850](https://arxiv.org/abs/2604.25850)) | 성능 향상은 시스템 프롬프트가 아니라 도구·미들웨어·메모리에서 → 훅(C층) 투자 노선 | 약식 |
| Evaluating AGENTS.md ([2602.11988](https://arxiv.org/abs/2602.11988)) · Codified Context | 컨텍스트 파일은 비표준 관행 문서화만 유효, 단일 파일은 확장 안 됨 → ADR-010 세 층 | 약식(Codified Context) |

## 6. A2 검증 깊이 배정

- **정밀 6편**: TDAD(2603.17973) · Agent Skills Can Be Harmful(2608.11888) · From Anatomy to Smells(2607.01456) · PROJECTMEM(2606.12329) · Agent Security is a Systems Problem(2605.18991) · AI-DLC quality-gate(GitHub) + AI-DLC 2026(han.guru). 설계 방향을 결정한 수치를 가진 출처.
- **약식 16편**: RSTD · Security Debt · Codified Context · Reversa · Your AI My Shell · LoopsBench · Agentic Harness Engineering · S21 5편 · 팀 배포 3편 · E2EDevBench.
- **도구 사양**: Claude Code 훅(Stop·SubagentStop·PreToolUse·SessionStart·PreCompact, timeout, `stop_hook_active`, block JSON). S9·S7·S18과 사이클 4 후속 2건이 직접 의존.

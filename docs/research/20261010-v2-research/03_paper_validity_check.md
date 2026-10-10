# A2. 근거 논문의 유효성 재검증 — 2026-10-10 기준

> 상태: 분석(wf-design 입력 자료). 승인 전 자료이며 편집을 지시하지 않는다.
> 대상: [02_unapplied_items_papers.md](./02_unapplied_items_papers.md) §6의 정밀 6편·약식 16편·Claude Code 훅 사양. 이전 조사 시점은 2026-08-27.
> 방법: 서브에이전트 3개 병렬. arXiv abs 페이지의 Submission history·Comments, GitHub 커밋 이력, 공식 문서·changelog를 직접 fetch. 2차 출처(자동 리뷰 사이트·블로그)는 보조로만 썼다. fetch한 URL 목록은 §6.
> 판정 어휘: **유효**(근거·수치 그대로) · **수정**(방향은 유효하나 수치·표현·출처를 고쳐야 함) · **폐기**(근거 상실).
> 작성 2026-10-10.

---

## 0. 요지

1. **폐기 판정은 없다.** 22편 모두 철회되지 않았고 반박 논문도 없다. 설계 노선(대장·관문·훅·세 층)은 유지된다.
2. **수정 4건이 설계에 직접 닿는다.** (a) PROJECTMEM v2(9/30)가 "토큰 50%+ 절감"을 스스로 철회 — S7의 기대 효과를 낮춘다. (b) AI-DLC 논문 URL(han.guru)이 404 — 출처 교체. 래칫은 기술적 차단이 아니라 리뷰어 플래그 — S9·S20의 "래칫" 표현 보정. (c) Skills Harmful의 68.8%·36.8%는 분모가 달라 재해석 — S3·S10 근거 문장 보정. (d) Security Debt의 치명 자격증명은 대부분 사람 협업자 귀속 — S16 근거 문장 보정.
3. **도구 사양이 S9 설계를 바꾼다.** Claude Code 훅의 `onFailure` 기본값이 `continue`라서(2.1.295, 10/8) 게이트 훅은 `"onFailure": "block"`을 명시해야 한다. Stop 훅 연속 차단 상한 8회, `shell: "powershell"` 필드 공식 지원, PreToolUse 결정은 `hookSpecificOutput.permissionDecision`.
4. **강화 1건.** Agent Security is a Systems Problem이 NeurIPS 2026 Oral(10/1 공개) — S18·S20의 권위 상승.
5. **S8(TASK 모드 필드)은 폐기 후보.** AI-DLC 저장소·논문 모두 4월 이후 정체이고 모드 전환 트리거는 여전히 정의되지 않았다. A3 §3-A의 "AI-DLC 모드 정밀"은 이 결과로 종결 가능.

---

## 1. 정밀 6편

| 출처 | 최신 버전 | 8/27 이후 | 게재처 | 핵심 주장 생존 | 실험 모델 | 판정 |
|---|---|---|---|---|---|---|
| TDAD (2603.17973) | v2, 2026-03-19 | 없음 | AIware 2026 투고. 7월 프로그램에 미등재 → 미채택 추정(공식 목록 확인 불가) | 6.08→1.82%, TDD 지시만 9.94% 악화 — 초록 그대로. 단 저자 README(72%, 29% vs 31%)와 초록(70%, 24%→32%) 불일치. 독립 재현 없음 | Qwen3-Coder 30B(100건)·Qwen3.5-35B-A3B(25건), 로컬 하드웨어. Claude·GPT 세대 결과 아님 | **수정** — 방향 유효, 단일 근거로 두지 말 것. Skills Harmful(Opus 4.6)이 "절차 처방의 역효과"를 보강 |
| Agent Skills Can Be Harmful (2608.11888) | v1, 2026-08-12 | 없음 | 프리프린트(MSR) | "verification scope and pipeline depth를 task uncertainty·change size·budget에 조건화" 원문 확인. **분모 보정**: 68.8%(86/125)는 Task-Implementation Fault 전체(incorrect fill 36.8% + omission 28.8%). Excessive Procedure 62.6%(114/182) 맞음. Over-verification 36.8%(67)는 전체 182건 대비(Excessive Procedure 대비 58.8%) | **Claude Opus 4.6**, OpenCode 1.15.1. 귀인 도구 GPT-5.5 | **수정(수치 재해석)** — 현행 모델 세대와 가장 가까운 근거. S3·S10·S6의 핵심 |
| From Anatomy to Smells (2607.01456) | v2, 2026-07-03 | 없음 | 프리프린트 | 26 smells·평균 10.5·Rationalization Loophole 94%·Oversized 5,000 words·비영어 9,830 제외 — v2 본문 그대로. 비판(Pith): 스멜=모범사례의 역이라 성능 인과 미측정, 탐지기 F1 0.78, 표본 228 vs 238 불일치 | 탐지기 Qwen3.6-27B. 실행 에이전트 실험 아님 | **유효** — S6(기계적 조건) 근거로 충분. "스멜 제거 → 성능 향상"은 주장하지 말 것 |
| PROJECTMEM (2606.12329) | **v2, 2026-09-30** | **있음(대폭 개정)** | 프리프린트. 코드 v0.3.4 | 자기연구 2개월/10프로젝트/207이벤트 → 6개월/27프로젝트/3,228이벤트. precheck 42.0s → 79.3ms. **"50%+ 토큰 절감" 철회**("we made no paired comparison, so we report no percentage reduction"). precheck는 **파일 단위 advisory**이며 제안된 변경과 과거 실패 접근을 비교하지 않음. 반복 실패 예방 효과 미측정(427건 중 86건에 실패 시도 선행 = 경고 후보일 뿐) | 이벤트 작성 모델 미기록. 호환성: Antigravity·Claude desktop·Codex | **수정** — 이벤트 로그·precheck 구조는 유효, "반복 방지 효과"와 토큰 수치는 전제에서 제거. S7의 기대 효과를 "경고 제공"으로 낮추고 측정은 D에서 |
| Agent Security is a Systems Problem (2605.18991) | v2, 2026-05-20 | 없음 | **NeurIPS 2026 Oral**(956편 중 5편) | 5원칙: Least Privilege · TCB Tamper Resistance · Complete Mediation · Secure Information Flow · Human Weak Link. "명령-데이터 분리"는 3대 메커니즘 중 하나이나 **열린 연구 문제**로 다룸("prompt injection을 완전히 해결하진 못할 것"). "자기 게이트 약화 금지"는 TCB Tamper Resistance + 부록 A Amp AI 사례("enforce immutability on security-critical configuration files") | 실험 아님(실제 공격 11건 분석). Claude Code·skills 사례 포함 | **유효(강화, 표현 보정)** — S20은 TCB 불변성으로, S18은 "완화 수단" 수준으로 서술 |
| AI-DLC quality-gate + AI-DLC 2026 | 저장소 최종 커밋 2026-04-03(1.84.1). `quality-gate.sh` 실질 변경 2026-03-30 | 없음(8/27 이후 커밋 0) | **han.guru 논문 URL 404**. 정상 URL: https://ai-dlc.dev/paper (2026-01-21자). 원본 md: `website/content/papers/ai-dlc-2026.md` | 가산 병합("# Merge gates additively", 동명 게이트는 둘 다 실행)·`stop_hook_active`=true면 exit 0·builder/implementer/refactorer hat만 — 확인. **래칫은 스크립트에 없음**: 논문이 "gates are add-only… reviewer hat verifies gate integrity… any gate removal triggers a request-changes"로 규정(리뷰 플래그). hooks.json: Stop·SubagentStop에 quality-gate.sh(120s)+enforce-iteration.sh(async). **모드 전환 트리거 여전히 미정의**("Default to more supervision when uncertain", Bolt별 선택표만) | Claude Code 플러그인. 모델 미지정 | **수정** — 출처 URL 교체, 저장소 정체 표기. S9의 가산 병합·one-attempt는 유효, "래칫"은 S20(불변성)+리뷰 문항으로 분리. S8은 폐기 후보 |

## 2. 약식 16편

| # | 출처 | 최신 버전 | 8/27 이후 | 게재처 | 반박·후속 | 판정 |
|---|---|---|---|---|---|---|
| 1 | RSTD (2605.15425) | v1, 05-14 | 없음 | ACM CAIS 2026 Agentic SE WS | 없음 | 유효 |
| 2 | Trust but Verify? Security Debt (2607.12428) | v2, 07-19 | 없음 | KDD 2026 AgenticSE WS | 없음. **초록·포스터는 치명 하드코딩 자격증명의 다수를 사람 협업자 책임으로 귀속** | **수정(표현)** — S16 근거 문장에서 "에이전트가 넣는다"로 읽히지 않게. 스캔 게이트의 필요성은 그대로(누가 넣든 잡아야 함) |
| 3 | Codified Context (2602.20478) | v1, 02-24 | 없음 | 프리프린트(+Zenodo) | 없음. 저자 "24.2%는 보편 목표 아님" | 유효 |
| 4 | Reversa (2605.18684) | v1, 05-18 | 없음 | 프리프린트. npm reversa@1.3.3 | 없음. 논문 스스로 "평가 프로토콜 제안" 수준 | 유효 |
| 5 | Your AI, My Shell (2509.22040) | v2, 04-28 | 없음 | 미표기 | **확장판 추정 2605.25871**("…Become the Attacker's Shell", 성공률 41–84%) — 동일 저자 여부 미확인 | 유효 — A3에서 2605.25871 확인 |
| 6 | LoopsBench (2608.00267) | v2, 08-10 | 없음 | 미표기(loopsbench.ai) | 후속 LoopArena(2608.28281) | 유효 |
| 7 | Agentic Harness Engineering (2604.25850) | v4, 05-18 | 없음 | 미표기 | 제3자 리뷰: 단일 벤치마크 한정, "regression blindness" | 유효(한계 표기) |
| 8 | Ask Early, Ask Late, Ask Right (2605.07937) | v1, 05-08 | 없음 | 미표기 | 해설이 "곡선은 단일 연구 근거" 주의 | 유효 |
| 9 | Ask or Assume? (2603.26233) | **v3, 09-07** | **있음** | **EMNLP 2026** camera-ready | 없음 | **수정(재확인)** — S21 편집안의 수치(55.81% vs 65.99%, $3.50 vs $1.63)가 v2 기준일 수 있음. A3 또는 C 착수 시 v3로 재확인 |
| 10 | Ambig-SWE (2502.13069) | v3, 02-21 | 없음 | ICLR 2026 | 없음 | 유효 |
| 11 | Agentic Abstention (2606.28733) | v1, 06-27 | 없음 | 미표기 | 동명 유사 AgentAbstain(2607.10059) 혼동 주의 | 유효 |
| 12 | Knowing When to Ask for Help (2608.24087) | v1, 08-25 | 없음 | 미표기 | 단독 저자 이론+시뮬레이션. 유사 제목 2606.11349 혼동 주의 | 유효(이론) |
| 13 | A Few Pages of Markdown (2608.25241) | **v2, 09-14** | **있음** | **arXiv Comments에 venue 없음** — 9월 조사의 "ASE 2026" 표기 확인 불가 | 저자 "hypothesis-generating" | **수정(출처 표기)** — venue 표기 삭제 또는 근거 제시 |
| 14 | Shared Organizational Memory (2608.00122) | v1, 07-31 | 없음 | 미표기 | 유사 제목 2607.03228 혼동 주의 | 유효 |
| 15 | Early Adoption (2607.14037) | v2, 07-16 | 없음 | KDD 2026 Agentic SE WS | 없음 | 유효 |
| 16 | E2EDevBench (2511.04064) | v1, 2025-11-06 | 없음 | 미표기 | 동명 유사 E2EDev(2510.14509) 혼동 주의. ProjDevBench(2602.01655)가 인용 | 유효 |

## 3. Claude Code 훅 사양(2026-10-10, 문서 v2.1.295·changelog 2.1.296)

우리 훅([install-hooks.ps1](../../../setup/hooks/install-hooks.ps1))은 `SessionStart(startup|resume|clear)`·`SessionStart(compact)`·`PostToolUse(*)` 3종, `command: powershell.exe` + `args` exec form, `timeout = 10`이다. 8월 설계를 깨는 삭제·개명은 없다. 묶음 A 설계에 닿는 사항:

| 항목 | 현행 사양 | 묶음 A에의 영향 |
|---|---|---|
| `onFailure` | 2.1.295(10/8) 추가. 기본 `continue` — 훅이 시작 실패·timeout·예상 밖 exit·잘못된 출력이면 **통과** | S9 게이트 훅은 `"onFailure": "block"` 명시 필수. 설치 스크립트에 필드 추가(버전 하한 2.1.295) |
| Stop 차단 | exit 2(stderr=사유) 또는 stdout `{"decision":"block","reason":…}` 중 하나. 입력 `stop_hook_active`. **연속 차단 상한 8회**(`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`), 도구 호출 시 리셋 | AI-DLC의 one-attempt-only(`stop_hook_active` 즉시 exit 0)를 그대로 쓰거나, 상한 8회를 믿고 재시도 허용 — §3.1 설계 질문에 추가 |
| Stop 비차단 피드백 | `hookSpecificOutput.additionalContext` | 린트 경고(exit 1 아님)를 차단 없이 전달하는 자리 |
| `timeout` | handler별, 단위 초. command 기본 600, `UserPromptSubmit` 등은 30. `async: true`면 미적용 | 우리 10초 고정은 그대로 가능. 게이트(테스트 전량)는 AI-DLC처럼 120초 이상 필요 → 파라미터화(분석표 §3.1 선행 조건 확인) |
| PreToolUse | 입력 `tool_name`·`tool_input`·`tool_use_id`. 결정은 `hookSpecificOutput.permissionDecision` = allow/deny/ask/defer(우선순위 deny>defer>ask>allow). `updatedInput` 존재(전체 교체) | S7 precheck: `deny`가 아니라 `additionalContext`로 경고(PROJECTMEM v2의 advisory 성격과 일치) |
| SessionStart | `source` = startup/resume/clear/compact/fork. resume·fork에 `seconds_since_last_response`·`context_tokens`·`prompt_cache_likely_expired`(2.1.251). 출력은 `hookSpecificOutput.additionalContext` 권장(plain stdout 주입은 미검증). `additionalContext` 10,000자 상한 | 사이클 4 후속 "활성 경로 뷰 주입"은 `additionalContext` JSON으로. 우리 훅이 plain stdout을 쓰는지 점검 |
| Windows 셸 | `shell` 필드 = bash 또는 powershell. 공식 지원. Git Bash 없으면 기본 powershell. exec form은 `.exe`만 | PS 5.1 ASCII 관례 유지 가능. `shell: powershell` + shell form도 선택지 |
| 신규 이벤트 | `PreModelSwitch`·`PostModelSwitch`(2.1.251), `SubagentStart`, `TaskCompleted`, `PostCompact`, `Setup` 등 32종 | `PostCompact`가 있으므로 우리 `SessionStart(compact)` 배선과 비교 검토(경량) |
| 기타 | 2.1.248: 잘못된 `{…}` stdout은 훅 오류로 보고. 2.1.292: 훅 출력의 system-reminder 태그 이스케이프. 2.1.296: PowerShell 훅의 `CLAUDE_ENV_FILE` 수정 | 메시지 파일(`messages/*.md`)에 태그 모양 문자열이 없는지 점검 |

미검증(공식 전문 미확보): Stop에서 `continue:false`·`stopReason`의 동작, settings.json 훅 객체 스키마 예시 전문, `Setup`·`PostCompact`·`defer`의 도입 버전. 묶음 A wf-design §4.1에서 https://code.claude.com/docs/en/hooks#stop 을 직접 확인한다.

## 4. 항목별 결론 — 02 대응표에의 반영

| 항목 | A2 결과 | 02 판정 변경 |
|---|---|---|
| S9 Stop 게이트 | 가산 병합·one-attempt 유효. 래칫은 리뷰 플래그. `onFailure:block`·상한 8회·timeout 파라미터화 추가 | 재작성 유지. 설계 질문에 "one-attempt vs 상한 8회", "`onFailure`" 추가 |
| S20 불변 보안 설정 | NeurIPS Oral로 강화. TCB Tamper Resistance로 서술 | 그대로 유지. AI-DLC "래칫" 의미를 여기에 합침(리뷰 문항 1개) |
| S18 명령-데이터 분리 | 유효하되 "열린 문제" | 그대로 유지. 완화 수단으로만 서술 |
| S19 선택적 재시도 | 유효 | 유지 |
| S10·S3 잔여·S6 | 유효. 수치 분모 보정 | 유지. 근거 문장만 보정 |
| S16 보안 게이트 | 유효. 귀속 표현 보정 | 유지 |
| S7 시도 등록부 | 구조 유효, 효과 수치 철회, precheck=advisory | 재작성 유지. 기대 효과를 "경고"로, PreToolUse는 `additionalContext`. 측정은 D |
| S15 | 유효 | 보류 유지 |
| S21 CRP | 5편 유효. Ask or Assume v3 재확인 | 재작성 유지. 착수 시 v3 수치 반영 |
| S14 역공학 | 유효 | 유지 |
| S8 TASK 모드 | 트리거 미정의 확정, 출처 정체 | **보류 → 폐기 후보**(A5에서 결정) |
| S11 | 유효 | 보류 유지 |
| S17 | 유효 + 확장판 2605.25871 | A3 대상에 2605.25871 추가 |
| 팀 배포 3편 | 유효. A Few Pages venue 표기 보정 | 별도 트랙 유지 |
| 배경(TDAD·LoopsBench·Harness Eng·Codified Context) | 유효. TDAD는 소형 모델 한정·단일 근거 금지 | 노선 유지 |

**사이클 편성에의 영향([01 §6](./01_rebaseline.md#6-사이클-편성-후보-갱신)):** A → C 순서와 D 병행은 그대로. A의 입력에 §3의 훅 사양 표를 추가하고, S8은 A5에서 폐기 여부를 결정한다. A3 §3-A 중 "AI-DLC 모드 정밀"은 이 문서로 종결하고 MCP 보안·악성 스킬(+2605.25871)만 남긴다.

## 5. 이 검증의 한계

- 반박·재현 검색은 논문당 WebSearch 1~2회다. 인용 논문 전수는 보지 않았다.
- AIware 2026 Benchmark 트랙 채택 목록 페이지가 404라 TDAD 미채택은 추정이다.
- han.guru 아카이브(web.archive.org)는 접근하지 못했다. 9월 조사가 읽은 han.guru 판과 ai-dlc.dev/paper 판이 같은지는 미확인.
- Claude Code 훅 문서의 Stop 절 전문과 settings 스키마 예시는 가져오지 못했다(§3 미검증 항목).

## 6. fetch한 URL

- arXiv abs/html: 2603.17973(v1·v2) · 2608.11888(v1 html) · 2607.01456(v1·v2 html) · 2606.12329(v1·v2 html) · 2605.18991(v2 html) · 2605.15425 · 2607.12428 · 2602.20478 · 2605.18684 · 2509.22040 · 2608.00267 · 2604.25850 · 2605.07937 · 2603.26233 · 2502.13069 · 2606.28733 · 2608.24087 · 2608.25241 · 2608.00122 · 2607.14037 · 2511.04064
- GitHub: pepealonso95/TDAD(commits) · riponcm/projectmem · thebushidocollective/ai-dlc(commits, `plugin/hooks/quality-gate.sh` 이력, `website/content/papers/ai-dlc-2026.md` 이력, releases, raw: quality-gate.sh·hooks.json·CHANGELOG.md·README.md·ai-dlc-2026.md) · thebushidocollective/han
- 기타: https://cns.ucsd.edu/neurips-2026-oral-presentation-for-agent-security-is-a-systems-problem/ · https://pith.science/paper/2607.01456 · https://2026.aiwareconf.org/track/aiware-2026-papers · https://ai-dlc.dev/paper · https://han.guru/papers/ai-dlc-2026/ (404) · https://iclr.cc/virtual/2026/poster/10009007 · https://sprite.utsa.edu/publications/posters/llm-judge-smell-kdd-agenticse.pdf · https://eprints.cs.univie.ac.at/8742 · https://arxiv.org/pdf/2608.28281 · https://arxiv.org/pdf/2602.01655
- Claude Code: https://code.claude.com/docs/en/hooks · https://code.claude.com/docs/en/changelog · https://code.claude.com/docs/en/claude_code_docs_map.md

# 3차 검색 — 단계 세분화 · AI 고유 방법론 · 개발 과정 보안 (2026-08-27)

> 질문 3개: ① 개발 단계의 세분화(2단계 vs 다단계)에 대한 실증 ② 전통 SDLC를 벗어난 AI 고유 방법론 ③ 개발 *과정* 자체의 보안.
> 핵심 논문은 초록·본문을 확인해 요약. 워크플로우(wf-design → 승인 → wf-implement 2단계)와의 관련성을 각 표에 표기.

---

## 1. 개발 단계의 세분화 — "몇 단계가 맞는가"

### 핵심 논문

| 논문 | 출처 | 핵심 발견 | 2단계 워크플로우에의 함의 |
|---|---|---|---|
| **Evaluating Software Process Models for Multi-Agent Class-Level Code Generation** (Shafin·Rafi·Li·Chen) | [arXiv 2511.09794](https://arxiv.org/html/2511.09794v1) | 4단계 워터폴(요구→설계→구현→테스트)을 ablation: **모델에 따라 결과가 정반대** — GPT-4o-mini·DeepSeek은 정확도 30–40% 하락, Claude-3.5-Haiku는 +9.5%. 품질(유지보수성)은 일관 개선. **가장 기여가 큰 단계는 테스트.** 단계화는 구조 오류를 줄이고 의미 오류를 늘림 | 단계 수의 정답은 없고 모델 의존적. "검증 단계가 최대 기여"는 wf-implement의 검증 비중을 지지. 단 소형 모델·ClassEval 100건 실험 |
| **E2EDevBench: Benchmarking LLM-based Agent System in End-to-End SW Development** (PKU) | [arXiv 2511.04064](https://arxiv.org/html/2511.04064) | 실전급 프로젝트(평균 19.2파일·2,011줄)에서 SOTA 에이전트는 요구사항의 ~50%만 충족. **실패의 55.8%가 계획 단계**(요구 누락 27.9%+오해석 22.2%), 실행 38.6%, 검증 5.7%. 21%는 상류 실패의 연쇄. **Developer-Tester 2역 구조(53.5%)가 단일·다단계보다 우수** | 병목은 단계 수가 아니라 **요구 이해**. "잘 짜인 2역 분업이 다단계를 이긴다"는 결과는 현 2단계 구조를 직접 지지. wf-design의 요구 누락 방지(§4.2·추적성)가 55.8% 실패 구간을 정조준 |
| **Runtime-Structured Task Decomposition (RSTD)** (IBM·Zoom) | [arXiv 2605.15425](https://arxiv.org/html/2605.15425v1) | **정적 분해는 모놀리식보다 재시도 비용을 80.5% 증가**시킴(하류 연쇄 재실행). 실행 시점 분기 + 실패 서브태스크만 선택 재시도가 재시도 토큰 51.7–73.2% 절감 | 단계를 "사전에 고정된 문서"가 아니라 "실패 시 되돌아갈 경계"로 쓰라는 것. wf-implement의 DCR 반환 흐름(영향 구현만 보류)이 이미 이 방향 — 전면 재실행 금지를 명문화할 근거 |
| Think-on-Process (ToP) (Capital Normal·Tsinghua) | [arXiv 2409.06568](https://arxiv.org/html/2409.06568v1) | 개발 프로세스 자체를 태스크마다 동적 생성, 성공 인스턴스를 마이닝해 프로세스 모델로 재사용. ChatDev식 고정 워터폴 대비 GPT-3.5 +32% | "프로세스는 고정이 아니라 태스크별 산출물"이라는 급진안. 사용자의 경량/정식 경로 분기의 일반화 형태 |
| Mise en Place for Agentic Coding | [arXiv 2605.05400](https://arxiv.org/abs/2605.05400) | 구현 전 "의도적 준비"를 방법론화(본문 추출 실패 — 초록 기준) | wf-design·§3.1 재확인의 이론적 동류 |
| 참고: LLM-Based MAS for SE 서베이 (TOSEM) | [arXiv 2404.04834](https://arxiv.org/html/2404.04834v4) | MetaGPT·ChatDev류 단계 구조의 계보 정리 | 배경 지도 |

### 판정 — 현 2단계 구조에 대한 근거

세 실증이 한 방향을 가리킨다: **단계를 늘리는 것 자체는 이득이 아니다.** 워터폴 4단계는 모델에 따라 해가 되고(2511.09794), 정적 분해는 재시도 비용을 늘리며(RSTD), 다단계 설계는 2역 분업에 진다(E2EDevBench). 반면 (a) 검증 단계의 기여가 가장 크고, (b) 실패의 절반 이상이 요구 이해에서 나며, (c) 실패 지점으로의 선택적 복귀가 핵심이라는 점은 — **"요구·설계를 앞에 두껍게, 검증을 뒤에 두껍게, 사이 반환은 영향 범위만"이라는 현 구조를 지지**한다. 세분화를 검토한다면 단계 추가가 아니라 wf-implement 안의 **복귀 경계(계획 항목 단위 재시도)**를 명확히 하는 쪽이 근거에 맞다.

---

## 2. 전통 SDLC를 벗어난 AI 고유 방법론

| 논문 | 출처 | 제안 내용 | 성격 |
|---|---|---|---|
| **Agentic Software Engineering: Foundational Pillars and a Research Roadmap** (Hassan 외 — SE 3.0 그룹) | [arXiv 2509.06216](https://arxiv.org/html/2509.06216v2) | 4기둥(행위자·프로세스·산출물·도구) 재정의. 새 산출물 어휘: **BriefingScript**(버전 관리되는 임무 브리핑), **LoopScript**(선언적 워크플로우), **MentorScript**(팀 규범 코드화), **CRP**(에이전트→인간 자문 요청 팩), **MRP**(병합 준비 증거 번들), **VCR**(감사 가능한 인간 응답). 인간 역할 = "Agent Coach" | 비전·로드맵 (실증 아님). **사용자 워크플로우와의 대응이 놀랍도록 정확**: req-design.md≈BriefingScript, 스킬≈MentorScript, 완료 보고+검증 증거≈MRP, 승인 기록≈VCR, DCR 반환≈CRP |
| The Rise of AI-Native Software Engineering (Alenezi) | [arXiv 2606.12986](https://arxiv.org/html/2606.12986) | 코드 중심→의도 중심. 3기둥: Intent·Collaboration·Verification. "판단이 희소 자원". 신뢰 역설(도입 증가·보안 악화·신뢰 하락) 정리 | 개관 논문. 교육·역량 관점 포함 |
| Vibe Coding: Toward an AI-Native Paradigm (2025.10) | [arXiv 2510.17842](https://arxiv.org/abs/2510.17842) | 의도+정성 기술자(톤·스타일)로 코드를 생성하는 대화형 패러다임의 형식화: 의도 파서→의미 임베딩→에이전트 생성→피드백 루프 | 형식화+참조 아키텍처(실증 얇음). 사용자 접근과 대척점 — "승인된 명세" 없이 의도에서 직행 |
| Think-on-Process (§1 참조) | [2409.06568](https://arxiv.org/html/2409.06568v1) | **프로세스 자체를 생성·마이닝·진화** — 방법론이 고정물이 아니라 학습되는 산출물 | AI 고유 방법론의 실증 사례 |
| Self-Evolving Software Agents (Trento, AAMAS '26) | [arXiv 2604.27264](https://arxiv.org/html/2604.27264v1) | BDI+LLM: 에이전트가 경험을 관찰해 지식·목표·행동 코드를 스스로 진화. 환경 복잡도가 오르면 견고성 한계 | 탐색적. "요구사항 없이 목표를 발견"하는 극단 |
| Self-Evolving Coding Agents / MOSS (소스 수준 자기 재작성) | [2608.03392](https://arxiv.org/html/2608.03392v2) · [2605.22794](https://arxiv.org/abs/2605.22794) | 에이전트가 자기 소스를 재작성하며 진화 | 미정독(429) — 후보로만 |
| (기존 순회에서 다룬 것) AI-DLC 2026(Intent-Unit-Bolt·3모드·backpressure), Spec-Driven Development(spec-as-source), Ralph 루프, AHE(하네스 자동 진화) | 1·2차 보고서 | — | AI 고유 방법론의 주류는 이미 커버됨 |

### 판정

AI 고유 방법론은 두 갈래다. **(a) 구조 강화형** — SE 3.0·AI-DLC·SDD: 전통 단계를 버리는 게 아니라 산출물을 기계 판독 가능하게 재발명(사용자 워크플로우가 이 갈래의 개인 구현체에 가깝고, SE 3.0의 어휘는 팀 배포 시 대외 설명 언어로 쓸 수 있다). **(b) 구조 해체형** — vibe coding·프로세스 동적 생성·자기 진화: 명세·승인 관문 자체를 우회. 해체형의 실증은 아직 소규모·탐색적이며, E2EDevBench의 "실패 55.8%가 요구 이해"라는 결과가 해체형의 약점을 정확히 찌른다. **깊이 팔 가치가 가장 큰 것은 SE 3.0 로드맵**(사용자 산출물과의 1:1 대응 지도 작성)과 **Think-on-Process**(경량/정식 경로 분기를 "프로세스 선택 학습"으로 일반화할 수 있는지).

---

## 3. 개발 과정의 보안 — 파이프라인 자체가 공격면

| 논문 | 출처 | 핵심 발견 | 워크플로우 관련성 |
|---|---|---|---|
| **"Your AI, My Shell": Prompt Injection on Agentic AI Coding Editors** (Liu·Zhao·Lo 외) | [arXiv 2509.22040](https://arxiv.org/html/2509.22040v2) | AIShellJack: 314개 공격 페이로드·70개 MITRE ATT&CK 기법. **감염 경로가 정확히 개발 재료** — 코딩 룰 파일, 가져온 GitHub 리포, MCP 서버 설정. Cursor·Copilot에서 **공격 성공률 41–84%**, 성공 시 89.6%가 의도한 악성 행동 완전 실행 | **직격**: 사용자의 스킬·룰 파일·훅이 바로 그 "코딩 룰 파일" 채널. 외부 스킬·룰 도입 시 검사 게이트 필요(1차 리스트의 Malicious Skills 계열과 합류) |
| **Agent Security is a Systems Problem** (Christodorescu·Fernandes·Rehberger 외) | [arXiv 2605.18991](https://arxiv.org/html/2605.18991v1) | 입장: **모델을 신뢰 불가 컴포넌트로 취급, 불변식은 시스템 수준에서 강제**. 3기제: 명령-데이터 분리(W⊕X 유추), 자연어→형식 정책 자동 변환+결정적 참조 모니터, 정보 흐름 제어. "ML 가드 중첩은 상관된 실패 — 비ML 강제로 보완" | 묶음 B의 결론(산문 규칙 → 훅 승격)의 보안판. Stop 게이트·pre-commit이 "비ML 결정적 강제"에 해당. 사람이 아니라 시스템이 불변식을 든다 |
| Layered Attack Surface (LASM) 서베이 | [arXiv 2604.23338](https://arxiv.org/html/2604.23338v2) | 7계층(모델→인지→메모리→도구→멀티에이전트→생태계→거버넌스) × 시간 차원. L4의 주범은 "환경 입력을 권위로 취급하는 principal trust inversion". 고위험 미연구 지대는 L5–L7 | 위협 지도로 사용. 사용자 관련 최상위: L4(도구 실행 — 훅·게이트), L3(메모리 — work-log·팀 메모리 오염), L6(스킬·MCP 공급망) |
| When Agents Handle Secrets: Confidential Computing for Agentic AI | [arXiv 2605.03213](https://arxiv.org/html/2605.03213v1) | 에이전트의 비밀 취급을 기밀 컴퓨팅 관점에서 서베이 | 게이트웨이 업무 쪽 확장 후보 |
| Agent Audit | [arXiv 2603.22853](https://arxiv.org/pdf/2603.22853) | LLM 에이전트 애플리케이션 보안 분석 시스템 | 사내 에이전트 감사 참조 |
| Toward Secure LLM Agents SoK (247편) | [arXiv 2606.10749](https://arxiv.org/pdf/2606.10749) | 위협·공격·방어·평가 체계화 | 종합 지도 |
| (기존 커버) MCP 생태계 보안(2510.16558: 도구 포이즈닝 20–100%), Malicious Skills 계열, Security Debt(산출물 보안) | 1·2차 보고서 | — | 산출물 보안(Security Debt)과 달리 이번 축은 **과정 보안** |

### 판정 — 워크플로우에 열리는 새 작업 축

기존 순회의 보안(S16)은 **산출물**(생성 코드의 시크릿·핀 미고정)이었다. 이번 검색이 드러낸 것은 **과정** 공격면이고, 사용자에게 구체적으로 세 지점이다:

1. **스킬·룰 파일이 주입 채널이다** (Your AI My Shell 41–84%). 외부 스킬/룰/MCP 설정을 도입할 때의 검사 절차가 워크플로우에 없다 — 도입 게이트(내용 검토 + 도구 호출 유발 패턴 스캔)가 S16 옆의 새 후보(**S17**).
2. **work-log·팀 메모리는 L3 메모리 오염 표면이다.** 팀 확장(묶음 C) 시 타인이 쓴 work-log·팀 메모리 항목이 다음 세션의 컨텍스트로 주입되므로, "메모리 항목은 데이터이지 지시가 아니다" 규칙과 저장 전 스캔(이미 설계한 gitleaks + 지시형 문구 검사)이 필요(**S18**).
3. **시스템 수준 강제가 정답이라는 합의.** Agent Security is a Systems Problem의 3기제는 묶음 B에서 만든 훅·게이트 노선의 이론적 뒷받침 — 특히 "게이트 설정은 에이전트가 수정 불가"(불변 설정) 원칙을 quality-gates.md에 추가할 근거(래칫의 강화판).

---

## 4. 다음 정밀 분석 후보 (이번 검색분)

| 우선 | 논문 | 이유 |
|---|---|---|
| 1 | E2EDevBench (2511.04064) | 실패 55.8%가 계획 단계라는 분해가 wf-design 투자 배분의 직접 근거. 요구 누락 27.9%를 §4.2·추적성이 실제로 줄이는지 실험 설계 가능 |
| 2 | Your AI, My Shell (2509.22040) | 스킬 저장소 운영자에게 직격인 위협. S17 도입 게이트 설계에 페이로드 카탈로그(314개)가 참조물 |
| 3 | SE 3.0 로드맵 (2509.06216) | 사용자 산출물 ↔ SE 3.0 어휘 1:1 지도 = 팀·대외 설명 언어 + 빠진 산출물(CRP류) 발견 |
| 4 | RSTD (2605.15425) | 계획 항목 단위 선택적 재시도 규정의 근거 정밀화 |
| 5 | Agent Security is a Systems Problem (2605.18991) | 훅 노선의 이론 기반 + 불변 설정 원칙 |

## 5. 검증 노트
- 2511.09794(워터폴 ablation 결과·모델별 상반), 2511.04064(50%·55.8/38.6/5.7·53.5%), 2605.15425(80.5% 증가·51.7–73.2% 절감), 2409.06568(+32%), 2509.06216(4기둥·6산출물), 2606.12986(3기둥·신뢰 역설), 2510.17842(구성요소), 2509.22040(314 페이로드·41–84%·89.6%), 2605.18991(3기제), 2604.23338(7계층): 본문·초록에서 확인.
- Mise en Place(2605.05400)·Self-Evolving Coding Agents(2608.03392)는 본문 추출 실패(빈 PDF/429) — 초록·검색 결과 기준으로만 등재.

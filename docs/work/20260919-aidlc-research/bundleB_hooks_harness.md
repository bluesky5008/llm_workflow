# 묶음 B — 훅·강제 게이트 설계 (Agentic Harness Engineering × PROJECTMEM precheck × AI-DLC quality-gate)

> 목적: S7(실패 등록부 PreToolUse 훅)·S9(Stop 게이트 훅)의 설계 근거와 구현 초안. 부수적으로 "스킬 텍스트 vs 훅 인프라 투자 배분"의 근거 확보.
> 논문·소스: Agentic Harness Engineering (arXiv 2604.25850, 첫 정밀 독해) + PROJECTMEM (2606.12329) 구현 세부 + AI-DLC `plugin/hooks/quality-gate.sh` (GitHub 실코드).
> 핵심 수치·코드는 원문에서 재확인. 작성 2026-08-27.

---

## 0. 이번 묶음의 결론 한 줄

**"산문 규칙이 반복 실패를 못 막으면 그 규칙을 훅으로 승격하라"** — AHE의 ablation(프롬프트 단독 −2.3pp vs 메모리 +5.6, 도구 +3.3, 미들웨어 +2.2)이 이 처방을 수치로 뒷받침하고, 용스님의 기존 훅 3종은 이미 이기는 조합(인프라가 규율을 배달)이며, S7·S9는 그 연장선에서 논문의 1·3위 컴포넌트(메모리·미들웨어)를 결합하는 것이다.

---

# 1. Agentic Harness Engineering 정밀 분석

arXiv 2604.25850 (v1 2026-04-28 → v4 05-18), Lin·Liu·Dou·Xi 외(Fudan 계열).

## 1.1 "하네스"의 정의와 문제의식

하네스 = "the system surrounding the model, including its tools, interfaces, memory, execution constraints, and feedback loops." 구현체(NexAU)는 7개 직교 컴포넌트를 파일화한다: 시스템 프롬프트 / 도구 설명 / 도구 구현 / 미들웨어 / 스킬 / 서브에이전트 설정 / 장기 메모리. 논리적 편집 1건 = git 커밋 1건 — 파일 단위 diff·롤백이 공짜.

수동 하네스 엔지니어링의 세 가지 문제: 이질적 행동 공간, 궤적 속에 묻히는 신호, 편집 효과의 귀속 불가. 이 셋이 해결되지 않으면 자동 진화는 "trial-and-error collapse".

## 1.2 관측성 3요소

1. **컴포넌트 관측성**: 7유형의 명시적 파일 표현. 시드는 의도적 최소("셸 도구 하나, 미들웨어·스킬·서브에이전트 없음") — 추가되는 모든 컴포넌트가 측정된 롤아웃 대비 제 몫을 증명하게 강제.
2. **경험 관측성(궤적 증류)**: 태스크당 k=2 롤아웃의 원시 궤적을 Agent Debugger가 "메시지 1개=파일 1개" 환경으로 만들고, 태스크별 근본 원인 리포트 + 벤치마크 수준 개요로 증류(`runs/iteration_NNN/analysis/overview.md` + `detail/{task}.md`). 원시본 보존 + 점진적 공개로 검증 가능성과 토큰 절약 동시 확보.
3. **결정 관측성(예측 검증)**: 모든 편집에 변경 매니페스트(실패 증거·근본 원인·수정·**예측: 고칠 태스크 목록 + 퇴행 위험 목록**). 다음 라운드에서 예측 vs 실측 delta를 교차해 편집별 판정, 기각은 파일 단위 자동 롤백. "각 편집이 반증 가능한 계약이 된다."

## 1.3 진화가 실제로 만든 것 (Terminal-Bench 2, 69.7→77.0, 10회 반복 × 약 32시간)

| 반복 | 변경 | 성격 |
|---|---|---|
| 2 (~71%) | 8규칙 "계약 우선" 프롬프트(수락 계약 추출·평가기 미러링·최소 편집) + 셸 도구 `timeout_ms` | 프롬프트+도구 |
| 5 (~75.8%) | 검증 완료 산출물을 cleanup으로부터 보호하는 **상태 파괴 가드 미들웨어** | 미들웨어 |
| 6 | 성공 후 수정에 `ALLOW_POST_SUCCESS_RESET` 토큰을 요구하는 **publish-state 가드** + 위험 패턴 감지 시 리마인더를 주입하는 **패턴 카탈로그 미들웨어** | 미들웨어 |
| 8 | 반복 5 가드의 허점 패치 | 가드는 반복 조임이 필요 |
| 10 (77.0%) | 최종: 1,364줄 셸 도구(주변 파일의 계약 힌트 표면화), **12개 경계 사례 교훈의 장기 메모리**, 79줄 프롬프트, 재사용 스킬 소수 | — |

사례 mcmc-sampling-stan이 결정적: **프롬프트 규칙만으로는 프록시 검증 선호를 못 이겼고**, 미들웨어 리마인더+가드 결합이 필요했다.

## 1.4 결과·ablation (재확인 완료)

**Table 3 — 시드에 진화 컴포넌트 하나만 이식:**

| 변형 | 전체 89 | Hard 30 | Δ |
|---|---|---|---|
| 시드 | 69.7 | 51.7 | — |
| +장기 메모리만 | 75.3 | 63.3 | **+5.6** |
| +도구만 | 73.0 | 46.7 | +3.3 |
| +미들웨어만 | 71.9 | 50.0 | +2.2 |
| +시스템 프롬프트만 | 67.4 | 46.7 | **−2.3** |
| 전체 | 77.0 | 53.3 | +7.3 |

"3/4 단일 컴포넌트가 시드를 상회, 프롬프트 교체만 유일한 퇴행." 79줄 프롬프트는 "실행 가능성이 나머지 셋에 의존하는 보편 규율"이라 홀로는 짐. 결론: **"사실적 하네스 구조는 전이되지만 산문 수준 전략은 전이되지 않는다."** 단 양의 기여 합(+11.1) > 전체(+7.3) — 겹쳐 쌓으면 중복 재확인에 턴 소모(과잉 검증 경고와 합치).

**전이**: SWE-bench-verified에 하네스 동결 이식 → 성공률 동급(75.6 vs 75.2)에 토큰 461k vs 526k(**−12.3%**). 교차 모델: DeepSeek-V4-Flash **+10.1pp**, Qwen-3.6-Plus +6.3, Gemini-Flash-Lite +5.1 — 약한 모델일수록 이득 큼("약한 모델은 프롬프트에서 재유도하는 대신 도구·미들웨어·메모리에 인코딩된 패턴에 의존").

**최약점(정직한 독해)**: 수정 예측 정밀도/재현율 33.7%/51.4%인데 **퇴행 예측은 11.8%/11.1%** — 저자들이 "regression blindness"를 최우선 과제로 지목. 교훈: **퇴행은 예측에 기대지 말고 회귀 벤치 실측으로 잡아라** (S2 회귀 의무 목록의 독립적 재확인).

## 1.5 사용자에의 함의

**(a) 투자 배분.** "프롬프트 무용론"이 아니다 — 반복 2의 규칙은 유효했고, 퇴행은 집행 인프라 없이 홀로 이식했을 때 일이다. 처방: SKILL.md 규칙은 짧게(묶음 A 다이어트와 정합), **모델이 자주 어기는 규칙부터 훅·스크립트·상태 파일로 승격.** 메모리가 최대 기여(+5.6, hard +11.6)라는 것은 work-log·ADR 같은 파일 기반 외부 기억 투자의 가장 강한 정당화다.

**(b) 기존 훅 3종의 자리매김.** 셋 다 논문 분류의 미들웨어이며 "인프라가 산문 규율을 배달"하는 이기는 조합: wf-session-start = 메모리-로더, wf-context-threshold = 컨텍스트 관리 + 패턴 카탈로그 유사물(재경고 간격 포함), wf-post-compact = publish-state 가드 계열("검증된 상태를 지켜라"). ADR-001의 대안 기각("모델은 자기 컨텍스트를 모른다 → 스킬 지시가 아닌 훅으로")은 이 논문의 ablation 결론을 독립 재발견한 것.

**(c) 진화 루프의 축소 이식.** 스킬·훅 개정마다 미니 매니페스트(증거 세션·근본 원인·변경·수정 예측+퇴행 위험)를 남기고, 대표 태스크 5–10개 k=2 소형 회귀 벤치로 다음 개정 때 채점, 기각은 revert. TDAD 개선 루프와의 차이: TDAD는 사전 테스트로 즉시 검증, AHE는 다음 라운드 delta로 사후 검증 + 퇴행 예측을 산출물로 강제 — 그리고 그 퇴행 예측이 최약점이므로 실측 우선.

## 1.6 S7·S9에 대한 판정

- **S7 지지**: 최대 기여 컴포넌트가 경계 사례 교훈의 장기 메모리이고, 패턴 카탈로그는 문자 그대로 "실패 패턴 감지 시 리마인더 주입" — S7은 1·3위 컴포넌트의 결합. **경계**: 카탈로그는 매 호출이 아니라 패턴 감지 시 발화. 모든 PreToolUse에 뿌리면 "중복 재확인 낭비" 재현 → 조건부 발화 + 세션당 1회 억제 필수.
- **S9 강한 지지**: 진화된 하네스가 스스로 만든 것이 Stop 게이트다(finish-hook: 완료 시도를 가로채 "평가기와 동형인 종결 확인 1회" 강제). **경계**: ① 가드는 허점 패치가 반복 필요(반복 8), ② 탈출구 설계 필수(`ALLOW_POST_SUCCESS_RESET` 류), ③ 논문 게이트는 명시적 평가기를 거울삼았다 — 사용자 게이트는 기계 확인 가능한 조건으로 한정해야 한다(이 부분은 외삽).

---

# 2. 구현 참조 — PROJECTMEM precheck와 AI-DLC quality-gate.sh

## 2.1 PROJECTMEM 구현 세부

**이벤트 스키마** (JSONL, 원문 예시):
```json
{"type":"issue",  "id":"0042","at":"run.py:42","text":"pipeline crashes on empty input"}
{"type":"attempt","issue":"0042","outcome":"failed","text":"guarded with if-not-x -- still crashes"}
{"type":"attempt","issue":"0042","outcome":"worked","text":"reordered validation before parse"}
{"type":"fix",    "issue":"0042","text":"validate inputs before parsing"}
```
`precheck_file(path)`는 그 경로의 **실패 시도·미해결 이슈·고빈도 수정**을 조회해 경고("you tried this 2 days ago—it failed"). 기본 advisory(오탐 전제). 현재는 커밋 경계 발화, 향후 도구 호출 경계로 앞당기는 것을 제안. `summary.md`는 fold로 결정적 재생성("can never silently diverge from history"). **attempt 기록은 자동이 아니라 에이전트의 `record_attempt` MCP 호출 — 준수는 "assumed but not enforced".** 비밀 마스킹은 접두사 앵커 패턴(`sk-`, AKIA, AIza, JWT, Bearer, PEM…) → `[REDACTED:<kind>]`. 한계: 콜드 스타트, 오탐, 의미 검색 없음(의도적).

## 2.2 AI-DLC quality-gate.sh (GitHub 실코드 확인)

- `hooks.json`이 `Stop`·`SubagentStop`에 결선(timeout 120).
- `yq --front-matter=extract`로 intent.md와 unit.md의 `quality_gates:`를 읽어 `jq -s '.[0] + .[1]'`로 **가산 병합**("additive merge guarantees no gate is silently dropped").
- `case "$HAT" in builder|implementer|refactorer) ;; *) exit 0` — building hat만 강제. status `completed|blocked`는 통과.
- 게이트마다 `timeout 30 bash -c`, 출력 500자 절단, 실패 시 `jq -n '{"decision":"block","reason":$reason}'` + `exit 0`.
- **재진입 방지**: block 후 재시도에는 `stop_hook_active=true`가 오고 즉시 exit 0 — "enforcement is one-attempt-only per stop"(무한 루프 방지의 대가).
- 래칫: "Gates can never be removed during construction (ratchet effect — the reviewer will catch removal)" — 리뷰어 hat이 git 이력으로 게이트 삭제·약화를 점검하는 인간 측 래칫과 쌍.

## 2.3 사용자 훅 인프라의 관례 (구현 제약)

스크립트 본문 ASCII 전용(PS 5.1 한글 리터럴 문제 — 한국어는 `messages/*.md` + `Get-WfMessage`), 전면 fail-open(`try{…exit 0}catch{exit 0}`), `Get-WfWorkDir` 가드(docs/work 없으면 무동작), 주입은 `Write-WfContext`, 상태는 `%TEMP%\claude-wf\<session>.json`, work-log 상태는 백틱 ASCII 토큰 매칭. 주의: `New-WfCommandHook`의 timeout이 10초 고정 — **Stop 게이트 등록 시 timeout 파라미터화 필요.**

---

# 3. S7 설계 — 시도 등록부 + PreToolUse 훅

## 3.1 work-log 등록부 표 (wf-doc 문체)

```markdown
## 시도 등록부

| 시도 ID | 대상 | 시도 내용 | 결과 | 증거·비고 |
|---|---|---|---|---|
| A-01 | `src/pipeline.py:42` | 빈 입력 가드 추가 | `failed` | [검증 V-03](#검증) — 여전히 크래시 |
| A-02 | `src/pipeline.py:42` | 파싱 전 검증 재배치 | `worked` | [검증 V-04](#검증) |
```

결과 토큰은 PROJECTMEM의 `worked|failed|partial`을 ASCII 그대로 사용(§3.4 어휘 "성공·실패·미수행"과의 대응은 머리말 1줄로) — PS 5.1 훅이 로케일 무관 grep 가능해야 하기 때문(기존 상태 토큰 관례와 동일).

## 3.2 기록 주체 문제 — 옵션 비교와 추천

| 옵션 | 장점 | 단점 |
|---|---|---|
| ① 스킬 규정만("실패한 검증 후 등록부 행 추가") | 구현 0. 의미(시도 의도·결과 해석)는 모델만 기록 가능 | 준수율이 컨텍스트 압력에 취약 — PROJECTMEM과 같은 약점 |
| ② PostToolUse 자동 기록 | 강제됨 | 훅은 "무엇을 시도했는지" 모름 → 잡음 행 양산. work-log를 훅이 쓰면 정본 오염 |
| ③ **병행: 규정 + PostToolUse 리마인더**(테스트류 명령 exit≠0 감지 시 "등록부에 기록하라" 주입) | 의미는 모델이, 트리거는 훅이. 쓰기 주체 단일 유지 | 리마인더 잡음 — 재경고 억제 필요 |

**추천 ③.** §7 불변식("저장소에서 재구성할 수 없는 정보 우선")과 일치하고, threshold 훅의 rewarn 패턴 재사용.

## 3.3 `wf-attempt-check.ps1` 초안 (PreToolUse, matcher `Edit|Write`, advisory)

```powershell
# DES-06 - PreToolUse(Edit|Write) hook. Warns when the target file has
# recorded failed attempts in any open work-log's attempt registry.
# Advisory only (PROJECTMEM precheck analog); fail-open; once per file/session.
try {
    . (Join-Path $PSScriptRoot 'wf-common.ps1')
    $hookInput = Read-WfHookInput
    $workDir = Get-WfWorkDir $hookInput
    if (-not $workDir) { exit 0 }

    $target = $hookInput.tool_input.file_path
    if (-not $target) { exit 0 }
    $rel = "$target"
    if ($hookInput.cwd -and $rel.StartsWith("$($hookInput.cwd)", [StringComparison]::OrdinalIgnoreCase)) {
        $rel = $rel.Substring("$($hookInput.cwd)".Length).TrimStart('\', '/')
    }
    $rel = $rel.Replace('\', '/')
    if (-not $rel) { exit 0 }

    # Dedup: warn at most once per file per session (false-positive fatigue guard).
    $sidecar = (Get-WfStatePath $hookInput) -replace '\.json$', '-attempts.json'
    $warned = @()
    if (Test-Path $sidecar) { $warned = @(Get-Content $sidecar -Raw -Encoding UTF8 | ConvertFrom-Json) }
    if ($warned -contains $rel) { exit 0 }

    $hits = @()
    foreach ($name in (Get-WfOpenWorkLogs $workDir)) {
        $log = Join-Path (Join-Path $workDir $name) 'work-log.md'
        foreach ($line in @(Get-Content $log -Encoding UTF8)) {
            if ($line -match '^\s*\|' -and $line -match '`failed`' -and
                $line -match [regex]::Escape($rel)) {
                $hits += ('- docs/work/' + $name + '/work-log.md : ' + $line.Trim())
            }
        }
    }
    if ($hits.Count -eq 0) { exit 0 }

    [IO.File]::WriteAllText($sidecar,
        (ConvertTo-Json -InputObject @($warned + $rel) -Compress),
        (New-Object Text.UTF8Encoding($false)))
    $body = (Get-WfMessage 'attempt-check.md').TrimEnd() + "`n" +
            (@($hits | Select-Object -First 5) -join "`n")
    Write-WfContext 'PreToolUse' $body
    exit 0
} catch { exit 0 }
```

`messages/attempt-check.md`:
```markdown
[llm_workflow 시도 등록부] 지금 수정하려는 파일에 실패로 기록된 시도가 있다. 아래 등록부 행을 먼저 읽고, 같은 접근을 반복하려는 것이면 실패 원인과 증거를 확인한 뒤 다른 접근을 계획하라. 이 경고는 차단이 아니라 자문이며, 과거 실패가 현재 변경과 무관하면 무시하고 진행해도 된다(이유를 작업 기록에 한 줄 남겨라). 관련 시도:
```

주의: PreToolUse `additionalContext` 주입은 비교적 최근 Claude Code 버전 기능 — 설치 문서에 최소 버전 명시. AHE의 경계대로 **세션당 파일별 1회** 억제를 코드에 내장했다.

---

# 4. S9 설계 — Stop 게이트 훅

## 4.1 게이트 정의 위치 — 옵션 비교

| 옵션 | 평가 |
|---|---|
| plan.md 검증 계획 절 | 이미 존재하나 산문이라 파싱 취약, 래칫 감사 어려움 |
| work-log frontmatter(AI-DLC 방식) | wf-doc 공통 머리말(인용 블록)과 형식 충돌 |
| **전용 파일 + work-log 절 (추천)** | 저장소 전역 `docs/quality-gates.md`(intent 수준) + work-log `## 품질 게이트` 절(unit 수준)을 **가산 병합**. ` ```gates ` 펜스 안 `이름 = 명령` 한 줄 형식(첫 `=` 분할 — Windows 경로 `:` 충돌 회피) |

## 4.2 `wf-stop-gate.ps1` 초안 (Stop 훅, 등록 시 timeout 120초)

```powershell
# DES-07 - Stop hook. Runs quality gates from docs/quality-gates.md and open
# work-logs' gates fences; blocks stop only on verification failure.
# Infra errors (cannot launch, file unreadable) pass — fail-open preserved.
try {
    . (Join-Path $PSScriptRoot 'wf-common.ps1')
    $hookInput = Read-WfHookInput
    $workDir = Get-WfWorkDir $hookInput
    if (-not $workDir) { exit 0 }
    if ($hookInput.stop_hook_active) { exit 0 }          # re-entry guard (AI-DLC)
    if ($env:CLAUDE_WF_GATE_DISABLE -eq '1') { exit 0 }  # human escape hatch
    $open = Get-WfOpenWorkLogs $workDir
    if ($open.Count -eq 0) { exit 0 }  # gates enforced only while work is open

    function Get-WfGateLines([string]$Path) {
        $lines = @(); $inFence = $false
        if (-not (Test-Path $Path)) { return ,$lines }
        foreach ($l in @(Get-Content $Path -Encoding UTF8)) {
            if ($l -match '^```gates\s*$') { $inFence = $true; continue }
            if ($inFence -and $l -match '^```') { $inFence = $false; continue }
            if ($inFence -and $l.Trim() -and $l.Contains('=')) { $lines += $l.Trim() }
        }
        return ,$lines
    }

    $gates = @(Get-WfGateLines (Join-Path $hookInput.cwd 'docs\quality-gates.md'))
    foreach ($name in $open) {   # additive merge: repo gates + per-work gates
        $gates += @(Get-WfGateLines (Join-Path (Join-Path $workDir $name) 'work-log.md'))
    }
    if ($gates.Count -eq 0) { exit 0 }

    $timeoutSec = 60
    if ($env:CLAUDE_WF_GATE_TIMEOUT_SEC -match '^\d+$') { $timeoutSec = [int]$env:CLAUDE_WF_GATE_TIMEOUT_SEC }
    $failures = @()
    foreach ($g in $gates) {
        $i = $g.IndexOf('=')
        $gname = $g.Substring(0, $i).Trim(); $gcmd = $g.Substring($i + 1).Trim()
        if (-not $gcmd) { continue }
        try {
            $out = Join-Path $env:TEMP ("claude-wf\gate-" + [guid]::NewGuid() + ".log")
            $p = Start-Process cmd.exe -ArgumentList '/d', '/c', $gcmd `
                -WorkingDirectory $hookInput.cwd -WindowStyle Hidden `
                -RedirectStandardOutput $out -PassThru
            if (-not $p.WaitForExit($timeoutSec * 1000)) {
                $p.Kill(); continue   # timeout = infra, not verdict -> pass (fail-open)
            }
            if ($p.ExitCode -ne 0) {
                $tail = ''
                if (Test-Path $out) { $tail = ((Get-Content $out -Encoding UTF8 | Select-Object -Last 8) -join ' / ') }
                if ($tail.Length -gt 500) { $tail = $tail.Substring(0, 500) }
                $failures += ('- ' + $gname + ' (exit ' + $p.ExitCode + '): ' + $gcmd + ' :: ' + $tail)
            }
        } catch { continue }          # launch failure = infra error -> pass
        finally { if (Test-Path $out) { Remove-Item $out -Force -ErrorAction SilentlyContinue } }
    }
    if ($failures.Count -eq 0) { exit 0 }

    $reason = (Get-WfMessage 'stop-gate.md').TrimEnd() + "`n" + ($failures -join "`n")
    $payload = @{ decision = 'block'; reason = $reason }
    $w = New-Object IO.StreamWriter([Console]::OpenStandardOutput(), (New-Object Text.UTF8Encoding($false)))
    $w.Write((ConvertTo-Json -InputObject $payload -Compress -Depth 5)); $w.Flush()
    exit 0
} catch { exit 0 }
```

`messages/stop-gate.md`:
```markdown
[llm_workflow 품질 게이트] 미완료 작업이 있는 상태에서 아래 게이트가 실패했다. wf-implement §5 완료 조건("관련 자동화 테스트와 빌드가 성공했다")을 충족하지 못했으므로 종료 전에 실패 원인을 진단해 수정하거나, 수정 불가하면 작업 기록에 실패·미수행 검증과 차단 사유를 기록하고 상태를 갱신하라. 실패 게이트:
```

## 4.3 설계 결정의 근거

- **fail-open과 block의 긴장 해소**: 인프라 오류(기동 실패·파일 판독 불가·훅 예외)는 전부 통과 — 기존 관례 유지. **게이트가 실행됐고 exit≠0인 검증 실패만 block.** 타임아웃은 AI-DLC(실패 처리)와 달리 인프라로 분류해 통과 — 느린 머신의 오차단 방지 우선. 단 타임아웃 발생을 상태 파일에 카운트해 무력화 빈도를 감시(실험 지표 ④).
- **래칫의 사용자 어휘 번역**: "gates can never be removed during construction" = §3.4 "인수 조건을 완화하거나 의미를 바꾸지 않는다"의 기계 판독 형태. 규칙: **게이트는 구현 중 추가만 가능, 삭제·완화는 §4.2 중대한 변경(wf-design 재승인)으로만.** §3.5 자체 리뷰에 "git diff로 게이트 삭제·약화 점검" 항목 추가(AI-DLC 리뷰어 hat의 인간 측 래칫 대응).
- **재진입 방지**: `stop_hook_active` 즉시 통과(one-attempt-only의 한계 공유 — 두 번째 stop의 공백은 §3.5가 보완). 열린 work-log 없으면 통과(작업 상태가 게이트 적용 범위를 정의 — AI-DLC의 hat·status 게이팅 대응). `CLAUDE_WF_GATE_DISABLE=1` 인간 탈출구(AHE의 `ALLOW_POST_SUCCESS_RESET` 교훈).
- **게이트 조건은 기계 확인 가능한 것으로 한정**: 논문 게이트는 명시적 평가기를 거울삼았다. 사용자 저장소에서는 결정적 명령(pytest 특정 모듈, lint, 링크 검사 스크립트)만 게이트로 등록하고, flaky 테스트는 넣지 않는다.

---

# 5. 실험 설계

**S7**: ① 동일 파일·동일 접근 반복 실패율(경고 이후 같은 경로 `failed` 행 증가 빈도 — 훅 on/off 비교) ② 경고 정밀도(모델이 "무관하여 무시" 판정한 비율 = 오탐 대리) ③ 등록부 기록 준수율(실패한 검증 대비 행 수). 혼동: 콜드 스타트(등록부 빈 초기 세션 제외), 준수율과 훅 효과의 얽힘(②③ 분리 측정), 경로 매칭의 조악함.

**S9**: ① 종료 시 게이트 통과율·block 발생률 ② block 후 1회 재시도 안에 실제 수정된 비율 vs 그냥 빠져나간 비율(one-attempt-only의 실효 손실) ③ 오차단률(인프라성 실패가 block으로 샌 사례 수동 분류) ④ 타임아웃-통과 발생 빈도(게이트 무력화 감시) ⑤ 세션 길이·토큰 증가. 혼동: 게이트 flakiness(결정적 명령 한정), threshold 훅과의 상호작용(block이 세션을 늘려 임계 경고 유발 — 동시 on 조건 별도 군).

**개정 프로세스(AHE 축소 이식)**: 두 훅의 도입·수정마다 `docs/work/<ID>/`에 미니 매니페스트(증거 세션, 근본 원인, 변경, 수정 예측+퇴행 위험)를 남기고, 다음 개정 시 예측 대비 실측 채점, 기각이면 revert. 퇴행은 예측이 아니라 대표 태스크 5–10개 실측으로 잡는다.

---

# 6. 검증 노트
- AHE: ablation 표(69.7/75.3/73.0/71.9/67.4/77.0), SWE-bench 전이(461k vs 526k, 75.6 vs 75.2), 교차 모델(+10.1/+6.3), 예측 정밀도(33.7/51.4, 11.8/11.1), "산문 전략은 전이 안 됨", 반복당 ~32시간 — 본문 재확인 전부 CONFIRMED. 반복당 후보 편집 수 고정값·달러 비용: 확인 못함.
- AI-DLC quality-gate.sh: 실파일 존재, frontmatter 읽기·hat 게이팅·가산 병합·stop_hook_active 가드·decision:block JSON·게이트당 30초 — 코드 라인 인용으로 CONFIRMED.
- PROJECTMEM: 이벤트 JSON 예시·precheck 조회 대상 3종·advisory 기본·기록 비강제("assumed but not enforced") — CONFIRMED. CLI 19개 전체 목록·churn 임계값: 확인 못함.
- 훅 관례(ASCII 전용·fail-open·timeout 10초 고정)는 클론본 실코드에서 확인.

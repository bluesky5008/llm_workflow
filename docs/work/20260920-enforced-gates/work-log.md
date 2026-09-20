# WORK-20260920-enforced-gates: 강제 게이트 — 작업 기록

> 문서 유형: `work-log`
> 작업 ID: `20260920-enforced-gates`
> 상태: `completed`
> 기준선: `v2` ([REQ-DESIGN-enforced-gates](./req-design.md), 2026-09-21 승인 · [DCR-006](./DCR-006-게이트-시간-예산.md))
> 작성일: 2026-09-20
> 최종 갱신: 2026-09-20
> 관련 문서: [PLAN-llm-workflow: 구현 계획](../../plan.md), [REQ-DESIGN-enforced-gates](./req-design.md), [ADR-005](./ADR-005-게이트-정의-위치와-실행-정책.md), [TESTMAP-20260920-enforced-gates](./test-map.md), [DCR-006](./DCR-006-게이트-시간-예산.md)

## 요약

- 목적: 기준선 v1(TASK-37~43)의 구현 경과·검증 증거·설계 차이를 기록한다. 이 저장소에서 **TDD가 실제로 적용되고 회귀 의무 목록에 실제 행이 생기는 첫 사이클**이다.
- 현재 결론 또는 상태: **완료** — TASK-37~43 전부 completed(2026-09-21 00:30), AC-01~11 전부 성공. 기준선은 [DCR-006](./DCR-006-게이트-시간-예산.md)로 v2.
- 다음 행동: 없음 — 커밋은 사용자 요청에 따른다. 후속 후보는 [미완료 항목](#미완료-항목) 참조.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-enforced-gates](./req-design.md) | FR-01~13, AC-01~11, DES-01~10 | 승인 기준선 v1 |
| input | decision | [ADR-005](./ADR-005-게이트-정의-위치와-실행-정책.md) | 결정 | 원천 C, 인프라 통과, 트리 키 인용 |
| output | decision | [DCR-006](./DCR-006-게이트-시간-예산.md) | NFR-04, DES-05, RISK-01 | 자기 적용 실측이 낳은 기준선 변경(v1 → v2) |
| input | related | [PLAN-llm-workflow](../../plan.md) | TASK-37~43 | 진행 상태의 원천 |
| input | related | [TESTMAP-20260920-enforced-gates](./test-map.md) | 매핑 | 의무 목록 후보의 원천 |

## 기준선과 현재 계획

기준선은 [REQ-DESIGN-enforced-gates](./req-design.md) v1(2026-09-20 승인)과 [ADR-005](./ADR-005-게이트-정의-위치와-실행-정책.md)(approved). 계획은 [PLAN-llm-workflow](../../plan.md)의 TASK-37~43이며 계획 트리를 사용한다.

## 현재 상태

- 진행 중인 작업: 없음
- 마지막 완료 작업: TASK-43 — 자기 적용·검증·자체 리뷰 (2026-09-21 00:30)
- 차단 요인: 없음 — 두 차단 요인 모두 해소(DCR-006 승인, `pytest`·`python-pptx` 설치)

## 회귀 의무 목록

| 발행 TASK | 테스트·명령 | 보호 스코프 | 마지막 성공 (일시 · SHA) | 상태 | 비고 |
|---|---|---|---|---|---|
| TASK-37 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` | `setup/hooks/` 전체 (훅 5파일·설치·메시지) | 2026-09-21 00:30 · `2ff74ee`+미커밋 | 유지 | T22~T38 포함 38건. 실측 72.3초 (게이트 상한 300초, v2). 아래 주석 참조 |
| TASK-40 | `gitleaks detect --no-git --source . --no-banner --redact --exit-code 2 --config .gitleaks.toml` | 저장소 워킹트리 전체 | 2026-09-21 00:30 · `2ff74ee`+미커밋 | 유지 | 전역 게이트이므로 정본은 [quality-gates.md](../../quality-gates.md). 실측 0.3초 |

- 마지막 전량 재실행: 2026-09-21 00:30 · `2ff74ee`+미커밋 — 성공 2 / 실패 0 / 미수행 0. **Stop 훅이 직접 실행한 결과**이며(63.7초, `infraCount: 0`), 에이전트의 직접 실행과 일치한다

**행이 하나인 이유(§2.4 "가장 작은 검증 하나").** `run-tests.ps1`은 테스트 선택 인자가 없는 단일 스크립트라, 이 저장소에서 실행 가능한 가장 작은 단위가 스위트 전체다. 따라서 이후 TASK들은 같은 명령을 중복 발행하지 않고 이 행의 보호 스코프와 비고를 넓힌다.

**여기서 나온 설계 요구.** 같은 이유로 **Stop 게이트는 가산 합집합 뒤 명령 기준 중복을 제거해야 한다** — 열린 작업이 여럿이면 같은 스위트를 여러 번 돌리게 되고, 이는 RISK-01(세션 지연)을 직결로 악화시킨다. TASK-38에서 반영한다.

**사전 실행 기준선(§3.1).** `2ff74ee` · 21 성공 / 0 실패 / exit 0 (2026-09-20 23:1x). 기존 실패 없음.

## 계획 트리

<!-- snapshot: 2026-09-21 완료 시점 -->

```text
└─ [✓] 20260920-enforced-gates ........... completed (7/7, TASK-37~43) .. 2026-09-21 00:30
    ├─ [✓] TASK-37 구현: wf-common.ps1 게이트 헬퍼 ................. 2026-09-20 23:39
    │   └─ [✓] 테스트: T22~T26 파서·트리 키 (선행) ............... 2026-09-20 23:39
    ├─ [✓] TASK-38 구현: wf-stop-gate.ps1 + stop-gate.md      depends: TASK-37 .. 2026-09-20 23:52
    │   └─ [✓] 테스트: T27~T35 차단·통과·합집합·인프라·인용·가드 (선행) . 2026-09-20 23:52
    ├─ [✓] TASK-39 구현: install-hooks.ps1 Stop 등록·timeout  depends: TASK-38 .. 2026-09-20 23:57
    │   └─ [✓] 테스트: T36~T37 등록 계약·멱등성 (선행) ................. 2026-09-20 23:57
    ├─ [✓] TASK-40 구현: quality-gates.md + .gitleaks.toml ............ 2026-09-20 23:59
    ├─ [✓] TASK-41 구현: 훅 메시지 명령-데이터 분리          depends: TASK-38 .. 2026-09-21 00:03
    ├─ [✓] TASK-42 구현: wf-implement·verification-depth 규칙 문장 ..... 2026-09-21 00:03
    └─ [✓] TASK-43 검증: 자기 적용 + AC-01~11 + 자체 리뷰    depends: TASK-37~42 .. 2026-09-21 00:30
        └─ [✓] ★ 승인: DCR-006 게이트 시간 예산 (v1 → v2) ............. 2026-09-21 00:28
```

## 수행 기록

### 2026-09-20 — 승인 관문과 계획 수립

- 수행 내용: wf-design 승인 관문 재개 — Q-02~Q-05를 권고안과 함께 제시해 전부 권고대로 확정, 기준선 v1 발행(상태 `approved`, 승인 기록·변경 이력, ADR-005 `approved`, `docs/decisions.md` 갱신). 이어 wf-implement §3.1 현재 상태 재확인과 §3.2 계획 수립 — 테스트 맵 생성, TASK-37~43 정의, 계획 트리 렌더링
- 변경 파일: `docs/work/20260920-enforced-gates/req-design.md`, `ADR-005-게이트-정의-위치와-실행-정책.md`, `test-map.md`(신설), `work-log.md`(신설), `docs/decisions.md`, `docs/plan.md`
- 발견 사항:
  - **Q-01 전제가 뒤집혔다.** 이 세션은 Windows PowerShell 5.1.26100을 직접 실행할 수 있다 — `run-tests.ps1` 21/21 pass·exit 0 실측. 이전 세션이 정한 A′ 더블클릭 래퍼(DES-11)의 명분이 사라져 사용자 승인으로 DES-11을 전체 삭제하고 RISK-04를 잔여 위험으로 강등했다
  - **DES-07의 게이트 명령에 결함이 있었다.** 설치된 gitleaks 8.18.0에는 `dir` 하위명령이 없고 `detect`만 있다. 미지원 명령은 exit≠0을 내므로 FR-03상 *실패*로 분류되어 상시 block을 유발했을 것이다. 신구 버전 공통인 `detect --no-git --source .`으로 교정
  - **의무 목록 파서는 표 부재를 견뎌야 한다.** 사이클 1의 work-log는 `## 회귀 의무 목록` 절에 표 없이 "유지할 테스트 없음" 산문만 둔다(wf-doc 템플릿이 허용하는 형태). DES-01의 표 파서는 이 경우 빈 결과를 내야 하며, TASK-37의 선행 테스트에 이 케이스를 포함했다
  - **열린 작업이 지금도 하나 있다.** `20260814-multiuser-workflow`가 `in-progress`이며 의무 목록 절이 없다 — Stop 게이트가 켜지면 이 작업도 탐색 대상이 되므로 "절 없음"도 빈 결과 경로로 처리해야 한다
  - **T18~T21의 기대값이 바뀐다.** T18이 "2 SessionStart + 1 PostToolUse"를 단언하므로 Stop 등록 추가 시 실패한다. 이는 회귀가 아니라 계약 변경이며 TASK-39에서 기대값을 갱신한다
- 결정과 이유: Q-02 제외(사이클을 Stop 게이트 하나로 유지), Q-03 의무 목록 재사용(중복 정의 제거), Q-04 통과+카운트(오차단이 게이트 신뢰를 먼저 깎음), Q-05 지금 설치(AC-09를 이번 사이클에서 실측). 근거는 [req-design 가정과 미해결 질문](./req-design.md#가정과-미해결-질문)
- 실행한 검증: `run-tests.ps1` 직접 실행(사전 실행 기준선), `gitleaks version`, `gitleaks --help`(하위명령 확인)
- 결과: 기준선 v1 발행 완료, 계획 수립 완료. 상세 검증 표는 TASK-43에서 작성

### 2026-09-20 — 환경 준비: gitleaks 설치

- 수행 내용: Q-05 확정에 따라 scoop으로 gitleaks 설치
- 변경 파일: 저장소 밖 — `~/scoop/apps/gitleaks/8.18.0/`, `~/scoop/shims/gitleaks.cmd`(수동 생성)
- 발견 사항: scoop 자체가 손상된 상태(`apps/scoop/current/supporting/shims/kiennq/shim.exe` 부재, 버킷 업데이트도 실패)라 `gitleaks.exe` shim 생성이 실패했다. scoop 복구는 이 작업 범위 밖이므로 이미 PATH에 있는 `~/scoop/shims`에 전달용 `gitleaks.cmd`를 두어 해결. 버킷이 오래되어 8.18.0이 설치됐고, 이 때문에 위의 DES-07 결함이 드러났다
- 결정과 이유: 최소 개입 — 사용자 환경의 패키지 관리자를 고치는 대신 게이트가 필요로 하는 것(`gitleaks`가 `cmd.exe`에서 해석될 것)만 충족했다. DES-02가 `cmd.exe /d /c`로 게이트를 기동하므로 `.cmd` 래퍼로 충분하다
- 실행한 검증: `cmd /d /c "gitleaks version"` → `8.18.0`
- 결과: 성공. AC-09를 이번 사이클에서 실측 가능

### 2026-09-20 — TASK-37: wf-common.ps1 게이트 헬퍼

- 수행 내용: TDD 사이클. 선행 테스트 T22~T26을 `run-tests.ps1`에 먼저 작성해 Red를 확인한 뒤, `wf-common.ps1`에 `Get-WfGateLines`·`Get-WfObligationGates`·`Get-WfTreeKey`·`Write-WfBlock` 네 함수를 구현해 Green
- 변경 파일: `setup/hooks/wf-common.ps1`, `setup/hooks/tests/run-tests.ps1`
- 발견 사항:
  - **Red가 깨끗한 `[FAIL]`이 아니라 종료 예외로 나타난다.** 하네스가 `$ErrorActionPreference='Stop'`이라 미정의 함수 호출이 스위트를 중단시키고 요약 줄이 찍히지 않는다. 종료 코드는 1이므로 게이트 관점에서는 정상(실패=차단)이지만, 사람이 읽는 Red 증거로는 거칠다
  - **배열 반환 관용구 충돌.** 저장소의 기존 헬퍼는 `return ,$array` 관용구를 쓰고 호출측은 `$x = Get-Wf...`로 받는다. 첫 테스트는 `@(Get-Wf...)`로 감싸 배열이 중첩되어 T22~T24가 실패했다 — 구현 결함이 아니라 테스트가 저장소 관례를 어긴 것이므로 테스트를 관례에 맞췄다
  - **의무 행은 하나로 충분하고, 그 결과 게이트에 중복 제거가 필요하다.** 위 의무 목록 주석 참조
- 결정과 이유: 파서가 표 부재·절 부재·파일 부재를 전부 "빈 결과"로 처리하도록 했다 — 이 저장소에 세 경우가 모두 실재하며(사이클 1은 산문 절, `20260814-multiuser-workflow`는 절 자체가 없음), 어느 하나라도 예외로 다루면 훅이 fail-open을 거쳐 게이트 전체가 조용히 무력화된다. `Get-WfTreeKey`는 git 실패 시 `$null`을 반환하고 호출측은 이를 "변경 없음"이 아니라 "인용 불가 — 실행하라"로 읽는다(DES-03)
- 실행한 검증: `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` — Red 1회, Green 2회, `completed` 전이 1회
- 결과: Green 26/26 exit 0. 진입 조건(같은 SHA `2ff74ee`에서 2회 통과) 충족 — 의무 목록에 `유지` 행 발행

### 2026-09-20 — TASK-38: wf-stop-gate.ps1 + stop-gate.md

- 수행 내용: 선행 테스트 T27~T34(AC-01~06 + 중복 제거)를 작성해 Red(스크립트 부재)를 확인한 뒤 Stop 훅과 차단 메시지를 구현. 분류 결함이 드러나 T35를 추가하고 판별 방식을 고쳤다
- 변경 파일: `setup/hooks/wf-stop-gate.ps1`(신설), `setup/hooks/messages/stop-gate.md`(신설), `setup/hooks/wf-common.ps1`(`Write-WfGateState`·`Test-WfGateCommand` 추가), `setup/hooks/tests/run-tests.ps1`(T27~T35)
- 발견 사항:
  - **`cmd`는 "명령 없음"을 9009가 아니라 exit 1로 보고한다.** 이 Windows에서 `cmd /d /c <없는명령>`의 프로세스 종료 코드는 1이며, 리다이렉션 유무와 무관했다. FR-03·DES-02가 전제한 9009 신호가 존재하지 않으므로, 종료 코드만으로는 "gitleaks 미설치"와 "gitleaks가 시크릿을 찾음"이 같은 값으로 붕괴한다 — ADR-005가 피하려던 바로 그 도입 장벽의 반대편 실패다
  - 그래서 **실행 전에 명령을 해석**해 판별하도록 바꿨다(`Test-WfGateCommand`): 첫 토큰이 cmd 내장 명령이거나 `Get-Command`로 해석되면 실행하고, 해석되지 않으면 실행하지 않고 인프라 사건으로 센다. 9009 분기는 그 코드를 내는 Windows 빌드를 위해 남겼다
  - 판별 근거가 종료 코드에서 명령 해석으로 옮겨졌으므로, **해석되는 명령의 exit 1은 여전히 실패**임을 고정하는 T35를 추가했다. 이 테스트가 없으면 위 변경이 조용히 모든 실패를 인프라로 흘려보내는 회귀로 바뀔 수 있다
  - **인용 키는 인프라 사건이 있으면 기록하지 않는다.** 실행되지 못한 게이트가 하나라도 있으면 "전 게이트 통과"라고 말할 수 없고, 그 트리를 통과로 기록하면 다음 턴에 인용으로 건너뛰어 스캔이 영구히 생략된다
- 결정과 이유: 게이트 실행은 `cmd`가 파일로 리다이렉트하게 했다 — PowerShell이 파이프를 읽으면서 동시에 종료를 기다리면 교착이 생긴다. 실패 시 인용 키를 비우는 것은 실패한 실행이 다음 트리에 대해 아무것도 보증하지 않기 때문이다. `Write-WfGateState`는 기존 `Write-WfState`와 상태 모양이 달라 별도 함수로 뒀다(DES-04의 헬퍼 집합에 대한 가산 변경)
- 실행한 검증: `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` — Red 1회, 분류 결함 발견 1회(T30 실패), 수정 후 Green 1회, `completed` 전이 1회. 별도로 `cmd /d /c <없는명령>`의 종료 코드를 4가지 형태로 실측
- 결과: Green 35/35 exit 0. 같은 SHA 2회 통과로 의무 목록 행의 스코프를 갱신

### 2026-09-20 — TASK-39: install-hooks.ps1 Stop 등록과 timeout 파라미터화

- 수행 내용: 선행 테스트 T36~T37을 작성해 Red를 확인한 뒤 `New-WfCommandHook`·`New-WfEntry`에 `TimeoutSec` 매개변수(기본 10)를 더하고 `Stop` 이벤트에 `wf-stop-gate.ps1`을 timeout 120으로 등록. `setup_claude.ps1`의 설치 주석·안내 문구에 Stop 게이트와 구버전 동작(무동작 = fail-open)을 명시
- 변경 파일: `setup/hooks/install-hooks.ps1`, `setup/setup_claude.ps1`, `setup/hooks/tests/run-tests.ps1`(T36~T37)
- 발견 사항: **T18이 깨질 것이라는 계획 수립 시의 예측이 틀렸다.** T18은 `SessionStart`와 `PostToolUse`의 개수만 단언하고 `Stop`은 별도 키이므로 영향을 받지 않았다. 계약 변경이 아니라 순수 가산이었고, 기대값 갱신은 불필요했다. 대신 T37을 추가해 **파라미터화가 기존 훅의 10초 예산을 조용히 올리지 않았는지**를 고정했다 — 그쪽이 실제 위험이었다
- 결정과 이유: `setup_claude.ps1`은 이미 `install-hooks.ps1`을 dot-source 해 `Install-WfHooks`를 호출하므로 설치 경로는 코드 변경 없이 Stop을 포함한다. 최소 Claude Code 버전은 숫자로 못 박지 않고 필요한 계약(`stop_hook_active` 전달, Stop의 `decision: block` 존중)으로 적었다 — 이 환경에서 `claude --version`을 확인할 수 없어 특정 번호를 적으면 근거 없는 수치가 된다(RISK-07은 fail-open으로 이미 무해)
- 실행한 검증: `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` — Red 1회, Green 1회, `completed` 전이 1회
- 결과: Green 37/37 exit 0

### 2026-09-20 — TASK-40: quality-gates.md + .gitleaks.toml

- 수행 내용: 저장소 전역 게이트 정본 신설(불변 설정 원칙 + `gates` 펜스 + 실행 규칙 + 게이트 추가 기준)과 시크릿 스캔 설정 신설. AC-09를 3건 실측
- 변경 파일: `docs/quality-gates.md`(신설), `.gitleaks.toml`(신설)
- 발견 사항: 기준선의 allowlist 예시(`tests/fixtures/**`)는 이 저장소에 없는 경로였다 — 실제 픽스처는 `setup/hooks/tests/`가 임시 디렉터리에 만들고, 논문 조사 문서는 샘플 토큰을 인용한다. 두 경로만 좁게 허용하고, 값 자리를 `<...>`·`{{...}}`로 쓰는 문서 관례를 정규식으로 더했다
- 결정과 이유: allowlist를 넓히는 것은 게이트를 약화하는 것과 같은 동작이므로, 그 취지를 `.gitleaks.toml` 머리 주석에 적어 다음 편집자가 "경고를 없애려고" 항목을 늘리지 않게 했다. `--redact`로 탐지된 값이 차단 사유에 실리지 않게 한다
- 실행한 검증: `gitleaks detect --no-git --source . --no-banner --redact --exit-code 2 --config .gitleaks.toml` 3회 — (1) 정상 워킹트리, (2) 심어둔 AWS 키 형태 픽스처, (3) allowlist에 걸리는 플레이스홀더. 픽스처는 즉시 삭제
- 결과: (1) exit 0 "no leaks found", (2) exit 2 "leaks found: 1"(값은 redact됨), (3) exit 0. AC-09 충족

### 2026-09-21 — TASK-41: 훅 메시지 명령-데이터 분리

- 수행 내용: `resume.md`·`post-compact.md`에 구분자 문장 추가(`stop-gate.md`는 TASK-38에서 신설 시 포함)
- 변경 파일: `setup/hooks/messages/resume.md`, `setup/hooks/messages/post-compact.md`
- 발견 사항: 두 메시지는 끝이 "미완료 작업 기록:"이고 훅이 그 뒤에 파일 목록을 이어 붙인다. 문장을 끝에 더하면 콜론과 목록 사이에 끼어 구분자 역할이 무너지므로 콜론 **앞**에 넣었다. 처음에 상대 경로 마크다운 링크를 썼다가 평문으로 고쳤다 — 주입 메시지는 대화에 문자열로 들어가므로 파일 위치 기준 상대 링크가 가리킬 대상이 없다(기존 `resume.md`의 "wf-implement §3.1 재개 절차" 표기 관례와 일치)
- 결정과 이유: `threshold.md`는 대상에서 제외했다 — 작업 기록 본문을 주입하지 않고 에이전트에게 절차만 지시하므로 분리할 데이터가 없다(DES-06의 세 메시지와 일치)
- 실행한 검증: T01·T14(주입 경로)와 전량. AC-08 grep 대조
- 결과: 37/37 exit 0. 세 메시지 모두 문장 확인

### 2026-09-21 — TASK-42: wf-implement·verification-depth 규칙 문장

- 수행 내용: §2.3에 자기 강제 설정 승인 항목·이유 문단·주입 문맥 데이터 문단, §3.3에 선택적 재시도, §3.4-1에 시크릿 스캔 상시, §3.5 보안 블록에 핀 확인·품질 블록에 게이트 약화 점검과 관례 호환, §3.6에 Stop 게이트와 의무 목록의 관계, §7 세션 인계에 마지막 게이트 통과 키. `verification-depth.md` §1에 `Stop 훅` 행과 그 성격 설명, §2 §3.4-1 행 세 열에 시크릿 스캔 포함
- 변경 파일: `skills/wf-implement/SKILL.md`, `skills/wf-implement/references/verification-depth.md`
- 발견 사항: `verification-depth.md` §1의 여섯 시점은 모두 "에이전트가 수행하는 의무"인데 Stop 훅 행만 "기계가 확인하는 층"이라 성격이 다르다. 같은 표에 섞으면 게이트를 검증 단계 중 하나로 오독하기 쉬워, 표 아래에 둘이 대체 관계가 아님을 명시했다 — §3.6에 넣은 문장과 같은 취지다
- 결정과 이유: NFR-05 경계 유지 — 게이트 원천의 *형식*(의무 목록 표·`gates` 펜스)은 wf-doc 소유이므로 형식 규정을 wf-implement에 쓰지 않고 실행·차단·인용의 *의미*만 적었다. 형식은 `docs/quality-gates.md`가 설명한다
- 실행한 검증: AC-08 grep 대조 16항목, 전량 실행
- 결과: 16/16 확인, 37/37 exit 0. 산문 변경이라 TDD 부적용(테스트 체계 없음) — 후행 검증으로 대체

### 2026-09-21 — TASK-43: 자기 적용·검증·자체 리뷰 (진행 중)

- 수행 내용: Stop 훅을 이 저장소에 직접 실행해 세 경로(실행·인용·차단)를 확인하고, AC-01~11을 판정했으며, §3.5 자체 리뷰를 수행했다. 리뷰에서 나온 수정 두 건을 반영하고 T38을 추가했다
- 변경 파일: `setup/hooks/wf-stop-gate.ps1`, `setup/hooks/tests/run-tests.ps1`, `docs/work/20260920-enforced-gates/DCR-006-게이트-시간-예산.md`(신설), `docs/decisions.md`
- 발견 사항:
  - **차단 사유에 ANSI 이스케이프가 섞였다.** 게이트 출력의 색상 코드가 그대로 실려 사유 본문을 덮었다. 꼬리에서 제거하도록 고치고 T38로 고정. 명령 문자열 자체의 이스케이프는 기록된 그대로 두는 것이 맞으므로, 픽스처는 색상을 **출력**에만 두도록 다시 짰다
  - **게이트 명령에 `&`가 있으면 우리가 덧붙인 리다이렉션이 명령 전체가 아니라 마지막 조각에만 붙었다.** T38이 이 결함을 드러냈다. 명령을 임시 배치 파일에 넣고 그 파일을 실행하도록 바꿔, 게이트가 `&`·`|`·자체 리다이렉션을 써도 출력이 온전히 잡히게 했다
  - 그 과정에서 **`cmd /c "..."`의 인용 규칙**에 걸렸다 — 인자 문자열이 따옴표로 시작하면 cmd가 첫·끝 따옴표를 제거해 리다이렉션이 깨진다. `call`을 앞에 두어 인자가 따옴표로 시작하지 않게 했다(T28·T29·T31·T32가 한꺼번에 실패해 즉시 드러났다)
  - **게이트가 의무 테스트를 완주시키지 못한다.** 자기 적용 실행의 상태 파일이 `infraCount: 1`·`lastPassKey: null`을 남겼고, 측정 결과 `run-tests.ps1`이 72.3초로 게이트당 상한 60초를 넘었다. RISK-02가 가정이 아니라 기본값에서 즉시 발생한다. NFR-04의 값을 바꾸는 사안이므로 §4.2에 따라 구현을 보류하고 [DCR-006](./DCR-006-게이트-시간-예산.md)을 발행했다
  - **§3.6 전체 스위트를 실행할 수 없다.** `docs/presentation/tests/test_make_pptx.py`(8건)에 필요한 `pytest`·`python-pptx`가 설치되어 있지 않고 요구사항 파일도 없다. 이 작업의 변경 파일과 무관한 스위트지만 통합 의무에는 포함되므로 `미수행 — 도구 없음`으로 기록한다
- 결정과 이유: 시간 예산은 스스로 올리지 않았다. 60초는 기준선이 명시한 값이고 올리면 RISK-01(세션 지연)과 맞바꾸는 것이라, "게이트를 통과시키려 게이트를 고치지 않는다"는 이 사이클이 세운 원칙이 그대로 적용된다 — 값을 바꾸는 주체는 사용자다
- 실행한 검증: 아래 검증 표
- 결과: AC-01~10 성공, AC-11 부분 → DCR-006 승인 후 재판정하여 **AC-01~11 전부 성공**

### 2026-09-21 — TASK-43(이어서): DCR-006 반영과 완결

- 수행 내용: DCR-006 대안 A 승인에 따라 게이트당 300초·훅 전체 600초로 상향하고 기준선 v2를 발행. `pytest`·`python-pptx`를 설치해 §3.6 전체 스위트를 실행. 자기 적용을 재실행해 AC-11을 재판정
- 변경 파일: `setup/hooks/wf-stop-gate.ps1`, `setup/hooks/install-hooks.ps1`, `setup/hooks/tests/run-tests.ps1`(T36 기대값), `docs/quality-gates.md`, `req-design.md`(v2), `DCR-006-게이트-시간-예산.md`, `docs/decisions.md`
- 발견 사항: 상향 후 Stop 훅의 자기 적용이 **63.7초에 완주**하고 `infraCount: 0`·`lastPassKey` 기록. 직접 측정한 72.3초보다 짧은 것은 훅이 게이트를 중복 제거해 `gitleaks`를 한 번만 돌리고, 측정 시의 관측 부하가 없기 때문이다. 어느 쪽이든 60초는 넘고 300초에는 크게 못 미친다
- 결정과 이유: 값만 바꾸고 구현은 그대로 뒀다(DCR-006 영향 범위대로). 상수 2개와 T36의 단언 1개가 전부이며, TASK-37~42의 구현·검증은 되돌리거나 다시 하지 않았다 — 이번 사이클이 §3.3에 새로 넣은 **선택적 재시도** 원칙의 첫 적용 사례다
- 실행한 검증: `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` 전량, `python -m pytest tests/test_make_pptx.py -q` (`docs/presentation`), Stop 훅 자기 적용 재실행
- 결과: 38/38 + 8/8 성공, 자기 적용 `infraCount: 0`. AC-11 성공, 사이클 완결

## 검증

| 항목 | 테스트 집합 | 커밋 SHA | 실행 명령 | 결과 | 분류 |
|---|---|---|---|---|---|
| 사전 실행 기준선(§3.1) | `run-tests.ps1` T01~T21 | `2ff74ee` | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` | 21 성공 / 0 실패 / exit 0 | 성공 |
| TASK-37 Red | `run-tests.ps1` T22~T26 | `2ff74ee`+미커밋 | 위와 동일 | `Get-WfGateLines` 미정의로 종료 예외, exit 1 (T01~T21은 pass) | 의도한 실패 |
| TASK-37 Green(1차) | `run-tests.ps1` 전량 | `2ff74ee`+미커밋 | 위와 동일 | 23 성공 / 3 실패 (T22~T24) | 실패 — 테스트 측 관용구 오류 |
| TASK-37 Green(2차) | `run-tests.ps1` 전량 | `2ff74ee`+미커밋 | 위와 동일 | 26 성공 / 0 실패 / exit 0 | 성공 |
| TASK-37 `completed` 전이 | 회귀 의무 목록 전량 | `2ff74ee`+미커밋 | 위와 동일 | 26 성공 / 0 실패 / exit 0 | 성공 |
| 환경: gitleaks 가용성 | — | `2ff74ee` | `cmd /d /c "gitleaks version"` | `8.18.0` | 성공 |
| TASK-38 Red | `run-tests.ps1` T27~T34 | `2ff74ee`+미커밋 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` | `wf-stop-gate.ps1` 부재로 exit 1 (T01~T26은 pass) | 의도한 실패 |
| TASK-38 Green(1차) | `run-tests.ps1` 전량 | `2ff74ee`+미커밋 | 위와 동일 | 33 성공 / 1 실패 (T30) | 실패 — 9009 전제 오류 |
| 분류 실측 | — | `2ff74ee`+미커밋 | `cmd /d /c wf-no-such-command-xyz` (리다이렉션 유·무) | 종료 코드 1 (9009 아님) | 성공(측정) |
| TASK-38 Green(2차) | `run-tests.ps1` 전량 | `2ff74ee`+미커밋 | 위와 동일 | 35 성공 / 0 실패 / exit 0 | 성공 |
| TASK-38 `completed` 전이 | 회귀 의무 목록 전량 | `2ff74ee`+미커밋 | 위와 동일 | 35 성공 / 0 실패 / exit 0 | 성공 |
| TASK-39 Red | `run-tests.ps1` T36~T37 | `2ff74ee`+미커밋 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` | 36 성공 / 1 실패 (T36) | 의도한 실패 |
| TASK-39 Green·`completed` 전이 | `run-tests.ps1` 전량 | `2ff74ee`+미커밋 | 위와 동일 | 37 성공 / 0 실패 / exit 0 (2회) | 성공 |
| AC-09 (1) 정상 트리 | 전역 시크릿 게이트 | `2ff74ee`+미커밋 | `gitleaks detect --no-git --source . --no-banner --redact --exit-code 2 --config .gitleaks.toml` | exit 0, `no leaks found` | 성공 |
| AC-09 (2) 심어둔 시크릿 | 전역 시크릿 게이트 | `2ff74ee`+미커밋+픽스처 | 위와 동일 | exit 2, `leaks found: 1` (값 redact) | 성공 |
| AC-09 (3) allowlist 대상 | 전역 시크릿 게이트 | `2ff74ee`+미커밋+픽스처 | 위와 동일 | exit 0 | 성공 |
| TASK-40 `completed` 전이 | 회귀 의무 목록 전량 | `2ff74ee`+미커밋 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` | 37 성공 / 0 실패 / exit 0 | 성공 |
| AC-08 규칙 문장 대조 | grep 16항목 | `2ff74ee`+미커밋 | `grep -q <문장> <파일>` × 16 | 16/16 확인 | 성공 |
| TASK-41·42 `completed` 전이 | 회귀 의무 목록 전량 | `2ff74ee`+미커밋 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` 및 `gitleaks detect --no-git --source . --no-banner --redact --exit-code 2 --config .gitleaks.toml` | 37 성공 / 0 실패 / exit 0; 스캔 exit 0 | 성공 |
| TASK-43 자기 적용 run 1 (실행) | 이 저장소의 게이트 전량 | `2ff74ee`+미커밋 | Stop 훅 직접 호출(`wf-stop-gate.ps1`) | 무출력, exit 0, `infraCount:0`, `lastPassKey` 기록 | 성공 |
| TASK-43 자기 적용 run 2 (인용) | 동일 | 동일 트리 | 동일 | 무출력, 1.97초 — 게이트 미실행 | 성공 |
| TASK-43 자기 적용 run 3 (차단) | 동일 + 심어둔 시크릿 | `2ff74ee`+미커밋+픽스처 | 동일 | `{"decision":"block"}`, `secrets (exit 2)` 명시 | 성공 |
| TASK-43 ANSI 결함 수정 후 | `run-tests.ps1` 전량 | `2ff74ee`+미커밋 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` | 38 성공 / 0 실패 / exit 0 | 성공 |
| TASK-43 통합 실행 | `run-tests.ps1` 전량 + 시크릿 게이트 | `2ff74ee`+미커밋 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` 및 `gitleaks detect --no-git --source . --no-banner --redact --exit-code 2 --config .gitleaks.toml` | 38 성공 / 0 실패; 스캔 exit 0 | 성공 |
| TASK-43 자기 적용 최종 | 이 저장소의 게이트 전량 | `2ff74ee`+미커밋 | Stop 훅 직접 호출 | 무출력이나 `infraCount:1`, `lastPassKey:null` | **실패 — 이번 변경으로 발생** (의무 게이트 미완주) |
| 게이트 소요 실측 | — | `2ff74ee`+미커밋 | 각 게이트 명령의 벽시계 측정 | `run-tests.ps1` 72.3초 / `gitleaks` 0.3초 (상한 60초) | 성공(측정) |
| §3.6 전체 스위트 (1) | `run-tests.ps1` 38건 | `2ff74ee`+미커밋 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` | 38 성공 / 0 실패 / exit 0 | 성공 |
| §3.6 전체 스위트 (2) | `test_make_pptx.py` 8건 | `2ff74ee`+미커밋 | `python -m pytest tests/test_make_pptx.py -q` (`docs/presentation`) | 8 passed | 성공 |
| DCR-006 반영 후 전량 | `run-tests.ps1` 38건 | `2ff74ee`+미커밋 | `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` | 38 성공 / 0 실패 / exit 0 (T36 기대값 600) | 성공 |
| AC-11 재판정 자기 적용 | 이 저장소의 게이트 전량 | `2ff74ee`+미커밋 | Stop 훅 직접 호출 | 무출력, 63.7초 완주, `infraCount:0`, `lastPassKey` 기록 | 성공 |

### 인수 조건 판정

| AC | 판정 | 증거 |
|---|---|---|
| AC-01 차단 | 성공 | T27 + 자기 적용 run 3 (`decision:block`, 게이트 이름 포함) |
| AC-02 통과 | 성공 | T28 + 자기 적용 run 1 (무출력, exit 0) |
| AC-03 원천 합집합 | 성공 | T29 — 펜스 1 + `유지` 1 실행, `보류` 1 미실행 |
| AC-04 인프라 통과 | 성공 | T30(명령 부재) · T31(타임아웃) — 둘 다 통과 + 카운터 증가 |
| AC-05 인용 | 성공 | T32 + 자기 적용 run 2 (동일 트리, 게이트 미실행) |
| AC-06 가드 | 성공 | T33 — `stop_hook_active` · `DISABLE` · 열린 작업 없음 · `docs/work` 없음(상태 파일 미생성) |
| AC-07 등록 | 성공 | T36 (Stop 1개·timeout 120·멱등) · T37 (기존 훅 10초 유지) |
| AC-08 규칙 문장 | 성공 | grep 16/16 — FR-07~11 + DES-08·09 + §7 |
| AC-09 시크릿 게이트 | 성공 | 정상 트리 exit 0 / 심어둔 시크릿 exit 2(redact) / allowlist exit 0 |
| AC-10 회귀 없음 | 성공 | T01~T21 통과 유지(38/38). 범위 밖 변경 없음, 완료 사이클 기록 무변경. 삭제된 줄은 전부 제자리 재작성 |
| AC-11 자기 적용 | 성공 | test-map·의무 목록 `유지` 2행·검증 표(전 행 SHA·명령·분류) 존재. Stop 게이트 실행 증거 5회 — 실행·인용·차단·상한 초과(DCR-006 증거)·상향 후 완주(`infraCount: 0`) |

### 자체 리뷰 (§3.5)

- 요구사항·설계: FR-01~13 구현됨. 설계 차이 6건은 아래 절에 기록. 범위 밖 변경 없음
- 정확성·안정성: 리뷰 중 2건 수정(ANSI 누출, `&` 리다이렉션 결합) 후 관련 테스트 재실행. 남은 약점 — 타임아웃 시 `$proc.Kill()`은 `cmd`만 종료하고 손자 프로세스(예: `ping`)는 남는다. 수명이 짧아 방치했으나 긴 게이트에서는 고아가 될 수 있다
- 보안·운영: 시크릿은 `--redact`로 차단 사유에 실리지 않음을 실측. 훅은 `%TEMP%` 상태 파일 외에 아무것도 쓰지 않는다(NFR-03). CI·Dockerfile·IaC 변경 없음 — 핀 확인 해당 없음
- 품질: 게이트·의무 목록·훅·테스트의 삭제나 약화 없음(`git diff` 확인, 위 검증 표). `infraCount`가 1로 늘어 원인을 추적했고 그것이 DCR-006이 됐다 — 신설한 리뷰 항목이 첫 실행에서 실제로 작동했다. 저장소 관례 충돌 없음(ASCII 전용 소스·fail-open·`,$array` 반환·`%TEMP%` 상태 파일 모두 준수). 인용한 검증의 SHA는 전부 `2ff74ee`+미커밋으로 현재 트리와 일치


AC-01~11의 최종 판정은 TASK-43에서 수행한다.

## 설계와 달라진 점

| 항목 | 설계 | 실제 | 분류 | 처리 |
|---|---|---|---|---|
| DES-11 실행 래퍼 | `run-tests.cmd` + `last-run.log` 더블클릭 경로 | 삭제 — Claude가 PowerShell 직접 실행 | 기준선 변경 | 승인 관문에서 사용자 승인, v1에 반영 완료 |
| DES-07 게이트 명령 | `gitleaks dir .` | `gitleaks detect --no-git --source .` | 기준선 변경 | 승인 관문에서 사용자 승인, v1에 반영 완료 |
| FR-03·DES-02 명령 부재 신호 | `cmd` 종료 코드 9009 | 실행 전 명령 해석(`Test-WfGateCommand`); 9009 분기는 병존 | 경미(§4.1) — 요구의 분류 규칙("명령 없음 = 인프라")은 그대로이고 탐지 수단만 바뀜 | 기록 후 계속. 기준선 본문의 괄호 예시(`cmd 9009`)는 부정확해졌으므로 TASK-43 자체 리뷰에서 표기 수정 여부를 제기 |
| DES-04 헬퍼 집합 | 4종 | 6종 — `Write-WfGateState`, `Test-WfGateCommand` 추가 | 경미(§4.1) — 가산이며 훅 본문은 여전히 조합만 | 기록 후 계속 |
| DES-02 인용 기록 조건 | 전 게이트 통과 시 기록 | 전 게이트 통과 **그리고 인프라 사건 없음**일 때만 기록 | 경미(§4.1) — 요구를 좁히는 방향(더 자주 실행) | 기록 후 계속 |
| DES-07 allowlist 경로 | `tests/fixtures/**` | `setup/hooks/tests/**`, `docs/work/20260919-aidlc-research/**` | 경미(§4.1) — 기준선의 예시 경로가 이 저장소에 없음 | 기록 후 계속 |
| FR-12 T18 기대값 | Stop 추가로 갱신 필요 예상 | 갱신 불필요 — Stop은 별도 키 | 예측 정정 | T37 신설로 실제 위험(기존 timeout 상승)을 대신 고정 |
| DES-02 게이트 기동 | `cmd.exe /d /c <명령>` 직접 | 명령을 임시 배치 파일에 쓰고 `cmd /d /c call <배치>` | 경미(§4.1) — 기동 방식만 바뀌고 판정은 동일 | 기록 후 계속. `&`·`|`를 쓰는 게이트에서 출력이 유실되던 결함의 수정 |
| DES-06 차단 사유 | 출력 꼬리 ≤500자 | 동일 + ANSI 이스케이프 제거 | 경미(§4.1) | 기록 후 계속. T38이 고정 |
| NFR-04 시간 예산 | 게이트당 60초, 훅 전체 120초 | 게이트당 300초, 훅 전체 600초 | **중대(§4.2)** | [DCR-006](./DCR-006-게이트-시간-예산.md) 대안 A 승인 → 기준선 v2 발행, 값 반영 완료 |

## 미완료 항목

- 이 폴더와 변경 파일은 **미커밋**(워킹트리에만 존재) — 커밋은 사용자 요청에 따른다
- 후속 후보: 게이트별 예산(DCR-006 대안 B — 의무 목록이 길어져 합계가 600초에 접근하면), 타임아웃 시 손자 프로세스 정리(현재 `cmd`만 종료되고 손자는 남는다), 사이클 2b 시도 등록부(AI-11), `docs/presentation`의 의존성 명시(요구사항 파일이 없어 이번에 수동 설치했다)
- 이 폴더·`docs/plan.md`·`docs/decisions.md`는 **미커밋**(워킹트리에만 존재)

## 재개 지점

- 다음 작업: 없음 — 사이클 완료. 다음 사이클은 새 요구·설계 관문부터
- 먼저 확인할 사항: 회귀 의무 목록의 마지막 성공 SHA(`2ff74ee`+미커밋)와 현재 HEAD·워킹트리를 비교한다 — 다르면 목록 전량을 재실행한다(§3.1). 게이트 상태 파일의 마지막 값은 `infraCount: 0`·`lastPassKey: 14e4be31…`(2026-09-21 00:30)이다. **Stop 훅이 이 저장소에 설치되어 있지 않다면**(`~/.claude/settings.json`) `setup/setup_claude.ps1`을 재실행해야 게이트가 실제로 동작한다
- 필요한 명령 또는 파일: `powershell -NoProfile -ExecutionPolicy Bypass -File setup\hooks\tests\run-tests.ps1` (Claude가 직접 실행), `setup/hooks/wf-common.ps1`, `setup/hooks/tests/run-tests.ps1`, [test-map](./test-map.md)

## 변경 이력

| 날짜 | 변경 | 근거 | 상태 또는 기준선 | 작성자·승인자 |
|---|---|---|---|---|
| 2026-09-20 | 최초 작성 — 승인 관문·계획 수립 기록, 사전 실행 기준선 | wf-implement §3.1·§3.2 | in-progress, v1 | Claude(작성) |
| 2026-09-20 | TASK-37 completed — 의무 목록 첫 행 발행, 검증 표 신설 | TDD Red→Green, 진입 조건 충족 | in-progress, v1 | Claude(작성) |
| 2026-09-20 | TASK-38 completed — Stop 훅·차단 메시지 신설, 명령 부재 판별을 해석 기반으로 변경 | TDD, `cmd` 종료 코드 실측 | in-progress, v1 | Claude(작성) |
| 2026-09-20 | TASK-39·40 completed — Stop 등록·timeout 파라미터화, 전역 게이트와 시크릿 스캔 신설 | TDD, AC-09 3건 실측 | in-progress, v1 | Claude(작성) |
| 2026-09-21 | TASK-41·42 completed — 명령-데이터 분리 문장, wf-implement·verification-depth 규칙 문장 | AC-08 대조 16/16 | in-progress, v1 | Claude(작성) |
| 2026-09-21 | TASK-43 진행 — AC-01~10 성공, AC-11 부분. 리뷰 수정 2건(ANSI·배치 실행)과 T38 추가, DCR-006 발행 | 자기 적용 실측 | in-progress(차단), v1 | Claude(작성) |
| 2026-09-21 | TASK-43 completed — DCR-006 대안 A 반영, §3.6 전체 스위트 실행, AC-01~11 전부 성공 | 사용자 승인(DCR-006), 자기 적용 재실행 | completed, v2 | 사용자(승인)·Claude(작성) |

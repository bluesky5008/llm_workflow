# DCR-022: C층 설계에 공용 모듈과 의존 표 명시 — `wf-common.ps1` DES-09 등재(명확화)

> 문서 유형: `dcr`
> 작업 ID: `20261026-component-deps`
> 상태: `completed`
> 기준선: `v5 유지` ([REQ-llm-workflow](../../requirements.md)·[DESIGN-llm-workflow](../../design.md)) — 명확화, 재승인 대상 아님
> 작성일: 2026-10-26
> 최종 갱신: 2026-10-27
> 관련 문서: [REQ-DESIGN-component-deps](./req-design.md), [ADR-021](./ADR-021-컴포넌트-의존-표와-설계-린트.md), [DESIGN-llm-workflow: 설계](../../design.md), [WORK-20261026-component-deps: 작업 기록](./work-log.md)

## 요약

- 목적: C층 설계 문서에 이미 있는 공용 모듈을 DES-09로 적고, DES-01~09의 의존 표(ADR-021 형식)를 둔다.
- 현재 결론 또는 상태: 적용 완료(2026-10-27) — `docs/design.md` DES-09·의존 표, `lint_design.py` exit 0. 기준선 v5 유지.
- 다음 행동: 없음.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | change | [DESIGN-llm-workflow](../../design.md) | 컴포넌트와 책임, 관련 문서, 변경 이력 | v5 유지 |
| input | requirement | [REQ-DESIGN-component-deps](./req-design.md) | FR-09, DES-05, Q-04 | 변경 사유 |
| input | decision | [ADR-021](./ADR-021-컴포넌트-의존-표와-설계-린트.md) | 결정 1 | 표 형식 |

## 변경 사유와 증거

- `setup/hooks/wf-common.ps1`(함수 17개)을 훅 6개가 dot-source하고(`grep -c wf-common setup/hooks/wf-*.ps1` 각 1), 상태 파일 `Read/Write-WfState`와 메시지 로더 `Get-WfMessage`(`messages\<이름>` 읽기)를 정의하지만 [docs/design.md 컴포넌트와 책임](../../design.md#컴포넌트와-책임)에 없다. 의존 표를 쓰면 6개 훅의 `의존`이 정의되지 않은 대상을 가리킨다.

## 기존 기준선과 설계

- v5 `- DES-01`~`- DES-08` 불릿. 상태 파일 형식은 `데이터와 인터페이스` 절, 공용 모듈은 언급 없음.

## 제안 설계

DES-08 불릿 뒤에 DES-09 불릿과 의존 표를 둔다.

- DES-09: **`wf-common.ps1`** — 훅 6개가 dot-source하는 공용 함수: 입력 읽기, 열린 작업 기록 목록(판정 규칙은 DES-01·`열린 작업 판정`), transcript 크기·usage 토큰 판독(DES-02 신호 규칙의 구현), 상태 파일 읽기·쓰기(형식은 `데이터와 인터페이스`), 메시지 로드(DES-05), 출력 계약 직렬화, 대장 판독(규칙은 DES-06). 규칙·형식을 정하지 않는 공용 구현이며 이벤트를 처리하지 않는다.

| ID | 의존 | 피의존 | 소유 데이터 | 출처 |
|---|---|---|---|---|
| DES-01 | DES-05, DES-09 | DES-04 | — | 재사용(setup/hooks/wf-session-start.ps1) |
| DES-02 | DES-05, DES-09 | DES-04 | — | 재사용(setup/hooks/wf-context-threshold.ps1) |
| DES-03 | DES-05, DES-09 | DES-04 | — | 재사용(setup/hooks/wf-post-compact.ps1) |
| DES-04 | DES-01~03, DES-06~08 | — | `~/.claude/settings.json` 훅 항목 | 재사용(setup/hooks/install-hooks.ps1) |
| DES-05 | — | DES-01~03, DES-06~09 | `setup/hooks/messages/*.md` | 재사용(setup/hooks/messages/) |
| DES-06 | DES-05, DES-09 | DES-04 | — | 재사용(setup/hooks/wf-test-guard.ps1) |
| DES-07 | DES-05, DES-09 | DES-04 | — | 재사용(setup/hooks/wf-stop-gate.ps1) |
| DES-08 | DES-05, DES-09 | DES-04 | — | 재사용(setup/hooks/wf-approval-gate.ps1) |
| DES-09 | DES-05 | DES-01~03, DES-06~08 | — | 재사용(setup/hooks/wf-common.ps1) |

## 변경 항목

| 대상 | 변경 전 | 변경 후 | 이유 |
|---|---|---|---|
| design.md 컴포넌트와 책임 | DES-01~08 불릿 | + DES-09 불릿, 의존 표 | 기존 공용 모듈 기록 누락, ADR-021 시범 |
| design.md 추적성 | FR-01~03·05~08 행 설계 칸에 DES-09 없음 | 그 행들에 DES-09 추가 | 훅 6개의 공용 구현 — D10 경고 해소 |
| design.md 머리말 관련 문서·`## 문서 연결` | DCR-019까지 | + DCR-022(머리말, 문서 연결 행) | 문서 연결(이전 DCR 선례) |
| design.md 변경 이력 | v5 행까지 | + 명확화 행(기준선 v5 유지) | 변경 기록 |

## 영향 범위

- 요구사항과 인수 조건: 없음(`requirements.md` 무변경)
- 인터페이스와 데이터: 없음 — 상태 파일 형식·책임 불변(소유 지정 없음, `—`)
- 보안과 운영: 없음
- 진행 중인 구현: 없음
- 테스트와 문서: `docs/design.md`만. TST-01 무변경

## 고려한 대안

- 픽스처로만 시범(Q-04 (B)) — 실제 문서의 누락이 남는다. 사용자가 (A) 선택.
- DES-09를 설계 변경으로 분류해 v6 — 코드·동작·계약이 바뀌지 않아 명확화가 맞다(design-change §3C).

## 구현된 코드의 처리

- 유지: `setup/hooks/` 전부
- 수정: 없음
- 되돌림: 없음

## 마이그레이션과 롤백

- 문서만 변경. 롤백은 커밋 되돌림.

## 검증 방법

- `python skills/wf-doc/scripts/lint_design.py docs/design.md` exit 0.
- 표의 `의존`을 `setup/hooks/*.ps1`의 dot-source, 각 훅의 `Get-WfMessage '<파일>'`(메시지 파일을 이름으로 지정 — DES-05 의존), `install-hooks.ps1` 등록 행(`setup_claude.ps1`이 dot-source)과 grep 대조.

## 남은 위험

- 분류(명확화)는 작성자 판단이다 — 적대 검토 3번이 책임 재배치 여지를 지적해 DES-09를 규칙 없는 공용 구현으로 한정하고 소유 지정을 하지 않았다. 사용자가 설계 변경으로 보면 v6 재승인.

## 적대 검토

N/A — DCR 명확화(adversarial-review §1). 단, 같은 작업의 req-design 적대 검토 대상 문서에 포함한다.

## 승인 기록

- 2026-10-27 — 사용자가 [REQ-DESIGN-component-deps](./req-design.md#승인-기록) v1과 함께 **승인**. 응답: "승인합니다". 승인 요청에서 분류(명확화, v5 유지)를 결정 항목으로 공개했고 설계 변경(v6) 전환 요청 없음.

## 변경 이력

| 날짜 | 변경 내용 | 근거 | 상태 전이 | 작성·승인 |
|---|---|---|---|---|
| 2026-10-26 | 최초 작성 | REQ-DESIGN-component-deps Q-04 | → proposed | Claude(작성) |
| 2026-10-26 | 적대 검토 1라운드 반영(지적 3·4·8·9·10) — DES-09 기술 한정, 출처 `재사용`, 상태 파일 소유 `—`, 추적표·문서 연결 행 | REQ-DESIGN-component-deps 적대 검토 | proposed 유지 | Claude(작성) |
| 2026-10-26 | 적대 검토 2라운드 16번 — DES-04 위치 `install-hooks.ps1` | REQ-DESIGN-component-deps 적대 검토 | proposed 유지 | Claude(작성) |
| 2026-10-27 | 사용자 승인(명확화, v5 유지) | 사용자 응답 "승인합니다" | proposed → approved | 사용자(승인) |
| 2026-10-27 | `docs/design.md` 적용(TASK-05) — 의존은 `setup/hooks/*.ps1` grep으로 재확인 | [PLAN TASK-05](./plan.md#task-05-c층-docsdesignmd-적용-des-05-dcr-022) | approved → completed | Claude(작성) |

## 인계

- 다음 단계 또는 워크플로우: 없음
- 다음 행동: 없음

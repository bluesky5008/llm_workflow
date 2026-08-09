# PLAN-llm-workflow: 구현 계획

> 문서 유형: `plan`
> 작업 ID: `20260809-dev-briefing`
> 상태: `in-progress`
> 기준선: `v2` ([REQ-DESIGN-dev-briefing](./work/20260809-dev-briefing/req-design.md), 2026-08-09 승인, [DCR-002](./work/20260809-dev-briefing/DCR-002-디자인-적용.md))
> 작성일: 2026-08-09
> 최종 갱신: 2026-08-09
> 관련 문서: [REQ-DESIGN-dev-briefing: 요구사항·설계](./work/20260809-dev-briefing/req-design.md), [WORK-20260809-dev-briefing: 작업 기록](./work/20260809-dev-briefing/work-log.md)

## 요약

- 목적: 승인된 발표 자료 요구사항·설계(v2)를 md 초판 → 사용자 검토 → pptx 구현 → 디자인 적용 → 완성도 검토 순서로 실행한다.
- 현재 결론 또는 상태: TASK-07~11 완료(기준선 v1). DCR-002 승인으로 기준선 v2 발행 — 디자인 구현 TASK-13~15 추가, TASK-12는 최종 관문으로 이동.
- 다음 행동: TASK-13(테스트 확장 Red)부터 TDD로 구현, 이후 TASK-15 검증을 거쳐 TASK-12 최종 검토.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | baseline | [REQ-DESIGN-dev-briefing: 요구사항·설계](./work/20260809-dev-briefing/req-design.md) | FR-01~06, AC-01~05, DES-01~06 | 승인 기준선 v2 |
| input | change | [DCR-002: 발표 자료 디자인 적용](./work/20260809-dev-briefing/DCR-002-디자인-적용.md) | TASK-13~15 | v2 변경이 추가한 작업 |
| output | implementation | [WORK-20260809-dev-briefing: 작업 기록](./work/20260809-dev-briefing/work-log.md) | document | 진행 상태·검증의 정본 |
| input | related | [WORK-20260809-claude-hooks: 작업 기록](./work/20260809-claude-hooks/work-log.md) | document | 완료된 이전 사이클(아래 축약) |

## 작업 정의

- 목표: `docs/presentation/`에 발표 자료 3종(md 정본, 생성 스크립트, pptx)을 만들고 사용자 검토 2회를 통과한다.
- 범위·범위 밖·가정·위험: [기준선 문서](./work/20260809-dev-briefing/req-design.md) 참조.

## 작업 목록

완료된 이전 사이클 (작업 `20260809-claude-hooks`, 기준선 [REQ](./requirements.md)·[DESIGN](./design.md) v1 — 상세는 [작업 기록](./work/20260809-claude-hooks/work-log.md)):

- [x] TASK-01 — 훅 테스트 하니스 작성(Red)
- [x] TASK-02 — 공용 라이브러리 + 세션 시작 훅 구현
- [x] TASK-03 — 컨텍스트 임계값 훅 구현
- [x] TASK-04 — 컴팩션 사후 재정렬 훅 구현
- [x] TASK-05 — 설치 병합 로직 + setup 통합
- [x] TASK-06 — README·실설치·통합 확인

현재 사이클 (작업 `20260809-dev-briefing`):

### TASK-07: 발표 내용 md 초판 작성

- 상태: completed
- 목표: `docs/presentation/dev-briefing.md` — DES-01 형식 계약과 DES-02 구성(18장)에 따른 내용 정본
- 관련 요구사항과 설계: FR-01·FR-02, NFR-01·NFR-03, DES-01·DES-02
- 변경 대상: `docs/presentation/dev-briefing.md` (신규)
- 의존성: 없음
- 위험: 사실 왜곡(RISK-01) — 원천 문서 대조로 완화
- 검증 방법: 커버리지 매핑 (a)~(j)를 작업 기록에 남기고 누락 확인(AC-01). 슬라이드별 사실의 원천을 자체 리뷰로 대조(NFR-01)
- 완료 조건: 매핑 완비 + DES-01 계약 준수 확인

### TASK-08: 사용자 md 내용 검토 (관문)

- 상태: completed
- 목표: AC-04 (1) — 내용 검토 통과. 수정 요청은 md에 반영 후 재검토
- 의존성: TASK-07
- 완료 조건: 사용자의 내용 검토 통과 응답. **통과 전에는 TASK-09 이후를 시작하지 않는다**

### TASK-09: 생성 스크립트 테스트 작성 (Red)

- 상태: completed
- 목표: `docs/presentation/tests/test_make_pptx.py` — 견본 md(표지+본문 2장, 중첩 불릿·코드 블록·노트)로 파서·생성기·대조를 검증. 시작 시 `pip install python-pptx` 수행(RISK-02 확인)
- 관련 요구사항과 설계: FR-03·FR-04, DES-04
- 의존성: TASK-08
- 검증 방법: 구현 부재 상태에서 실행해 의도한 이유로 실패(Red)함을 확인
- 완료 조건: Red 확인 기록

### TASK-10: make_pptx.py 구현 (Green)

- 상태: completed
- 목표: DES-01 파싱 + DES-03 생성·자동 대조. 테스트 전체 성공
- 관련 요구사항과 설계: FR-03·FR-04, NFR-02, DES-01·DES-03
- 의존성: TASK-09
- 완료 조건: `python tests/test_make_pptx.py` 성공(Green)

### TASK-11: 실제 pptx 생성과 검증

- 상태: completed
- 목표: `dev-briefing.md` → `dev-briefing.pptx` 생성, 자동 대조 통과(AC-02), PowerShell COM으로 PowerPoint 실열기·슬라이드 수 확인(AC-03 기계 확인 부분)
- 의존성: TASK-10
- 위험: 한글 폰트·텍스트 넘침(RISK-03)
- 완료 조건: 생성·대조·실열기 성공 기록

### TASK-12: 사용자 완성도 검토와 완료 보고 (관문)

- 상태: in-progress (v1에서 진행 중이었으나 DCR-002 승인으로 기준선 v2의 최종 관문으로 이동, TASK-15 완료로 재개)
- 목표: AC-04 (2)·AC-05 (4) — pptx 구현 완성도 검토(육안 확인 포함) 통과, 완료 보고 작성. **슬라이드 18(현재 상태와 남은 과제) 재확인을 사용자에게 별도 요청**(TASK-08의 재검토 예약)
- 의존성: TASK-15
- 완료 조건: 사용자 검토 통과, 작업 기록에 완료 보고 기록

기준선 v2 추가 작업 ([DCR-002](./work/20260809-dev-briefing/DCR-002-디자인-적용.md), 2026-08-09 승인):

### TASK-13: 디자인·인포그래픽 테스트 확장 (Red)

- 상태: completed
- 목표: `tests/test_make_pptx.py` 확장 — 태그 펜스(flow·rows·ladder) 파싱, 다이어그램 도형 존재(도형 수), 무태그 펜스 폴백(고정폭 패널 유지), 카드 매핑 폴백(제목 불일치 시 불릿 렌더), 디자인 시스템 적용(배경·색) 케이스
- 관련 요구사항과 설계: FR-05·FR-06, NFR-04, DES-01(v2)·DES-04(v2)·DES-05·DES-06
- 변경 대상: `docs/presentation/tests/test_make_pptx.py` (확장)
- 의존성: DCR-002 승인(완료)
- 검증 방법: 확장 기능 부재 상태에서 실행해 의도한 이유로 실패(Red)함을 확인. 기존 4개 케이스는 계속 통과해야 한다
- 완료 조건: Red 확인 기록(신규 케이스 실패, 기존 케이스 영향 없음)

### TASK-14: 디자인 시스템 + 인포그래픽 렌더러 구현 (Green)

- 상태: completed
- 목표: `make_pptx.py`에 DES-05(5색 시스템, 표지·본문 배치, 언더바·마진)와 DES-06(flow/rows/ladder 렌더러, 카드형 배치 2곳 + 폴백) 구현. `dev-briefing.md`는 펜스 태그·사다리 행 구조만 조정(문구 불변)
- 관련 요구사항과 설계: FR-05·FR-06, NFR-04, DES-05·DES-06
- 변경 대상: `docs/presentation/make_pptx.py`(확장), `docs/presentation/dev-briefing.md`(태그만)
- 의존성: TASK-13
- 위험: 다이어그램 텍스트 넘침(RISK-03), 색 선호(RISK-04)
- 완료 조건: 테스트 전체 성공(Green — 기존 4 + 신규)

### TASK-15: pptx 재생성과 검증

- 상태: completed
- 목표: `dev-briefing.md` → `dev-briefing.pptx` 재생성, 자동 대조 통과(AC-02), PowerPoint 실열기·한글 확인(AC-03), 디자인·다이어그램 적용 확인(AC-05 기계 확인 부분)
- 관련 요구사항과 설계: AC-02·03·05, NFR-02·04
- 의존성: TASK-14
- 완료 조건: 생성·대조·실열기 성공 기록(VER-06)

의존성 요약: TASK-07 → TASK-08(관문) → TASK-09 → TASK-10 → TASK-11 → [DCR-002 승인] → TASK-13 → TASK-14 → TASK-15 → TASK-12(최종 관문).

## 검증 계획

각 AC의 검증 방법은 [기준선의 검증 전략](./work/20260809-dev-briefing/req-design.md#검증-전략)을 따른다. AC-01은 TASK-07, AC-02는 TASK-10·11(v1)과 TASK-15(v2 재수행), AC-03은 TASK-11·15(기계 확인)와 TASK-12(육안), AC-04는 TASK-08·12의 사용자 관문, AC-05는 TASK-13~15(테스트·재생성)와 TASK-12(완성도 재검토)로 판정한다. 결과는 [작업 기록](./work/20260809-dev-briefing/work-log.md#검증)에 기록한다.

## 마이그레이션과 롤백

N/A — 신규 파일 추가만 수행하며 기존 시스템 동작을 변경하지 않는다(기준선 문서의 동일 절 참조).

## 인계

작업 기록 [WORK-20260809-dev-briefing](./work/20260809-dev-briefing/work-log.md)의 인계 절이 정본이다.

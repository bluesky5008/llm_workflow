# 노드 유형, 예시 트리와 자체 검토

[wf-tree §3 노드 유형](../SKILL.md#3-노드-유형)·[§9 자체 검토](../SKILL.md#9-자체-검토)가 소유하는 유형 표, 예시 트리와 검토 문항이다. 유형의 채택과 항목의 의미·완료 판정은 wf-design·wf-implement가 소유하며, 이 문서는 어휘와 문항만 둔다. 필수 게이트는 [본문 §4](../SKILL.md#4-필수-게이트)에 있다.

## 노드 유형

| 유형 | 설명 | 기존 생태계 매핑 |
|---|---|---|
| `investigate` 조사 | 현재 상태 조사, 역공학, 재현 | [wf-design §4.1](../../wf-design/SKILL.md#41-현재-상태-조사), [역공학 절차](../../wf-design/references/reverse-engineering.md) |
| `design` 설계 | 구조·계약·데이터 설계 | `DES-NN` |
| `decide` 결정 | 대안 비교·선택. OR-분기의 해소 지점 | `ADR-NNN` |
| `approve` 승인 ★ | 사용자 승인 관문 (기준선·범위·외부 작업) | `APR`, [wf-design §8](../../wf-design/SKILL.md#8-사용자-승인-관문) |
| `prototype` 실험 | 가설 검증용 임시 구현 (폐기 전제) | [프로토타입 규칙](../../wf-design/SKILL.md#1-적용-시점) |
| `implement` 구현 | 코드·테스트·설정 변경 | `TASK-NN` |
| `test` 테스트 | 구현 활동으로서의 테스트 작성·실행. TDD에서는 구현 전 Red 테스트 작성이 시작점 | [wf-implement §3.3](../../wf-implement/SKILL.md#33-구현) TDD 사이클, [§3.4](../../wf-implement/SKILL.md#34-검증) 1~3단계 |
| `review` 리뷰 | 설계 일관성 검토 / 구현 자체 리뷰 | [wf-design §4.5](../../wf-design/SKILL.md#45-일관성-검토), [wf-implement §3.5](../../wf-implement/SKILL.md#35-자체-리뷰) |
| `verify` 검증 | 인수 조건 판정 (test와 구분: AC 기준 판정) | `VER-NN` ↔ `AC-NN` |
| `document` 문서화 | 요구사항·설계·운영 문서 갱신 | [wf-doc](../../wf-doc/SKILL.md) |
| `integrate` 통합 | 빌드·회귀·일관 반영 | [wf-implement §3.6](../../wf-implement/SKILL.md#36-통합) |
| `migrate` 전환 ★ | 데이터·설정 마이그레이션 + 롤백 준비 | [wf-implement §3.2](../../wf-implement/SKILL.md#32-계획-수립) |
| `release` 릴리스 ★ | push·PR·배포 — 외부·비가역, 별도 승인 필수 | [wf-implement §2.3](../../wf-implement/SKILL.md#23-자율-진행과-승인) |
| `change` 설계 변경 | 구현 중 기준선 충돌 시 DCR 분기 | `DCR-NNN`, [DCR 절차](../../wf-design/references/design-change.md) |
| `question` 질문/차단 | 사용자 답변·외부 요인 대기 | `Q-NN`, `blocked` |

★는 [필수 게이트](../SKILL.md#4-필수-게이트) 유형이다. 새 유형을 만들지 않는다.

## 예시 트리

```text
[포트폴리오] 인증 시스템 개선 (ST-auth-improvement)
├─ [작업] 20260808-login-rate-limit ......... in-progress (3/7)
│   ├─ [✓] 설계: 정책·저장 방식 ............. 2026-08-08 14:20
│   ├─ [✓] 승인: 기준선 v1 .................. 2026-08-08 15:02
│   ├─ [▶] 구현: 미들웨어 (TASK-01)
│   │   ├─ [▶] 테스트: 단위 (선행)
│   │   └─ [ ] 리뷰: 자체 리뷰
│   └─ [ ] 검증: AC 판정 (VER-01)
├─ [작업] 20260815-session-store ............ pending  depends: rate-limit
└─ [작업] 20260820-2fa ...................... pending
```

표기의 의미는 [렌더링 세칙](rendering.md)을 따른다. 예시의 하위 항목은 전부 계획 목록의 항목이어야 하며, 목록에 없는 노드를 트리에만 두지 않는다.

## 자체 검토

트리를 생성하거나 갱신한 뒤 확인한다.

- 생성 시점의 트리가 계획 문서의 항목 목록과 일치하는가? (이후의 어긋남은 결함이 아니며, 다르면 목록이 맞다)
- 생성된 표현에 생성 일시(`<!-- generated: YYYY-MM-DD HH:MM -->`)가 있는가?
- 필수 게이트(`approve`·`release`·`migrate` 검증)가 누락되거나 임의로 생략되지 않았는가?
- 포트폴리오가 저장 위치(`docs/status.md` 또는 `docs/status-<슬러그>.md`)에 실제 파일로 존재하고, 범위 승인의 결과가 문서 상태와 승인 기록에 반영되었는가?
- 롤업 집계가 문서의 상태 필드를 바꾸지 않았는가?
- OR-분기의 기각 대안이 삭제되지 않고 보존되었는가?
- 완료 노드가 기준선 변경을 이유로 미완료로 되돌려지지 않고, 재작업이 새 노드로 표현되었는가?
- `상위:`(분해)와 `depends:`(순서)가 혼동 없이 기록되었는가?
- 파일 겹침·심볼 참조로 검출한 `depends:` 후보가 목록에 반영되었거나 제외 이유가 있는가?([wf-implement §3.2](../../wf-implement/SKILL.md#32-계획-수립)가 의미를 소유)
- 세션 재개 시 활성 경로 뷰만으로 "지금 어디"를 알 수 있는가?

# 대장 판독 공유 견본 (DES-08)

regression_guard.py(TST-02)와 wf-test-guard.ps1(TST-01)이 함께 읽어 판독 결과 일치를 고정한다.
`## 대장` 아래 첫 표만 대장이다. `## 판독 기대`는 경로별로 보호하는 행 ID(없으면 `-`)를 적는다.

## 대장

| ID | 테스트·명령 | 테스트 파일 | 보호 스코프 | 크기 | 발행 작업 | 상태 | 마지막 성공 (일시 · SHA) | 비고 |
|---|---|---|---|---|---|---|---|---|
| TST-01 | `run-tests.ps1` | setup/hooks/tests/run-tests.ps1 | 훅 | medium | x | 유지 | 2026-01-02 10:00 · abc1234 | |
| TST-02 | `pytest` | skills/wf-doc/scripts/tests/*.py; Extra\Sub\Test_?.PS1 | 린트 | small | x | 유지 | 2026-01-02 10:00 · abc1234+dirty | 구분자·역슬래시·대소문자 |
| TST-03 | `python t.py` | docs/x/test_y.py | 빌드 | medium | x | 격리(환경, x) | 없음 — 견본 | 유지 아님 |
| TST-04 | `python u.py` | docs/u/*.py | 폐기 | small | x | 폐기(고아, 2026-02-01) | 2026-01-02 10:00 · abc1234 | 유지 아님 |

## 판독 기대

| 경로 | 보호 행 |
|---|---|
| setup/hooks/tests/run-tests.ps1 | TST-01 |
| SETUP\hooks\tests\Run-Tests.ps1 | TST-01 |
| skills/wf-doc/scripts/tests/test_new.py | TST-02 |
| extra/sub/test_1.ps1 | TST-02 |
| extra/sub/test_10.ps1 | - |
| docs/x/test_y.py | - |
| docs/u/a.py | - |
| setup/hooks/wf-common.ps1 | - |

## 재정비 기록

| ID | 테스트 파일 | 상태 |
|---|---|---|
| TST-09 | not/the/register.py | 유지 |

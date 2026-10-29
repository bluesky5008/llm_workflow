# regression_guard.py 검증 — 실행: python -m pytest skills/wf-doc/scripts/tests -q
# 임시 git 저장소에 대장·테스트 파일·작업 기록을 만들고 exit 코드와 출력 행을 본다(FR-04·08, DES-04·08).
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import regression_guard as rg  # noqa: E402

SAMPLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "test-register.sample.md")

REGISTER = """# 대장

## 대장

| ID | 테스트·명령 | 테스트 파일 | 상태 | 마지막 성공 (일시 · SHA) | 비고 |
|---|---|---|---|---|---|
{rows}
## 변경 이력
"""

WORKLOG = """# WORK-20260101-sample: 작업 기록

> 상태: `{state}`

## 검증 결과

### 테스트 대장 변경

{body}

## 완료 보고
"""


def git(root, *args):
    return subprocess.run(["git", "-C", root, "-c", "user.name=t", "-c", "user.email=t@t", *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def row(sha, state="유지", files="tests/t.py", rid="TST-01"):
    return "| %s | `pytest` | %s | %s | 2026-01-02 10:00 · %s | |" % (rid, files, state, sha)


def repo(tmp_path):
    """테스트 파일을 커밋하고, 그 SHA를 마지막 성공으로 적은 대장을 두 번째 커밋으로 둔다."""
    root = str(tmp_path)
    git(root, "init", "-q")
    write(root, "tests/t.py", "def test_a(): pass\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "c1")
    sha = git(root, "rev-parse", "--short", "HEAD")
    write(root, "docs/test-register.md", REGISTER.format(rows=row(sha)))
    git(root, "add", ".")
    git(root, "commit", "-qm", "c2")
    return root, sha


def log(root, body, state="in-progress"):
    write(root, "docs/work/20260101-sample/work-log.md", WORKLOG.format(state=state, body=body))


def run(root, capsys):
    code = rg.main([root])
    return code, capsys.readouterr().out.strip().splitlines()


def test_no_register_is_silent_pass(tmp_path, capsys):
    git(str(tmp_path), "init", "-q")
    assert run(str(tmp_path), capsys) == (0, [])


def test_clean_repo_passes(tmp_path, capsys):
    root, _ = repo(tmp_path)
    assert run(root, capsys) == (0, [])


def test_changed_test_file_without_record_fails(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "tests/t.py", "def test_a(): assert False\n")
    code, out = run(root, capsys)
    assert code == 1 and out == ["TST-01: 테스트 파일 변경 tests/t.py"]


def test_committed_change_after_sha_also_fails(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "tests/t.py", "def test_a(): assert False\n")
    git(root, "commit", "-qam", "c3")
    assert run(root, capsys)[0] == 1


def test_changed_test_file_with_record_passes(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "tests/t.py", "def test_a(): assert False\n")
    log(root, "| TST-01 | 유지 → 유지(수정) | Breaking | — | 승인 대기 |")
    assert run(root, capsys) == (0, [])


def test_record_in_closed_worklog_is_ignored(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "tests/t.py", "def test_a(): assert False\n")
    log(root, "| TST-01 | 유지 → 유지(수정) | Breaking | — | 승인 |", state="completed")
    assert run(root, capsys)[0] == 1


def test_record_outside_register_change_section_is_ignored(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "tests/t.py", "def test_a(): assert False\n")
    log(root, "없음.\n\n### 다른 절\n\nTST-01")
    assert run(root, capsys)[0] == 1


def test_quarantine_without_record_fails(tmp_path, capsys):
    root, sha = repo(tmp_path)
    write(root, "docs/test-register.md", REGISTER.format(rows=row(sha, state="격리(환경, x)")))
    code, out = run(root, capsys)
    assert code == 1 and out == ["TST-01: 대장 상태 변경(격리(환경, x)) docs/test-register.md"]


def test_row_deleted_without_record_fails(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "docs/test-register.md", REGISTER.format(rows=""))
    code, out = run(root, capsys)
    assert code == 1 and out == ["TST-01: 대장 삭제 docs/test-register.md"]


def test_test_file_value_changed_without_record_fails(tmp_path, capsys):
    root, sha = repo(tmp_path)
    write(root, "docs/test-register.md", REGISTER.format(rows=row(sha, files="tests/other.py")))
    code, out = run(root, capsys)
    assert code == 1 and out == ["TST-01: 대장 테스트 파일 변경 docs/test-register.md"]


def test_register_shrink_with_record_passes(tmp_path, capsys):
    root, sha = repo(tmp_path)
    write(root, "docs/test-register.md", REGISTER.format(rows=row(sha, state="폐기(고아, 2026-02-01)")))
    log(root, "| TST-01 | 유지 → 폐기 | 고아 | 아님 | 승인 |")
    assert run(root, capsys) == (0, [])


def test_head_register_without_file_column_is_not_a_change(tmp_path, capsys):
    root, sha = repo(tmp_path)
    old = "| ID | 테스트·명령 | 상태 | 마지막 성공 (일시 · SHA) |\n|---|---|---|---|\n| TST-01 | x | 유지 | 2026-01-02 10:00 · %s |\n" % sha
    write(root, "docs/test-register.md", "## 대장\n\n" + old)
    git(root, "commit", "-qam", "c3")
    write(root, "docs/test-register.md", REGISTER.format(rows=row(sha)))
    assert run(root, capsys) == (0, [])


def test_unreadable_register_is_internal_error(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "docs/test-register.md", "## 대장\n\n표 없음\n")
    assert rg.main([root]) == 2


def test_onboarding_notation_protects_only_kept_rows():
    # 편입 표기(격리(기존 실패, …)·미확정·명령줄 제외·파이프 없는 실패 메시지)는 판독을 바꾸지 않는다(legacy-onboarding DES-05)
    text = """## 대장

| ID | 테스트·명령 | 테스트 파일 | 보호 스코프 | 크기 | 발행 작업 | 상태 | 마지막 성공 (일시 · SHA) | 비고 |
|---|---|---|---|---|---|---|---|---|
| TST-01 | `pytest tests --deselect tests/legacy/test_flaky.py::test_x --ignore=tests/legacy/test_old.py` | tests/unit/*.py | 미확정 | medium | 20260101-onboard | 유지 | 2026-01-02 10:00 · abc1234 | 편입 |
| TST-02 | `pytest tests/legacy/test_old.py` | tests/legacy/test_old.py | 미확정 | small | 20260101-onboard | 격리(기존 실패, 20260102-fix) | 없음 — 편입 2회 실패 | 2 failed — AssertionError: a / b |
| TST-03 | `pytest tests/legacy/test_flaky.py::test_x` | tests/legacy/test_flaky.py | 미확정 | small | 20260101-onboard | 격리(불일치, 20260102-fix) | 없음 — 편입 2회 불일치 | |
"""
    rows = rg.parse_register(text)
    assert rows["TST-02"][0] == "격리(기존 실패, 20260102-fix)"
    assert rg.protecting(rows, "tests/unit/test_a.py") == ["TST-01"]
    assert rg.protecting(rows, "tests/legacy/test_old.py") == []
    assert rg.protecting(rows, "tests/legacy/test_flaky.py") == []


def test_sample_register_reading_matches_expectations():
    text = open(SAMPLE, encoding="utf-8").read()
    rows = rg.parse_register(text)
    expect = text.split("\n## 판독 기대\n", 1)[1].split("\n## ", 1)[0]
    cases = [[c.strip() for c in line.strip("|").split("|")] for line in expect.strip().splitlines()[2:]]
    assert len(cases) == 8
    for path, rid in cases:
        assert rg.protecting(rows, path) == ([] if rid == "-" else [rid]), path


def test_cleanup_batch_record_passes_refactor_and_discard(tmp_path, capsys):
    # 재정비 작업 표기(비고 `리팩터(…)`, 대장 변경 절 `유지 → 유지(리팩터)`·`유지 → 폐기`, 승인 열의 따옴표 인용)는
    # 판독을 바꾸지 않는다 — 기록이 있으면 통과, 없으면 두 위반(legacy-cleanup DES-04)
    root, sha = repo(tmp_path)
    kept = "| TST-01 | `pytest` | tests/t.py | 유지 | 2026-01-02 10:00 · %s | 리팩터(Lazy Test, 2026-02-01) |" % sha
    write(root, "tests/u.py", "def test_b(): pass\n")
    write(root, "docs/test-register.md", REGISTER.format(rows=kept + "\n" + row(sha, files="tests/u.py", rid="TST-02")))
    git(root, "add", ".")
    git(root, "commit", "-qm", "c3")
    write(root, "tests/t.py", "def test_a():\n    assert True\n")
    write(root, "docs/test-register.md", REGISTER.format(
        rows=kept + "\n" + row(sha, state="폐기(중복, 2026-02-01)", files="tests/u.py", rid="TST-02")))
    code, out = run(root, capsys)
    assert code == 1 and out == ["TST-01: 테스트 파일 변경 tests/t.py",
                                 "TST-02: 대장 상태 변경(폐기(중복, 2026-02-01)) docs/test-register.md"]
    log(root, '| TST-01 | 유지 → 유지(리팩터) | 리팩터 — Lazy Test, 수정 전후 통과·단언 보존 | 해당 없음 | 배치 1 승인(2026-02-01, "전부") |\n'
              '| TST-02 | 유지 → 폐기 | 중복 — 단언 대조 | 아니오 | 배치 1 승인(2026-02-01, "전부") |')
    assert run(root, capsys) == (0, [])

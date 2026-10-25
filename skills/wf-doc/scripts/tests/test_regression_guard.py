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


def test_sample_register_reading_matches_expectations():
    text = open(SAMPLE, encoding="utf-8").read()
    rows = rg.parse_register(text)
    expect = text.split("\n## 판독 기대\n", 1)[1].split("\n## ", 1)[0]
    cases = [[c.strip() for c in line.strip("|").split("|")] for line in expect.strip().splitlines()[2:]]
    assert len(cases) == 8
    for path, rid in cases:
        assert rg.protecting(rows, path) == ([] if rid == "-" else [rid]), path

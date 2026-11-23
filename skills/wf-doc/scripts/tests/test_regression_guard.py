# regression_guard.py 검증 — 실행: python -m pytest skills/wf-doc/scripts/tests -q
# 임시 git 저장소에 대장·테스트 파일·작업 기록을 만들고 exit 코드와 출력 행을 본다(FR-04·08, DES-04·08).
# 내용 단위 판정·지문·지문 해소·비활성화 패턴은 REQ-DESIGN-hook-friction FR-01·02·05, DES-01·02, AC-03·05.
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import regression_guard as rg  # noqa: E402

SAMPLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "test-register.sample.md")
SAMPLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "disable-pattern-samples.txt")
LISTED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "disable-pattern-list.txt")

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

BASE = "def test_a():\n    assert 1\n    assert 2\n"


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


def repo(tmp_path, text="def test_a(): pass\n", files="tests/t.py"):
    """테스트 파일을 커밋하고, 그 SHA를 마지막 성공으로 적은 대장을 두 번째 커밋으로 둔다."""
    root = str(tmp_path)
    git(root, "init", "-q")
    write(root, "tests/t.py", text)
    git(root, "add", ".")
    git(root, "commit", "-qm", "c1")
    sha = git(root, "rev-parse", "--short", "HEAD")
    write(root, "docs/test-register.md", REGISTER.format(rows=row(sha, files=files)))
    git(root, "add", ".")
    git(root, "commit", "-qm", "c2")
    return root, sha


def log(root, body, state="in-progress"):
    write(root, "docs/work/20260101-sample/work-log.md", WORKLOG.format(state=state, body=body))


def run(root, capsys):
    code = rg.main([root])
    return code, capsys.readouterr().out.strip().splitlines()


def samples():
    """공유 표본 (기대, 줄) — 패턴에 맞는 줄은 픽스처에만 두고 이 소스에는 두지 않는다(AC-05)."""
    with open(SAMPLES, encoding="utf-8") as f:
        return [(line[0] == "1", line[2:]) for line in f.read().splitlines() if line and not line.startswith("#")]


def fp_of(out):
    """출력 첫 행 끝의 `[지문]`."""
    return out[0].rsplit(" ", 1)[1]


SKIP = next(line for want, line in samples() if want)


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
    assert code == 1 and len(out) == 1 and re.fullmatch(r"TST-01: 테스트 파일 변경 tests/t\.py \[[0-9a-f]{8}\]", out[0])


def test_committed_change_after_sha_also_fails(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "tests/t.py", "def test_a(): assert False\n")
    git(root, "commit", "-qam", "c3")
    assert run(root, capsys)[0] == 1


def test_changed_test_file_with_record_passes(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "tests/t.py", "def test_a(): assert False\n")
    fp = fp_of(run(root, capsys)[1])
    log(root, "| TST-01 | 유지 → 유지(수정) | Breaking %s | — | 승인 대기 |" % fp)
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
    assert code == 1 and out == ["TST-01: 대장 상태 변경(격리(환경, x)) docs/test-register.md [-]"]


def test_row_deleted_without_record_fails(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "docs/test-register.md", REGISTER.format(rows=""))
    code, out = run(root, capsys)
    assert code == 1 and out == ["TST-01: 대장 삭제 docs/test-register.md [-]"]


def test_test_file_value_changed_without_record_fails(tmp_path, capsys):
    root, sha = repo(tmp_path)
    write(root, "docs/test-register.md", REGISTER.format(rows=row(sha, files="tests/other.py")))
    code, out = run(root, capsys)
    assert code == 1 and out == ["TST-01: 대장 테스트 파일 변경 docs/test-register.md [-]"]


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


def test_escaped_pipe_in_cell_is_cell_content():
    # GFM: 칸 안의 `\|`는 칸 경계가 아니라 내용이다 — 명령 칸에 파이프를 쓴 대장도 읽고 보호 대상을 그대로 찾는다
    text = REGISTER.format(rows="| TST-01 | `jar tf a.jar \\| grep -q x` | tests/*.py | 유지 | 2026-01-02 10:00 · abc1234 | 끝 칸 \\| |\n")
    rows = rg.parse_register(text)
    assert rows["TST-01"][1] == ["tests/*.py"]
    assert rg.protecting(rows, "tests/t.py") == ["TST-01"]
    assert rg.protecting(rows, "src/a.py") == []


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
    assert code == 1 and [line.rsplit(" ", 1)[0] for line in out] == [
        "TST-01: 테스트 파일 변경 tests/t.py",
        "TST-02: 대장 상태 변경(폐기(중복, 2026-02-01)) docs/test-register.md"] and out[1].endswith(" [-]")
    fp = fp_of(out)
    log(root, '| TST-01 | 유지 → 유지(리팩터) | 리팩터 — Lazy Test, 수정 전후 통과·단언 보존, 지문 %s | 해당 없음 | 배치 1 승인(2026-02-01, "전부") |\n'
              '| TST-02 | 유지 → 폐기 | 중복 — 단언 대조 | 아니오 | 배치 1 승인(2026-02-01, "전부") |' % fp)
    assert run(root, capsys) == (0, [])


# ---- 내용 단위 판정(REQ-DESIGN-hook-friction AC-03·05) ----

def test_disable_pattern_samples_match_expectations():
    pats = rg.load_patterns()
    cases = samples()
    wrong = [line for want, line in cases if rg.disabling(line, pats) != want]
    assert len(cases) == 8 and sum(want for want, _ in cases) == 4 and wrong == []


def test_pure_addition_in_worktree_passes(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", BASE + "\ndef test_b():\n    assert 3\n")
    assert run(root, capsys) == (0, [])


def test_committed_pure_addition_passes(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "import os\n" + BASE)
    git(root, "commit", "-qam", "c3")
    assert run(root, capsys) == (0, [])


def test_deleted_line_fails_with_fingerprint(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    code, out = run(root, capsys)
    assert code == 1 and len(out) == 1 and re.fullmatch(r"TST-01: 테스트 파일 변경 tests/t\.py \[[0-9a-f]{8}\]", out[0])


def test_added_disabling_line_fails(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", SKIP + "\n" + BASE)
    assert run(root, capsys)[0] == 1


def test_added_valueless_return_fails(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\n    return\n    assert 1\n    assert 2\n")
    assert run(root, capsys)[0] == 1


def test_fingerprint_ignores_shifts_and_other_pure_additions(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE, files="tests/*.py")
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    fp = fp_of(run(root, capsys)[1])
    write(root, "tests/t.py", "import os\n\ndef test_a():\n    assert 1\n")
    write(root, "tests/u.py", "def test_u():\n    assert 0 == 0\n")
    assert run(root, capsys) == (1, ["TST-01: 테스트 파일 변경 tests/t.py " + fp])


def test_other_deletion_changes_fingerprint(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    first = fp_of(run(root, capsys)[1])
    write(root, "tests/t.py", "def test_a():\n    assert 2\n")
    assert fp_of(run(root, capsys)[1]) != first


def test_rename_with_deletion_reports_original_path(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE, files="tests/*.py")
    git(root, "mv", "tests/t.py", "tests/t2.py")
    write(root, "tests/t2.py", "def test_a():\n    assert 1\n")
    git(root, "commit", "-qam", "c3")
    code, out = run(root, capsys)
    assert code == 1 and [line.rsplit(" ", 1)[0] for line in out] == ["TST-01: 테스트 파일 변경 tests/t.py"]


def test_untracked_protected_file_is_judged_by_content(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE, files="tests/*.py")
    write(root, "tests/new_test.py", "def test_n():\n    assert 1\n")
    assert run(root, capsys) == (0, [])
    write(root, "tests/new_test.py", SKIP + "\ndef test_n():\n    assert 1\n")
    code, out = run(root, capsys)
    assert code == 1 and len(out) == 1 and out[0].startswith("TST-01: 테스트 파일 변경 tests/new_test.py [")


def test_record_needs_row_id_and_fingerprint(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    fp = fp_of(run(root, capsys)[1])
    log(root, "| TST-01 | 유지 → 유지 | 단언 보존 변경 — 사유 | 해당 없음 | 완료 보고 관문 |")
    assert run(root, capsys)[0] == 1
    log(root, "| TST-01 | 유지 → 유지 | 단언 보존 변경 — 사유, 지문 %s | 해당 없음 | 완료 보고 관문 |" % fp)
    assert run(root, capsys) == (0, [])


def test_row_deleted_with_row_id_record_passes(tmp_path, capsys):
    root, _ = repo(tmp_path)
    write(root, "docs/test-register.md", REGISTER.format(rows=""))
    log(root, "| TST-01 | 유지 → 폐기 | 고아 | 아님 | 승인 |")
    assert run(root, capsys) == (0, [])


def test_missing_pattern_file_is_internal_error(tmp_path, capsys, monkeypatch):
    root, _ = repo(tmp_path)
    monkeypatch.setattr(rg, "PATTERNS", str(tmp_path / "none.txt"))
    assert rg.main([root]) == 2


def test_file_tracked_at_sha_but_untracked_now_reports_deletion(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    git(root, "rm", "--cached", "-q", "tests/t.py")
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    code, out = run(root, capsys)
    assert code == 1 and [line.rsplit(" ", 1)[0] for line in out] == ["TST-01: 테스트 파일 변경 tests/t.py"]


def test_external_diff_setting_does_not_hide_deletion(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    git(root, "config", "diff.external", "true")
    assert run(root, capsys)[0] == 1


def test_textconv_attribute_does_not_hide_deletion(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    write(root, ".gitattributes", "*.py diff=quiet\n")
    git(root, "config", "diff.quiet.textconv", "true")
    assert run(root, capsys)[0] == 1


# ---- 통합 뮤테이션 Missing 보강(FR-02·05) ----

def test_further_deletion_changes_fingerprint(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\n    assert 2\n")
    first = fp_of(run(root, capsys)[1])
    write(root, "tests/t.py", "def test_a():\n")
    assert fp_of(run(root, capsys)[1]) != first


def test_other_fingerprint_in_record_does_not_resolve(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    log(root, "| TST-01 | 유지 → 유지 | 단언 보존 변경 — 사유, 지문 00000000 | 해당 없음 | 완료 보고 관문 |")
    assert run(root, capsys)[0] == 1


def test_row_id_and_fingerprint_must_share_a_line(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    fp = fp_of(run(root, capsys)[1])
    log(root, "| TST-01 | 유지 → 유지 | 사유 | 해당 없음 | 완료 보고 관문 |\n"
              "| TST-02 | 유지 → 유지 | 사유, 지문 %s | 해당 없음 | 완료 보고 관문 |" % fp)
    assert run(root, capsys)[0] == 1


def test_tracked_binary_change_is_reported(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\0\n")
    assert run(root, capsys) == (1, ["TST-01: 테스트 파일 변경 tests/t.py [bin]"])


def test_untracked_binary_file_is_reported(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE, files="tests/*.py")
    write(root, "tests/n.py", "x\0\n")
    assert run(root, capsys) == (1, ["TST-01: 테스트 파일 변경 tests/n.py [bin]"])


def test_disabling_patterns_ignore_case():
    assert rg.disabling(SKIP.upper(), rg.load_patterns())


def test_patterns_without_shared_sample_match_their_own_sample():
    with open(LISTED, encoding="utf-8") as f:
        lines = [t for t in f.read().splitlines() if t and not t.startswith("#")]
    pats = rg.load_patterns()
    assert len(lines) == 8 and [t for t in lines if not rg.disabling(t, pats)] == []


def test_many_changed_files_share_git_calls(tmp_path, capsys, monkeypatch):
    root, _ = repo(tmp_path, BASE, files="tests/*.py")
    for i in range(120):
        write(root, "tests/n%03d.py" % i, BASE)
    git(root, "add", ".")
    calls, real = [], rg.git
    monkeypatch.setattr(rg, "git", lambda *a: calls.append(a) or real(*a))
    assert run(root, capsys) == (0, []) and len(calls) < 10


def test_files_in_one_diff_are_judged_separately(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE, files="tests/*.py")
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    alone = run(root, capsys)
    write(root, "tests/a.py", "def test_x():\n    assert 3\n")
    write(root, "tests/z.py", "def test_z():\n    assert 4\n")
    git(root, "add", ".")
    assert alone[0] == 1 and run(root, capsys) == alone


def test_non_ascii_file_name_with_space_is_judged(tmp_path, capsys):
    root, _ = repo(tmp_path, BASE, files="tests/*.py")
    git(root, "config", "core.safecrlf", "false")  # 한글 경로가 든 줄바꿈 경고를 끈다
    write(root, "tests/한글 이름.py", SKIP + "\n" + BASE)
    git(root, "add", ".")
    code, out = run(root, capsys)
    assert code == 1 and [line.rsplit(" ", 1)[0] for line in out] == ["TST-01: 테스트 파일 변경 tests/한글 이름.py"]


def test_failed_batch_is_retried_per_file(tmp_path, capsys, monkeypatch):
    root, _ = repo(tmp_path, BASE, files="tests/*.py")
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    write(root, "tests/a.py", BASE)
    git(root, "add", ".")
    real = rg.file_diff
    cut = (128, "diff --git a/tests/t.py b/tests/t.py\n")
    monkeypatch.setattr(rg, "file_diff", lambda r, sha, *ps: cut if len(ps) > 1 else real(r, sha, *ps))
    assert run(root, capsys)[0] == 1


def test_path_missing_from_batch_is_judged_alone(tmp_path, capsys, monkeypatch):
    root, _ = repo(tmp_path, BASE)
    write(root, "tests/t.py", "def test_a():\n    assert 1\n")
    monkeypatch.setattr(rg, "file_diffs", lambda *a: {})
    assert run(root, capsys)[0] == 1

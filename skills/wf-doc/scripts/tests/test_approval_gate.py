# approval_gate.py 검증 — 실행: python -m pytest skills/wf-doc/scripts/tests -q
# 임시 저장소에 작업 기록·기준선 문서·선언을 만들고 exit 코드와 출력 행을 본다(REQ-DESIGN-approval-gate AC-01~03).
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import approval_gate as ag  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

WORKLOG = """# WORK-{wid}: 작업 기록

> 문서 유형: `work-log, verification, completion`
> 작업 ID: `{wid}`
> 상태: `{state}`
> 기준선: {baseline}

## 요약
"""

DOC = """# REQ-DESIGN-x: 문서

> 문서 유형: `requirements, design`
> 상태: `{state}`

## 승인 기록

{record}

## 인계
"""

QUOTED = '- 2026-10-26 — 사용자가 대화형 승인 관문에서 **승인**. 응답: "승인".'
TABLE = '| v1 | 2026-10-09 | 승인 | 대화형 승인 관문에서 사용자 응답 "승인" — 진행 |'
LIGHT = "`N/A — 경량 경로로 기준선 없음`"
LINKED = "`[REQ-DESIGN-x](./req-design.md) v1`"


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def repo(tmp_path, works=(), git=False, gate=None):
    """works: (작업 ID, 작업 상태, 기준선 값, 문서 상태 또는 None, 승인 기록 행)."""
    root = str(tmp_path)
    os.makedirs(os.path.join(root, "docs", "work"), exist_ok=True)
    for wid, state, baseline, doc_state, record in works:
        d = os.path.join(root, "docs", "work", wid)
        write(os.path.join(d, "work-log.md"), WORKLOG.format(wid=wid, state=state, baseline=baseline))
        if doc_state:
            write(os.path.join(d, "req-design.md"), DOC.format(state=doc_state, record=record))
    if gate is not None:
        write(os.path.join(root, ".wf-gate.json"), gate)
    if git:
        subprocess.run(["git", "init", "-q", root], check=True)
    return root


def run(root, target, capsys):
    code = ag.main([root, os.path.join(root, target)])
    return code, capsys.readouterr().out


def touch(root, *rels):
    for rel in rels:
        write(os.path.join(root, rel), "x\n")


# ---- 승인 판정 (AC-01) ----

def test_no_docs_work_passes(tmp_path, capsys):
    assert run(str(tmp_path), "src/a.py", capsys) == (0, "")


def test_unapproved_baseline_asks_with_work_and_doc(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "awaiting-approval", LINKED, "awaiting-approval", "- 아직 없음.")])
    code, out = run(root, "src/a.py", capsys)
    assert code == 1
    assert "20260101-a" in out and "req-design.md" in out and "awaiting-approval" in out


def test_approved_with_quoted_response_passes(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", LINKED, "approved", QUOTED)])
    assert run(root, "src/a.py", capsys) == (0, "")


def test_approved_without_response_quote_asks(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", LINKED, "approved", "- 2026-10-26 — 승인.")])
    code, out = run(root, "src/a.py", capsys)
    assert code == 1 and "응답 인용" in out


def test_response_word_without_quote_asks(tmp_path, capsys):
    # survived mutant G1: "응답" alone must not count as a recorded response
    root = repo(tmp_path, [("20260101-a", "in-progress", LINKED, "approved", "- 2026-10-26 — 승인. 응답은 대화에만 있음.")])
    assert run(root, "src/a.py", capsys)[0] == 1


def test_table_form_and_completed_doc_pass(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", LINKED, "completed", TABLE)])
    assert run(root, "src/a.py", capsys) == (0, "")


def test_baseline_without_link_asks(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", "`N/A — 미승인`", None, "")])
    code, out = run(root, "src/a.py", capsys)
    assert code == 1 and "링크" in out


def test_missing_linked_doc_asks(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", LINKED, None, "")])
    assert run(root, "src/a.py", capsys)[0] == 1


def test_closed_and_on_hold_works_are_ignored(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "completed", LINKED, "draft", ""),
                           ("20260101-b", "on-hold", LINKED, "draft", "")])
    assert run(root, "src/a.py", capsys) == (0, "")


def test_docs_path_and_outside_root_pass(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", LINKED, "draft", "")])
    assert run(root, "docs/notes.md", capsys) == (0, "")
    assert ag.main([root, os.path.join(os.path.dirname(root), "elsewhere.py")]) == 0


# ---- 제품 코드 선언 .wf-gate.json (AC-01, DES-09) ----

def test_declaration_exclude_and_product(tmp_path, capsys):
    gate = json.dumps({"product": ["docs/tools/*.py"], "exclude": ["notes/*"]})
    root = repo(tmp_path, [("20260101-a", "in-progress", LINKED, "draft", "")], gate=gate)
    assert run(root, "notes/todo.txt", capsys) == (0, "")
    assert run(root, "docs/tools/build.py", capsys)[0] == 1


def test_broken_declaration_is_internal_error(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", LINKED, "draft", "")], gate="{not json")
    assert run(root, "src/a.py", capsys)[0] == 2


# ---- 경량 표지 기계 조건 (AC-02, DES-02) ----

def test_lightweight_within_limit_passes(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", LIGHT, None, "")], git=True)
    touch(root, "src/a.py", "src/b.py", "src/c.py", "src/d.py")
    assert run(root, "src/a.py", capsys) == (0, "")


def test_lightweight_exactly_five_passes(tmp_path, capsys):
    # survived mutant G2: the limit is inclusive
    root = repo(tmp_path, [("20260101-a", "in-progress", LIGHT, None, "")], git=True)
    touch(root, "src/a.py", "src/b.py", "src/c.py", "src/d.py", "src/e.py")
    assert run(root, "src/a.py", capsys) == (0, "")


def test_lightweight_sixth_product_file_asks(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", LIGHT, None, "")], git=True)
    touch(root, "src/a.py", "src/b.py", "src/c.py", "src/d.py", "src/e.py", "docs/x.md")
    code, out = run(root, "src/f.py", capsys)
    assert code == 1 and "(a)" in out


def test_lightweight_sensitive_target_asks(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", LIGHT, None, "")], git=True)
    touch(root, "requirements.txt")
    write(os.path.join(root, ".wf-gate.json"), "{}")
    assert "(b)" in run(root, "requirements.txt", capsys)[1]
    assert "(b)" in run(root, ".wf-gate.json", capsys)[1]
    touch(root, ".claude/settings.local.json", "config/settings.json")
    assert "(b)" in run(root, ".claude/settings.local.json", capsys)[1]
    assert run(root, "config/settings.json", capsys) == (0, "")


def test_lightweight_new_file_must_be_test(tmp_path, capsys):
    root = repo(tmp_path, [("20260101-a", "in-progress", LIGHT, None, "")], git=True)
    code, out = run(root, "src/new_module.py", capsys)
    assert code == 1 and "(c)" in out
    assert run(root, "tests/test_new.py", capsys) == (0, "")


# ---- 실제 완료 작업의 승인 기록 두 형식 (AC-03) ----

def test_repository_baselines_in_both_forms_are_approved():
    bullet = os.path.join(REPO, "docs", "work", "20261026-test-quality", "req-design.md")
    table = os.path.join(REPO, "docs", "work", "20261009-skill-diet", "req-design.md")
    assert ag.baseline_problem(bullet) is None
    assert ag.baseline_problem(table) is None

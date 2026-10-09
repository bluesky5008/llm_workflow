# lint_skill.py 검증 — 실행: python -m pytest skills/wf-doc/scripts/tests -q
# 크기 라벨: small. K1~K7마다 실패·통과 입력(14) + 대상 탐색 + exit 코드.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lint_skill as ls  # noqa: E402

GOOD_BODY = """# wf-x — 견본

## 경계

규칙은 [세부](references/a.md#세부-규칙)를 따른다.

## 주의 — 자주 틀리는 것

1. 승인 없이 구현을 시작하지 않는다.

## 1. 절차

본문.
"""

REF_A = """# 세부

## 세부 규칙

- 항목.
"""


def skill(tmp_path, name="wf-x", desc="견본 스킬.", body=GOOD_BODY, refs=None, frontmatter=True):
    folder = tmp_path / "skills" / name
    folder.mkdir(parents=True, exist_ok=True)
    fm = "---\nname: %s\ndescription: %s\n---\n\n" % (name, desc) if frontmatter else ""
    (folder / "SKILL.md").write_text(fm + body, encoding="utf-8")
    for rel, text in (refs if refs is not None else {"references/a.md": REF_A}).items():
        p = folder / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return str(folder / "SKILL.md")


def codes(findings, level=None):
    return sorted(f.code for f in findings if level is None or f.level == level)


def run(path):
    return ls.lint_paths([path])


# ---- K1 frontmatter ----

def test_k1_fail(tmp_path):
    assert "K1" in codes(run(skill(tmp_path, name="x" * 65)), "E")
    assert "K1" in codes(run(skill(tmp_path, name="wf-y", desc="가" * 1025)), "E")
    assert "K1" in codes(run(skill(tmp_path, name="wf-z", desc="가" * 950)), "W")
    assert "K1" in codes(run(skill(tmp_path, name="wf-w", frontmatter=False)), "E")


def test_k1_pass(tmp_path):
    assert "K1" not in codes(run(skill(tmp_path, desc="가" * 900)))


# ---- K2 description ----

def test_k2_fail(tmp_path):
    assert "K2" in codes(run(skill(tmp_path, desc="<example>태그</example>")), "E")
    assert "K2" in codes(run(skill(tmp_path, name="wf-y", desc="경로 C:\\src\\x")), "E")


def test_k2_pass(tmp_path):
    assert "K2" not in codes(run(skill(tmp_path, desc="경로 skills/wf-x/SKILL.md, 비교 a < b")))


# ---- K3 어절 상한 ----

def words(n):
    return GOOD_BODY + "\n" + " ".join("어절%d" % i for i in range(n)) + "\n"


def test_k3_fail(tmp_path):
    base = len(GOOD_BODY.split())
    assert "K3" in codes(run(skill(tmp_path, name="wf-tree", body=words(1201 - base))), "E")
    assert "K3" in codes(run(skill(tmp_path, name="wf-tree", body=words(1150 - base))), "W")
    assert "K3" in codes(run(skill(tmp_path, name="wf-other", body=words(5001 - base))), "E")


def test_k3_pass(tmp_path):
    base = len(GOOD_BODY.split())
    assert "K3" not in codes(run(skill(tmp_path, name="wf-tree", body=words(1100 - base))))
    assert ls.body_words(skill(tmp_path, name="wf-w", desc="제외되는 설명 어절", body=words(5))) == base + 5


# ---- K4 링크 ----

def test_k4_fail(tmp_path):
    bad_file = GOOD_BODY.replace("references/a.md#세부-규칙", "references/none.md")
    assert "K4" in codes(run(skill(tmp_path, body=bad_file)), "E")
    bad_anchor = GOOD_BODY.replace("references/a.md#세부-규칙", "references/a.md#없는-절")
    assert "K4" in codes(run(skill(tmp_path, name="wf-y", body=bad_anchor)), "E")
    ref_bad = {"references/a.md": REF_A + "\n[본문](../SKILL.md#없는-절)\n"}
    assert "K4" in codes(run(skill(tmp_path, name="wf-z", refs=ref_bad)), "E")


def test_k4_pass(tmp_path):
    fenced = GOOD_BODY + "\n```markdown\n[예시](./work/<작업-ID>/plan.md)\n```\n\n`[코드](none.md)` 인라인.\n"
    assert "K4" not in codes(run(skill(tmp_path, body=fenced)))


# ---- K5 고아 references ----

def test_k5_fail(tmp_path):
    refs = {"references/a.md": REF_A, "references/orphan.md": "# 고아\n"}
    assert "K5" in codes(run(skill(tmp_path, refs=refs)), "W")


def test_k5_pass(tmp_path):
    refs = {"references/a.md": REF_A + "\n[둘](b.md)\n", "references/b.md": "# 둘\n"}
    assert "K5" not in codes(run(skill(tmp_path, refs=refs)))


# ---- K6 표·코드블록 ----

def table(n):
    return "| a | b |\n|---|---|\n" + "".join("| %d | x |\n" % i for i in range(n - 2))


def test_k6_fail(tmp_path):
    assert "K6" in codes(run(skill(tmp_path, body=GOOD_BODY + "\n" + table(10))), "W")
    block = "\n```text\n" + "\n".join("l%d" % i for i in range(12)) + "\n```\n"
    assert "K6" in codes(run(skill(tmp_path, name="wf-y", body=GOOD_BODY + block)), "W")


def test_k6_pass(tmp_path):
    block = "\n```text\n" + "\n".join("l%d" % i for i in range(11)) + "\n```\n"
    assert "K6" not in codes(run(skill(tmp_path, body=GOOD_BODY + "\n" + table(9) + block)))
    two_tables = GOOD_BODY + "\n" + table(5) + "\n문단.\n\n" + table(5)   # 떨어진 표 둘은 합쳐 세지 않는다(실제 wf-tree에서 발견)
    assert "K6" not in codes(run(skill(tmp_path, name="wf-y", body=two_tables)))


# ---- K7 주의 절·가드 ----

def test_k7_fail(tmp_path):
    no_caution = GOOD_BODY.replace("## 주의 — 자주 틀리는 것", "## 메모")
    assert "K7" in codes(run(skill(tmp_path, body=no_caution)), "E")
    no_guard = GOOD_BODY.replace("시작하지 않는다", "시작한다")
    assert "K7" in codes(run(skill(tmp_path, name="wf-y", body=no_guard)), "W")


def test_k7_pass(tmp_path):
    assert "K7" not in codes(run(skill(tmp_path)))


# ---- 대상 탐색·exit ----

def test_default_targets_find_all_skills(tmp_path):
    a, b = skill(tmp_path, name="wf-a"), skill(tmp_path, name="wf-b")
    nested = tmp_path / "docs" / "work"
    nested.mkdir(parents=True)
    root = ls.find_root(str(nested))
    assert root == str(tmp_path)
    assert sorted(ls.default_targets(root)) == sorted([a, b])


def test_main_exit_codes(tmp_path, capsys):
    assert ls.main([skill(tmp_path)]) == 0
    assert ls.main([skill(tmp_path, name="wf-y", body=GOOD_BODY.replace("## 주의 — 자주 틀리는 것", "## 메모"))]) == 1
    assert "K7" in capsys.readouterr().out

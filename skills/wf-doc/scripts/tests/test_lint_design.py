# lint_design.py 검증 — 실행: python -m pytest skills/wf-doc/scripts/tests -q
# 크기 라벨: small. D1~D10마다 위반 견본, 정상 견본, ID 펼침, 표 없음·추적표 없음, 대상 탐색, exit 0/1/2.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lint_design as ld  # noqa: E402

DEPS = """| ID | 의존 | 피의존 | 소유 데이터 | 출처 |
|---|---|---|---|---|
| DES-01 | — | DES-02, DES-03 | 형식 | 확장(templates.md 설계 템플릿) |
| DES-02 | DES-01 | DES-03 | 검사 코드 | 신규 — 설계를 읽는 스크립트 없음 |
| DES-03 | DES-01·02 | — | — | 재사용(SKILL.md) |
"""

TRACE = """## 추적성

| 요구사항 | 설계 | 인수 조건 |
|---|---|---|
| [FR-01](./req.md#기능)·02 | DES-01, DES-02 | AC-01 |
| FR-03 | DES-03 | AC-02 |
| NFR-01 | DES-01~03 | AC-03 |
"""

GOOD = """# 견본

## 기능 요구사항

| ID | 이름 | 내용 |
|---|---|---|
| FR-01 | a | a |
| FR-02 | b | b |
| FR-03 | c | c |

## 비기능 요구사항

| ID | 이름 | 내용 |
|---|---|---|
| NFR-01 | n | n |

## 설계

| ID | 이름 | 내용 |
|---|---|---|
| DES-01 | 형식 | x |
| DES-02 | 린트 | y |
| DES-03 | 본문 | z |

""" + DEPS + "\n" + TRACE


def write(tmp_path, text, rel="req-design.md"):
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return str(p)


def lint(tmp_path, text):
    return ld.lint_design_file(write(tmp_path, text))


def codes(findings, level="E"):
    return sorted(f.code for f in findings if f.level == level)


def test_good_document_has_no_findings(tmp_path):
    assert lint(tmp_path, GOOD) == []


def test_expand_ranges_lists_and_links():
    assert ld.expand("[FR-01](./a.md#x)~03·05, NFR-02") == ["FR-01", "FR-02", "FR-03", "FR-05", "NFR-02"]
    assert ld.expand("DES-01~DES-03, DES-06~08") == ["DES-01", "DES-02", "DES-03", "DES-06", "DES-07", "DES-08"]
    assert ld.expand("—") == []


def test_document_without_dependency_table_is_silent(tmp_path):
    assert lint(tmp_path, GOOD.replace(DEPS, "")) == []


def test_d1_row_not_defined_or_duplicated(tmp_path):
    extra = DEPS + "| DES-04 | — | — | — | 재사용(a) |\n"
    assert "D1" in codes(lint(tmp_path, GOOD.replace(DEPS, extra)))
    dup = DEPS + "| DES-03 | DES-01·02 | — | — | 재사용(SKILL.md) |\n"
    assert "D1" in codes(lint(tmp_path, GOOD.replace(DEPS, dup)))


def test_d2_definition_missing_from_table(tmp_path):
    text = GOOD.replace("| DES-03 | 본문 | z |\n", "| DES-03 | 본문 | z |\n| DES-04 | 추가 | w |\n")
    assert "D2" in codes(lint(tmp_path, text))


def test_d3_undefined_id_in_dependency_cell(tmp_path):
    text = GOOD.replace("| DES-03 | DES-01·02 | — |", "| DES-03 | DES-01·02, DES-07 | — |")
    assert "D3" in codes(lint(tmp_path, text))


def test_d4_asymmetric_pair(tmp_path):
    text = GOOD.replace("| DES-02 | DES-01 | DES-03 |", "| DES-02 | DES-01 | — |")
    fs = lint(tmp_path, text)
    assert codes(fs) == ["D4"]
    assert "DES-03" in fs[0].msg and "DES-02" in fs[0].msg


def test_d5_cycle_reports_path(tmp_path):
    text = GOOD.replace("| DES-01 | — | DES-02, DES-03 |", "| DES-01 | DES-02 | DES-02, DES-03 |") \
               .replace("| DES-02 | DES-01 | DES-03 |", "| DES-02 | DES-01 | DES-01, DES-03 |")
    fs = lint(tmp_path, text)
    assert codes(fs) == ["D5"]
    assert "DES-01 → DES-02 → DES-01" in fs[0].msg


def test_d6_duplicate_owner_but_dash_is_exempt(tmp_path):
    assert "D6" in codes(lint(tmp_path, GOOD.replace("| 검사 코드 |", "| 형식 |")))
    assert lint(tmp_path, GOOD.replace("| 검사 코드 |", "| — |")) == []


def test_d7_source_format(tmp_path):
    for bad in ["—", "", "재사용", "확장 templates.md", "신규"]:
        text = GOOD.replace("| 재사용(SKILL.md) |", "| %s |" % bad)
        assert codes(lint(tmp_path, text)) == ["D7"], bad


def test_d8_trace_row_without_design(tmp_path):
    assert codes(lint(tmp_path, GOOD.replace("| FR-03 | DES-03 | AC-02 |", "| FR-03 | — | AC-02 |"))) == ["D8"]


def test_d8_defined_requirement_missing_from_trace(tmp_path):
    fs = lint(tmp_path, GOOD.replace("| FR-03 | DES-03 | AC-02 |\n", ""))
    assert codes(fs) == ["D8"] and "FR-03" in fs[0].msg


def test_d8_once_and_no_d10_without_trace_table(tmp_path):
    fs = lint(tmp_path, GOOD.replace(TRACE, ""))
    assert codes(fs) == ["D8"]
    assert codes(fs, "W") == []


def test_d9_orphan_and_trace_rescues(tmp_path):
    text = GOOD.replace("| DES-03 | 본문 | z |\n", "| DES-03 | 본문 | z |\n| DES-04 | 고립 | w |\n") \
               .replace(DEPS, DEPS + "| DES-04 | — | — | — | 신규 — 견본 |\n")
    assert codes(lint(tmp_path, text)) == ["D9"]
    assert lint(tmp_path, text.replace("| NFR-01 | DES-01~03 |", "| NFR-01 | DES-01~04 |")) == []


def test_d10_warns_design_missing_from_trace(tmp_path):
    text = GOOD.replace("| FR-03 | DES-03 | AC-02 |", "| FR-03 | DES-01 | AC-02 |") \
               .replace("| NFR-01 | DES-01~03 |", "| NFR-01 | DES-01, DES-02 |")
    fs = lint(tmp_path, text)
    assert codes(fs) == [] and codes(fs, "W") == ["D10"]


def test_bullet_definitions_and_linked_trace(tmp_path):
    text = """# 설계

## 컴포넌트와 책임

- DES-01: **a** — 첫째.
- DES-02 (v3, [ADR-012](./x.md)): **b** — 둘째.

| ID | 의존 | 피의존 | 소유 데이터 | 출처 |
|---|---|---|---|---|
| DES-01 | DES-02 | — | — | 재사용(a.ps1) |
| DES-02 | — | DES-01 | `상태 파일` | 재사용(b.ps1) |

## 추적성

| 요구사항 | 설계 | 작업 |
|---|---|---|
| [FR-01](./requirements.md#기능-요구사항) | DES-01, DES-02 | [TASK-01](./w.md) |
"""
    assert lint(tmp_path, text) == []


def test_default_targets(tmp_path):
    root = str(tmp_path)
    for rel in ["docs/design.md", "docs/work/a/req-design.md", "docs/work/b/design.md", "docs/work/b/plan.md"]:
        write(tmp_path, GOOD, rel)
    rels = sorted(os.path.relpath(p, root).replace(os.sep, "/") for p in ld.default_targets(root))
    assert rels == ["docs/design.md", "docs/work/a/req-design.md", "docs/work/b/design.md"]


def test_main_exit_codes(tmp_path, capsys, monkeypatch):
    assert ld.main([write(tmp_path, GOOD)]) == 0
    assert capsys.readouterr().out == ""
    bad = write(tmp_path, GOOD.replace("| 재사용(SKILL.md) |", "| — |"), "bad.md")
    assert ld.main([bad]) == 1
    assert ": E D7 " in capsys.readouterr().out
    assert ld.main([str(tmp_path / "missing.md")]) == 2
    monkeypatch.setattr(ld, "find_root", lambda start: None)
    assert ld.main([]) == 2

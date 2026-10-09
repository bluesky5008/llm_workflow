# render.py 검증 — 실행: python -m pytest skills/wf-tree/scripts/tests -q
# 크기 라벨: small. 파싱 2 · 중첩 2 · 접기 1 · 뷰 2 · depends 1 · 완료 시점 1 · write 1 · 경고 2 · exit 1.
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import render  # noqa: E402

PLAN = """# PLAN-20260101-sample: 구현 계획 — 견본 계획

> 문서 유형: `plan`
> 작업 ID: `20260101-sample`
> 상태: `in-progress`

## 요약

- 목적: 견본.

## 계획 트리

<!-- generated: 2026-01-01 09:00 — 손 렌더 -->

```text
(옛 트리)
```

## 작업 목록

### TASK-01: 첫 작업

- 상태: completed
- 완료: 2026-01-01 10:00
- 상위: 없음
- 목표: 첫째
- 의존성: 없음

### TASK-02: 둘째 작업

- 상태: completed
- 완료: 2026-01-01 11:00
- 상위: TASK-01
- 의존성: 없음

### TASK-03: 셋째 작업

- 상태: in-progress
- 상위: 없음
- 의존성: TASK-01(링크 대상)

### TASK-04: 넷째 작업

- 상태: pending
- 상위: TASK-03
- 의존성: TASK-02

### TASK-05: 승인: 범위 확정

- 상태: pending
- 상위: 없음
- 의존성: TASK-01~04

## 검증 계획
"""

STATUS = """# ST-sample: 포트폴리오 — 진행 중 작업

> 문서 유형: `status`
> 상태: `in-progress`

## 작업 목록

| 작업 ID | 제목 | 상태 | 계획·기록 | 의존 | 다음 행동 |
|---|---|---|---|---|---|
| 20260101-alpha | 알파 | in-progress | [plan](./a.md) | 없음 | TASK-02 |
| 20260102-beta | 베타 | on-hold | [plan](./b.md) | 20260101-alpha | 재개 조건 |
"""


def write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def lines_of(text):
    return text.rstrip("\n").split("\n")


def find(lines, token):
    return next(l for l in lines if token in l)


# ---- 파싱 ----

def test_parse_plan_items_and_fields(tmp_path):
    doc = render.load(write(tmp_path, "plan.md", PLAN))
    assert doc.kind == "plan"
    assert doc.root_id == "20260101-sample" and doc.title == "견본 계획" and doc.status == "in-progress"
    assert [it.id for it in doc.items] == ["TASK-01", "TASK-02", "TASK-03", "TASK-04", "TASK-05"]
    t2 = doc.items[1]
    assert (t2.title, t2.status, t2.done, t2.parent) == ("둘째 작업", "completed", "2026-01-01 11:00", "TASK-01")
    assert doc.items[2].depends == ["TASK-01"] and doc.items[4].depends == ["TASK-01~04"]


def test_parse_status_rows(tmp_path):
    doc = render.load(write(tmp_path, "status.md", STATUS))
    assert doc.kind == "status" and doc.root_id == "ST-sample" and doc.title == "진행 중 작업"
    assert [(it.id, it.title, it.status, it.depends) for it in doc.items] == [
        ("20260101-alpha", "알파", "in-progress", []),
        ("20260102-beta", "베타", "on-hold", ["20260101-alpha"]),
    ]


# ---- 중첩 ----

def test_nesting_follows_parent_field(tmp_path):
    doc = render.load(write(tmp_path, "plan.md", PLAN))
    lines = lines_of(render.render(doc, view="all"))
    assert lines[0].startswith("[작업] 20260101-sample — 견본 계획")
    assert find(lines, "(TASK-02)").startswith("│   └─ [✓] 둘째 작업 (TASK-02)")
    assert find(lines, "(TASK-04)").startswith("│   └─ [ ] 넷째 작업 (TASK-04)")
    assert find(lines, "(TASK-05)").startswith("└─ [ ] ★ 승인: 범위 확정 (TASK-05)")


def test_orphan_parent_attaches_to_root_with_warning(tmp_path):
    text = PLAN.replace("- 상위: TASK-03\n", "- 상위: TASK-99\n")
    doc = render.load(write(tmp_path, "plan.md", text))
    out = render.render(doc, view="all")
    assert find(lines_of(out), "(TASK-04)").startswith("├─ [ ] 넷째 작업 (TASK-04)")
    assert any("TASK-99" in w and "상위" in w for w in doc.warnings)


# ---- 접기 ----

def test_completed_subtree_folds_in_active_view(tmp_path):
    doc = render.load(write(tmp_path, "plan.md", PLAN))
    active = lines_of(render.render(doc, view="active"))
    full = lines_of(render.render(doc, view="all"))
    assert not any("(TASK-02)" in l for l in active)
    assert re.search(r"\[✓\] 첫 작업 \(TASK-01\) \.+ \(1/1\)  2026-01-01 10:00$", find(active, "(TASK-01)"))
    assert any("(TASK-02)" in l for l in full)


# ---- 뷰 ----

def test_active_view_expands_only_in_progress_path(tmp_path):
    text = PLAN.replace("## 검증 계획", "### TASK-06: 여섯째\n\n- 상태: pending\n- 상위: TASK-05\n- 의존성: 없음\n\n## 검증 계획")
    doc = render.load(write(tmp_path, "plan.md", text))
    active = lines_of(render.render(doc, view="active"))
    assert any("(TASK-04)" in l for l in active)          # 진행 중 TASK-03의 자식은 펼침
    assert not any("(TASK-06)" in l for l in active)      # 대기 중 TASK-05의 자식은 깊이 1 요약
    assert re.search(r"\(TASK-05\) \.+ \(0/1\)  depends: TASK-01~04$", find(active, "(TASK-05)"))


def test_remaining_and_branch_views(tmp_path):
    doc = render.load(write(tmp_path, "plan.md", PLAN))
    remaining = lines_of(render.render(doc, view="remaining"))
    assert not any("(TASK-01)" in l or "(TASK-02)" in l for l in remaining)
    assert any("(TASK-04)" in l for l in remaining)
    branch = lines_of(render.render(doc, view="branch=TASK-03"))
    assert [l for l in branch if "(TASK-" in l] == [find(branch, "(TASK-03)"), find(branch, "(TASK-04)")]


# ---- depends ----

def test_depends_annotation_uses_task_tokens_only(tmp_path):
    doc = render.load(write(tmp_path, "plan.md", PLAN))
    lines = lines_of(render.render(doc, view="all"))
    assert re.search(r"\(TASK-03\) \.+ \(0/1\)  depends: TASK-01$", find(lines, "(TASK-03)"))
    assert find(lines, "(TASK-05)").endswith("depends: TASK-01~04")
    assert "depends" not in find(lines, "(TASK-01)")


# ---- 완료 시점 ----

def test_completion_time_and_root_rollup(tmp_path):
    doc = render.load(write(tmp_path, "plan.md", PLAN))
    lines = lines_of(render.render(doc, view="all"))
    assert re.search(r"in-progress \(2/5\)$", lines[0])
    assert find(lines, "(TASK-02)").endswith("2026-01-01 11:00")
    doc2 = render.load(write(tmp_path, "plan2.md", PLAN.replace("- 완료: 2026-01-01 10:00\n", "")))
    folded = find(lines_of(render.render(doc2, view="active")), "(TASK-01)")
    assert folded.endswith("2026-01-01 11:00")            # 자신의 완료 필드가 없으면 자식 최댓값


# ---- write ----

def test_write_replaces_fence_and_generated_comment(tmp_path):
    path = write(tmp_path, "plan.md", PLAN)
    doc = render.load(path)
    render.write_tree(path, render.render(doc, view="active"), view="active", now="2026-01-02 12:34")
    text = open(path, encoding="utf-8").read()
    assert "(옛 트리)" not in text and "<!-- generated: 2026-01-01" not in text
    assert "<!-- generated: 2026-01-02 12:34 — scripts/render.py --view active -->" in text
    assert text.index("## 계획 트리") < text.index("[작업] 20260101-sample") < text.index("## 작업 목록")
    assert "### TASK-05: 승인: 범위 확정" in text and "## 요약" in text
    tree_section = "## 계획 트리\n\n<!-- generated: 2026-01-01 09:00 — 손 렌더 -->\n\n```text\n(옛 트리)\n```\n\n"
    path2 = write(tmp_path, "plan2.md", PLAN.replace(tree_section, ""))
    render.write_tree(path2, "TREE", view="all", now="2026-01-02 12:34")
    text2 = open(path2, encoding="utf-8").read()
    assert text2.index("## 계획 트리") < text2.index("TREE") < text2.index("## 작업 목록")


# ---- 경고 ----

def test_depth_limit_warning(tmp_path):
    text = PLAN.replace("## 검증 계획", "### TASK-06: 깊은 항목\n\n- 상태: pending\n- 상위: TASK-04\n- 의존성: 없음\n\n## 검증 계획")
    doc = render.load(write(tmp_path, "plan.md", text))
    render.render(doc, view="all", depth=2)
    assert any("TASK-06" in w and "깊이" in w for w in doc.warnings)
    doc2 = render.load(write(tmp_path, "plan2.md", text))
    render.render(doc2, view="all", depth=3)
    assert not any("깊이" in w for w in doc2.warnings)


def test_bad_status_and_cycle_warn_but_render(tmp_path):
    text = PLAN.replace("- 상태: pending\n- 상위: TASK-03\n", "- 상태: done\n- 상위: TASK-03\n")
    text = text.replace("- 상위: 없음\n- 목표: 첫째\n", "- 상위: TASK-02\n- 목표: 첫째\n")  # TASK-01 ↔ TASK-02 순환
    doc = render.load(write(tmp_path, "plan.md", text))
    out = render.render(doc, view="all")
    assert any("상태" in w and "done" in w for w in doc.warnings)
    assert any("순환" in w for w in doc.warnings)
    assert "[ ] 넷째 작업 (TASK-04)" in out and "(TASK-01)" in out and "(TASK-02)" in out


# ---- exit ----

def test_main_exit_codes(tmp_path, capsys):
    assert render.main([str(tmp_path / "none.md")]) == 1
    assert render.main([write(tmp_path, "plan.md", PLAN.replace("## 작업 목록", "## 목록"))]) == 1
    assert render.main([write(tmp_path, "ok.md", PLAN)]) == 0
    assert "[작업] 20260101-sample" in capsys.readouterr().out

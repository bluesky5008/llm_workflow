# render.py 속성 기반 검증 — 실행: python -m pytest skills/wf-tree/scripts/tests -q
# 크기 라벨: small. 파싱 왕복 1 · 트리 구성 1. hypothesis 필요(README 테스트 전제) — 없으면 수집 오류로 드러낸다.
import os
import sys

from hypothesis import given, settings, strategies as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import render  # noqa: E402

DETERMINISTIC = settings(derandomize=True, database=None, deadline=None)

titles = st.text(alphabet="가나다라abc XYZ0123-", min_size=1, max_size=12).map(str.strip).filter(bool)


@st.composite
def plans(draw):
    """(id, title, status, parent) 목록 — parent는 앞선 TASK 또는 None."""
    n = draw(st.integers(min_value=1, max_value=8))
    out = []
    for k in range(1, n + 1):
        parent = draw(st.sampled_from([None] + ["TASK-%02d" % j for j in range(1, k)]))
        out.append(("TASK-%02d" % k, draw(titles), draw(st.sampled_from(sorted(render.STATUSES))), parent))
    return out


def plan_body(tasks):
    lines = []
    for id, title, status, parent in tasks:
        lines += ["### %s: %s" % (id, title), "", "- 상태: %s" % status,
                  "- 상위: %s" % (parent or "없음"), "- 의존성: 없음", ""]
    return lines


@DETERMINISTIC
@given(plans())
def test_parse_preserves_id_title_status_parent(tasks):
    items = render.parse_plan_items(plan_body(tasks))
    assert [(i.id, i.title, i.status, i.parent) for i in items] == tasks


@DETERMINISTIC
@given(st.lists(st.sampled_from(["TASK-%02d" % k for k in range(1, 7)] + [None]), min_size=1, max_size=6))
def test_build_tree_places_every_item_exactly_once(parents):
    # 상위가 없는 대상·순환이어도 모든 항목이 트리에 정확히 한 번 나타나야 한다
    items = [render.Item("TASK-%02d" % k, "t", "pending", parent=p) for k, p in enumerate(parents, 1)]
    doc = render.Doc("plan", "x", "t", "in-progress", items)
    render.build_tree(doc)
    seen = [it.id for r in doc.roots for it in [r] + render.descendants(r)]
    assert sorted(seen) == sorted(it.id for it in items)

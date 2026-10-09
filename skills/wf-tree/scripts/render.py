#!/usr/bin/env python3
"""계획 트리 렌더 — plan.md 또는 status.md의 항목 목록에서 ASCII 트리를 생성한다.

사용: python render.py <plan.md|status.md> [--view all|active|remaining|branch=TASK-NN] [--depth N] [--write]
  plan.md:   `## 작업 목록`의 `### TASK-NN: 제목` 블록과 상태·완료·상위·의존성 필드를 읽는다.
  status.md: `## 작업 목록` 표의 작업 ID·제목·상태·의존 열을 읽는다.
  --view:    기본 active(루트→진행 중 경로만 펼침, 완료 가지 접기). 뷰의 용도는 references/rendering.md.
  --depth:   작업 내부 트리의 분해 상한(기본 2). 초과는 경고하고 그대로 그린다.
  --write:   `## 계획 트리` 절의 첫 코드 펜스와 generated 주석을 교체한다(절이 없으면 `## 작업 목록` 앞에 삽입).
출력: 트리는 stdout, 경고(W)는 stderr, exit 0. 파일·절 없음은 오류(E), exit 1.
스킬이 다른 위치에 설치되었으면 그 경로로 실행한다(예: ~/.claude/skills/wf-tree/scripts/render.py).
표준 라이브러리만 사용한다. 표기의 의미는 references/rendering.md, 생성 시점은 SKILL.md §7을 따른다.
"""
import argparse
import io
import os
import re
import sys
import unicodedata
from datetime import datetime

STATUSES = {"pending", "in-progress", "completed", "blocked",
            "awaiting-approval", "approved", "rejected", "on-hold"}
DONE = {"completed", "approved"}
MARK = {"completed": "✓", "approved": "✓", "in-progress": "▶"}
GATE_RE = re.compile(r"^(승인|릴리스|전환)\s*:")
TASK_RE = re.compile(r"^###\s+(TASK-\d+)\s*:\s*(.*?)\s*$")
FIELD_RE = re.compile(r"^\s*[-*]\s+([^:：]+?)\s*:\s*(.*)$")
HEAD_RE = re.compile(r"^>\s*([^:]+?)\s*:\s*(.*)$")
H1_RE = re.compile(r"^#\s+(?:PLAN-)?(\S+?)\s*:\s*(.*)$")
DEP_PLAN_RE = re.compile(r"TASK-\d+(?:~\d+)?")
DEP_STATUS_RE = re.compile(r"\d{8}-[\w-]+")
GEN_RE = re.compile(r"^\s*<!--\s*generated\b.*-->\s*$")
TREE_H2, LIST_H2 = "## 계획 트리", "## 작업 목록"


class RenderError(Exception):
    pass


class Item:
    def __init__(self, id, title, status, done=None, parent=None, depends=()):
        self.id, self.title, self.status, self.done = id, title, status, done
        self.parent, self.depends, self.children, self.depth = parent, list(depends), [], 1


class Doc:
    def __init__(self, kind, root_id, title, status, items):
        self.kind, self.root_id, self.title, self.status, self.items = kind, root_id, title, status, items
        self.warnings, self.by_id, self.roots = [], {}, []


# ---- 파싱 ----

def read_text(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return f.read()


def plain(value):
    return value.strip().strip("`").strip()


def head_fields(lines):
    fields = {}
    for text in lines:
        if text.startswith("## "):
            break
        m = HEAD_RE.match(text)
        if m:
            fields.setdefault(m.group(1), plain(m.group(2)))
    return fields


def section(lines, h2):
    """H2 절의 (시작 행 번호, 본문 행 목록). 없으면 None."""
    start = next((i for i, t in enumerate(lines) if t.strip() == h2), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, lines[start + 1:end]


def parse_plan_items(body):
    items, fields = [], None
    for text in body:
        m = TASK_RE.match(text)
        if m:
            fields = {}
            items.append((m.group(1), m.group(2), fields))
            continue
        m = FIELD_RE.match(text) if fields is not None else None
        if m and m.group(1) not in fields:
            fields[m.group(1)] = plain(m.group(2))
    out = []
    for id, title, f in items:
        parent = f.get("상위", "")
        out.append(Item(id, title, f.get("상태", "pending"), f.get("완료") or None,
                        parent if parent and parent != "없음" else None,
                        DEP_PLAN_RE.findall(f.get("의존성", ""))))
    return out


def parse_status_items(body):
    rows = [t for t in body if t.strip().startswith("|") and not re.match(r"^\s*\|\s*-", t)]
    if not rows:
        return []
    cells = lambda t: [c.strip() for c in t.strip().strip("|").split("|")]  # noqa: E731
    head = cells(rows[0])
    col = {name: head.index(name) for name in ("작업 ID", "제목", "상태", "의존") if name in head}
    out = []
    for t in rows[1:]:
        c = cells(t)
        get = lambda name: c[col[name]] if name in col and col[name] < len(c) else ""  # noqa: E731
        out.append(Item(get("작업 ID"), get("제목"), plain(get("상태")), depends=DEP_STATUS_RE.findall(get("의존"))))
    return out


def load(path):
    if not os.path.isfile(path):
        raise RenderError("파일 없음: %s" % path)
    lines = read_text(path).replace("\r\n", "\n").split("\n")
    kind = "status" if os.path.basename(path).startswith("status") else "plan"
    head = head_fields(lines)
    h1 = next((t for t in lines if t.startswith("# ")), "")
    m = H1_RE.match(h1)
    root_id = (m.group(1) if m else "") if kind == "status" else head.get("작업 ID") or (m.group(1) if m else "")
    rest = m.group(2) if m else h1[2:]
    title = rest.rsplit(" — ", 1)[-1].strip()
    sec = section(lines, LIST_H2)
    if sec is None:
        raise RenderError("'%s' 절 없음: %s" % (LIST_H2, path))
    items = parse_status_items(sec[1]) if kind == "status" else parse_plan_items(sec[1])
    doc = Doc(kind, root_id, title, head.get("상태", ""), items)
    build_tree(doc)
    return doc


def build_tree(doc):
    doc.by_id = {it.id: it for it in doc.items}
    for it in doc.items:
        if it.status not in STATUSES:
            doc.warnings.append("상태 어휘 오류: %s '%s'" % (it.id, it.status))
        if it.parent and it.parent not in doc.by_id:
            doc.warnings.append("상위 대상 없음: %s → %s (루트 아래로 그림)" % (it.id, it.parent))
            it.parent = None
    for it in doc.items:
        seen, cur = {it.id}, it.parent
        while cur:
            if cur in seen:
                doc.warnings.append("상위 순환: %s (끊고 루트 아래로 그림)" % it.id)
                it.parent = None
                break
            seen.add(cur)
            cur = doc.by_id[cur].parent
    for it in doc.items:
        (doc.by_id[it.parent].children if it.parent else doc.roots).append(it)

    def set_depth(it, d):
        it.depth = d
        for c in it.children:
            set_depth(c, d + 1)
    for r in doc.roots:
        set_depth(r, 1)


# ---- 집계 ----

def descendants(it):
    out = []
    for c in it.children:
        out.append(c)
        out.extend(descendants(c))
    return out


def rollup(items):
    return (sum(1 for d in items if d.status in DONE), len(items), sum(1 for d in items if d.status == "blocked"))


def time_of(it):
    if it.done:
        return it.done
    times = [time_of(c) for c in it.children]
    return max(times) if times and all(times) else None


def has_active(it):
    return it.status == "in-progress" or any(has_active(c) for c in it.children)


# ---- 렌더 ----

def width(s):
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in s)


def annotations(it, items_for_rollup, with_status):
    head = []
    if with_status:
        head.append("(기각)" if it.status == "rejected" else it.status)
    done, total, blocked = rollup(items_for_rollup)
    if items_for_rollup:
        head.append("(%d/%d)" % (done, total))
    parts = [" ".join(head)] if head else []
    if blocked:
        parts.append("⚠ blocked %d" % blocked)
    if it.depends:
        parts.append("depends: " + ", ".join(it.depends))
    if it.status in DONE:
        t = time_of(it)
        if t:
            parts.append(t)
    return "  ".join(parts)


def join_rows(rows):
    """[(indent, left, right)] → 형제 블록 안에서 점선 리더의 열을 맞춘 라인."""
    target = max((width(left) for _, left, right in rows if right), default=0)
    out = []
    for indent, left, right in rows:
        line = indent + left
        if right:
            line += " " + "." * (target - width(left) + 3) + " " + right
        out.append(line)
    return out


def render(doc, view="active", depth=2):
    mode, _, branch = view.partition("=")
    if mode not in ("all", "active", "remaining", "branch"):
        raise RenderError("뷰 옵션 오류: %s" % view)
    for it in doc.items:
        if it.depth > depth:
            doc.warnings.append("깊이 상한 초과: %s (깊이 %d > %d)" % (it.id, it.depth, depth))
    if mode == "branch":
        if branch not in doc.by_id:
            raise RenderError("가지 없음: %s" % branch)
        roots = [doc.by_id[branch]]
    else:
        roots = doc.roots

    def visible(children, it):
        if mode == "all" or mode == "branch":
            return children
        if it is not None and it.status in DONE:
            return []
        if mode == "remaining":
            return [c for c in children if c.status not in DONE]
        return children if it is None or has_active(it) else []

    def left_of(it):
        mark = MARK.get(it.status, " ")
        if doc.kind == "status":
            return "[%s] %s %s" % (mark, it.id, it.title)
        star = "★ " if GATE_RE.match(it.title) else ""
        return "[%s] %s%s (%s)" % (mark, star, it.title, it.id)

    def emit(items, indent):
        rows, out = [], []
        for i, it in enumerate(items):
            conn = "└─ " if i == len(items) - 1 else "├─ "
            plain_status = it.status in {"pending", "in-progress"} | DONE
            rows.append((indent + conn, left_of(it),
                         annotations(it, descendants(it), with_status=doc.kind == "status" or not plain_status)))
        lines = join_rows(rows)
        for i, it in enumerate(items):
            out.append(lines[i])
            out.extend(emit(visible(it.children, it), indent + ("    " if i == len(items) - 1 else "│   ")))
        return out

    label = "[포트폴리오]" if doc.kind == "status" else "[작업]"
    root_left = "%s %s — %s" % (label, doc.root_id, doc.title)
    root_right = (doc.status if doc.kind == "status"
                  else annotations(Item("", "", doc.status), doc.items, with_status=True))
    lines = join_rows([("", root_left, root_right)])
    lines.extend(emit(visible(roots, None), ""))
    return "\n".join(lines) + "\n"


# ---- 쓰기 ----

def write_tree(path, tree, view="active", now=None):
    now = now or datetime.now().strftime("%Y-%m-%d %H:%M")
    raw = read_text(path)
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.replace("\r\n", "\n").split("\n")
    comment = "<!-- generated: %s — scripts/render.py --view %s -->" % (now, view)
    fence = ["```text"] + tree.rstrip("\n").split("\n") + ["```"]
    sec = section(lines, TREE_H2)
    if sec is None:
        at = next((i for i, t in enumerate(lines) if t.strip() == LIST_H2), len(lines))
        lines[at:at] = [TREE_H2, "", comment, ""] + fence + [""]
    else:
        start, body = sec
        span = len(body)
        gen = next((i for i, t in enumerate(body) if GEN_RE.match(t)), None)
        if gen is not None:
            body[gen] = comment
        opens = [i for i, t in enumerate(body) if t.lstrip().startswith("```")]
        if len(opens) >= 2:
            body[opens[0]:opens[1] + 1] = fence
        else:
            while body and not body[-1].strip():
                body.pop()
            body += [""] + fence + [""]
        if gen is None:
            body[0:0] = ["", comment]
        lines[start + 1:start + 1 + span] = body
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(nl.join(lines))


# ---- 실행 ----

def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description="계획 트리 렌더 (wf-tree)")
    ap.add_argument("path")
    ap.add_argument("--view", default="active")
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)
    try:
        doc = load(args.path)
        tree = render(doc, view=args.view, depth=args.depth)
        if args.write:
            write_tree(args.path, tree, view=args.view)
    except RenderError as e:
        print("E %s" % e, file=sys.stderr)
        return 1
    for w in doc.warnings:
        print("W %s" % w, file=sys.stderr)
    sys.stdout.write(tree)
    return 0


if __name__ == "__main__":
    sys.exit(main())

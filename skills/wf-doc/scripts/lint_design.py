#!/usr/bin/env python3
"""설계 문서 린트 — 컴포넌트 의존 표(ADR-021)를 검사한다.

사용: python lint_design.py [설계 문서 ...]
  인자 없음: 현재 디렉터리(없으면 상위 3단계까지)에서 docs/를 찾아 docs/design.md와
             docs/work/*/req-design.md·design.md를 검사한다.
  의존 표(헤더 `| ID | 의존 | 피의존 | 소유 데이터 | 출처 |`)가 없는 문서는 검사하지 않는다(무출력).
검사: D1 의존 표 ID가 DES 정의에 없음·중복, D2 DES 정의가 의존 표에 없음, D3 `의존`·`피의존`의 미정의 ID,
      D4 비대칭, D5 순환, D6 `—`가 아닌 소유 데이터 중복, D7 출처 형식, D8 추적표 GAP(설계 칸이 빈 행,
      추적표에 없는 정의된 FR·NFR, 추적표 없음), D9 고아, D10(경고) 추적표에 없는 DES.
출력: 경로:행: E|W Dn 메시지. 오류(E)가 1건 이상이면 exit 1, 루트 미발견·경로 없음·읽기 실패는 exit 2.
표준 라이브러리만 사용한다. 형식은 wf-doc templates.md 설계 템플릿, 결정은 ADR-021을 따른다.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_worklog import Finding, find_root, outside_fences, read_lines, section  # noqa: E402

DEPS_HEADER = ["ID", "의존", "피의존", "소유 데이터", "출처"]
LINK_TEXT_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
ID_RE = re.compile(r"\b(NFR|FR|DES)-(\d+)((?:\s*[~·]\s*(?:(?:NFR|FR|DES)-)?\d+)*)")
TAIL_RE = re.compile(r"([~·])\s*(?:(?:NFR|FR|DES)-)?(\d+)")
DEF_BULLET_RE = re.compile(r"^\s*[-*]\s+(DES-\d+)\b")
SOURCE_RE = re.compile(r"^(?:재사용\(.+\)|확장\(.+\)|신규 — .+)$")
EMPTY = "—"


def expand(cell):
    """셀의 FR·NFR·DES ID를 펼친다 — 범위 `~`, 나열 `·`, 링크 텍스트."""
    out = []
    for m in ID_RE.finditer(LINK_TEXT_RE.sub(r"\1", cell)):
        kind, cur = m.group(1), int(m.group(2))
        nums = [cur]
        for sep, num in TAIL_RE.findall(m.group(3)):
            n = int(num)
            nums.extend(range(cur + 1, n + 1) if sep == "~" else [n])
            cur = n
        out.extend("%s-%02d" % (kind, n) for n in nums)
    return out


def cells(text):
    return [c.strip() for c in text.strip().strip("|").split("|")]


def tables(nf):
    """펜스 밖 표 → [(헤더 셀, [(행, 셀)])]. 구분 행은 건너뛴다."""
    out, cur, prev = [], None, None
    for i, text in nf:
        if text.lstrip().startswith("|"):
            if cur is None or prev != i - 1:
                cur = (cells(text), [])
                out.append(cur)
            elif not re.match(r"^\s*\|[\s:|-]+\|\s*$", text):
                cur[1].append((i, cells(text)))
            prev = i
        else:
            cur = None
    return out


def lint_design_file(path):
    nf, _ = outside_fences(read_lines(path))
    all_tables = tables(nf)
    deps_tables = [t for t in all_tables if t[0] == DEPS_HEADER]
    if not deps_tables:
        return []
    trace_tables = tables(section(nf, "추적성"))
    trace = trace_tables[0] if trace_tables else None
    F = []

    def err(line, code, msg, level="E"):
        F.append(Finding(path, line, level, code, msg))

    # 정의: 의존 표·추적표가 아닌 표의 첫 칸, `- DES-NN` 불릿 머리
    defs, reqs = {}, {}
    for header, rows in all_tables:
        if header == DEPS_HEADER or (trace and header == trace[0] and rows == trace[1]):
            continue
        for i, row in rows:
            key = row[0].strip("`*")
            if re.fullmatch(r"DES-\d+", key):
                defs.setdefault(key, i)
            elif re.fullmatch(r"N?FR-\d+", key):
                reqs.setdefault(key, i)
    for i, text in nf:
        m = DEF_BULLET_RE.match(text)
        if m:
            defs.setdefault(m.group(1), i)

    # 의존 표 행
    rows = {}
    for _, body in deps_tables:
        for i, row in body:
            row = (row + [""] * 5)[:5]
            rid = row[0].strip("`*")
            if rid not in defs:
                err(i, "D1", "의존 표 ID %s가 DES 정의에 없음" % rid)
                continue
            if rid in rows:
                err(i, "D1", "의존 표 ID %s 중복" % rid)
                continue
            rows[rid] = (i, expand(row[1]), expand(row[2]), row[3], row[4])
    for d, i in sorted(defs.items()):
        if d not in rows:
            err(i, "D2", "DES 정의 %s가 의존 표에 없음" % d)

    owners = {}
    for rid, (i, deps, rdeps, owner, source) in rows.items():
        for x in deps + rdeps:
            if x not in defs:
                err(i, "D3", "%s의 의존·피의존 %s가 정의에 없음" % (rid, x))
        for x in deps:
            if x in rows and rid not in rows[x][2]:
                err(i, "D4", "%s의 의존에 %s가 있으나 %s의 피의존에 %s가 없음" % (rid, x, x, rid))
        for x in rdeps:
            if x in rows and rid not in rows[x][1]:
                err(i, "D4", "%s의 피의존에 %s가 있으나 %s의 의존에 %s가 없음" % (rid, x, x, rid))
        if owner not in ("", EMPTY):
            if owner in owners:
                err(i, "D6", "소유 데이터 %s를 %s와 %s가 함께 소유" % (owner, owners[owner], rid))
            owners.setdefault(owner, rid)
        if not SOURCE_RE.match(source):
            err(i, "D7", "%s의 출처 `%s`가 재사용(<위치>)·확장(<위치>)·신규 — <이유> 형식이 아님" % (rid, source))

    # D5 순환 — 의존 방향 DFS, 뒤로 가는 간선마다 경로를 보고
    state, stack = {}, []

    def visit(n):
        state[n] = 1
        stack.append(n)
        for x in rows[n][1]:
            if x not in rows:
                continue
            if state.get(x) == 1:
                cyc = stack[stack.index(x):] + [x]
                err(rows[cyc[0]][0], "D5", "순환 %s" % " → ".join(cyc))
            elif x not in state:
                visit(x)
        stack.pop()
        state[n] = 2

    for n in sorted(rows):
        if n not in state:
            visit(n)

    # D8 GAP·D9 고아·D10 추적
    traced = None
    if trace is None:
        err(1, "D8", "`## 추적성` 표가 없음 — 요구사항→설계 GAP을 판정할 수 없음")
    else:
        header, body = trace
        if "요구사항" not in header or "설계" not in header:
            err(body[0][0] if body else 1, "D8", "추적표에 `요구사항`·`설계` 열이 없음")
        else:
            ri, di = header.index("요구사항"), header.index("설계")
            traced, traced_reqs = set(), set()
            for i, row in body:
                row = row + [""] * len(header)
                designs = [x for x in expand(row[di]) if x.startswith("DES-")]
                if not designs:
                    err(i, "D8", "추적표 행 `%s`의 설계 칸에 DES가 없음" % row[ri])
                traced.update(designs)
                traced_reqs.update(expand(row[ri]))
            for r, i in sorted(reqs.items()):
                if r not in traced_reqs:
                    err(i, "D8", "%s가 추적표에 없음" % r)
    for rid, (i, deps, rdeps, _, _) in sorted(rows.items()):
        if not deps and not rdeps and (traced is None or rid not in traced):
            err(i, "D9", "%s가 의존·피의존이 모두 없고 추적표에도 없는 고아" % rid)
    if traced is not None:
        for d, i in sorted(defs.items()):
            if d not in traced:
                err(i, "D10", "%s가 추적표 설계 칸에 없음" % d, "W")
    return F


# ---- 대상 선택과 실행 ----

def default_targets(root):
    docs = os.path.join(root, "docs")
    targets = [os.path.join(docs, "design.md")] if os.path.isfile(os.path.join(docs, "design.md")) else []
    for name in ("req-design.md", "design.md"):
        targets.extend(glob.glob(os.path.join(docs, "work", "*", name)))
    return sorted(targets)


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        paths = argv
    else:
        root = find_root(os.getcwd())
        if root is None:
            print("docs/ 디렉터리를 찾지 못함(현재 디렉터리와 상위 3단계)", file=sys.stderr)
            return 2
        paths = default_targets(root)
    findings = []
    for p in paths:
        try:
            findings.extend(lint_design_file(p))
        except (OSError, UnicodeDecodeError) as e:
            print("%s: 읽을 수 없음 — %s" % (p, e), file=sys.stderr)
            return 2
    for f in sorted(findings, key=lambda f: (f.path, f.line, f.code)):
        try:
            rel = os.path.relpath(f.path)
        except ValueError:
            rel = f.path
        print("%s:%d: %s %s %s" % (rel, f.line, f.level, f.code, f.msg))
    errors = sum(1 for f in findings if f.level == "E")
    print("검사 %d파일, 오류 %d, 경고 %d" % (len(paths), errors, len(findings) - errors), file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

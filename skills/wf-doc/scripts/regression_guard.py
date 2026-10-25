#!/usr/bin/env python3
"""회귀 보호 판정 — 테스트 대장 `유지` 행의 테스트 파일·대장 축소가 기록 없이 바뀌었는지 본다.

사용: python regression_guard.py [저장소 루트]   (인자 없으면 현재 디렉터리)
  (a) `유지` 행의 테스트 파일이 그 행의 마지막 성공 SHA 이후(커밋+워킹트리) 바뀜
  (b) HEAD 대장의 `유지` 행이 워킹트리 대장에서 `유지` 아님·삭제·`테스트 파일` 값 변경
  위반 행 ID가 열린 작업 기록의 `### 테스트 대장 변경` 절에 있으면 통과한다.
출력: `TST-NN: <사유> <파일>` 행. 위반 있으면 exit 1, 내부 오류 exit 2, 그 밖은 무출력 exit 0.
docs/test-register.md가 없으면 무출력 exit 0. 테스트는 실행하지 않는다.
표준 라이브러리와 git만 사용한다. 판독 규칙은 REQ-DESIGN-regression-guard DES-08을 따르며
견본 tests/fixtures/test-register.sample.md를 setup/hooks/wf-test-guard.ps1과 공유한다.
"""
import fnmatch
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lint_worklog as lw  # noqa: E402

REGISTER = "docs/test-register.md"
SHA_RE = re.compile(r"· ([0-9a-f]{7,40})(?:\+dirty)?$")
ID_RE = re.compile(r"\bTST-\d+\b")
CHANGE_SECTION = "### 테스트 대장 변경"


class ParseError(Exception):
    pass


def norm(path):
    return path.strip().replace("\\", "/").lower()


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def parse_register(text):
    """`## 대장` 아래 첫 표 → {ID: (상태, 테스트 파일 glob 목록 | 열 없으면 None, 마지막 성공)}."""
    nf, _ = lw.outside_fences(text.replace("\r\n", "\n").split("\n"))
    inside, table = False, []
    for _, t in nf:
        if t.startswith("## "):
            if table:
                break
            inside = t[3:].strip() == "대장"
        elif inside and t.startswith("|"):
            table.append(t)
        elif table:
            break
    if len(table) < 2:
        raise ParseError("`## 대장` 표를 찾지 못함")
    head = cells(table[0])

    def col(name):
        return next((i for i, h in enumerate(head) if h.startswith(name)), None)

    fi, si, li = col("테스트 파일"), col("상태"), col("마지막 성공")
    if si is None or li is None:
        raise ParseError("대장 표에 `상태`·`마지막 성공` 열이 없음")
    rows = {}
    for t in table[2:]:
        c = cells(t)
        if len(c) != len(head):
            raise ParseError("열 수가 헤더와 다른 행: %s" % c[0])
        files = None if fi is None else [norm(g) for g in c[fi].split(";") if g.strip()]
        rows[c[0]] = (c[si], files, c[li])
    return rows


def kept(state):
    return state.startswith("유지")


def protecting(rows, path):
    """경로를 보호하는 `유지` 행 ID 목록."""
    p = norm(path)
    return sorted(rid for rid, (st, files, _) in rows.items()
                  if kept(st) and any(fnmatch.fnmatchcase(p, g) for g in files or []))


def git(root, *args):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def violations(root):
    """(행 ID, 사유, 파일) 목록. 대장이 없으면 빈 목록."""
    path = os.path.join(root, REGISTER)
    if not os.path.isfile(path):
        return []
    with io.open(path, encoding="utf-8-sig") as f:
        rows = parse_register(f.read())
    out, by_sha = [], {}
    for rid, (st, files, last) in rows.items():
        m = SHA_RE.search(last)
        if kept(st) and files and m:
            by_sha.setdefault(m.group(1), []).append(rid)
    for sha, rids in sorted(by_sha.items()):
        code, text = git(root, "diff", "--name-only", "--relative", "-z", sha)
        if code:
            raise RuntimeError("git diff %s 실패" % sha)
        for p in filter(None, text.split("\0")):
            out += [(rid, "테스트 파일 변경", p) for rid in protecting(rows, p) if rid in rids]
    code, text = git(root, "show", "HEAD:./" + REGISTER)
    if code == 0:
        for rid, (st, files, _) in parse_register(text).items():
            cur = rows.get(rid)
            if not kept(st):
                continue
            if cur is None:
                why = "삭제"
            elif not kept(cur[0]):
                why = "상태 변경(%s)" % cur[0]
            elif files is not None and cur[1] != files:
                why = "테스트 파일 변경"
            else:
                continue
            out.append((rid, "대장 " + why, REGISTER))
    return out


def recorded_ids(root):
    """열린 작업 기록의 `### 테스트 대장 변경` 절에 나오는 행 ID 집합."""
    ids = set()
    for log in lw.worklogs_under(root):
        if lw.worklog_state(log) in lw.CLOSED:
            continue
        nf, _ = lw.outside_fences(lw.read_lines(log))
        inside = False
        for _, t in nf:
            if re.match(r"^#{1,3}\s", t):
                inside = t.strip() == CHANGE_SECTION
            elif inside:
                ids.update(ID_RE.findall(t))
    return ids


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    argv = sys.argv[1:] if argv is None else argv
    root = os.path.abspath(argv[0] if argv else os.getcwd())
    try:
        found = violations(root)
        ids = recorded_ids(root) if found else set()
    except Exception as e:  # 판정 불가는 래퍼가 통과시킨다(DES-04 exit 2)
        print("regression_guard: %s" % e, file=sys.stderr)
        return 2
    bad = [v for v in found if v[0] not in ids]
    for v in bad:
        print("%s: %s %s" % v)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

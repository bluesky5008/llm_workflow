#!/usr/bin/env python3
"""회귀 보호 판정 — 테스트 대장 `유지` 행의 테스트 파일·대장 축소가 기록 없이 바뀌었는지 본다.

사용: python regression_guard.py [저장소 루트]   (인자 없으면 현재 디렉터리)
  (a) `유지` 행의 테스트 파일이 그 행의 마지막 성공 SHA 이후(커밋+워킹트리+미추적, 이름 변경 감지 끔)
      기존 줄을 잃었거나(삭제·변경) 비활성화 패턴(test-disable-patterns.txt)에 맞는 줄을 얻음.
      기존 줄을 모두 두고 줄만 더한 순수 추가는 위반이 아니다.
  (b) HEAD 대장의 `유지` 행이 워킹트리 대장에서 `유지` 아님·삭제·`테스트 파일` 값 변경
  해소: 열린 작업 기록 `### 테스트 대장 변경` 절의 한 줄에 (a)는 행 ID와 지문이, (b)는 행 ID가 있으면 통과.
출력: `TST-NN: <사유> <파일> [<지문>]` 행((b)의 지문은 `-`). 위반 있으면 exit 1, 내부 오류 exit 2, 그 밖은 무출력 exit 0.
docs/test-register.md가 없으면 무출력 exit 0. 테스트는 실행하지 않는다.
표준 라이브러리와 git만 사용한다. 판독 규칙은 REQ-DESIGN-regression-guard DES-08, 내용 판정·지문·해소는
REQ-DESIGN-hook-friction DES-01·02를 따른다. 견본 tests/fixtures/의 대장·패턴 표본을 setup/hooks/와 공유한다.
"""
import fnmatch
import hashlib
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lint_worklog as lw  # noqa: E402

REGISTER = "docs/test-register.md"
PATTERNS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test-disable-patterns.txt")
SHA_RE = re.compile(r"· ([0-9a-f]{7,40})(?:\+dirty)?$")
ID_RE = re.compile(r"\bTST-\d+\b")
PRINT_RE = re.compile(r"\b(?:[0-9a-f]{8}|bin)\b")
CHANGE_SECTION = "### 테스트 대장 변경"
SHRINK = "-"
BATCH = 50  # git diff 한 번에 넘기는 파일 수(명령줄 길이 상한 안)


class ParseError(Exception):
    pass


def norm(path):
    return path.strip().replace("\\", "/").lower()


def cells(row):
    """표 행의 칸. GFM처럼 `\\|`는 칸 경계가 아니라 칸 내용(`|`)이다(wf-common.ps1 Split-WfRow와 같은 규칙)."""
    t = re.sub(r"(?<!\\)\|+$", "", re.sub(r"^\|+", "", row.strip()))
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", t)]


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


def git_list(root, *args):
    code, text = git(root, *args)
    if code:
        raise RuntimeError("git %s 실패" % " ".join(args[:2]))
    return [p for p in text.split("\0") if p]


def load_patterns(path=None):
    """비활성화 패턴(한 줄에 정규식 하나, `#` 주석·빈 줄 무시). 파일이 없으면 OSError — 내부 오류(exit 2)."""
    with io.open(path or PATTERNS, encoding="utf-8-sig") as f:
        lines = [t.strip() for t in f.read().splitlines()]
    return [re.compile(t, re.IGNORECASE) for t in lines if t and not t.startswith("#")]


def disabling(line, patterns):
    return any(p.search(line) for p in patterns)


def fingerprint(hits):
    """위반 줄(`-`·`+` 접두 포함, 나온 순서) → 지문 8자. 위반 줄이 없으면 None(순수 추가)."""
    return hashlib.sha1("\n".join(hits).encode("utf-8")).hexdigest()[:8] if hits else None


def judge_diff(text, patterns):
    """`git diff --unified=0` 한 파일 → 지문 또는 None. 첫 `@@` 앞은 위치로 헤더로 본다."""
    lines = text.split("\n")
    start = next((i for i, t in enumerate(lines) if t.startswith("@@")), len(lines))
    if any(t.startswith("Binary files") for t in lines[:start]):
        return "bin"
    return fingerprint([t for t in lines[start:]
                        if t.startswith("-") or (t.startswith("+") and disabling(t[1:], patterns))])


def file_diff(root, sha, *paths):
    """보호 파일의 diff. 사용자 git 설정(외부 diff·textconv·접두사·경로 인용)이 출력 형식을 바꿔 위반을 가리지 않게 한다."""
    return git(root, "-c", "core.quotePath=false", "diff", "--no-renames", "--no-ext-diff", "--no-textconv",
               "--unified=0", "--no-color", "--src-prefix=a/", "--dst-prefix=b/", "--relative", sha, "--",
               *[":(literal)" + p for p in paths])


def file_diffs(root, sha, paths):
    """{경로: diff}. 프로세스 기동을 줄이려고 묶어 부르고 `diff --git` 머리줄로 나눈다(내용 줄은 접두 문자가 있어 겹치지 않음).
    머리줄이 맞지 않는 경로(인용된 이름 등)와 실패한 묶음은 빠지며 부른 쪽이 파일 하나로 다시 부른다."""
    found, heads = {}, {"diff --git a/%s b/%s" % (p, p): p for p in paths}
    for i in range(0, len(paths), BATCH):
        code, text = file_diff(root, sha, *paths[i:i + BATCH])
        cur = None
        for t in [] if code else text.split("\n"):
            if t.startswith("diff --git "):
                cur = heads.get(t)
            if cur:
                found.setdefault(cur, []).append(t)
    return {p: "\n".join(ts) for p, ts in found.items()}


def judge_new_file(path, patterns):
    """미추적 파일 — 전 줄을 추가 줄로 본다. NUL 바이트가 있으면 이진(위반)."""
    with open(path, "rb") as f:
        data = f.read()
    if b"\0" in data:
        return "bin"
    text = data.decode("utf-8", "replace").replace("\r\n", "\n")
    return fingerprint(["+" + t for t in text.split("\n") if disabling(t, patterns)])


def violations(root):
    """(행 ID, 사유, 파일, 지문) 목록. 대장이 없으면 빈 목록."""
    path = os.path.join(root, REGISTER)
    if not os.path.isfile(path):
        return []
    patterns = load_patterns()
    with io.open(path, encoding="utf-8-sig") as f:
        rows = parse_register(f.read())
    out, by_sha = [], {}
    for rid, (st, files, last) in rows.items():
        m = SHA_RE.search(last)
        if kept(st) and files and m:
            by_sha.setdefault(m.group(1), []).append(rid)
    untracked = git_list(root, "ls-files", "--others", "--exclude-standard", "-z") if by_sha else []
    for sha, rids in sorted(by_sha.items()):
        changed = git_list(root, "diff", "--no-renames", "--name-only", "--relative", "-z", sha)
        ids_of = {p: [rid for rid in protecting(rows, p) if rid in rids] for p in changed + untracked}
        diffs = file_diffs(root, sha, [p for p in changed if ids_of[p]])
        # SHA에서 추적되던 파일이 지금 미추적이면 양쪽에 든다 — 추적분은 삭제로, 미추적분은 새 파일로 각각 판정한다.
        for p, new in [(p, False) for p in changed] + [(p, True) for p in untracked]:
            ids = ids_of[p]
            if not ids:
                continue
            if new:
                fp = judge_new_file(os.path.join(root, p), patterns)
            else:
                code, text = (0, diffs[p]) if p in diffs else file_diff(root, sha, p)
                fp = "bin" if code else judge_diff(text, patterns)
            if fp:
                out += [(rid, "테스트 파일 변경", p, fp) for rid in ids]
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
            out.append((rid, "대장 " + why, REGISTER, SHRINK))
    return out


def recorded(root):
    """열린 작업 기록의 `### 테스트 대장 변경` 절에서 행 ID가 있는 줄마다 (행 ID 집합, 지문 토큰 집합)."""
    found = []
    for log in lw.worklogs_under(root):
        if lw.worklog_state(log) in lw.CLOSED:
            continue
        nf, _ = lw.outside_fences(lw.read_lines(log))
        inside = False
        for _, t in nf:
            if re.match(r"^#{1,3}\s", t):
                inside = t.strip() == CHANGE_SECTION
            elif inside and ID_RE.search(t):
                found.append((set(ID_RE.findall(t)), set(PRINT_RE.findall(t))))
    return found


def resolved(violation, rec):
    """대장 축소는 행 ID만, 테스트 파일 변경은 같은 줄의 행 ID + 지문으로 해소된다."""
    rid, _, _, fp = violation
    return any(rid in ids and (fp == SHRINK or fp in prints) for ids, prints in rec)


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    argv = sys.argv[1:] if argv is None else argv
    root = os.path.abspath(argv[0] if argv else os.getcwd())
    try:
        found = violations(root)
        rec = recorded(root) if found else []
    except Exception as e:  # 판정 불가는 래퍼가 통과시킨다(DES-04 exit 2)
        print("regression_guard: %s" % e, file=sys.stderr)
        return 2
    bad = [v for v in found if not resolved(v, rec)]
    for v in bad:
        print("%s: %s %s [%s]" % v)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

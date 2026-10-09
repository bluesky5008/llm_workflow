#!/usr/bin/env python3
"""작업 기록 린트 — 열린 docs/work/*/work-log.md와 docs/status.md를 검사한다.

사용: python lint_worklog.py [경로 ...]
  인자 없음: 현재 디렉터리(없으면 상위 3단계까지)에서 docs/를 찾아, 닫힘 상태가 아닌
            작업 기록 전부와 docs/status.md를 검사한다.
  인자 있음: 지정한 파일만 검사한다(파일명이 status.md면 포트폴리오 검사).
출력: 경로:행: E|W Lx 메시지. 오류(E)가 1건 이상이면 exit 1.
스킬이 다른 위치에 설치되었으면 그 경로로 실행한다(예: ~/.claude/skills/wf-doc/scripts/lint_worklog.py).
표준 라이브러리만 사용하며 네트워크를 쓰지 않는다. 검사 항목과 교정 방법은
wf-doc references/worklog-style.md, 실행 시점은 wf-implement §7을 따른다.
"""
import glob
import io
import os
import re
import sys
from collections import namedtuple
from urllib.parse import unquote

# ---- 상한과 어휘(초깃값: 2026-10-09 측정값. 두 사이클 운용 후 조정 가능) ----
MAX_ENTRY_LINES = 8          # 수행 기록 항목 하나의 비어 있지 않은 행 수
MAX_ENTRY_CHARS = 600        # 수행 기록 항목 하나의 글자 수(행 길이 합)
MAX_BULLET_CHARS = 300       # 불릿 한 줄의 글자 수
WARN_FILE_BYTES = 12 * 1024  # 초과 시 경고

STATUSES = {"draft", "proposed", "awaiting-approval", "approved", "in-progress", "on-hold",
            "blocked", "completed", "rejected", "withdrawn", "superseded"}
# 기본 검사 대상에서 제외하는 닫힘 상태. 훅(setup/hooks/wf-common.ps1)의 목록과 같다.
CLOSED = {"completed", "superseded", "rejected", "withdrawn", "on-hold"}
# docs/status.md에 행이 남아 있으면 안 되는 상태(on-hold는 포트폴리오에 남는다).
FINAL = CLOSED - {"on-hold"}

HEAD_FIELDS = ["문서 유형", "작업 ID", "상태", "기준선", "작성일", "최종 갱신", "관련 문서"]
H2_ORDER = ["요약", "문서 연결", "기준선과 현재 계획", "수행 기록", "설계와 달라진 점",
            "검증 결과", "완료 보고", "인계"]
ENTRY_REQUIRED = ["결정과 이유", "검증", "결과"]
HANDOFF_OPEN = ["다음 단계 또는 워크플로우", "시작 조건", "입력 문서와 기준선", "완료된 항목",
                "미완료 항목", "차단 요인", "다음 행동"]
RESUME_RE = re.compile(r'^작업 (\S+) 재개 — (\S+)의 인계 절을 읽고 "다음 행동"부터 진행하라\.$')

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)[^)]*\)")
FIELD_RE = re.compile(r"^\s*[-*]\s+([^:：]+?)\s*:\s*(.*)$")
HEAD_RE = re.compile(r"^>\s*([^:]+?)\s*:\s*(.*)$")
ROW_RE = re.compile(r"^\|\s*(\d{8}-[\w-]+)\s*\|")

Finding = namedtuple("Finding", "path line level code msg")


# ---- 파서 ----

def read_lines(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return f.read().replace("\r\n", "\n").split("\n")


def outside_fences(lines):
    """펜스 밖의 (행 번호, 텍스트) 목록과 펜스 시작 행 번호 목록."""
    out, fences, inside = [], [], False
    for i, text in enumerate(lines, 1):
        if text.lstrip().startswith("```"):
            if not inside:
                fences.append(i)
            inside = not inside
            continue
        if not inside:
            out.append((i, text))
    return out, fences


def head_fields(lines):
    """선두 블록쿼트의 `> 이름: 값` 필드 → {이름: (값, 행)}. 본문 첫 H2 전까지만 본다."""
    fields = {}
    for i, text in enumerate(lines, 1):
        if text.startswith("## "):
            break
        m = HEAD_RE.match(text)
        if m:
            fields.setdefault(m.group(1), (m.group(2).strip(), i))
    return fields


def plain(value):
    return value.strip().strip("`").strip()


def headings(nf):
    out = []
    for i, text in nf:
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", text)
        if m:
            out.append((len(m.group(1)), m.group(2).strip(), i))
    return out


def slug(title):
    """GitHub 제목 앵커: 소문자, 문자·숫자·공백·하이픈만 남기고 공백은 하이픈."""
    s = title.replace("`", "").strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s", "-", s)


def anchors_of(path):
    nf, _ = outside_fences(read_lines(path))
    seen, out = {}, set()
    for _, title, _ in headings(nf):
        s = slug(title)
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(s if n == 0 else "%s-%d" % (s, n))
    return out


def fields_in(block):
    """불릿 필드 `- 이름: 값` → {이름: 값} (첫 번째 값만)."""
    out = {}
    for _, text in block:
        m = FIELD_RE.match(text)
        if m and m.group(1) not in out:
            out[m.group(1)] = m.group(2)
    return out


def section(nf, h2_title):
    """H2 제목이 h2_title인 절의 본문 (행, 텍스트) 목록(다음 H2 전까지)."""
    out, inside = [], False
    for i, text in nf:
        if text.startswith("## "):
            inside = text[3:].strip() == h2_title
            continue
        if inside:
            out.append((i, text))
    return out


# ---- 작업 기록 검사 ----

def lint_worklog_file(path, root=None):
    F = []
    lines = read_lines(path)
    nf, fences = outside_fences(lines)
    E = lambda line, code, msg: F.append(Finding(path, line, "E", code, msg))  # noqa: E731

    # L1 머리말
    head = head_fields(lines)
    for name in HEAD_FIELDS:
        if name not in head:
            E(1, "L1", "머리말 필드 없음: %s" % name)
    state = plain(head["상태"][0]) if "상태" in head else ""
    if "상태" in head and state not in STATUSES:
        E(head["상태"][1], "L1", "알 수 없는 상태값: %s" % state)
    if "문서 유형" in head and "work-log" not in head["문서 유형"][0]:
        E(head["문서 유형"][1], "L1", "문서 유형에 work-log가 없음")
    work_id = plain(head["작업 ID"][0]) if "작업 ID" in head else ""

    # L2 H2 목록·순서·중복
    h2 = [(t, i) for lvl, t, i in headings(nf) if lvl == 2]
    titles = [t for t, _ in h2]
    if titles != H2_ORDER:
        seen = set()
        for t, i in h2:
            if t not in H2_ORDER:
                E(i, "L2", "합본 템플릿에 없는 절: %s" % t)
            elif t in seen:
                E(i, "L2", "절 중복: %s" % t)
            seen.add(t)
        for t in H2_ORDER:
            if t not in titles:
                E(1, "L2", "필수 절 없음: %s" % t)
        kept = list(dict.fromkeys(t for t in titles if t in H2_ORDER))
        if kept != [t for t in H2_ORDER if t in kept]:
            E(h2[0][1] if h2 else 1, "L2", "절 순서가 합본 템플릿과 다름: %s" % " → ".join(kept))

    # L3 수행 기록 항목
    body = section(nf, "수행 기록")
    entries, cur = [], None
    for i, text in body:
        if text.startswith("### "):
            cur = (i, text[4:].strip(), [])
            entries.append(cur)
        elif cur is not None and text.strip():
            cur[2].append((i, text))
    for i, title, block in entries:
        got = fields_in(block)
        for name in ENTRY_REQUIRED:
            if name not in got:
                E(i, "L3", "수행 기록 항목 '%s'에 필수 필드 없음: %s" % (title, name))
        if len(block) > MAX_ENTRY_LINES:
            E(i, "L3", "수행 기록 항목 '%s' %d행 (상한 %d)" % (title, len(block), MAX_ENTRY_LINES))
        chars = sum(len(t) for _, t in block)
        if chars > MAX_ENTRY_CHARS:
            E(i, "L3", "수행 기록 항목 '%s' %d자 (상한 %d)" % (title, chars, MAX_ENTRY_CHARS))

    # L4 펜스
    for i in fences:
        E(i, "L4", "펜스 코드블록 — 명령·경로는 인라인 코드, 긴 출력은 요약과 원본 위치")

    # L5 불릿 길이
    for i, text in nf:
        if re.match(r"^\s*[-*]\s", text) and len(text) > MAX_BULLET_CHARS:
            E(i, "L5", "불릿 %d자 (상한 %d)" % (len(text), MAX_BULLET_CHARS))

    # L6 로컬 링크·앵커
    base = os.path.dirname(os.path.abspath(path))
    cache = {}
    for i, text in nf:
        for m in LINK_RE.finditer(re.sub(r"`[^`]*`", "", text)):
            target = m.group(1)
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("<"):
                continue
            rel, _, anchor = target.partition("#")
            full = os.path.normpath(os.path.join(base, unquote(rel))) if rel else os.path.abspath(path)
            if not os.path.isfile(full):
                E(i, "L6", "링크 대상 파일 없음: %s" % target)
                continue
            if anchor:
                if full not in cache:
                    cache[full] = anchors_of(full)
                if unquote(anchor).lower() not in cache[full]:
                    E(i, "L6", "앵커 없음: %s" % target)

    # L7 인계 절
    handoff = fields_in(section(nf, "인계"))
    h_line = next((i for i, t in nf if t.strip() == "## 인계"), 1)
    if state == "completed":
        if handoff.get("다음 행동", "").strip() != "없음":
            E(h_line, "L7", "completed 상태의 인계는 `다음 행동: 없음`이어야 함")
        if "재개 프롬프트" in handoff:
            E(h_line, "L7", "completed 상태의 인계에 재개 프롬프트가 남아 있음")
    else:
        for name in HANDOFF_OPEN:
            if name not in handoff:
                E(h_line, "L7", "인계 필드 없음: %s" % name)
        if "재개 프롬프트" not in handoff:
            E(h_line, "L7", "열린 상태의 인계에 재개 프롬프트 없음")
        else:
            m = RESUME_RE.match(handoff["재개 프롬프트"].strip())
            if not m:
                E(h_line, "L7", "재개 프롬프트 형식이 표준과 다름(wf-doc §2.7)")
            elif work_id and m.group(1) != work_id:
                E(h_line, "L7", "재개 프롬프트의 작업 ID %s ≠ 머리말 %s" % (m.group(1), work_id))

    # L9 파일 크기
    size = os.path.getsize(path)
    if size > WARN_FILE_BYTES:
        F.append(Finding(path, 1, "W", "L9", "파일 %d바이트 (경고 기준 %d)" % (size, WARN_FILE_BYTES)))
    return F


# ---- 포트폴리오(docs/status.md) 검사 ----

def worklog_state(path):
    head = head_fields(read_lines(path))
    return plain(head["상태"][0]) if "상태" in head else ""


def worklogs_under(root):
    return sorted(glob.glob(os.path.join(root, "docs", "work", "*", "work-log.md")))


def lint_status_file(path, root=None):
    F = []
    root = root or find_root(os.path.dirname(os.path.abspath(path))) or os.getcwd()
    nf, _ = outside_fences(read_lines(path))
    rows = {}
    for i, text in nf:
        m = ROW_RE.match(text)
        if m:
            rows.setdefault(m.group(1), i)
    table_line = next((i for i, t in nf if t.strip() == "## 작업 목록"), 1)
    for log in worklogs_under(root):
        wid = os.path.basename(os.path.dirname(log))
        if worklog_state(log) not in CLOSED and wid not in rows:
            F.append(Finding(path, table_line, "E", "L8", "열린 작업 %s의 행이 없음" % wid))
    for wid, i in rows.items():
        log = os.path.join(root, "docs", "work", wid, "work-log.md")
        if not os.path.isfile(log):
            F.append(Finding(path, i, "E", "L8", "행 %s의 작업 기록 파일 없음" % wid))
        elif worklog_state(log) in FINAL:
            F.append(Finding(path, i, "E", "L8", "닫힌 작업 %s의 행이 남아 있음(%s)" % (wid, worklog_state(log))))
    return F


# ---- 대상 선택과 실행 ----

def find_root(start):
    cur = os.path.abspath(start)
    for _ in range(4):
        if os.path.isdir(os.path.join(cur, "docs")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return None


def default_targets(root):
    targets = [p for p in worklogs_under(root) if worklog_state(p) not in CLOSED]
    status = os.path.join(root, "docs", "status.md")
    if os.path.isfile(status):
        targets.append(status)
    return targets


def lint_paths(paths, root=None):
    F = []
    for p in paths:
        if os.path.basename(p) == "status.md":
            F.extend(lint_status_file(p, root))
        else:
            F.extend(lint_worklog_file(p, root))
    return sorted(F, key=lambda f: (f.path, f.line, f.code))


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        paths, root = argv, None
    else:
        root = find_root(os.getcwd())
        if root is None:
            print("docs/ 디렉터리를 찾지 못함(현재 디렉터리와 상위 3단계)", file=sys.stderr)
            return 2
        paths = default_targets(root)
    findings = lint_paths(paths, root)
    for f in findings:
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

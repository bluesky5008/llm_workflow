#!/usr/bin/env python3
"""스킬 문서 린트 — skills/*/SKILL.md와 references/*.md의 계층 규칙(ADR-010)을 검사한다.

사용: python lint_skill.py [SKILL.md ...]
  인자 없음: 현재 디렉터리(없으면 상위 3단계까지)에서 skills/를 찾아 skills/*/SKILL.md 전부를 검사한다.
  인자 있음: 지정한 SKILL.md만 검사한다(그 스킬의 references/*.md 링크도 함께).
검사: K1 frontmatter name·description 길이, K2 description의 XML 태그·백슬래시, K3 본문 어절 상한,
      K4 상대 링크의 파일·앵커, K5 어디서도 링크되지 않는 references, K6 본문의 큰 표·코드블록(이관 검토),
      K7 `## 주의` 절 부재·가드 문구 0회.
출력: 경로:행: E|W Kx 메시지. 오류(E)가 1건 이상이면 exit 1.
스킬이 다른 위치에 설치되었으면 그 경로로 실행한다(예: ~/.claude/skills/wf-doc/scripts/lint_skill.py).
표준 라이브러리만 사용한다. 실행 시점(SKILL.md·references 변경 커밋 전)은 README 실행 기준,
계층 규칙과 상한 조정 절차는 docs/work/20261009-skill-diet/ADR-010을 따른다.
"""
import glob
import os
import re
import sys
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_worklog import Finding, anchors_of, headings, outside_fences, read_lines  # noqa: E402

# ---- 상한(초깃값: REQ-DESIGN-skill-diet Q-01 승인값, 2026-10-09. 변경은 wf-design 경량 경로) ----
MAX_BODY_WORDS = {"wf-implement": 2850, "wf-doc": 2350, "wf-tree": 1200, "wf-design": 2300}
DEFAULT_MAX = 5000
WARN_RATIO = 0.95
MAX_NAME = 64
MAX_DESC = 1024
WARN_DESC = 900
MAX_TABLE_ROWS = 10
MAX_CODE_LINES = 12
GUARD_RE = re.compile(r"지 않는다|생략하지|간주하지|대신하지")
CAUTION_PREFIX = "주의"

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)[^)]*\)")
XML_RE = re.compile(r"<[A-Za-z][^<>]*>")


# ---- 파서 ----

def split_frontmatter(lines):
    """(frontmatter 필드 dict 또는 None, 본문 시작 행 인덱스)."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fields = {}
            for text in lines[1:i]:
                m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", text)
                if m:
                    fields[m.group(1)] = m.group(2).strip()
            return fields, i + 1
    return None, 0


def body_words(path):
    lines = read_lines(path)
    _, start = split_frontmatter(lines)
    return len("\n".join(lines[start:]).split())


def local_links(path):
    """펜스·인라인 코드 밖의 (행, 대상) 상대 링크."""
    nf, _ = outside_fences(read_lines(path))
    out = []
    for i, text in nf:
        for m in LINK_RE.finditer(re.sub(r"`[^`]*`", "", text)):
            target = m.group(1)
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith(("<", "#")):
                continue
            out.append((i, target))
    return out


def resolve(base_dir, target):
    rel, _, anchor = target.partition("#")
    return os.path.normpath(os.path.join(base_dir, unquote(rel))), unquote(anchor).lower()


# ---- 검사 ----

def lint_skill_file(path, cache=None):
    F, cache = [], cache if cache is not None else {}
    E = lambda line, code, msg: F.append(Finding(path, line, "E", code, msg))  # noqa: E731
    W = lambda line, code, msg: F.append(Finding(path, line, "W", code, msg))  # noqa: E731
    lines = read_lines(path)
    folder = os.path.dirname(os.path.abspath(path))
    skill_name = os.path.basename(folder)

    # K1·K2 frontmatter
    fm, start = split_frontmatter(lines)
    if fm is None:
        E(1, "K1", "frontmatter(---) 없음")
        fm = {}
    name, desc = fm.get("name"), fm.get("description")
    if name is None:
        E(1, "K1", "frontmatter에 name 없음")
    elif len(name) > MAX_NAME:
        E(1, "K1", "name %d자 (상한 %d)" % (len(name), MAX_NAME))
    if desc is None:
        E(1, "K1", "frontmatter에 description 없음")
    else:
        if len(desc) > MAX_DESC:
            E(1, "K1", "description %d자 (상한 %d)" % (len(desc), MAX_DESC))
        elif len(desc) > WARN_DESC:
            W(1, "K1", "description %d자 (경고 기준 %d)" % (len(desc), WARN_DESC))
        if XML_RE.search(desc):
            E(1, "K2", "description에 XML 태그")
        if "\\" in desc:
            E(1, "K2", "description 경로에 백슬래시")

    # K3 어절
    words = len("\n".join(lines[start:]).split())
    limit = MAX_BODY_WORDS.get(skill_name, DEFAULT_MAX)
    if words > limit:
        E(1, "K3", "본문 %d어절 (상한 %d)" % (words, limit))
    elif words > limit * WARN_RATIO:
        W(1, "K3", "본문 %d어절 (상한 %d의 %d%% 초과)" % (words, limit, int(WARN_RATIO * 100)))

    # K4 링크 — 본문과 references/*.md
    refs = sorted(glob.glob(os.path.join(folder, "references", "*.md")))
    linked = set()
    for src in [path] + refs:
        base = os.path.dirname(os.path.abspath(src))
        for i, target in local_links(src):
            full, anchor = resolve(base, target)
            if not os.path.isfile(full):
                F.append(Finding(src, i, "E", "K4", "링크 대상 파일 없음: %s" % target))
                continue
            linked.add(full)
            if anchor:
                if full not in cache:
                    cache[full] = anchors_of(full)
                if anchor not in cache[full]:
                    F.append(Finding(src, i, "E", "K4", "앵커 없음: %s" % target))

    # K5 고아 references
    for ref in refs:
        if os.path.abspath(ref) not in linked:
            F.append(Finding(ref, 1, "W", "K5", "어디서도 링크되지 않는 references"))

    # K6 큰 표·코드블록
    nf, _ = outside_fences(lines)
    runs, prev_row = [], None      # 연속한 표 행 묶음 [시작 행, 행 수]; prev_row = 직전 표 행 번호
    for i, text in nf:
        if text.lstrip().startswith("|"):
            if runs and prev_row == i - 1:
                runs[-1][1] += 1
            else:
                runs.append([i, 1])
            prev_row = i
    for start_line, n in runs:
        if n >= MAX_TABLE_ROWS:
            W(start_line, "K6", "표 %d행 — references 이관 검토" % n)
    inside, open_at, count = False, 0, 0
    for i, text in enumerate(lines, 1):
        if text.lstrip().startswith("```"):
            if inside and count >= MAX_CODE_LINES:
                W(open_at, "K6", "코드블록 %d행 — references 이관 검토" % count)
            inside, open_at, count = not inside, i, 0
        elif inside:
            count += 1

    # K7 주의 절·가드
    h2 = [t for lvl, t, _ in headings(nf) if lvl == 2]
    if not any(t.startswith(CAUTION_PREFIX) for t in h2):
        E(1, "K7", "`## 주의` 절 없음")
    if not any(GUARD_RE.search(text) for _, text in nf):
        W(1, "K7", "가드 문구 패턴 0회")
    return F


# ---- 대상 선택과 실행 ----

def find_root(start):
    cur = os.path.abspath(start)
    for _ in range(4):
        if os.path.isdir(os.path.join(cur, "skills")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return None


def default_targets(root):
    return sorted(glob.glob(os.path.join(root, "skills", "*", "SKILL.md")))


def lint_paths(paths):
    F, cache = [], {}
    for p in paths:
        F.extend(lint_skill_file(p, cache))
    return sorted(F, key=lambda f: (f.path, f.line, f.code))


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
            print("skills/ 디렉터리를 찾지 못함(현재 디렉터리와 상위 3단계)", file=sys.stderr)
            return 2
        paths = default_targets(root)
    findings = lint_paths(paths)
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

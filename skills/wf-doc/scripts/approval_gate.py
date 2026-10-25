#!/usr/bin/env python3
"""승인 게이트 판정 — 기준선이 승인되지 않은 열린 작업이 있을 때 제품 코드 편집을 확인 대상으로 본다.

사용: python approval_gate.py <저장소 루트> <대상 경로>
  제품 코드: 루트 아래 `docs/` 밖 전부. 루트의 선택 선언 `.wf-gate.json`
    {"product": [glob…], "exclude": [glob…]}이 덮어쓴다(exclude 우선, 루트 기준 상대 경로).
  열린 작업(닫힘 계열 제외)의 머리말 `기준선`:
    `N/A — 경량 경로…` → 기계 조건 (a) 제품 코드 변경 ∪ 대상 ≤ 5 (b) 민감 파일 아님 (c) 새 파일은 테스트
    그 외 → 값 안의 링크 문서가 모두 상태 approved·completed이고 `## 승인 기록`에 응답 인용이 있어야 승인.
출력: 확인이 필요하면 `<작업 ID>: <사유>` 행과 exit 1, 통과는 무출력 exit 0, 내부 오류 exit 2.
표준 라이브러리와 git만 사용한다. 정본은 REQ-DESIGN-approval-gate DES-01·02·09, ADR-018.
"""
import fnmatch
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lint_worklog as lw  # noqa: E402

GATE_FILE = ".wf-gate.json"
APPROVED = {"approved", "completed"}
LIGHT_PREFIX = "N/A — 경량 경로"
MAX_LIGHT_FILES = 5
QUOTE_RE = re.compile(r"[\"“][^\"”]+[\"”]")
SENSITIVE = {GATE_FILE, "requirements.txt", "pyproject.toml", "setup.py", "setup.cfg", "package.json",
             "package-lock.json", "go.mod", "Cargo.toml", "pom.xml"}
SENSITIVE_GLOBS = ["requirements*.txt", "*.csproj", "build.gradle*"]
SENSITIVE_PATHS = [".claude/settings*.json", "*/.claude/settings*.json"]
TEST_NAME_GLOBS = ["test_*", "*_test.*", "*.test.*", "*Tests.*"]


class GateError(Exception):
    pass


def rel_of(root, target):
    """루트 기준 상대 경로(`/` 구분). 루트 밖이면 None."""
    path = os.path.normcase(os.path.abspath(target if os.path.isabs(target) else os.path.join(root, target)))
    base = os.path.normcase(os.path.abspath(root))
    rel = os.path.relpath(path, base)
    return None if rel == os.pardir or rel.startswith(os.pardir + os.sep) else rel.replace(os.sep, "/")


def load_gate(root):
    path = os.path.join(root, GATE_FILE)
    if not os.path.isfile(path):
        return {"product": [], "exclude": []}
    try:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
        return {k: [str(g) for g in data.get(k, [])] for k in ("product", "exclude")}
    except (ValueError, AttributeError, TypeError) as e:
        raise GateError("%s 판독 실패: %s" % (GATE_FILE, e))


def is_product(rel, gate):
    match = lambda key: any(fnmatch.fnmatch(rel, g) for g in gate[key])  # noqa: E731
    if match("exclude"):
        return False
    return match("product") or not (rel == "docs" or rel.startswith("docs/"))


def baseline_problem(doc_path):
    """기준선 문서가 승인되었으면 None, 아니면 사유."""
    if not os.path.isfile(doc_path):
        return "기준선 문서 없음 %s" % os.path.basename(doc_path)
    lines = lw.read_lines(doc_path)
    head = lw.head_fields(lines)
    state = lw.plain(head["상태"][0]) if "상태" in head else ""
    name = os.path.basename(doc_path)
    if state not in APPROVED:
        return "기준선 미승인 %s (%s)" % (name, state or "상태 없음")
    nf, _ = lw.outside_fences(lines)
    if not any("응답" in t and QUOTE_RE.search(t) for _, t in lw.section(nf, "승인 기록")):
        return "승인 기록에 사용자 응답 인용 없음 %s" % name
    return None


def changed_product_files(root, gate):
    try:
        out = subprocess.run(["git", "-C", root, "status", "--porcelain", "--untracked-files=all"],
                             capture_output=True, text=True, encoding="utf-8", timeout=5)
    except (OSError, subprocess.SubprocessError):
        return set()
    if out.returncode != 0:
        return set()
    files = set()
    for line in out.stdout.splitlines():
        path = line[3:].split(" -> ")[-1].strip().strip('"')
        if path and is_product(path, gate):
            files.add(path)
    return files


def light_problem(root, rel, gate):
    name = rel.rsplit("/", 1)[-1]
    if len(changed_product_files(root, gate) | {rel}) > MAX_LIGHT_FILES:
        return "경량 경로 기계 조건 위반 (a) 제품 코드 변경 %d개 초과" % MAX_LIGHT_FILES
    if (name in SENSITIVE or any(fnmatch.fnmatch(name, g) for g in SENSITIVE_GLOBS)
            or any(fnmatch.fnmatch(rel, g) for g in SENSITIVE_PATHS)):
        return "경량 경로 기계 조건 위반 (b) 민감 파일 %s" % rel
    if not os.path.exists(os.path.join(root, rel)):
        parts = rel.split("/")[:-1]
        if not ({"test", "tests"} & set(parts) or any(fnmatch.fnmatch(name, g) for g in TEST_NAME_GLOBS)):
            return "경량 경로 기계 조건 위반 (c) 테스트가 아닌 새 파일 %s" % rel
    return None


def judge(root, target):
    """확인이 필요한 사유 [(작업 ID, 사유)]. 빈 목록이면 통과."""
    rel = rel_of(root, target)
    if rel is None or not os.path.isdir(os.path.join(root, "docs", "work")):
        return []
    gate = load_gate(root)
    if not is_product(rel, gate):
        return []
    reasons = []
    for log in lw.worklogs_under(root):
        if lw.worklog_state(log) in lw.CLOSED:
            continue
        wid = os.path.basename(os.path.dirname(log))
        head = lw.head_fields(lw.read_lines(log))
        value = head["기준선"][0] if "기준선" in head else ""
        if lw.plain(value).startswith(LIGHT_PREFIX):
            problem = light_problem(root, rel, gate)
            if problem:
                reasons.append((wid, problem))
            continue
        links = [m.split("#")[0] for m in lw.LINK_RE.findall(value)]
        if not links:
            reasons.append((wid, "기준선 링크 없음"))
            continue
        for link in links:
            problem = baseline_problem(os.path.normpath(os.path.join(os.path.dirname(log), link)))
            if problem:
                reasons.append((wid, problem))
    return reasons


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        print("사용: approval_gate.py <저장소 루트> <대상 경로>", file=sys.stderr)
        return 2
    try:
        reasons = judge(argv[0], argv[1])
    except Exception as e:  # 판독 실패는 확인 요청으로 이어진다(fail-to-ask)
        print("gate=error (%s)" % e)
        return 2
    for wid, why in reasons:
        print("%s: %s" % (wid, why))
    return 1 if reasons else 0


if __name__ == "__main__":
    sys.exit(main())

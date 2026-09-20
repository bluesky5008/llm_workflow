#!/usr/bin/env python3
"""회귀검사 기준선 측정 — llm_workflow 작업 기록(work-log.md) 파서.

docs/work/*/work-log.md 를 읽어 검증 실행의 구조적 지표를 뽑는다.
AI-01(01_solution_plan.md §2.3) 의 측정 항목:
  (a) 검증 항목 수와 결과 분포
  (b) 검증 방법 분류 — 자동 테스트 / 통독·검색 / 사용자 검토 / 실행 확인
  (c) 3튜플 앵커 기록률 — 실행 명령 문자열, 커밋 SHA
  (d) 테스트 실행 언급 횟수(같은 스위트 반복 추정)
  (e) 실패 분류 어휘 사용 여부
  (f) 재실행·결과 변화 언급

사용법:
  python measure_regression_baseline.py <repo-root> [--md out.md]
어느 저장소든 docs/work/<id>/work-log.md 구조면 동작한다.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

# ── 패턴 ─────────────────────────────────────────────────────────────
VER_ROW = re.compile(r"^\|\s*(VER-\d+)\s*\|(.+)$")
RESULT_WORDS = ("성공", "실패", "미수행")
AUTO_TEST = re.compile(
    r"pytest|run-tests|Pester|unittest|npm test|jest|go test|cargo test|"
    r"\bT\d{2}\b|\d+/\d+\s*(pass|passed|성공)|Red|Green", re.I)
READ_ONLY = re.compile(r"통독|검색|grep|대조|확인\b|git (show|diff|log)", re.I)
USER_REVIEW = re.compile(r"사용자 (검토|응답|확인)|육안", re.I)
CMD_STR = re.compile(r"`(?:[^`]*(?:pytest|powershell|pwsh|python|npm|node|go |cargo|git |make |\.ps1|\.py)[^`]*|(?:grep|rg|test|ls|find|diff|sed|cat|wc) [^`]*)`", re.I)
SHA = re.compile(r"\b[0-9a-f]{7,40}\b")
DATE_LIKE = re.compile(r"\b\d{4}-?\d{2}-?\d{2}\b")
TEST_RUN = re.compile(r"(\d+)/(\d+)\s*(pass|passed|성공|통과)|Red 확인|Green|전체 \d+/\d+", re.I)
FAIL_CLASS = {
    "이번 변경": re.compile(r"이번 변경으로"),
    "기존 실패": re.compile(r"기존(에도)? (존재한 )?실패|기존 실패"),
    "환경 실패": re.compile(r"실행 환경|외부 의존성.*실패"),
    "원인 미확인": re.compile(r"원인을 확인하지 못"),
}
RERUN = re.compile(r"재실행|다시 실행|재수행|재검증", re.I)
RESULT_CHANGED = re.compile(r"실패 1회|처음.*실패.*(이후|후).*성공|플레이키|flaky|간헐", re.I)
NO_AUTO = re.compile(r"자동 회귀 검증(이)? 없음|TDD 부적용|테스트 체계 없음", re.I)
TASK_ID = re.compile(r"\bTASK-(\d+)\b")


def classify_method(text: str) -> str:
    if USER_REVIEW.search(text):
        return "사용자 검토"
    if AUTO_TEST.search(text):
        return "자동 테스트"
    if READ_ONLY.search(text):
        return "통독·검색·대조"
    return "기타"


def analyze(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    ver_rows = []
    for ln in lines:
        m = VER_ROW.match(ln)
        if m:
            cells = [c.strip() for c in m.group(2).split("|")]
            ver_rows.append((m.group(1), cells))

    results = Counter()
    methods = Counter()
    cmd_recorded = sha_recorded = 0
    for vid, cells in ver_rows:
        joined = " ".join(cells)
        # 결과 열: 셀 중 결과 어휘로 시작하는 것
        res = next((w for c in cells for w in RESULT_WORDS if c.startswith(w) or c.startswith(f"**{w}")), "불명")
        results[res] += 1
        methods[classify_method(joined)] += 1
        if CMD_STR.search(joined):
            cmd_recorded += 1
        # SHA: 날짜형(20260809)·숫자만인 토큰 제외
        shas = [s for s in SHA.findall(joined) if not s.isdigit() and not DATE_LIKE.fullmatch(s)]
        if shas:
            sha_recorded += 1

    test_runs = len(TEST_RUN.findall(text))
    tasks = sorted({int(t) for t in TASK_ID.findall(text)})
    fail_cls = {k: len(p.findall(text)) for k, p in FAIL_CLASS.items()}
    return {
        "cycle": path.parent.name,
        "lines": len(lines),
        "tasks": len(tasks),
        "ver_total": len(ver_rows),
        "results": dict(results),
        "methods": dict(methods),
        "cmd_recorded": cmd_recorded,
        "sha_recorded": sha_recorded,
        "test_run_mentions": test_runs,
        "fail_class": fail_cls,
        "rerun_mentions": len(RERUN.findall(text)),
        "result_changed": len(RESULT_CHANGED.findall(text)),
        "declares_no_auto": bool(NO_AUTO.search(text)),
    }


def to_markdown(rows: list[dict]) -> str:
    out = ["| 사이클 | TASK | VER | 성공/실패/미수행 | 자동테스트 | 통독·대조 | 사용자검토 | 명령 기록 | SHA 기록 | 실행 언급 | 재실행 언급 | 결과 변화 | 자동검증 없음 선언 |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    tot = Counter()
    for r in rows:
        res = r["results"]; m = r["methods"]
        out.append(
            f"| {r['cycle']} | {r['tasks']} | {r['ver_total']} | "
            f"{res.get('성공',0)}/{res.get('실패',0)}/{res.get('미수행',0)} | "
            f"{m.get('자동 테스트',0)} | {m.get('통독·검색·대조',0)} | {m.get('사용자 검토',0)} | "
            f"{r['cmd_recorded']}/{r['ver_total']} | {r['sha_recorded']}/{r['ver_total']} | "
            f"{r['test_run_mentions']} | {r['rerun_mentions']} | {r['result_changed']} | "
            f"{'예' if r['declares_no_auto'] else '—'} |")
        for k in ("tasks", "ver_total", "cmd_recorded", "sha_recorded", "test_run_mentions", "rerun_mentions", "result_changed"):
            tot[k] += r[k]
        for k, v in res.items():
            tot[f"res_{k}"] += v
        for k, v in m.items():
            tot[f"m_{k}"] += v
    out.append(
        f"| **합계** | {tot['tasks']} | {tot['ver_total']} | "
        f"{tot['res_성공']}/{tot['res_실패']}/{tot['res_미수행']} | "
        f"{tot['m_자동 테스트']} | {tot['m_통독·검색·대조']} | {tot['m_사용자 검토']} | "
        f"{tot['cmd_recorded']}/{tot['ver_total']} | {tot['sha_recorded']}/{tot['ver_total']} | "
        f"{tot['test_run_mentions']} | {tot['rerun_mentions']} | {tot['result_changed']} | |")
    fc = Counter()
    for r in rows:
        for k, v in r["fail_class"].items():
            fc[k] += v
    out.append("")
    out.append("실패 분류 어휘 사용(전체): " + ", ".join(f"{k} {v}건" for k, v in fc.items()))
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("--md", type=Path)
    a = ap.parse_args()
    logs = sorted((a.repo / "docs" / "work").glob("*/work-log.md"))
    if not logs:
        print("work-log.md 없음", file=sys.stderr); return 1
    rows = [analyze(p) for p in logs]
    md = to_markdown(rows)
    print(md)
    if a.md:
        a.md.write_text(md + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

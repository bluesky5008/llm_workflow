# lint_worklog.py 검증 — 실행: python -m pytest skills/wf-doc/scripts/tests -q
# 검사 항목 L1~L9마다 실패 입력에서 해당 코드가 나오고 통과 입력에서 나오지 않음을 보인다.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lint_worklog as lw  # noqa: E402

WORK_ID = "20260101-sample"

HEAD = """# WORK-20260101-sample: 작업 기록 — 견본

> 문서 유형: `work-log, verification, completion`
> 작업 ID: `20260101-sample`
> 상태: `{state}`
> 기준선: `v1`
> 작성일: 2026-01-01
> 최종 갱신: 2026-01-02
> 관련 문서: [PLAN-20260101-sample](./plan.md)

## 요약

- 목적: 견본.
- 현재 결론 또는 상태: TASK-01 완료.
- 다음 행동: [인계](#인계) 절.

## 문서 연결

| 방향 | 관계 | 대상 문서 | 대상 항목 | 비고 |
|---|---|---|---|---|
| input | implementation | [PLAN-20260101-sample](./plan.md#작업-목록) | TASK-01 | 계획 |

## 기준선과 현재 계획

- 기준선: v1
- 계획: [PLAN-20260101-sample](./plan.md)

## 수행 기록

{entries}
## 설계와 달라진 점

없음.

## 검증 결과

### 범위와 환경

- 대상 기준선 또는 구현: v1

### 결과 요약

- 성공: 0

### 인수 조건별 결과

| 검증 ID | 인수 조건 | 방법·명령 | 결과 | 증거 |
|---|---|---|---|---|

### 실패와 미수행 분석

없음.

## 완료 보고

### 완료 상태

- 결과: TBD — 완료 보고 종결 시 기입

## 인계

{handoff}"""

ENTRY = """### 2026-01-01 — TASK-01

- 결정과 이유: 없음
- 검증: `python -m pytest -q` 3 passed
- 결과: 완료 — 2026-01-01 10:00
"""

HANDOFF_OPEN = """- 다음 단계 또는 워크플로우: wf-implement §3.3
- 시작 조건: 충족
- 입력 문서와 기준선: [PLAN-20260101-sample](./plan.md)
- 완료된 항목: TASK-01
- 미완료 항목: TASK-02
- 차단 요인: 없음
- 다음 행동: TASK-02를 시작한다.
- 재개 프롬프트: 작업 20260101-sample 재개 — docs/work/20260101-sample/work-log.md의 인계 절을 읽고 "다음 행동"부터 진행하라.
"""
RESUME_LINE = HANDOFF_OPEN.splitlines()[-1] + "\n"

HANDOFF_DONE = """- 다음 단계 또는 워크플로우: 없음
- 완료된 항목: TASK-01, TASK-02
- 미완료 항목: 없음
- 다음 행동: 없음
"""

STATUS = """# ST-sample: 포트폴리오

> 문서 유형: `status`
> 상태: `in-progress`

## 작업 목록

| 작업 ID | 제목 | 상태 | 계획·기록 | 의존 | 다음 행동 |
|---|---|---|---|---|---|
{rows}
"""
ROW = "| 20260101-sample | 견본 | in-progress | [work-log](./work/20260101-sample/work-log.md) | — | TASK-02 |"
NO_ROWS = STATUS.format(rows="")


def good(state="in-progress", entries=ENTRY, handoff=HANDOFF_OPEN):
    return HEAD.format(state=state, entries=entries, handoff=handoff)


def write(root, rel, text):
    path = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path


def run(tmp_path, log, status=STATUS.format(rows=ROW), work_id=WORK_ID):
    root = str(tmp_path)
    write(root, "docs/work/%s/plan.md" % work_id, "# PLAN\n\n## 작업 목록\n")
    paths = [write(root, "docs/work/%s/work-log.md" % work_id, log)]
    if status is not None:
        paths.append(write(root, "docs/status.md", status))
    return lw.lint_paths(paths, root)


def codes(findings, level=None):
    return sorted({f.code for f in findings if level is None or f.level == level})


# ---- 통과 입력: 오류 0 ----

def test_good_open_log_has_no_findings(tmp_path):
    assert run(tmp_path, good()) == []


def test_good_completed_log_has_no_findings(tmp_path):
    assert run(tmp_path, good("completed", handoff=HANDOFF_DONE), status=NO_ROWS) == []


# ---- L1 머리말 ----

def test_l1_missing_head_field(tmp_path):
    log = good().replace("> 기준선: `v1`\n", "")
    assert "L1" in codes(run(tmp_path, log))


def test_l1_unknown_status(tmp_path):
    assert "L1" in codes(run(tmp_path, good("done")))


def test_l1_type_without_work_log(tmp_path):
    log = good().replace("`work-log, verification, completion`", "`plan`")
    assert "L1" in codes(run(tmp_path, log))


# ---- L2 H2 목록·순서·중복 ----

def test_l2_extra_section(tmp_path):
    log = good().replace("## 수행 기록\n", "## 현재 상태\n\n- 진행 중인 작업: 없음\n\n## 수행 기록\n")
    assert "L2" in codes(run(tmp_path, log))


def test_l2_wrong_order(tmp_path):
    log = good().replace("## 설계와 달라진 점\n\n없음.\n\n", "")
    log = log.replace("## 인계\n", "## 설계와 달라진 점\n\n없음.\n\n## 인계\n")
    assert "L2" in codes(run(tmp_path, log))


def test_l2_duplicate_section(tmp_path):
    log = good() + "\n## 인계\n\n- 다음 행동: 중복\n"
    assert "L2" in codes(run(tmp_path, log))


def test_l2_missing_section(tmp_path):
    log = good().replace("## 설계와 달라진 점\n\n없음.\n\n", "")
    assert "L2" in codes(run(tmp_path, log))


# ---- L3 수행 기록 항목 ----

def test_l3_missing_required_field(tmp_path):
    entry = ENTRY.replace("- 결정과 이유: 없음\n", "")
    assert "L3" in codes(run(tmp_path, good(entries=entry)))


def test_l3_too_many_lines(tmp_path):
    entry = ENTRY + "".join("- 메모 %d: 짧은 줄\n" % i for i in range(6))
    assert "L3" in codes(run(tmp_path, good(entries=entry)))


def test_l3_too_many_chars(tmp_path):
    entry = ENTRY.replace("- 검증: `python -m pytest -q` 3 passed", "- 검증: " + "가" * 290)
    entry = entry.replace("- 결정과 이유: 없음", "- 결정과 이유: " + "나" * 290)
    found = codes(run(tmp_path, good(entries=entry)))
    assert "L3" in found and "L5" not in found


def test_l3_optional_fields_allowed(tmp_path):
    entry = ENTRY.replace("- 결정과 이유:", "- 수행 내용: 계획과 다르게 수행\n- 발견 사항: 없음\n- 결정과 이유:")
    assert "L3" not in codes(run(tmp_path, good(entries=entry)))


# ---- L4 펜스 ----

def test_l4_fence(tmp_path):
    log = good().replace("없음.\n\n## 검증 결과", "```text\nlog\n```\n\n## 검증 결과")
    assert "L4" in codes(run(tmp_path, log))


# ---- L5 불릿 길이 ----

def test_l5_long_bullet(tmp_path):
    log = good().replace("- 성공: 0", "- 성공: " + "가" * 301)
    assert "L5" in codes(run(tmp_path, log))


def test_l5_bullet_at_limit_passes(tmp_path):
    log = good().replace("- 성공: 0", ("- 성공: " + "가" * 300)[: lw.MAX_BULLET_CHARS])
    assert "L5" not in codes(run(tmp_path, log))


# ---- L6 링크·앵커 ----

def test_l6_missing_file(tmp_path):
    log = good().replace("[PLAN-20260101-sample](./plan.md#작업-목록)", "[없음](./missing.md)")
    assert "L6" in codes(run(tmp_path, log))


def test_l6_missing_anchor(tmp_path):
    log = good().replace("(./plan.md#작업-목록)", "(./plan.md#없는-절)")
    assert "L6" in codes(run(tmp_path, log))


def test_l6_missing_self_anchor(tmp_path):
    log = good().replace("[인계](#인계)", "[인계](#재개-지점)")
    assert "L6" in codes(run(tmp_path, log))


def test_l6_external_and_inline_code_ignored(tmp_path):
    log = good().replace("- 성공: 0", "- 성공: [외부](https://example.com) `[TASK-03](../x/plan.md#작업-목록)`")
    assert "L6" not in codes(run(tmp_path, log))


# ---- L7 인계 절 ----

def test_l7_open_missing_field(tmp_path):
    handoff = HANDOFF_OPEN.replace("- 차단 요인: 없음\n", "")
    assert "L7" in codes(run(tmp_path, good(handoff=handoff)))


def test_l7_open_missing_resume_prompt(tmp_path):
    handoff = HANDOFF_OPEN.replace(RESUME_LINE, "")
    assert "L7" in codes(run(tmp_path, good(handoff=handoff)))


def test_l7_open_resume_prompt_format(tmp_path):
    handoff = HANDOFF_OPEN.replace("작업 20260101-sample 재개 — docs/work", "작업 20260101-other 재개 — docs/work")
    assert "L7" in codes(run(tmp_path, good(handoff=handoff)))


def test_l7_completed_next_action_must_be_none(tmp_path):
    handoff = HANDOFF_DONE.replace("- 다음 행동: 없음", "- 다음 행동: TASK-03")
    assert "L7" in codes(run(tmp_path, good("completed", handoff=handoff), status=NO_ROWS))


def test_l7_completed_must_not_keep_resume_prompt(tmp_path):
    log = good("completed", handoff=HANDOFF_DONE + RESUME_LINE)
    assert "L7" in codes(run(tmp_path, log, status=NO_ROWS))


# ---- L8 status.md 정합 ----

def test_l8_open_log_without_row(tmp_path):
    assert "L8" in codes(run(tmp_path, good(), status=NO_ROWS))


def test_l8_row_for_completed_log(tmp_path):
    assert "L8" in codes(run(tmp_path, good("completed", handoff=HANDOFF_DONE)))


def test_l8_row_for_missing_log(tmp_path):
    row = "| 20260101-ghost | 없음 | in-progress | — | — | — |"
    assert "L8" in codes(run(tmp_path, good(), status=STATUS.format(rows=ROW + "\n" + row)))


def test_l8_on_hold_row_is_optional(tmp_path):
    assert "L8" not in codes(run(tmp_path, good("on-hold"), status=NO_ROWS))
    assert "L8" not in codes(run(tmp_path, good("on-hold")))


# ---- L9 파일 크기(경고) ----

def test_l9_large_file_is_warning_only(tmp_path):
    filler = "".join("- 항목 %d: %s\n" % (i, "가" * 100) for i in range(60))
    log = good().replace("- 성공: 0\n", "- 성공: 0\n" + filler)
    findings = run(tmp_path, log)
    assert "L9" in codes(findings, "W")
    assert codes(findings, "E") == []


# ---- 대상 선택과 exit code ----

def test_default_targets_skip_closed_states(tmp_path):
    root = str(tmp_path)
    for i, state in enumerate(["in-progress", "completed", "on-hold", "blocked", "superseded"]):
        write(root, "docs/work/2026010%d-w/work-log.md" % i, good(state))
    write(root, "docs/status.md", NO_ROWS)
    rels = sorted(os.path.relpath(p, root).replace(os.sep, "/") for p in lw.default_targets(root))
    assert rels == ["docs/status.md", "docs/work/20260100-w/work-log.md", "docs/work/20260103-w/work-log.md"]


def test_find_root_walks_up(tmp_path):
    os.makedirs(os.path.join(str(tmp_path), "docs", "work"))
    deep = os.path.join(str(tmp_path), "a", "b")
    os.makedirs(deep)
    assert os.path.normcase(lw.find_root(deep)) == os.path.normcase(str(tmp_path))


def test_main_exit_codes(tmp_path, capsys):
    root = str(tmp_path)
    write(root, "docs/work/%s/plan.md" % WORK_ID, "# PLAN\n\n## 작업 목록\n")
    ok = write(root, "docs/work/%s/work-log.md" % WORK_ID, good())
    write(root, "docs/status.md", STATUS.format(rows=ROW))
    assert lw.main([ok]) == 0
    bad = write(root, "docs/work/20260102-bad/work-log.md", good().replace("> 기준선: `v1`\n", ""))
    assert lw.main([bad]) == 1
    out = capsys.readouterr().out
    assert ": E L1 " in out and out.startswith(os.path.relpath(bad))

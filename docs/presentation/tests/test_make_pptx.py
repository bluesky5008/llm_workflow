# make_pptx.py 검증 테스트 — 외부 프레임워크 없이 단독 실행: python tests/test_make_pptx.py
# 견본 md(표지+본문 2장, 중첩 불릿·코드 블록·노트)로 파서·생성기·자동 대조를 검증한다.
import os
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import make_pptx  # noqa: E402

SAMPLE = """# 견본 덱

- 부제 첫 줄
- 부제 둘째 줄

> 노트: 표지 노트입니다.

## 첫 슬라이드

- 항목 하나
  - 하위 항목

```
code line 1
code line 2
```

- 코드 뒤 항목

> 노트: 노트 한 줄.
> 둘째 줄.

## 둘째 슬라이드

- 단일 항목
"""


def test_parse():
    deck = make_pptx.parse_md(SAMPLE)
    assert deck.title == "견본 덱", deck.title
    assert deck.cover_lines == ["부제 첫 줄", "부제 둘째 줄"], deck.cover_lines
    assert deck.cover_notes == "표지 노트입니다.", repr(deck.cover_notes)
    assert len(deck.slides) == 2, len(deck.slides)

    s1 = deck.slides[0]
    assert s1.title == "첫 슬라이드", s1.title
    assert s1.blocks == [
        ("bullet", 0, "항목 하나"),
        ("bullet", 1, "하위 항목"),
        ("code", "code line 1\ncode line 2"),
        ("bullet", 0, "코드 뒤 항목"),
    ], s1.blocks
    assert s1.notes == "노트 한 줄.\n둘째 줄.", repr(s1.notes)

    s2 = deck.slides[1]
    assert s2.title == "둘째 슬라이드", s2.title
    assert s2.blocks == [("bullet", 0, "단일 항목")], s2.blocks
    assert s2.notes == "", repr(s2.notes)


def test_parse_rejects_unsupported():
    # 계약 밖 요소(표)는 줄 번호와 함께 실패해야 한다 (조용한 누락 금지).
    bad = "# 덱\n\n## 장\n\n| a | b |\n"
    try:
        make_pptx.parse_md(bad)
    except make_pptx.MdContractError as e:
        assert "5" in str(e), str(e)
    else:
        raise AssertionError("MdContractError not raised for table line")


def test_build_and_verify():
    deck = make_pptx.parse_md(SAMPLE)
    out = os.path.join(tempfile.mkdtemp(prefix="wf-pptx-test-"), "sample.pptx")
    make_pptx.build_pptx(deck, out)
    assert os.path.isfile(out), out

    problems = make_pptx.verify_pptx(deck, out)
    assert problems == [], problems

    from pptx import Presentation

    prs = Presentation(out)
    slides = list(prs.slides)
    assert len(slides) == 3, len(slides)
    assert slides[0].shapes.title.text == "견본 덱"
    assert slides[1].shapes.title.text == "첫 슬라이드"
    assert slides[2].shapes.title.text == "둘째 슬라이드"

    body = slides[1].placeholders[1].text_frame.text
    assert "항목 하나" in body, body
    assert "code line 1" in body, body
    assert slides[1].notes_slide.notes_text_frame.text == "노트 한 줄.\n둘째 줄."
    assert slides[0].notes_slide.notes_text_frame.text == "표지 노트입니다."


def test_verify_detects_mismatch():
    # 대조 함수가 실제 불일치를 잡아내는지 확인한다 (항상 빈 목록을 돌려주는 구현 방지).
    deck = make_pptx.parse_md(SAMPLE)
    out = os.path.join(tempfile.mkdtemp(prefix="wf-pptx-test-"), "sample.pptx")
    make_pptx.build_pptx(deck, out)
    deck.slides[0].title = "다른 제목"
    problems = make_pptx.verify_pptx(deck, out)
    assert problems, "verify_pptx must report a title mismatch"


# ---- 기준선 v2 (DCR-002): 디자인 시스템 + 인포그래픽 ----
# 색 기대값은 req-design.md DES-05가 정본이다.
INK = (0x24, 0x30, 0x4A)
BG = (0xFA, 0xF9, 0xF5)
ACCENT = (0x1B, 0x7A, 0x6E)
ACCENT_LIGHT = (0xE3, 0xF0, 0xED)
GATE = (0xC0, 0x5B, 0x2E)
GATE_LIGHT = (0xF7, 0xE7, 0xDC)
PANEL = (0xF0, 0xEE, 0xE7)
WHITE = (0xFF, 0xFF, 0xFF)


def _rgb(t):
    from pptx.dml.color import RGBColor

    return RGBColor(*t)


def _fill_rgb(obj):
    # solid 채움의 RGB를 돌려주고, 채움이 없거나 미지원 형식이면 None.
    try:
        fill = obj.fill
        if fill.type is None:
            return None
        return fill.fore_color.rgb
    except (TypeError, AttributeError):
        return None


def _free_shapes(slide):
    return [sh for sh in slide.shapes if not sh.is_placeholder]


def _shape_by_text(shapes, needle):
    for sh in shapes:
        if sh.has_text_frame and needle in sh.text_frame.text:
            return sh
    return None


DIAG_SAMPLE = """# 다이어그램 덱

- 부제

## 흐름 슬라이드

```flow
작업 요청
★ 사용자 승인 관문
완료
```

## 행 슬라이드

```rows
계획 → 구현 → 검증
```

## 사다리 슬라이드

```ladder
만들 필요가 있는가?
저장소에 이미 있는가?
표준 라이브러리가 해결하는가?
```

## 패널 슬라이드

- 패널 위 항목

```
plain line
```
"""

CARD_SAMPLE = """# 카드 덱

- 부제

## AI 코딩 위임의 실패 모드

- 실패 하나
- 실패 둘
- 실패 셋
- 실패 넷
- 결론 밴드 문구

## 세션 핸드오프 — 개념과 3층 설계

- 문제: 남는 지점
- A층 — 스킬 불변식
- B층 — 저장소 스크립트
- C층 — 하네스 자동화

## 다른 제목 슬라이드

- 실패 하나
- 실패 둘
"""


def test_parse_fence_tags():
    # 태그 펜스는 렌더 유형으로 기록되고, 무태그는 기존 ("code", text) 그대로다(하위 호환).
    deck = make_pptx.parse_md(DIAG_SAMPLE)
    assert deck.slides[0].blocks == [
        ("flow", "작업 요청\n★ 사용자 승인 관문\n완료")
    ], deck.slides[0].blocks
    assert deck.slides[1].blocks == [("rows", "계획 → 구현 → 검증")], deck.slides[1].blocks
    assert deck.slides[2].blocks == [
        ("ladder", "만들 필요가 있는가?\n저장소에 이미 있는가?\n표준 라이브러리가 해결하는가?")
    ], deck.slides[2].blocks
    assert deck.slides[3].blocks == [
        ("bullet", 0, "패널 위 항목"),
        ("code", "plain line"),
    ], deck.slides[3].blocks

    # 미지원 태그는 계약 위반 — 줄 번호와 함께 중단한다.
    bad = "# 덱\n\n## 장\n\n```python\nx\n```\n"
    try:
        make_pptx.parse_md(bad)
    except make_pptx.MdContractError as e:
        assert "5" in str(e), str(e)
    else:
        raise AssertionError("MdContractError not raised for unknown fence tag")


def test_design_system_applied():
    # DES-05: 표지·마무리는 네이비 배경 + 백색 제목, 본문은 웜 화이트 배경 + 틸 언더바.
    deck = make_pptx.parse_md(SAMPLE)
    out = os.path.join(tempfile.mkdtemp(prefix="wf-pptx-test-"), "design.pptx")
    make_pptx.build_pptx(deck, out)

    from pptx import Presentation

    prs = Presentation(out)
    slides = list(prs.slides)

    assert _fill_rgb(slides[0].background) == _rgb(INK), _fill_rgb(slides[0].background)
    cover_run = slides[0].shapes.title.text_frame.paragraphs[0].runs[0]
    assert cover_run.font.color.rgb == _rgb(WHITE), cover_run.font.color.rgb

    assert _fill_rgb(slides[1].background) == _rgb(BG), _fill_rgb(slides[1].background)
    underbars = [sh for sh in _free_shapes(slides[1]) if _fill_rgb(sh) == _rgb(ACCENT)]
    assert underbars, "body slide must have a teal title underbar"

    # 마지막 본문 슬라이드는 마무리 처리(네이비 배경).
    assert _fill_rgb(slides[-1].background) == _rgb(INK), _fill_rgb(slides[-1].background)


def test_diagram_shapes():
    # DES-06: flow/rows/ladder는 도형 다이어그램, 무태그는 연회색 패널.
    deck = make_pptx.parse_md(DIAG_SAMPLE)
    out = os.path.join(tempfile.mkdtemp(prefix="wf-pptx-test-"), "diagram.pptx")
    make_pptx.build_pptx(deck, out)
    assert make_pptx.verify_pptx(deck, out) == []

    from pptx import Presentation

    prs = Presentation(out)
    slides = list(prs.slides)

    flow = _free_shapes(slides[1])
    gate = _shape_by_text(flow, "★ 사용자 승인 관문")
    normal = _shape_by_text(flow, "작업 요청")
    assert _shape_by_text(flow, "완료") is not None
    assert gate is not None and normal is not None
    assert _fill_rgb(gate) in (_rgb(GATE), _rgb(GATE_LIGHT)), _fill_rgb(gate)
    assert _fill_rgb(normal) in (_rgb(ACCENT), _rgb(ACCENT_LIGHT)), _fill_rgb(normal)

    rows = _free_shapes(slides[2])
    for seg in ("계획", "구현", "검증"):
        assert _shape_by_text(rows, seg) is not None, seg

    ladder = _free_shapes(slides[3])
    assert _shape_by_text(ladder, "만들 필요가 있는가?") is not None
    chips = [sh for sh in ladder if sh.has_text_frame and sh.text_frame.text.strip() == "1"]
    assert chips, "ladder must render numbered chips"

    panel = [sh for sh in _free_shapes(slides[4]) if _fill_rgb(sh) == _rgb(PANEL)]
    assert panel, "untagged fence must render a light-gray panel"
    body_text = slides[4].placeholders[1].text_frame.text
    assert "plain line" in body_text, body_text


def test_card_layout_and_fallback():
    # DES-06: 매핑된 제목은 카드·밴드로, 그 외 제목은 기존 불릿으로(fail-soft).
    deck = make_pptx.parse_md(CARD_SAMPLE)
    out = os.path.join(tempfile.mkdtemp(prefix="wf-pptx-test-"), "cards.pptx")
    make_pptx.build_pptx(deck, out)
    assert make_pptx.verify_pptx(deck, out) == []

    from pptx import Presentation

    prs = Presentation(out)
    slides = list(prs.slides)

    cards = _free_shapes(slides[1])
    for text in ("실패 하나", "실패 둘", "실패 셋", "실패 넷", "결론 밴드 문구"):
        assert _shape_by_text(cards, text) is not None, text

    bands = _free_shapes(slides[2])
    for text in ("A층", "B층", "C층"):
        assert _shape_by_text(bands, text) is not None, text

    # 매핑 밖 제목은 본문 불릿 그대로 — 카드 도형에 흩어지지 않는다.
    body_text = slides[3].placeholders[1].text_frame.text
    assert "실패 하나" in body_text and "실패 둘" in body_text, body_text


def main():
    tests = [
        test_parse,
        test_parse_rejects_unsupported,
        test_build_and_verify,
        test_verify_detects_mismatch,
        test_parse_fence_tags,
        test_design_system_applied,
        test_diagram_shapes,
        test_card_layout_and_fallback,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print("PASS %s" % t.__name__)
        except Exception as e:  # noqa: BLE001 — 단독 하니스: 모든 실패를 보고
            failed += 1
            print("FAIL %s: %r" % (t.__name__, e))
    print("%d/%d passed" % (len(tests) - failed, len(tests)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

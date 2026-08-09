# dev-briefing.md -> dev-briefing.pptx 생성기.
#
# md 계약 요약 (정본: docs/work/20260809-dev-briefing/req-design.md DES-01):
#   - 문서 첫 '# ' 줄: 덱 제목(표지). 첫 '##' 전의 '- ' 줄은 표지 부제, '> 노트:'는 표지 노트.
#   - 각 '## ' 줄: 본문 슬라이드 1장.
#   - '- ' / '  - ' : 불릿(2단까지). ``` 펜스: 고정폭 단락. '> 노트:'(연속 '>' 줄 포함): 발표자 노트.
#   - 그 외 요소(표·이미지·### 등)는 오류로 중단한다 — 조용히 누락된 덱을 만들지 않는다.
#
# 실행: python make_pptx.py [입력.md] [출력.pptx]  (인자 없으면 같은 폴더의 dev-briefing.*)
# 생성 직후 결과 파일을 다시 열어 슬라이드 수·제목·노트를 md와 대조한다(AC-02).
import os
import sys

KOREAN_FONT = "맑은 고딕"
CODE_FONT = "Consolas"


class MdContractError(Exception):
    pass


class BodySlide:
    def __init__(self, title):
        self.title = title
        self.blocks = []  # ("bullet", level, text) | ("code", text)
        self.notes = ""


class Deck:
    def __init__(self):
        self.title = None
        self.cover_lines = []
        self.cover_notes = ""
        self.slides = []


def parse_md(text):
    deck = Deck()
    current = None  # None = 표지 영역, 이후 BodySlide
    code_lines = None
    in_notes = False

    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()

        if code_lines is not None:
            if line.startswith("```"):
                current.blocks.append(("code", "\n".join(code_lines)))
                code_lines = None
            else:
                code_lines.append(raw)
            continue

        if not line.strip():
            in_notes = False
            continue

        if line.startswith("## "):
            current = BodySlide(line[3:].strip())
            deck.slides.append(current)
            in_notes = False
        elif line.startswith("# ") and deck.title is None and current is None:
            deck.title = line[2:].strip()
        elif line.startswith("```"):
            if current is None:
                raise MdContractError("line %d: code block not allowed on cover" % lineno)
            code_lines = []
        elif line.startswith("> 노트:"):
            note = line[len("> 노트:"):].strip()
            if current is None:
                deck.cover_notes = (deck.cover_notes + "\n" + note).strip()
            else:
                current.notes = (current.notes + "\n" + note).strip()
            in_notes = True
        elif line.startswith(">") and in_notes:
            note = line.lstrip(">").strip()
            if current is None:
                deck.cover_notes += "\n" + note
            else:
                current.notes += "\n" + note
        elif line.startswith("- "):
            if current is None:
                deck.cover_lines.append(line[2:].strip())
            else:
                current.blocks.append(("bullet", 0, line[2:].strip()))
            in_notes = False
        elif line.startswith("  - "):
            if current is None:
                raise MdContractError("line %d: nested bullet not allowed on cover" % lineno)
            current.blocks.append(("bullet", 1, line[4:].strip()))
            in_notes = False
        else:
            raise MdContractError(
                "line %d: unsupported construct: %r" % (lineno, line[:60])
            )

    if code_lines is not None:
        raise MdContractError("unterminated code fence")
    if deck.title is None:
        raise MdContractError("missing deck title ('# ...') on first line")
    if not deck.slides:
        raise MdContractError("no body slides ('## ...') found")
    return deck


def _style_paragraph(para, size_pt, mono=False, bullet=True):
    from lxml import etree
    from pptx.oxml.ns import qn
    from pptx.util import Pt

    if not bullet:
        pPr = para._p.get_or_add_pPr()
        for tag in ("a:buChar", "a:buAutoNum", "a:buNone"):
            for el in pPr.findall(qn(tag)):
                pPr.remove(el)
        etree.SubElement(pPr, qn("a:buNone"))

    runs = para.runs or [para.add_run()]
    for run in runs:
        run.font.size = Pt(size_pt)
        run.font.name = CODE_FONT if mono else KOREAN_FONT
        rPr = run._r.get_or_add_rPr()
        ea = rPr.find(qn("a:ea"))
        if ea is None:
            ea = etree.SubElement(rPr, qn("a:ea"))
        ea.set("typeface", KOREAN_FONT)


def _fill_body(text_frame, blocks):
    first = True
    for block in blocks:
        if block[0] == "bullet":
            _, level, text = block
            para = text_frame.paragraphs[0] if first else text_frame.add_paragraph()
            first = False
            para.text = text
            para.level = level
            _style_paragraph(para, 20 if level == 0 else 17)
        else:  # code
            for code_line in block[1].split("\n"):
                para = text_frame.paragraphs[0] if first else text_frame.add_paragraph()
                first = False
                para.text = code_line
                _style_paragraph(para, 13, mono=True, bullet=False)


def _place(shape, left, top, width, height):
    from pptx.util import Inches

    shape.left = Inches(left)
    shape.top = Inches(top)
    shape.width = Inches(width)
    shape.height = Inches(height)


def build_pptx(deck, out_path):
    from pptx import Presentation
    from pptx.util import Inches

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    cover = prs.slides.add_slide(prs.slide_layouts[0])
    cover.shapes.title.text = deck.title
    _place(cover.shapes.title, 0.9, 2.2, 11.5, 1.6)
    for para in cover.shapes.title.text_frame.paragraphs:
        _style_paragraph(para, 40)
    subtitle = cover.placeholders[1]
    _place(subtitle, 0.9, 4.0, 11.5, 2.2)
    subtitle.text = "\n".join(deck.cover_lines)
    for para in subtitle.text_frame.paragraphs:
        _style_paragraph(para, 18)
    if deck.cover_notes:
        cover.notes_slide.notes_text_frame.text = deck.cover_notes

    for spec in deck.slides:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = spec.title
        _place(slide.shapes.title, 0.5, 0.3, 12.3, 1.0)
        for para in slide.shapes.title.text_frame.paragraphs:
            _style_paragraph(para, 30)
        body = slide.placeholders[1]
        _place(body, 0.5, 1.5, 12.3, 5.7)
        _fill_body(body.text_frame, spec.blocks)
        if spec.notes:
            slide.notes_slide.notes_text_frame.text = spec.notes

    prs.save(out_path)


def verify_pptx(deck, out_path):
    from pptx import Presentation

    problems = []
    prs = Presentation(out_path)
    slides = list(prs.slides)
    expected = 1 + len(deck.slides)
    if len(slides) != expected:
        problems.append("slide count: expected %d, got %d" % (expected, len(slides)))
        return problems

    expected_titles = [deck.title] + [s.title for s in deck.slides]
    expected_notes = [deck.cover_notes] + [s.notes for s in deck.slides]
    for i, (slide, title, notes) in enumerate(zip(slides, expected_titles, expected_notes)):
        actual = slide.shapes.title.text if slide.shapes.title else ""
        if actual != title:
            problems.append("slide %d title: expected %r, got %r" % (i + 1, title, actual))
        if notes:
            actual_notes = (
                slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
            )
            if actual_notes != notes:
                problems.append("slide %d notes mismatch" % (i + 1))
    return problems


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    base = os.path.dirname(os.path.abspath(__file__))
    md_path = argv[1] if len(argv) > 1 else os.path.join(base, "dev-briefing.md")
    out_path = argv[2] if len(argv) > 2 else os.path.join(base, "dev-briefing.pptx")

    try:
        import pptx  # noqa: F401
    except ImportError:
        print("python-pptx is required: pip install python-pptx")
        return 1

    with open(md_path, "r", encoding="utf-8-sig") as f:
        text = f.read()
    try:
        deck = parse_md(text)
    except MdContractError as e:
        print("md contract violation: %s" % e)
        return 1

    build_pptx(deck, out_path)
    problems = verify_pptx(deck, out_path)
    if problems:
        for p in problems:
            print("MISMATCH %s" % p)
        return 1
    print(
        "OK: %d slides (cover + %d), titles and notes match -> %s"
        % (1 + len(deck.slides), len(deck.slides), os.path.basename(out_path))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

"""Build an Instagram carousel (1080x1350 PNGs) from a lesson JSON spec.

Usage:
  python3 tools/build_lesson.py lessons/urok-16.json posts/2026-10-22-urok-16   (fonts come from fonts/manrope)

Spec format (all text in Russian, plain strings; no HTML):
{
  "lesson": 16,                      # number shown in the header; omit for non-lesson posts
  "header": "ФИНАНСЫ ДЛЯ ЧАЙНИКОВ",  # optional, default shown
  "slides": [ {"type": ..., ...}, ... ]
}
Slide types and their fields:
  cover      title, subtitle?, receipt?: [[label, amount], ...]  (max 3 lines)
  statement  label, big_lines: [..] (2-5 short lines), body?
  explain    label, heading, body?, callout?
  receipt    label, items: [[name, amount], ...] (max 7), totals: [[label, value, "accent"?], ...], after?, note?
  steps      label, items: [[title, desc], ...] (max 4)
  questions  label, heading, cards: [..] (max 3), conclusion?
  truth      text                                  (red "Неприятная правда" slide)
  checklist  label?, items: [..] (max 5)           (label default "5 МИНУТ ПРЯМО СЕЙЧАС")
  final      heading, save_text?, cta_title?, cta_sub?, book?   (book = one line about the book)
"""
import html, json, sys, pathlib
from playwright.sync_api import sync_playwright

BG, INK, GREEN, MUTED, SUB, CARD, RED = "#F4EFE7", "#1E2A23", "#2F4A3A", "#5B6B61", "#3E4F45", "#FFFDF9", "#8E2A20"
e = html.escape


def label(t, color=GREEN):
    return f'<div style="font-size:36px;font-weight:800;letter-spacing:0.06em;color:{color}">{e(t.upper())}</div>'


def pill(t, bg=GREEN, fg=BG):
    return f'<div style="align-self:flex-start;background:{bg};color:{fg};border-radius:999px;padding:14px 32px;font-size:32px;font-weight:800;letter-spacing:0.08em">{e(t.upper())}</div>'


def row(a, b, size=36, weight=600, color=INK, bcolor=None):
    return (f'<div style="display:flex;justify-content:space-between;gap:24px;font-size:{size}px;font-weight:{weight};color:{color}">'
            f'<span>{e(a)}</span><span style="white-space:nowrap;color:{bcolor or color}">{e(b)}</span></div>')


def body_cover(s):
    out = [f'<h1 style="margin:0;font-size:{112 if len(s["title"]) <= 34 else 92}px;line-height:1.02;font-weight:800;letter-spacing:-0.02em">{e(s["title"])}</h1>']
    if s.get("subtitle"):
        out.append(f'<p style="margin:0;font-size:42px;line-height:1.3;font-weight:500;color:{SUB}">{e(s["subtitle"])}</p>')
    main = f'<div style="flex-grow:1;display:flex;flex-direction:column;justify-content:center;gap:40px">{"".join(out)}</div>'
    if s.get("receipt"):
        lines = f'<div style="height:2px;background:#ECE5DA"></div>'.join(row(a, b, 34, 600, INK, RED) for a, b in s["receipt"][:3])
        main += f'<div style="background:{CARD};border-radius:28px;padding:36px 44px;display:flex;flex-direction:column;gap:22px">{lines}</div>'
    return main


def body_statement(s):
    big = "".join(f"<span>{e(t)}</span>" for t in s["big_lines"])
    longest = max(len(t) for t in s["big_lines"])
    size = 92 if longest <= 12 and len(s["big_lines"]) <= 4 else 76 if longest <= 17 else 62
    out = label(s["label"]) + f'<div style="display:flex;flex-direction:column;gap:8px;font-size:{size}px;line-height:1.08;font-weight:800;letter-spacing:-0.02em">{big}</div>'
    if s.get("body"):
        out += f'<p style="margin:0;font-size:46px;line-height:1.3;font-weight:500;color:{SUB}">{e(s["body"])}</p>'
    return center(out, 36)


def body_explain(s):
    out = label(s["label"]) + f'<h2 style="margin:0;font-size:{84 if len(s["heading"]) <= 40 else 68}px;line-height:1.08;font-weight:800;letter-spacing:-0.02em">{e(s["heading"])}</h2>'
    if s.get("body"):
        out += f'<p style="margin:0;font-size:44px;line-height:1.35;font-weight:500;color:{SUB}">{e(s["body"])}</p>'
    if s.get("callout"):
        out += f'<div style="background:{GREEN};color:{BG};border-radius:28px;padding:44px 48px;font-size:46px;line-height:1.3;font-weight:700">{e(s["callout"])}</div>'
    return center(out, 40)


def body_receipt(s):
    items = "".join(row(a, b) for a, b in s["items"][:7])
    tots = ""
    for i, t in enumerate(s.get("totals", [])):
        accent = len(t) > 2 and t[2] == "accent"
        style = "border-top:3px dashed #CFC5B6;margin-top:8px;padding-top:22px;" if i == 0 else ""
        tots += (f'<div style="{style}display:flex;justify-content:space-between;font-size:42px;font-weight:800;color:{RED if accent else INK}">'
                 f'<span>{e(t[0])}</span><span>{e(t[1])}</span></div>')
    out = label(s["label"]) + f'<div style="background:{CARD};border-radius:28px;padding:40px 48px;display:flex;flex-direction:column;gap:18px">{items}{tots}</div>'
    if s.get("after"):
        out += f'<p style="margin:0;font-size:54px;line-height:1.2;font-weight:800;letter-spacing:-0.01em">{e(s["after"])}</p>'
    if s.get("note"):
        out += f'<p style="margin:0;font-size:26px;font-weight:500;color:{MUTED}">{e(s["note"])}</p>'
    return center(out, 36)


def body_steps(s):
    out = label(s["label"])
    for i, (t, d) in enumerate(s["items"][:4], 1):
        out += (f'<div style="display:flex;gap:36px;align-items:flex-start">'
                f'<div style="flex-shrink:0;width:96px;height:96px;border-radius:48px;background:{GREEN};color:{BG};display:flex;align-items:center;justify-content:center;font-size:48px;font-weight:800">{i}</div>'
                f'<div style="display:flex;flex-direction:column;gap:10px"><span style="font-size:52px;font-weight:800;line-height:1.15">{e(t)}</span>'
                f'<span style="font-size:38px;font-weight:500;line-height:1.3;color:{SUB}">{e(d)}</span></div></div>')
    return center(out, 44 if len(s["items"]) <= 3 else 32)


def body_questions(s):
    out = label(s["label"]) + f'<h2 style="margin:0;font-size:80px;line-height:1.08;font-weight:800;letter-spacing:-0.02em">{e(s["heading"])}</h2>'
    out += "".join(f'<div style="background:{CARD};border-radius:28px;padding:40px 48px;font-size:48px;line-height:1.25;font-weight:700">{e(c)}</div>' for c in s["cards"][:3])
    if s.get("conclusion"):
        out += f'<p style="margin:0;font-size:52px;line-height:1.2;font-weight:800;color:{GREEN}">{e(s["conclusion"])}</p>'
    return center(out, 36)


def body_truth(s):
    size = 82 if len(s["text"]) <= 110 else 68
    out = (f'<div style="align-self:flex-start;border:3px solid #F6DCD6;border-radius:999px;padding:14px 32px;font-size:32px;font-weight:800;letter-spacing:0.08em;color:#F6DCD6">НЕПРИЯТНАЯ ПРАВДА</div>'
           f'<p style="margin:0;font-size:{size}px;line-height:1.12;font-weight:800;letter-spacing:-0.02em">{e(s["text"])}</p>')
    return center(out, 48)


def body_checklist(s):
    out = pill(s.get("label", "5 минут прямо сейчас"))
    for t in s["items"][:5]:
        out += (f'<div style="display:flex;gap:32px;align-items:center"><span style="flex-shrink:0;width:64px;height:64px;box-sizing:border-box;border:5px solid {GREEN};border-radius:14px"></span>'
                f'<span style="font-size:50px;line-height:1.2;font-weight:700">{e(t)}</span></div>')
    return center(out, 40)


def body_final(s):
    out = f'<h2 style="margin:0;font-size:88px;line-height:1.08;font-weight:800;letter-spacing:-0.02em">{e(s["heading"])}</h2>'
    if s.get("save_text"):
        out += (f'<div style="display:flex;gap:28px;align-items:center"><svg width="56" height="72" viewBox="0 0 56 72" style="flex-shrink:0"><path d="M6 4h44v64L28 52 6 68z" fill="none" stroke="{GREEN}" stroke-width="6" stroke-linejoin="round"/></svg>'
                f'<p style="margin:0;font-size:44px;line-height:1.3;font-weight:600;color:{SUB}">{e(s["save_text"])}</p></div>')
    if s.get("cta_title"):
        out += (f'<div style="background:{GREEN};color:{BG};border-radius:28px;padding:44px 48px;display:flex;flex-direction:column;gap:14px">'
                f'<span style="font-size:50px;line-height:1.2;font-weight:800">{e(s["cta_title"])}</span>'
                + (f'<span style="font-size:38px;line-height:1.3;font-weight:500;color:#D9E3DC">{e(s["cta_sub"])}</span>' if s.get("cta_sub") else "") + "</div>")
    if s.get("book"):
        out += f'<p style="margin:0;font-size:36px;line-height:1.35;font-weight:600;color:{GREEN};border-top:2px solid #DCD3C5;padding-top:28px">{e(s["book"])}</p>'
    return center(out, 44)


def center(inner, gap):
    return f'<div style="flex-grow:1;display:flex;flex-direction:column;justify-content:center;gap:{gap}px">{inner}</div>'


BUILDERS = {k[5:]: v for k, v in globals().items() if k.startswith("body_")}


def page(spec, i, n, s):
    red = s["type"] == "truth"
    bg, fg = (RED, "#FBF4EE") if red else (BG, INK)
    hdr_c, foot_c, arrow_c = ("#F6DCD6", "#F6DCD6", "#F6DCD6") if red else (GREEN, MUTED, GREEN)
    head = spec.get("header", "ФИНАНСЫ ДЛЯ ЧАЙНИКОВ") + (f' · УРОК {spec["lesson"]}' if spec.get("lesson") else "")
    right = "Листайте →" if i < n else "Просто о деньгах"
    return (f'<div style="width:1080px;height:1350px;box-sizing:border-box;padding:88px 96px;background:{bg};color:{fg};font-family:Manrope,sans-serif;display:flex;flex-direction:column;gap:48px">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:700;letter-spacing:0.08em;color:{hdr_c}"><span>{e(head)}</span><span style="letter-spacing:0">{i}/{n}</span></div>'
            f'{BUILDERS[s["type"]](s)}'
            f'<div style="display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:600;color:{foot_c}"><span>@o_finansah_</span><span style="color:{arrow_c if i < n else foot_c}">{right}</span></div></div>')


def main():
    args = sys.argv[1:4] if len(sys.argv) > 3 else sys.argv[1:3] + [str(pathlib.Path(__file__).resolve().parent.parent / "fonts" / "manrope")]
    spec_path, out, fontpkg = (pathlib.Path(a).resolve() for a in args)
    spec = json.loads(spec_path.read_text())
    out.mkdir(parents=True, exist_ok=True)
    font_css = "\n".join((fontpkg / f"{w}.css").read_text().replace("url(./files/", f"url(file://{fontpkg}/files/") for w in (400, 500, 600, 700, 800))
    slides = spec["slides"]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(slides, 1):
            doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{font_css}\nbody{{margin:0}}</style></head><body>{page(spec, i, len(slides), s)}</body></html>"
            tmp = out / "_tmp.html"
            tmp.write_text(doc)
            pg.goto(f"file://{tmp}")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(250)
            box = pg.locator("body > div").first
            overflow = pg.evaluate("(() => { const r = document.querySelector('body > div'); return r.scrollHeight > r.clientHeight + 1; })()")
            box.screenshot(path=str(out / f"slide-{i:02d}.png"))
            tmp.unlink()
            print(f"slide {i}: {s['type']}" + ("  !! TEXT OVERFLOWS — shorten it" if overflow else ""))
        b.close()


if __name__ == "__main__":
    main()

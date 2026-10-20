"""Render carousel artboards (.dc.html) to 1080x1350 PNGs.

Usage: python3 render_slides.py <project_dir> <out_dir> <fonts_package_dir>
Takes every *.dc.html in project_dir in canvas.json order, strips the
Design-canvas wrapper, and screenshots the slide markup with Manrope loaded locally.
"""
import json, re, sys, pathlib
from playwright.sync_api import sync_playwright

project, out, fontpkg = map(pathlib.Path, sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)

css = []
for w in (400, 500, 600, 700, 800):
    t = (fontpkg / f"{w}.css").read_text()
    css.append(t.replace("url(./files/", f"url(file://{fontpkg}/files/"))
font_css = "\n".join(css)

order = json.loads((project / "canvas.json").read_text())["order"]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, name in enumerate(order, 1):
        src = (project / name).read_text()
        body = re.search(r"</helmet>(.*)</x-dc>", src, re.S).group(1)
        html = f"<!doctype html><html><head><meta charset='utf-8'><style>{font_css}\nbody{{margin:0}}</style></head><body>{body}</body></html>"
        tmp = out / f"_slide{i}.html"
        tmp.write_text(html)
        pg.goto(f"file://{tmp}")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        pg.locator("body > div").first.screenshot(path=str(out / f"slide-{i:02d}.png"))
        tmp.unlink()
        print("rendered", name)
    b.close()

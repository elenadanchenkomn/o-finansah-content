# o-finansah-content

Картинки каруселей для Instagram @o_finansah_ («Финансы для чайников»).

- `posts/<дата>-urok-<N>/slide-XX.png` — готовые слайды 1080×1350, их забирает Metricool по прямым ссылкам.
- `lessons/urok-<N>/project/` — исходники слайдов (`.dc.html`, порядок в `canvas.json`).
- `tools/render_slides.py` — рендер исходников в PNG (Playwright + шрифт Manrope из `@fontsource/manrope`).

Рендер: `python3 tools/render_slides.py lessons/urok-15/project posts/2026-10-21-urok-15 <путь к распакованному @fontsource/manrope/package>`

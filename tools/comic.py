"""Comic slide for build_lesson.py: two recurring characters, panels with speech bubbles.

Slide spec:
  comic  title?, label?, panels: [ {caption?, chars: [{who, mood}], bubbles: [{who, text}]} ]  (exactly 1 panel)
    who:  "katya" (путается в деньгах, терракотовый свитер) | "sonya" (разобралась чуть раньше, очки, зелёный свитер)
    mood: neutral | happy | worried | shocked | thinking
    The first char stands on the left, the second on the right. Bubbles go top to bottom,
    each aligned to its speaker's side. One panel per slide. Max bubbles: 3 (2 if the slide has a title),
    keep each bubble under ~80 chars.
"""
import html

INK, GREEN, BG, CARD, SUB = "#1E2A23", "#2F4A3A", "#F4EFE7", "#FFFDF9", "#3E4F45"
SKIN, CHEEK = "#F2C9A5", "#EE9C86"
e = html.escape

CHARS = {
    "katya": {"sweater": "#C8643B", "hair": "#6B3E26", "style": "long"},
    "sonya": {"sweater": GREEN, "hair": "#2A2622", "style": "bob", "glasses": True},
}
S = f'stroke="{INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'


def face(mood):
    eye = lambda x, y, r=6: f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>'
    if mood == "happy":
        eyes = "".join(f'<path d="M{x-9} 104 Q{x} 92 {x+9} 104" fill="none" {S}/>' for x in (78, 122))
        mouth = f'<path d="M84 124 Q100 148 116 124 Z" fill="#7A2E22" {S}/>'
        extra = f'<circle cx="62" cy="122" r="9" fill="{CHEEK}" opacity="0.7"/><circle cx="138" cy="122" r="9" fill="{CHEEK}" opacity="0.7"/>'
        return eyes + mouth + extra
    if mood == "worried":
        return (eye(78, 102) + eye(122, 102)
                + f'<path d="M64 86 L88 78" fill="none" {S}/><path d="M112 78 L136 86" fill="none" {S}/>'
                + f'<path d="M86 134 Q93 127 100 134 Q107 141 114 134" fill="none" {S}/>'
                + f'<path d="M160 62 Q170 78 160 84 Q150 78 160 62 Z" fill="#8EC5E8" stroke="{INK}" stroke-width="3"/>')
    if mood == "shocked":
        return (f'<circle cx="78" cy="102" r="12" fill="#fff" {S}/><circle cx="122" cy="102" r="12" fill="#fff" {S}/>'
                + eye(78, 103, 5) + eye(122, 103, 5)
                + f'<path d="M64 80 Q76 70 88 78" fill="none" {S}/><path d="M112 78 Q124 70 136 80" fill="none" {S}/>'
                + f'<ellipse cx="100" cy="134" rx="9" ry="12" fill="#7A2E22" {S}/>')
    if mood == "thinking":
        return (eye(82, 98) + eye(126, 98)
                + f'<path d="M64 84 L88 82" fill="none" {S}/><path d="M112 76 Q124 68 136 76" fill="none" {S}/>'
                + f'<path d="M90 134 L112 130" fill="none" {S}/>')
    return eye(78, 102) + eye(122, 102) + f'<path d="M88 128 Q100 138 112 128" fill="none" {S}/>'


def character(who, mood, size):
    c = CHARS[who]
    body = f'<path d="M18 262 C18 192 52 172 100 172 C148 172 182 192 182 262 Z" fill="{c["sweater"]}" {S}/>'
    neck = f'<path d="M86 140 L86 176 Q100 186 114 176 L114 140 Z" fill="{SKIN}" {S}/>'
    head = f'<circle cx="100" cy="100" r="58" fill="{SKIN}" {S}/>'
    if c["style"] == "long":
        back = f'<path d="M40 104 C28 40 70 26 100 26 C134 26 174 42 160 104 L168 206 C150 214 132 196 138 176 L62 176 C68 196 50 214 32 206 Z" fill="{c["hair"]}" {S}/>'
        front = f'<path d="M42 92 C42 48 72 34 100 34 C130 34 160 50 158 94 C144 74 120 62 104 58 C92 74 66 86 42 92 Z" fill="{c["hair"]}" {S}/>'
    else:
        back = f'<path d="M34 108 C28 42 68 28 100 28 C134 28 172 42 166 108 L168 146 L32 146 Z" fill="{c["hair"]}" {S}/>'
        front = f'<path d="M40 96 C38 48 74 34 106 34 C142 34 164 56 160 98 C150 76 132 62 112 56 C96 72 66 88 40 96 Z" fill="{c["hair"]}" {S}/>'
    glasses = ""
    if c.get("glasses"):
        glasses = (f'<circle cx="78" cy="102" r="17" fill="none" stroke="{INK}" stroke-width="4"/>'
                   f'<circle cx="122" cy="102" r="17" fill="none" stroke="{INK}" stroke-width="4"/>'
                   f'<path d="M95 100 Q100 96 105 100" fill="none" stroke="{INK}" stroke-width="4"/>')
    return (f'<svg width="{size}" height="{size * 1.3:.0f}" viewBox="0 0 200 260" style="display:block;flex-shrink:0">'
            f'{back}{body}{neck}{head}{front}{face(mood)}{glasses}</svg>')


def bubble(text, side, fs):
    left = side == "left"
    tail_pos = "left:70px" if left else "right:70px"
    tail = (f'<div style="position:absolute;bottom:-26px;{tail_pos};width:0;height:0;border-left:18px solid transparent;border-right:18px solid transparent;border-top:26px solid {INK}"></div>'
            f'<div style="position:absolute;bottom:-17px;{"left:75px" if left else "right:75px"};width:0;height:0;border-left:13px solid transparent;border-right:13px solid transparent;border-top:19px solid #fff"></div>')
    return (f'<div style="align-self:{"flex-start" if left else "flex-end"};max-width:78%;position:relative;background:#fff;border:5px solid {INK};border-radius:36px;'
            f'padding:22px 32px;font-size:{fs}px;line-height:1.22;font-weight:700;color:{INK}">{e(text)}{tail}</div>')


def panel(p, mode):
    fs, size, maxb = {"title": (38, 220, 2), "one": (40, 220, 3)}[mode]
    compact = mode != "one"
    chars = p.get("chars", [])
    side_of = {ch["who"]: ("left" if i == 0 else "right") for i, ch in enumerate(chars)}
    cap = (f'<div style="align-self:flex-start;background:#F6D77A;border:4px solid {INK};border-radius:10px;padding:8px 20px;font-size:28px;font-weight:800;letter-spacing:0.04em">{e(p["caption"].upper())}</div>'
           if p.get("caption") else "")
    bubbles = "".join(bubble(b["text"], side_of.get(b["who"], "left"), fs) for b in p.get("bubbles", [])[:maxb])
    figs = "".join(character(ch["who"], ch.get("mood", "neutral"), size) for ch in chars[:2])
    just = "space-between" if len(chars) > 1 else ("flex-start" if side_of and list(side_of.values())[0] == "left" else "flex-end")
    return (f'<div data-ov="1" style="flex:1;min-height:0;background:#EAF0EA;border:5px solid {INK};border-radius:28px;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;padding:32px 36px 0">'
            f'<div style="display:flex;flex-direction:column;gap:{30 if compact else 38}px">{cap}{bubbles}</div>'
            f'<div style="display:flex;justify-content:{just};align-items:flex-end;padding:0 24px;margin-top:12px">{figs}</div></div>')


def body_comic(s):
    out = ""
    if s.get("label"):
        out += f'<div style="font-size:36px;font-weight:800;letter-spacing:0.06em;color:{GREEN}">{e(s["label"].upper())}</div>'
    if s.get("title"):
        out += f'<h1 style="margin:0;font-size:{88 if len(s["title"]) <= 30 else 72}px;line-height:1.04;font-weight:800;letter-spacing:-0.02em">{e(s["title"])}</h1>'
    panels = s["panels"][:1]
    mode = "title" if s.get("title") else "one"
    out += "".join(panel(p, mode) for p in panels)
    return f'<div style="flex-grow:1;min-height:0;display:flex;flex-direction:column;gap:32px">{out}</div>'

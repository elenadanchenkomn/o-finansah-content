"""Comic slide for build_lesson.py: two recurring characters, panels with speech bubbles.

Slide spec:
  comic  title?, label?, panels: [ {caption?, chars: [{who, mood}], bubbles: [{who, text}]} ]  (exactly 1 panel)
    who:  "masya" (девушка, разобралась чуть раньше — голос блога, зелёное худи)
          | "vasya" (парень, путается в деньгах и попадает в типичные ситуации, терракотовое худи)
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
    # Мася — разобралась чуть раньше (голос блога): пучок, шторка-чёлка, серьги-кольца, зелёное худи
    "masya": {"hoodie": GREEN, "hood": "#456B55", "hair": "#C4924F", "skin": "#F2C9A5", "style": "bun"},
    # Вася — путается в деньгах и попадает в типичные ситуации: кудрявый верх, щетина, терракотовое худи
    "vasya": {"hoodie": "#C8643B", "hood": "#A9512D", "hair": "#3A2A20", "skin": "#E2AE86", "style": "curly"},
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
    sk = c["skin"]
    body = f'<path d="M14 262 C14 190 50 168 100 168 C150 168 186 190 186 262 Z" fill="{c["hoodie"]}" {S}/>'
    hood = f'<path d="M56 178 Q100 214 144 178 Q132 168 100 168 Q68 168 56 178 Z" fill="{c["hood"]}" {S}/>'
    strings = (f'<path d="M88 200 L86 236" fill="none" stroke="#F4EFE7" stroke-width="5" stroke-linecap="round"/>'
               f'<path d="M112 200 L114 236" fill="none" stroke="#F4EFE7" stroke-width="5" stroke-linecap="round"/>')
    neck = f'<path d="M86 140 L86 180 Q100 190 114 180 L114 140 Z" fill="{sk}" {S}/>'
    head = f'<circle cx="100" cy="100" r="58" fill="{sk}" {S}/>'
    back = front = extra = ears = ""
    if c["style"] == "bun":
        back = (f'<circle cx="100" cy="30" r="26" fill="{c["hair"]}" {S}/>'
                f'<rect x="84" y="40" width="32" height="12" rx="6" fill="#E07A8B" {S}/>'
                f'<path d="M42 112 C34 50 70 36 100 36 C130 36 166 50 158 112 L158 152 Q146 154 144 132 L56 132 Q54 154 42 152 Z" fill="{c["hair"]}" {S}/>')
        front = (f'<path d="M42 108 C42 56 76 40 100 42 C124 40 158 56 158 108 C154 90 142 76 122 70 Q108 66 102 80 Q96 66 80 70 C60 76 48 90 42 108 Z" fill="{c["hair"]}" {S}/>'
                 f'<path d="M44 96 Q38 128 52 156 Q58 130 58 100 Z" fill="{c["hair"]}" {S}/>'
                 f'<path d="M156 96 Q162 128 148 156 Q142 130 142 100 Z" fill="{c["hair"]}" {S}/>')
        extra = (f'<circle cx="42" cy="150" r="8" fill="none" stroke="#D9A441" stroke-width="4"/>'
                 f'<circle cx="158" cy="150" r="8" fill="none" stroke="#D9A441" stroke-width="4"/>')
    else:
        ears = f'<circle cx="42" cy="106" r="13" fill="{sk}" {S}/><circle cx="158" cy="106" r="13" fill="{sk}" {S}/>'
        front = (f'<path d="M44 98 C36 66 48 42 68 40 C74 22 100 18 112 30 C126 18 152 26 154 46 C168 54 166 84 156 98 '
                 f'C150 80 140 72 128 70 C112 76 82 74 64 72 C54 78 48 88 44 98 Z" fill="{c["hair"]}" {S}/>')
        extra = f'<path d="M50 118 Q100 176 150 118 Q142 150 100 156 Q58 150 50 118 Z" fill="#5A4436" opacity="0.22"/>'
    return (f'<svg width="{size}" height="{size * 1.3:.0f}" viewBox="0 0 200 260" style="display:block;flex-shrink:0">'
            f'{back}{body}{hood}{strings}{neck}{ears}{head}{front}{extra}{face(mood)}</svg>')


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

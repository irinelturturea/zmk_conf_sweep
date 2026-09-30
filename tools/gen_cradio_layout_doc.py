#!/usr/bin/env python3
"""Generează documentația keymap-ului cradio (34 taste, Colemak-DH) — varianta
îngustă, pentru citit pe ecran fără scroll orizontal și pentru printat/PDF.

Citește `config/cradio.keymap` și scrie:
  - cradio-layout-de.md    (markdown, blocuri monospace înguste)
  - cradio-layout-de.html  (pentru print/PDF: A4 portrait, o zonă per layer)

Convenție: în tabele stă DOAR caracterul real care iese pe un host cu tastatură
germană (QWERTZ). Simboluri: `×` = nimic (&none), `↓` = passthrough (&trans,
cade pe layer 0). Modificatorii ținuți (home-row mods, lt) sunt pe linia
„Ținut" de sub fiecare layer, ca să nu încarce căsuțele.

Surse pentru maparea poziție fizică → caracter pe layout german:
  - https://kbdlayout.info/KBDGR/  (KBDGR.DLL, Windows de-DE)
  - https://en.wikipedia.org/wiki/German_keyboard_layout
Regenerare:  python3 tools/gen_cradio_layout_doc.py   (din rădăcina repo-ului)
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
KEYMAP = REPO / "config" / "cradio.keymap"
OUT_MD = REPO / "cradio-layout-de.md"
OUT_HTML = REPO / "cradio-layout-de.html"

KEYS_PER_SIDE = 5
POSITIONS_PER_LAYER = 34
NONE_SYM = "×"
TRANS_SYM = "↓"
MISSING = "<n/a>"          # marcaj intern pentru bindings nemapate (nu ajunge în document)

# Note de intenție per layer (Irinel, 30.09.2026) — apar sub grila layerului.
LAYER_NOTES = {
    1: "**Intenționat:** layer 1 ține literele în aranjamentul **US** (QWERTY ca "
       "usage-uri), nu în pozițiile Colemak-DH — pentru un host US sau software care "
       "așteaptă US. Pe host german rezultă `q w e r t y u i o p`.",
    3: "Simbolurile urmează aranjarea din **Neo2** (layerul **Mod3** al layout-ului "
       "german ergonomic Neo), nu pozițiile AltGr ale unei tastaturi germane "
       "obișnuite: simbolurile de programare stau pe rândul de sus, grupate după "
       "frecvență. Umlautele (ä ö ü ß) sunt în layer 4.",
}

# ---------------------------------------------------------------------------
# Tastă ZMK -> ce iese pe layout GERMAN (QWERTZ), pe poziția FIZICĂ a tastelor.
# ZMK trimite usage-ul HID al tastelor US; Windows/Linux cu layout german
# traduce poziția în caracterul german.
#   (neapăsat, cu Shift, cu AltGr)
# ---------------------------------------------------------------------------
KEY_TO_DE = {
    "Q": ("q", "Q", None), "W": ("w", "W", None), "E": ("e", "E", None),
    "R": ("r", "R", None), "T": ("t", "T", None), "Y": ("z", "Z", None),  # Y fizic = z pe DE
    "U": ("u", "U", None), "I": ("i", "I", None), "O": ("o", "O", None),
    "P": ("p", "P", None), "A": ("a", "A", None), "S": ("s", "S", None),
    "D": ("d", "D", None), "F": ("f", "F", None), "G": ("g", "G", None),
    "H": ("h", "H", None), "J": ("j", "J", None), "K": ("k", "K", None),
    "L": ("l", "L", None), "Z": ("y", "Y", None),  # Z fizic = y pe DE
    "X": ("x", "X", None), "C": ("c", "C", None), "V": ("v", "V", None),
    "B": ("b", "B", None), "N": ("n", "N", None), "M": ("m", "M", None),
    "N1": ("1", "!", None), "N2": ("2", '"', None), "N3": ("3", "§", None),
    "N4": ("4", "$", None), "N5": ("5", "%", None), "N6": ("6", "&", None),
    "N7": ("7", "/", None), "N8": ("8", "(", None), "N9": ("9", ")", None),
    "N0": ("0", "=", None),
    "COMMA": (",", ";", None),
    "DOT": (".", ":", None),
    "SLASH": ("-", "_", None),
    "MINUS": ("ß", "?", None),
    "SEMI": ("ö", "Ö", None),
    "SINGLE_QUOTE": ("ä", "Ä", None),
    "LEFT_BRACKET": ("ü", "Ü", None),
    "RIGHT_BRACKET": ("+", "*", None),
    "EQUAL": ("´", "`", None),
    "GRAVE": ("^", "°", None),
    "NUHS": ("'", "#", None),
    "NUBS": ("<", ">", "|"),
    "RBKT": ("+", "*", None),             # alias ZMK pentru RIGHT_BRACKET
    "LBKT": ("ü", "Ü", None),             # alias ZMK pentru LEFT_BRACKET
}
ALTGR = {
    "Q": "@", "E": "€",
    "N7": "{", "N8": "[", "N9": "]",
    "N0": "}", "MINUS": "\\", "NUBS": "|", "RBKT": "~",
    "N2": "²", "N3": "³",
}
SHORT = {
    "SPACE": "Spc", "RET": "Ent", "TAB": "Tab", "ESC": "Esc", "BSPC": "BkSp",
    "DEL": "Del", "INS": "Ins", "HOME": "Home", "END": "End",
    "PG_UP": "PgUp", "PG_DN": "PgDn",
    "UP_ARROW": "↑", "UP": "↑", "DOWN_ARROW": "↓", "DOWN": "↓",
    "LEFT": "←", "LEFT_ARROW": "←", "RIGHT": "→", "RIGHT_ARROW": "→",
    "LCTRL": "LCtrl", "RCTRL": "RCtrl", "LALT": "LAlt", "RALT": "RAlt",
    "LSHFT": "LShft", "RSHFT": "RShft", "LGUI": "LGui", "RGUI": "RGui",
}
for i in range(1, 13):
    SHORT[f"F{i}"] = f"F{i}"
BT_SHORT = {"BT_NXT": "BT+", "BT_PRV": "BT-", "BT_CLR_ALL": "CLR", "BT_CLR": "CLR"}


def de_char(key: str, mods: str = "") -> str:
    """Caracterul german pentru o tastă (cu Shift / AltGr)."""
    if mods == "RA":
        return ALTGR.get(key, MISSING)
    if key in KEY_TO_DE:
        base, shift, _ = KEY_TO_DE[key]
        return shift if "LS" in mods else base
    return SHORT.get(key, MISSING)


# ---------------------------------------------------------------------------
# Parsare keymap
# ----------------------------------------------------------------───────────
def strip_comments(text: str) -> str:
    return re.sub(r"//[^\n]*", "", text)


def parse_combos(raw: str):
    """Combos din blocul `combos { … }`: ordine-agnostic, cu comentariile de deasupra."""
    block = re.search(r"combos\s*\{(.*?)\n    \};", raw, re.S)
    if not block:
        return []
    body = block.group(1)
    combos = []
    for m in re.finditer(r"(\w+)\s*\{(.*?)\}\s*;", strip_comments(body), re.S):
        name, inner = m.group(1), m.group(2)

        def grab(key):
            mm = re.search(rf"{key}\s*=\s*<([^>]*)>", inner)
            return mm.group(1).split() if mm else []

        pos = grab("key-positions")
        if not pos:                     # `compatible = "zmk,combos";` etc.
            continue
        combos.append({
            "name": name,
            "bindings": " ".join(grab("bindings")),
            "positions": pos,
            "timeout": (grab("timeout-ms") or [None])[0],
        })
    comments = {}
    for m in re.finditer(r"((?:[ \t]*//[^\n]*\n)+)[ \t]*(\w+)[ \t]*\{", body):
        text = " ".join(l.strip().lstrip("/").strip() for l in m.group(1).strip().splitlines())
        comments[m.group(2)] = text
    for c in combos:
        c["comment"] = comments.get(c["name"], "")
    return combos


def split_bindings(raw: str):
    tokens, out, cur = raw.split(), [], []
    for tok in tokens:
        if tok.startswith("&") and cur:
            out.append(" ".join(cur))
            cur = [tok]
        else:
            cur.append(tok)
    if cur:
        out.append(" ".join(cur))
    return out


def parse_layers(src: str):
    km = re.search(r"keymap\s*\{(.*)\n        \};", src, re.S)
    if not km:
        sys.exit("nu găsesc blocul keymap")
    layers = []
    for m in re.finditer(
        r"(\w+)\s*\{\s*display-name\s*=\s*\"([^\"]*)\";\s*bindings\s*=\s*<(.*?)>\s*;",
        km.group(1),
        re.S,
    ):
        layers.append({
            "id": m.group(1),
            "name": m.group(2),
            "bindings": split_bindings(m.group(3)),
        })
    return layers


# ---------------------------------------------------------------------------
# Randare: o căsuță = caracterul real + (opțional) nota de „ținut"
# ---------------------------------------------------------------------------
def cell(binding: str):
    """(textul din căsuță, nota de ținut sau None)."""
    b = binding.strip()
    if b == "&none":
        return NONE_SYM, None
    if b == "&trans":
        return TRANS_SYM, None
    m = re.match(r"&bt\s+(\w+)(?:\s+(\d+))?", b)
    if m:
        cmd, arg = m.group(1), m.group(2)
        return BT_SHORT.get(cmd, f"BT{arg}") if arg is None else BT_SHORT.get(cmd, f"BT{arg}"), None
    if b.startswith("&tog "):
        return f"L{b[5:].strip()}", None
    m = re.match(r"&(mt|lt|to|mo)\s+(.*)", b)
    if m:
        beh, args = m.group(1), m.group(2).split()
        if beh in ("mt", "lt"):
            hold, tap = args[0], args[-1]
            mm = re.match(r"(LS|RA)\(([^)]+)\)", tap)
            tmod, tkey = (mm.group(1), mm.group(2)) if mm else ("", tap)
            held = SHORT.get(hold, hold) if beh == "mt" else f"L{hold}"
            return de_char(tkey, tmod), held
        if beh == "mo":
            return "–", f"L{args[0]}"
        return f"→{args[0]}", None
    m = re.match(r"&kp\s+(.*)", b)
    if m:
        arg = m.group(1).strip()
        mm = re.match(r"(LS|RA)\(([^)]+)\)", arg)
        if mm:
            return de_char(mm.group(2), "RA" if mm.group(1) == "RA" else "LS"), None
        return de_char(arg), None
    return MISSING, None


def cells_of(bindings):
    return [cell(b) for b in bindings]


def grid(chars, w):
    """Casete înguste: 2 jumătăți de câte 5, apoi rândul de thumbs."""
    gap = "  "

    def border(l, m, r, n):
        return l + m.join("─" * w for _ in range(n)) + r

    def line(cells):
        return "│" + "│".join(c.center(w) for c in cells) + "│"

    top, mid, bot = (border("┌", "┬", "┐", KEYS_PER_SIDE),
                     border("├", "┼", "┤", KEYS_PER_SIDE),
                     border("└", "┴", "┘", KEYS_PER_SIDE))
    lines = [top + gap + top]
    for row in range(3):
        row_cells = chars[row * 10:(row + 1) * 10]
        lines.append(line(row_cells[:5]) + gap + line(row_cells[5:]))
        lines.append((mid if row < 2 else bot) + gap + (mid if row < 2 else bot))
    t_top = border("┌", "┬", "┐", 4)
    t_bot = border("└", "┴", "┘", 4)
    indent = " " * (((w + 1) * 5 + 1 - (w * 4 + 5)) // 2)
    lines += [indent + t_top, indent + line(chars[30:34]), indent + t_bot]
    return "\n".join(lines)


def index_grid(w=2):
    """Grila numerelor de poziție (0-33), o dată la început."""
    nums = [str(i) for i in range(POSITIONS_PER_LAYER)]
    return grid(nums, w)


def hold_note(bindings) -> str | None:
    parts = []
    for pos, b in enumerate(bindings):
        _, held = cell(b)
        if held:
            parts.append(f"{pos} {held}")
    return "Ținut (hold): " + " · ".join(parts) if parts else None


def md_inline(text: str) -> str:
    """Markdown minimal (**bold**, `code`) -> HTML, escapând restul."""
    out = html.escape(text)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def md_layer(idx, layer):
    chars = [c for c, _ in cells_of(layer["bindings"])]
    out = [f"## Layer {idx} — `{layer['id']}`", ""]
    if layer["name"] and layer["name"].lower() != layer["id"].lower():
        out += [f"*{layer['name']}*", ""]
    out += ["```", "", grid(chars, 4), ""]
    note = hold_note(layer["bindings"])
    out += ["```", ""]
    if note:
        out += [note, ""]
    if idx in LAYER_NOTES:
        out += [LAYER_NOTES[idx], ""]
    return out


def html_layer(idx, layer):
    chars = [c for c, _ in cells_of(layer["bindings"])]
    body = [f"<h2>Layer {idx} — {html.escape(layer['id'])}</h2>"]
    if layer["name"] and layer["name"].lower() != layer["id"].lower():
        body.append(f"<p class=\"sub\">{html.escape(layer['name'])}</p>")
    body.append("<pre>" + html.escape(grid(chars, 4)) + "</pre>")
    note = hold_note(layer["bindings"])
    if note:
        body.append(f"<p class=\"note\">{html.escape(note)}</p>")
    if idx in LAYER_NOTES:
        body.append(f"<p class=\"note\">{md_inline(LAYER_NOTES[idx])}</p>")
    return "\n".join(body)


CAPCANE = [
    ("`kp Y` / `kp Z`", "**z / y** — inversate"),
    ("`kp SEMI`", "**ö**"),
    ("`kp SINGLE_QUOTE`", "**ä**"),
    ("`kp LEFT_BRACKET`", "**ü**"),
    ("`kp MINUS`", "**ß** (Shift: ?)"),
    ("`kp SLASH`", "**-** (Shift: _)"),
    ("`kp EQUAL`", "**´** dead key (Shift: `)"),
    ("`kp GRAVE`", "**^** dead key (Shift: °)"),
    ("`kp NUHS`", "**'** (Shift: #)"),
    ("`kp RBKT`", "**+** (Shift: *)"),
    ("`kp NUBS`", "**<** (Shift: >, AltGr: |)"),
    ("`kp LS(N6)`", "**&**"),
    ("`kp LS(N7)`", "**/**"),
    ("`kp LS(N8)`", "**(**"),
    ("`kp LS(N0)`", "**=**"),
    ("`kp LS(COMMA)`", "**;**"),
    ("`kp LS(DOT)`", "**:**"),
    ("`kp RA(N7)`", "**{**"),
    ("`kp RA(N8)` / `kp RA(N9)`", "**[ / ]**"),
    ("`kp RA(N0)`", "**}**"),
    ("`kp RA(Q)`", "**@**"),
    ("`kp RA(MINUS)`", "**\\\\**"),
    ("`kp RA(NUBS)`", "**|**"),
]


def main():
    raw = KEYMAP.read_text(encoding="utf-8")
    layers = parse_layers(strip_comments(raw))
    combos = parse_combos(raw)
    for l in layers:
        if len(l["bindings"]) != POSITIONS_PER_LAYER:
            sys.exit(f"layer {l['id']}: {len(l['bindings'])} bindings, aștept 34")

    unknown = [(idx, pos, b) for idx, l in enumerate(layers)
               for pos, b in enumerate(l["bindings"]) if MISSING in cell(b)[0]]
    if unknown:
        sys.exit("bindings nemapate (adaugă-le în KEY_TO_DE/SHORT/BT_SHORT): "
                 + ", ".join(f"L{i}:{p}={b}" for i, p, b in unknown))

    try:
        rev = subprocess.check_output(
            ["git", "-C", str(REPO), "log", "-1", "--format=%h", "--", "config/cradio.keymap"],
            text=True).strip()
        branch = subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
    except Exception:
        rev, branch = "?", "?"

    head = [
        "# cradio 34 — keymap pentru host german (Colemak-DH)",
        "",
        f"`config/cradio.keymap`, branch `{branch}`, keymap la commit `{rev}` · "
        f"generat {date.today().isoformat()} cu `tools/gen_cradio_layout_doc.py`.",
        "",
        "În tabele stă **doar caracterul care iese efectiv**, presupunând că sistemul "
        "folosește tastatură **germană (QWERTZ)**. Firmware-ul trimite coduri de tastă "
        "în ordinea tastaturii US, iar sistemul le traduce prin layout-ul german — de "
        "aceea ce scrie în keymap nu e ce vezi pe ecran: **Z și Y sunt inversate**, "
        "umlautele stau pe poziții de punctuație, o parte din simboluri cer **AltGr**.",
        "",
        f"`{NONE_SYM}` = nicio acțiune (`&none`) · `{TRANS_SYM}` = passthrough (`&trans`, "
        "cade pe layer 0) · `L2` = comută layer 2 · `Spc`/`Ent`/`BkSp` = Space/Enter/Backspace.",
        "Modificatorii ținuți (home-row mods) sunt pe linia *Ținut* de sub fiecare layer.",
        "",
        "## Pozițiile tastelor (0-33)",
        "",
        "```",
        "",
        index_grid(),
        "",
        "```",
        "",
        "---",
        "",
    ]

    md = list(head)
    for idx, layer in enumerate(layers):
        md += md_layer(idx, layer)
        md.append("---")
        md.append("")

    md += [
        "## Combos (poziții fizice — nu depind de layout-ul sistemului)",
        "",
        "| Combo | Poziții | Efect |",
        "|---|---|---|",
    ]
    for c in combos:
        tmo = f" (+{c['timeout']}ms)" if c["timeout"] else ""
        md.append(f"| `{c['name']}`{tmo} | {', '.join(c['positions'])} | `{c['bindings']}` |")
    md.append("")
    for c in combos:
        if c["comment"]:
            md.append(f"- **{c['name']}**: {c['comment']}")
    md += [
        "",
        "---",
        "",
        "## Capcanele layout-ului german",
        "",
        "| Ce scrie în keymap | Pe host german iese |",
        "|---|---|",
    ]
    md += [f"| {a} | {b} |" for a, b in CAPCANE]
    md += [
        "",
        "**Layer 1 (`qwertz`) e intenționat**: ține literele în aranjamentul **US** "
        "(QWERTY ca usage-uri), nu în pozițiile Colemak-DH — pentru un host US sau "
        "software care așteaptă US. Pe host german rezultă `q w e r t y u i o p`.",
        "",
        "**Simbolurile** din layer 3 urmează aranjarea din **Neo2** (layerul Mod3 al "
        "layout-ului german ergonomic Neo), nu pozițiile AltGr ale unei tastaturi "
        "germane obișnuite.",
        "",
        "## Surse",
        "",
        "- https://kbdlayout.info/KBDGR/ — layout-ul Windows de-DE",
        "- https://en.wikipedia.org/wiki/German_keyboard_layout — QWERTZ, umlaute, AltGr",
        "- https://neo-layout.org/ — layout-ul Neo (Neo2): sursa aranjării layerului de simboluri",
        "- `config/cradio.keymap` — sursa de adevăr pentru bindings",
        "",
        "Regenerare (după orice modificare de keymap): `python3 tools/gen_cradio_layout_doc.py` "
        "— scrie și `cradio-layout-de.md`, și `cradio-layout-de.html` (pentru print/PDF).",
        "",
    ]

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    # ---------------- HTML (print/PDF) ----------------
    h = [
        "<!doctype html>", '<html lang="ro">', "<head>", '<meta charset="utf-8">',
        "<title>cradio 34 — keymap (host german)</title>", "<style>",
        "@page { size: A4 portrait; margin: 12mm; }",
        "body { font: 9.5pt/1.4 'DejaVu Sans', system-ui, sans-serif; color:#000; }",
        "h1 { font-size: 15pt; margin: 0 0 6pt }",
        "h2 { font-size: 12pt; margin: 12pt 0 2pt }",
        "p { margin: 0 0 6pt } .sub { font-style: italic; font-size: 8.6pt }",
        "pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.4pt; line-height: 1.15;",
        "      margin: 2pt 0 4pt; page-break-inside: avoid; }",
        "table { border-collapse: collapse; font-size: 8.4pt; margin: 2pt 0 6pt;",
        "        page-break-inside: avoid; }",
        "th, td { border: 0.4pt solid #aaa; padding: 1pt 4pt; text-align: left; vertical-align: top }",
        ".note { font-size: 8.4pt; } .layer { page-break-inside: avoid; }",
        "ul { margin: 0 0 6pt; padding-left: 14pt }",
        "</style>", "</head>", "<body>",
        "<h1>cradio 34 — keymap pentru host german (Colemak-DH)</h1>",
        f"<p class=\"sub\"><code>config/cradio.keymap</code>, branch <code>{html.escape(branch)}</code>, "
        f"keymap la commit <code>{html.escape(rev)}</code> · generat {date.today().isoformat()}</p>",
        "<p>În tabele stă doar caracterul care iese efectiv, cu sistemul pe tastatură "
        "<b>germană (QWERTZ)</b>: Z și Y sunt inversate, umlautele stau pe poziții de "
        "punctuație, o parte din simboluri cer <b>AltGr</b>.</p>",
        f"<p class=\"note\"><code>{NONE_SYM}</code> = nicio acțiune · <code>{TRANS_SYM}</code> = "
        "passthrough (cade pe layer 0) · <code>L2</code> = comută layer 2 · "
        "<code>Spc</code>/<code>Ent</code>/<code>BkSp</code> = Space/Enter/Backspace. "
        "Modificatorii ținuți sunt pe linia <i>Ținut</i>.</p>",
        "<h2>Pozițiile tastelor (0-33)</h2>",
        "<pre>" + html.escape(index_grid()) + "</pre>",
    ]
    for idx, layer in enumerate(layers):
        h.append(f"<div class=\"layer\">{html_layer(idx, layer)}</div>")
    h.append("<h2>Combos (poziții fizice)</h2><table><tr><th>Combo</th><th>Poziții</th><th>Efect</th></tr>")
    for c in combos:
        tmo = f" (+{c['timeout']}ms)" if c["timeout"] else ""
        h.append(f"<tr><td><code>{html.escape(c['name'])}</code>{tmo}</td>"
                 f"<td>{html.escape(', '.join(c['positions']))}</td>"
                 f"<td><code>{html.escape(c['bindings'])}</code></td></tr>")
    h.append("</table><ul>")
    for c in combos:
        if c["comment"]:
            h.append(f"<li><b>{html.escape(c['name'])}</b>: {html.escape(c['comment'])}</li>")
    h.append("</ul>")
    h.append("<h2>Capcanele layout-ului german</h2><table><tr><th>Ce scrie în keymap</th>"
             "<th>Pe host german iese</th></tr>")
    for a, b in CAPCANE:
        h.append(f"<tr><td><code>{html.escape(a.strip('`'))}</code></td><td>"
                 f"{html.escape(b.replace('**', ''))}</td></tr>")
    h.append("</table>")
    h.append("<p class=\"note\">Layer 1 (<code>qwertz</code>) e intenționat: ține literele "
             "în aranjamentul US (QWERTY ca usage-uri), nu în pozițiile Colemak-DH — pentru "
             "un host US sau software care așteaptă US. Pe host german rezultă "
             "<code>q w e r t y u i o p</code>. Simbolurile din layer 3 urmează aranjarea "
             "din <b>Neo2</b> (layerul Mod3), nu pozițiile AltGr germane.</p>")
    h.append("<p class=\"note\">Surse: kbdlayout.info/KBDGR (Windows de-DE), "
             "en.wikipedia.org/wiki/German_keyboard_layout, <code>config/cradio.keymap</code>. "
             "Regenerare: <code>python3 tools/gen_cradio_layout_doc.py</code>.</p>")
    h += ["</body>", "</html>", ""]
    OUT_HTML.write_text("\n".join(h), encoding="utf-8")

    print(f"scris {OUT_MD.name} ({len(md)} linii) și {OUT_HTML.name} · "
          f"{len(layers)} layere, {len(combos)} combos")


if __name__ == "__main__":
    main()

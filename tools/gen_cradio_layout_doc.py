#!/usr/bin/env python3
"""Generate the graphical layout documentation for the cradio 34 keymap.

Reads `config/cradio.keymap` and writes:
  - cradio-layout-de.md    (markdown, narrow monospace blocks)
  - cradio-layout-de.html  (print source: A4 portrait, one block per layer)

Everything is in English because this is a public repository.

Convention: a cell shows ONLY the character that actually comes out on a host
running a **German (QWERTZ, de-DE) keyboard layout**. Two ASCII markers keep the
grids printer-safe (box-drawing glyphs fall back to non-monospace fonts in many
renderers and break the alignment):
  - `..` = no action (`&none`)
  - `==` = passthrough (`&trans` — falls through to layer 0)
Held modifiers (home-row mods, `&lt`) are listed on one `Hold:` line under each
layer instead of inside the cells, so the cells stay one character wide.

German mapping sources (physical position -> character):
  - https://kbdlayout.info/KBDGR/  (KBDGR.DLL, Windows de-DE)
  - https://en.wikipedia.org/wiki/German_keyboard_layout
Regenerate:  python3 tools/gen_cradio_layout_doc.py   (from the repo root)
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
NONE_SYM = ".."            # marker for &none
TRANS_SYM = "=="           # marker for &trans (passthrough to layer 0)
MISSING = "<n/a>"          # internal marker for unmapped bindings (never written out)

# Per-layer intent notes, supplied by the keymap author — rendered under the grid.
LAYER_NOTES = {
    1: "**Intentional:** layer 1 keeps the letters in the **US** arrangement (QWERTY "
       "key usages), not in the Colemak-DH positions — for a US host or software that "
       "expects a US layout. On a German host it therefore produces "
       "`q w e r t y u i o p`. It is not a German QWERTZ layer.",
    3: "The symbols follow the arrangement of **Neo2** (the *Mod3* layer of the German "
       "ergonomic Neo layout, see neo-layout.org), not the AltGr positions of a regular "
       "German keyboard: programming symbols sit on the top row, grouped by frequency. "
       "The umlauts (ä ö ü ß) are in layer 4.",
}

# English notes for the combos. The keymap keeps its own comments (in the author's
# language); those are printed verbatim when no translation is listed here.
COMBO_NOTES_EN = {
    "toggle_nav": "QWFP (left hand, top row) toggles layer 2 (nav/arrows); 50 ms default timeout.",
    "toggle_qwertz": "L U Z , (right hand, top row — mirror of QWFP) toggles layer 1 (qwertz).",
    "toggle_bt": "all four thumbs together toggle layer 5 (Bluetooth) — a deliberate chord, "
                 "practically impossible to hit by accident.",
}

# ---------------------------------------------------------------------------
# ZMK key -> what comes out on a GERMAN (QWERTZ) layout, by PHYSICAL position.
# ZMK sends the HID usage of the US keyboard; Windows/Linux with the German
# layout translates the position into the German character.
#   (unshifted, with Shift, with AltGr)
# ---------------------------------------------------------------------------
KEY_TO_DE = {
    "Q": ("q", "Q", None), "W": ("w", "W", None), "E": ("e", "E", None),
    "R": ("r", "R", None), "T": ("t", "T", None), "Y": ("z", "Z", None),  # physical Y -> z on DE
    "U": ("u", "U", None), "I": ("i", "I", None), "O": ("o", "O", None),
    "P": ("p", "P", None), "A": ("a", "A", None), "S": ("s", "S", None),
    "D": ("d", "D", None), "F": ("f", "F", None), "G": ("g", "G", None),
    "H": ("h", "H", None), "J": ("j", "J", None), "K": ("k", "K", None),
    "L": ("l", "L", None), "Z": ("y", "Y", None),  # physical Z -> y on DE
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
    "RBKT": ("+", "*", None),             # ZMK alias for RIGHT_BRACKET
    "LBKT": ("ü", "Ü", None),             # ZMK alias for LEFT_BRACKET
}
ALTGR = {
    "Q": "@", "E": "€",
    "N7": "{", "N8": "[", "N9": "]",
    "N0": "}", "MINUS": "\\", "NUBS": "|", "RBKT": "~",
    "N2": "²", "N3": "³",
}
# ASCII-only short labels: arrows/box glyphs are missing from some monospace
# fonts and would break the grid alignment.
SHORT = {
    "SPACE": "Spc", "RET": "Ent", "TAB": "Tab", "ESC": "Esc", "BSPC": "BkSp",
    "DEL": "Del", "INS": "Ins", "HOME": "Home", "END": "End",
    "PG_UP": "PgUp", "PG_DN": "PgDn",
    "UP_ARROW": "Up", "UP": "Up", "DOWN_ARROW": "Dn", "DOWN": "Dn",
    "LEFT": "Lt", "LEFT_ARROW": "Lt", "RIGHT": "Rt", "RIGHT_ARROW": "Rt",
    "LCTRL": "LCtrl", "RCTRL": "RCtrl", "LALT": "LAlt", "RALT": "RAlt",
    "LSHFT": "LShft", "RSHFT": "RShft", "LGUI": "LGui", "RGUI": "RGui",
}
for i in range(1, 13):
    SHORT[f"F{i}"] = f"F{i}"
BT_SHORT = {"BT_NXT": "BT+", "BT_PRV": "BT-", "BT_CLR_ALL": "CLR", "BT_CLR": "CLR"}


def de_char(key: str, mods: str = "") -> str:
    """German character for a key (optionally with Shift / AltGr)."""
    if mods == "RA":
        return ALTGR.get(key, MISSING)
    if key in KEY_TO_DE:
        base, shift, _ = KEY_TO_DE[key]
        return shift if "LS" in mods else base
    return SHORT.get(key, MISSING)


# ---------------------------------------------------------------------------
# Keymap parsing
# ---------------------------------------------------------------------------
def strip_comments(text: str) -> str:
    return re.sub(r"//[^\n]*", "", text)


def parse_combos(raw: str):
    """Combos from the `combos { … }` block: order-agnostic, keeps the comments above."""
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
        c["comment"] = COMBO_NOTES_EN.get(c["name"]) or comments.get(c["name"], "")
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
        sys.exit("cannot find the keymap block")
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
# Rendering: one cell = the real character (+ optional hold note)
# ---------------------------------------------------------------------------
def cell(binding: str):
    """(cell text, held modifier/layer or None)."""
    b = binding.strip()
    if b == "&none":
        return NONE_SYM, None
    if b == "&trans":
        return TRANS_SYM, None
    m = re.match(r"&bt\s+(\w+)(?:\s+(\d+))?", b)
    if m:
        cmd, arg = m.group(1), m.group(2)
        return BT_SHORT.get(cmd, f"BT{arg}"), None
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
            return "--", f"L{args[0]}"
        return f">{args[0]}", None
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
    """ASCII boxes (alignment-safe in every monospace font): 2 halves of 5, then thumbs."""
    gap = "  "

    def border(l, m, r, n):
        return l + m.join("-" * w for _ in range(n)) + r

    def line(cells):
        return "|" + "|".join(c.center(w) for c in cells) + "|"

    top = border("+", "+", "+", KEYS_PER_SIDE)
    mid = border("+", "+", "+", KEYS_PER_SIDE)
    bot = border("+", "+", "+", KEYS_PER_SIDE)
    lines = [top + gap + top]
    for row in range(3):
        row_cells = chars[row * 10:(row + 1) * 10]
        lines.append(line(row_cells[:5]) + gap + line(row_cells[5:]))
        lines.append(mid + gap + (mid if row < 2 else bot))
    t_top = border("+", "+", "+", 4)
    t_bot = border("+", "+", "+", 4)
    indent = " " * (((w + 1) * 5 + 1 - (w * 4 + 5)) // 2)
    lines += [indent + t_top, indent + line(chars[30:34]), indent + t_bot]
    return "\n".join(lines)


def index_grid(w=2):
    """Position-number grid (0-33), printed once at the top."""
    return grid([str(i) for i in range(POSITIONS_PER_LAYER)], w)


def hold_note(bindings) -> str | None:
    parts = []
    for pos, b in enumerate(bindings):
        _, held = cell(b)
        if held:
            parts.append(f"{pos} {held}")
    return "Hold: " + " · ".join(parts) if parts else None


def md_inline(text: str) -> str:
    """Minimal markdown (**bold**, `code`) -> HTML, escaping everything else."""
    out = html.escape(text)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def md_layer(idx, layer):
    chars = [c for c, _ in cells_of(layer["bindings"])]
    out = [f"## Layer {idx} — `{layer['id']}`", ""]
    if layer["name"] and layer["name"].lower() != layer["id"].lower():
        out += [f"*{layer['name']}*", ""]
    out += ["```", "", grid(chars, 4), "", "```", ""]
    note = hold_note(layer["bindings"])
    if note:
        out += [f"`{note}`", ""]
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


GOTCHAS = [
    ("`kp Y` / `kp Z`", "**z / y** — swapped"),
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
            sys.exit(f"layer {l['id']}: {len(l['bindings'])} bindings, expected 34")

    unknown = [(idx, pos, b) for idx, l in enumerate(layers)
               for pos, b in enumerate(l["bindings"]) if MISSING in cell(b)[0]]
    if unknown:
        sys.exit("unmapped bindings (add them to KEY_TO_DE/SHORT/BT_SHORT): "
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
        "# cradio 34 — keymap for a German host (Colemak-DH)",
        "",
        f"`config/cradio.keymap`, branch `{branch}`, keymap at commit `{rev}` · "
        f"generated {date.today().isoformat()} by `tools/gen_cradio_layout_doc.py`.",
        "",
        "Cells show **only the character that actually comes out**, assuming the host runs "
        "a **German (QWERTZ, de-DE) keyboard layout**. The firmware sends key *usages* in "
        "the US order and the host translates them through its own layout — which is why "
        "a keymap label is not what you see on screen: **Z and Y are swapped**, the "
        "umlauts sit on punctuation positions, and some symbols need **AltGr**.",
        "",
        f"`{NONE_SYM}` = no action (`&none`) · `{TRANS_SYM}` = passthrough (`&trans`, falls "
        "through to layer 0) · `L2` = toggles layer 2 · `Spc`/`Ent`/`BkSp` = "
        "Space/Enter/Backspace · `Up`/`Dn`/`Lt`/`Rt` = arrow keys.",
        "",
        "Held modifiers (home-row mods) are on the `Hold:` line under each layer.",
        "",
        "## Key positions (0-33)",
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
        "## Combos (physical positions — independent of the host layout)",
        "",
        "| Combo | Positions | Effect |",
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
        "## German layout gotchas",
        "",
        "| In the keymap | On a German host |",
        "|---|---|",
    ]
    md += [f"| {a} | {b} |" for a, b in GOTCHAS]
    md += [
        "",
        "**Layer 1 (`qwertz`) is intentional**: it keeps the letters in the **US** "
        "arrangement (QWERTY key usages), not the Colemak-DH positions — for a US host or "
        "software that expects US. On a German host it produces `q w e r t y u i o p`.",
        "",
        "**The symbols** in layer 3 follow the arrangement of **Neo2** (the Mod3 layer of "
        "the German ergonomic Neo layout), not the AltGr positions of a regular German "
        "keyboard. The umlauts (ä ö ü ß) live in layer 4.",
        "",
        "## Sources",
        "",
        "- https://kbdlayout.info/KBDGR/ — Windows de-DE layout (KBDGR.DLL)",
        "- https://en.wikipedia.org/wiki/German_keyboard_layout — QWERTZ, umlauts, AltGr",
        "- https://neo-layout.org/ — the Neo layout (Neo2), source for the symbol layer",
        "- `config/cradio.keymap` — source of truth for the bindings",
        "",
        "Regenerate after any keymap change: `python3 tools/gen_cradio_layout_doc.py` — "
        "writes both `cradio-layout-de.md` and `cradio-layout-de.html` (print/PDF source).",
        "",
    ]

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    # ---------------- HTML (print/PDF source) ----------------
    h = [
        "<!doctype html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
        "<title>cradio 34 — keymap for a German host</title>", "<style>",
        "@page { size: A4 portrait; margin: 12mm; }",
        "body { font: 9.5pt/1.4 'DejaVu Sans', system-ui, sans-serif; color:#000; }",
        "h1 { font-size: 15pt; margin: 0 0 6pt }",
        "h2 { font-size: 12pt; margin: 12pt 0 2pt }",
        "p { margin: 0 0 6pt } .sub { font-style: italic; font-size: 8.6pt }",
        "pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.6pt; line-height: 1.2;",
        "      margin: 2pt 0 4pt; page-break-inside: avoid; }",
        "table { border-collapse: collapse; font-size: 8.4pt; margin: 2pt 0 6pt;",
        "        page-break-inside: avoid; }",
        "th, td { border: 0.4pt solid #aaa; padding: 1pt 4pt; text-align: left; vertical-align: top }",
        ".note { font-size: 8.4pt; } .layer { page-break-inside: avoid; }",
        "ul { margin: 0 0 6pt; padding-left: 14pt }",
        "</style>", "</head>", "<body>",
        "<h1>cradio 34 — keymap for a German host (Colemak-DH)</h1>",
        f"<p class=\"sub\"><code>config/cradio.keymap</code>, branch <code>{html.escape(branch)}</code>, "
        f"keymap at commit <code>{html.escape(rev)}</code> · generated {date.today().isoformat()}</p>",
        "<p>Cells show only the character that actually comes out, with the host on a "
        "<b>German (QWERTZ)</b> keyboard layout: Z and Y are swapped, the umlauts sit on "
        "punctuation positions, and some symbols need <b>AltGr</b>.</p>",
        f"<p class=\"note\"><code>{NONE_SYM}</code> = no action · <code>{TRANS_SYM}</code> = "
        "passthrough (falls through to layer 0) · <code>L2</code> = toggles layer 2 · "
        "<code>Spc</code>/<code>Ent</code>/<code>BkSp</code> = Space/Enter/Backspace · "
        "<code>Up</code>/<code>Dn</code>/<code>Lt</code>/<code>Rt</code> = arrows. Held "
        "modifiers are on the <i>Hold:</i> line under each layer.</p>",
        "<h2>Key positions (0-33)</h2>",
        "<pre>" + html.escape(index_grid()) + "</pre>",
    ]
    for idx, layer in enumerate(layers):
        h.append(f"<div class=\"layer\">{html_layer(idx, layer)}</div>")
    h.append("<h2>Combos (physical positions)</h2><table><tr><th>Combo</th><th>Positions</th>"
             "<th>Effect</th></tr>")
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
    h.append("<h2>German layout gotchas</h2><table><tr><th>In the keymap</th>"
             "<th>On a German host</th></tr>")
    for a, b in GOTCHAS:
        h.append(f"<tr><td><code>{html.escape(a.strip('`'))}</code></td><td>"
                 f"{html.escape(b.replace('**', ''))}</td></tr>")
    h.append("</table>")
    h.append("<p class=\"note\">Layer 1 (<code>qwertz</code>) is intentional: it keeps the "
             "letters in the US arrangement (QWERTY usages), not the Colemak-DH positions — "
             "for a US host or software expecting US. On a German host it produces "
             "<code>q w e r t y u i o p</code>. The layer 3 symbols follow the arrangement of "
             "<b>Neo2</b> (Mod3 layer), not the German AltGr positions.</p>")
    h.append("<p class=\"note\">Sources: kbdlayout.info/KBDGR (Windows de-DE), "
             "en.wikipedia.org/wiki/German_keyboard_layout, neo-layout.org, "
             "<code>config/cradio.keymap</code>. Regenerate: "
             "<code>python3 tools/gen_cradio_layout_doc.py</code>.</p>")
    h += ["</body>", "</html>", ""]
    OUT_HTML.write_text("\n".join(h), encoding="utf-8")

    print(f"wrote {OUT_MD.name} ({len(md)} lines) and {OUT_HTML.name} · "
          f"{len(layers)} layers, {len(combos)} combos")


if __name__ == "__main__":
    main()

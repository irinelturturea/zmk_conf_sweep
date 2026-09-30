#!/usr/bin/env python3
"""Generează documentația grafică a keymap-ului cradio (34 taste, Colemak-DH).

Citește `config/cradio.keymap` din repo și scrie `cradio-layout-de.md`, cu câte
un tabel grafic per layer. Coloana „DE" arată caracterul care iese efectiv
când sistemul de operare folosește layout-ul **german (QWERTZ)** — diferențele
față de eticheta ZMK sunt exact motivul pentru care există documentul.

Surse pentru maparea fizică → caracter pe layout german:
  - https://kbdlayout.info/KBDGR/  (KBDGR.DLL, Windows de-DE)
  - https://en.wikipedia.org/wiki/German_keyboard_layout
Regenerare:  python3 tools/gen_cradio_layout_doc.py   (din rădăcina repo-ului)
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
KEYMAP = REPO / "config" / "cradio.keymap"
OUT = REPO / "cradio-layout-de.md"

KEYS_PER_SIDE = 5
POSITIONS_PER_LAYER = 34

# ---------------------------------------------------------------------------
# Mapare tastă ZMK -> ce iese pe layout GERMAN (QWERTZ), pe poziția FIZICĂ a
# tastelor. Valorile sunt poziții fizice: ZMK trimite usage-ul HID al tastelor
# US, iar Windows/Linux cu layout german traduce poziția în caracterul german.
#   base = neapăsat, shift = cu Shift, altgr = cu AltGr (Right Alt)
# ---------------------------------------------------------------------------
KEY_TO_DE = {
    # litere: pe poziția fizică germană (z și y sunt inversate!)
    "Q": ("q", "Q", None), "W": ("w", "W", None), "E": ("e", "E", None),
    "R": ("r", "R", None), "T": ("t", "T", None), "Y": ("z", "Z", None),  # Y fizic = z pe DE
    "U": ("u", "U", None), "I": ("i", "I", None), "O": ("o", "O", None),
    "P": ("p", "P", None), "A": ("a", "A", None), "S": ("s", "S", None),
    "D": ("d", "D", None), "F": ("f", "F", None), "G": ("g", "G", None),
    "H": ("h", "H", None), "J": ("j", "J", None), "K": ("k", "K", None),
    "L": ("l", "L", None), "Z": ("y", "Y", None),  # Z fizic = y pe DE
    "X": ("x", "X", None), "C": ("c", "C", None), "V": ("v", "V", None),
    "B": ("b", "B", None), "N": ("n", "N", None), "M": ("m", "M", None),
    # cifre (shift = simbolul german de pe cifră)
    "N1": ("1", "!", None), "N2": ("2", '"', None), "N3": ("3", "§", None),
    "N4": ("4", "$", None), "N5": ("5", "%", None), "N6": ("6", "&", None),
    "N7": ("7", "/", None), "N8": ("8", "(", None), "N9": ("9", ")", None),
    "N0": ("0", "=", None),
    # punctuație — pozițiile fizice diferă mult față de US
    "COMMA": (",", ";", None),            # Shift = ;  (nu < ca pe US)
    "DOT": (".", ":", None),
    "SLASH": ("-", "_", None),            # fizic: - _ (nu / ?)
    "MINUS": ("ß", "?", None),            # fizic: ß ? (nu - _)
    "SEMI": ("ö", "Ö", None),             # umlaut!
    "SINGLE_QUOTE": ("ä", "Ä", None),     # umlaut!
    "LEFT_BRACKET": ("ü", "Ü", None),     # umlaut!
    "RIGHT_BRACKET": ("+", "*", None),
    "EQUAL": ("´", "`", None),            # dead key accent
    "GRAVE": ("^", "°", None),            # dead key circumflex
    "NUHS": ("'", "#", None),             # "non-US hash": ' / #
    "NUBS": ("<", ">", "|"),              # ISO extra: < > | (AltGr = |)
    "RBKT": ("+", "*", None),             # alias ZMK pentru RIGHT_BRACKET
    "LBKT": ("ü", "Ü", None),             # alias ZMK pentru LEFT_BRACKET
    # AltGr (Strg+Alt = Right Alt) — nivelul 3 german
    "RA@Q": ("@", None, None), "RA@E": ("€", None, None),
}
ALTGR = {
    "Q": "@", "E": "€",
    "N7": "{", "N8": "[", "N9": "]",
    "N0": "}", "MINUS": "\\", "NUBS": "|", "RBKT": "~",
    "N2": "²", "N3": "³",
}
SPECIALS = {
    "SPACE": "Space", "RET": "Enter", "TAB": "Tab", "ESC": "Esc",
    "BSPC": "Backspace", "DEL": "Del", "INS": "Ins",
    "UP_ARROW": "↑", "DOWN_ARROW": "↓", "UP": "↑", "DOWN": "↓",
    "LEFT": "←", "RIGHT": "→", "LEFT_ARROW": "←", "RIGHT_ARROW": "→",
    "HOME": "Home", "END": "End", "PG_UP": "PgUp", "PG_DN": "PgDn",
}
for i in range(1, 13):
    SPECIALS[f"F{i}"] = f"F{i}"

MOD_TAP_NAMES = {
    "LCTRL": "LCtrl", "LALT": "LAlt", "LSHFT": "LShift", "LGUI": "LGui",
    "RCTRL": "RCtrl", "RALT": "RAlt", "RSHFT": "RShift", "RGUI": "RGui",
}


def de_char(key: str, mods: str = "") -> str:
    """Caracterul german pentru o tastă (și modificatorii Shift/AltGr)."""
    if mods == "RA":
        return ALTGR.get(key, "?")
    if key in KEY_TO_DE:
        base, shift, altgr = KEY_TO_DE[key]
        if "LS" in mods:
            return shift
        return base
    if key in SPECIALS:
        return SPECIALS[key]
    return "?"


# ---------------------------------------------------------------------------
# Parsare keymap
# ---------------------------------------------------------------------------
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
    """Împarte <&kp Q &mt LCTRL Y …> în 34 de binding-uri."""
    tokens = raw.split()
    out, cur = [], []
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
    body = km.group(1)
    layers = []
    for m in re.finditer(
        r"(\w+)\s*\{\s*display-name\s*=\s*\"([^\"]*)\";\s*bindings\s*=\s*<(.*?)>\s*;",
        body,
        re.S,
    ):
        layers.append({
            "id": m.group(1),
            "name": m.group(2),
            "bindings": split_bindings(m.group(3)),
        })
    return layers


# ---------------------------------------------------------------------------
# Randare
# ---------------------------------------------------------------------------
def cell_width(layers) -> int:
    """Lățimea unei căsuțe, cât să încapă cea mai lungă etichetă."""
    w = 9
    for l in layers:
        for pos, b in enumerate(l["bindings"]):
            z, ch, _ = cell_parts(b)
            w = max(w, len(f"{pos:>2} {z}"), len(f"   {ch}"))
    return min(w + 1, 20)


def cell_parts(binding: str):
    """(linia ZMK, caracterul german principal, ce e în plus)."""
    b = binding.strip()
    if b == "&none":
        return "none", "—", ""
    if b == "&trans":
        return "trans", "▽", "→ L0"
    if b.startswith("&bt "):
        arg = b[4:].strip()
        return f"bt {arg}", "BT", ""
    if b.startswith("&tog "):
        return f"tog {b[5:].strip()}", "TOG", ""
    m = re.match(r"&(mt|lt|to|mo|tog)\s+(.*)", b)
    if m:
        beh, args = m.group(1), m.group(2).split()
        if beh in ("mt", "lt"):
            hold, tap = args[0], args[-1]
            tmod, tkey = "", tap
            mm = re.match(r"(LS|RA)\(([^)]+)\)", tap)
            if mm:
                tmod, tkey = mm.group(1), mm.group(2)
            label_hold = MOD_TAP_NAMES.get(hold, hold) if beh == "mt" else hold
            return f"{beh} {label_hold} / {tap}", de_char(tkey, tmod), "hold"
        return f"{beh} {' '.join(args)}", "—", ""
    m = re.match(r"&kp\s+(.*)", b)
    if m:
        arg = m.group(1).strip()
        mm = re.match(r"(LS|RA)\(([^)]+)\)", arg)
        if mm:
            mod, key = mm.group(1), mm.group(2)
            return f"kp {mod}({key})", de_char(key, mod if mod == "RA" else "LS"), ""
        return f"kp {arg}", de_char(arg), ""
    return b, "?", ""


def grid(bindings, W):
    """Casete: două jumătăți de câte 5 coloane, plus rândul de thumbs (30-33)."""
    GAP = "   "
    half = KEYS_PER_SIDE

    def border(l, m, r, n=KEYS_PER_SIDE):
        return l + m.join("─" * W for _ in range(n)) + r

    def row_line(cells):
        return "│" + "│".join(cells) + "│"

    top = border("┌", "┬", "┐")
    mid = border("├", "┼", "┤")
    bot = border("└", "┴", "┘")

    lines = [top + GAP + top]
    for row in range(3):
        zcells, dcells = [], []
        for col in range(10):
            pos = row * 10 + col
            z, ch, _ = cell_parts(bindings[pos])
            zcells.append(f"{pos:>2} {z}".ljust(W)[:W])
            dcells.append(f"   {ch}".ljust(W)[:W])
        lines.append(row_line(zcells[:half]) + GAP + row_line(zcells[half:]))
        lines.append(row_line(dcells[:half]) + GAP + row_line(dcells[half:]))
        lines.append((mid if row < 2 else bot) + GAP + (mid if row < 2 else bot))

    t_top = border("┌", "┬", "┐", 4)
    t_mid = border("├", "┼", "┤", 4)
    t_bot = border("└", "┴", "┘", 4)
    tz, td = [], []
    for pos in (30, 31, 32, 33):
        z, ch, _ = cell_parts(bindings[pos])
        tz.append(f"{pos:>2} {z}".ljust(W)[:W])
        td.append(f"   {ch}".ljust(W)[:W])
    thumb_w = W * 4 + 5
    indent = " " * max(2, ((W + 1) * half + 1 - thumb_w) // 2)
    lines.append(indent + t_top)
    lines.append(indent + row_line(tz))
    lines.append(indent + row_line(td))
    lines.append(indent + t_bot)
    return "\n".join(lines)


def detail_table(bindings):
    rows = ["| # | ZMK | iese pe layout german | observații |", "|---|---|---|---|"]
    for pos, b in enumerate(bindings):
        z, ch, note = cell_parts(b)
        extra = ""
        if note == "hold":
            extra = "ținut = modificator/layer, apăsat scurt = caracterul din coloana DE"
        elif ch == "▽":
            extra = "transparent: cade pe layer 0"
        elif z.startswith("kp ") and "(" in z:
            extra = "Shift/AltGr citit pe poziția fizică germană"
        rows.append(f"| {pos} | `{b}` | **{ch}** | {extra} |")
    return "\n".join(rows)


def main():
    raw = KEYMAP.read_text(encoding="utf-8")
    src = strip_comments(raw)
    layers = parse_layers(src)
    combos = parse_combos(raw)
    W = cell_width(layers)
    for l in layers:
        if len(l["bindings"]) != POSITIONS_PER_LAYER:
            sys.exit(f"layer {l['id']}: {len(l['bindings'])} bindings, aștept 34")

    try:
        rev = subprocess.check_output(
            ["git", "-C", str(REPO), "log", "-1", "--format=%h", "--", "config/cradio.keymap"],
            text=True,
        ).strip()
        branch = subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()
    except Exception:
        rev, branch = "?", "?"

    out = [
        "# cradio 34 — keymap grafic (Colemak-DH)",
        "",
        f"Layere din `config/cradio.keymap` (branch `{branch}`, keymap la commit `{rev}`), "
        f"generate cu `tools/gen_cradio_layout_doc.py` la {date.today().isoformat()}.",
        "",
        "> **Premisa importantă:** toate coloanele «iese pe layout german» presupun că "
        "sistemul de operare e configurat cu **tastatură germană (QWERTZ, de-DE)**. "
        "Firmware-ul trimite coduri de tastă (usage HID, în ordinea tastaturii US), "
        "iar Windows/Linux le traduce prin layout-ul german — de aceea eticheta din "
        "keymap nu e ce vezi pe ecran. Consecințe: **Z și Y sunt inversate**, umlautele "
        "stau pe poziții de punctuație, iar o parte din simboluri cer **AltGr**.",
        "",
        "Fiecare căsuță arată trei lucruri: numărul poziției (0-33), comportamentul ZMK, "
        "și caracterul care iese efectiv pe un sistem german. Legenda:",
        "",
        "| Notație | Sens |",
        "|---|---|",
        "| `kp X` | tastă simplă |",
        "| `kp LS(X)` | Shift + X |",
        "| `kp RA(X)` | AltGr (Strg+Alt / Right Alt) + X |",
        "| `mt MOD / X` | ținut = modificator (home-row mod, 300 ms, tap-preferred); apăsat scurt = X |",
        "| `lt N / X` | ținut = layer N (momentary); apăsat scurt = X |",
        "| `none` | nimic (nu cade nicăieri) |",
        "| `trans` | transparent — cade pe layer 0 |",
        "| `bt X` | acțiune Bluetooth (executată pe jumătatea centrală) |",
        "| `▽` | valoarea moștenită de pe layer 0 |",
        "",
        "---",
        "",
    ]

    for idx, layer in enumerate(layers):
        out += [f"## Layer {idx} — `{layer['id']}` ({layer['name']})", "", "```", ""]
        out.append(grid(layer["bindings"], W))
        out += ["", "```", "", "### Detaliu pe poziții", "", detail_table(layer["bindings"]), "", "---", ""]

    out += [
        "## Combos (poziții fizice — nu depind de layout-ul sistemului)",
        "",
        "| Combo | Poziții | Efect | Nota din keymap |",
        "|---|---|---|---|",
    ]
    for c in combos:
        tmo = f" (timeout {c['timeout']} ms)" if c["timeout"] else ""
        out.append(
            f"| `{c['name']}` | {', '.join(c['positions'])}{tmo} | `{c['bindings']}` | {c['comment']} |"
        )
    out += [
        "",
        "---",
        "",
        "## Capcanele layout-ului german (de ce arată așa coloana «DE»)",
        "",
        "| Ce scrie în keymap | Ce iese pe US | Ce iese pe DE |",
        "|---|---|---|",
        "| `kp Y` / `kp Z` | y / z | **z / y** (inversate) |",
        "| `kp SEMI` | ; | **ö** |",
        "| `kp SINGLE_QUOTE` | ' | **ä** |",
        "| `kp LEFT_BRACKET` | [ | **ü** |",
        "| `kp MINUS` | - | **ß** (Shift = ?) |",
        "| `kp SLASH` | / | **-** (Shift = _) |",
        "| `kp EQUAL` | = | **´** (dead key; Shift = `) |",
        "| `kp GRAVE` | ` | **^** (dead key; Shift = °) |",
        "| `kp NUHS` | \\ | **'** (Shift = #) |",
        "| `kp RBKT` | ] | **+** (Shift = *) |",
        "| `kp NUBS` | \\ | **<** (Shift = >, AltGr = |) |",
        "| `kp LS(N6)` | ^ | **&** |",
        "| `kp LS(N7)` | & | **/** |",
        "| `kp LS(N8)` | * | **(** |",
        "| `kp LS(N0)` | ) | **=** |",
        "| `kp LS(COMMA)` | < | **;** |",
        "| `kp LS(DOT)` | > | **:** |",
        "| `kp RA(N7)` | { | **{** |",
        "| `kp RA(N8)` / `kp RA(N9)` | ( / ) | **[ / ]** |",
        "| `kp RA(N0)` | } | **}** |",
        "| `kp RA(Q)` | @ | **@** |",
        "| `kp RA(MINUS)` | _ | **\\\\** |",
        "| `kp RA(NUBS)` | | | **|** |",
        "",
        "**De ce există layer 1 (`qwertz`):** rescrie aranjarea literelor în ordinea "
        "Q W E R T Z U I O P (ca poziții fizice). **Atenție:** pe un host german poziția "
        "care trimite `Z` dă `y`, iar cea care trimite `Y` dă `z` — layer 1 iese deci "
        "`q w e r t y u i o p`, cu Z și Y inversate față de o tastatură germană fizică. "
        "În layer 0 (Colemak-DH) swap-ul e aplicat: poziția de sus-dreapta care trimite "
        "`Z` dă `y`, iar cea de jos-stânga care trimite `Y` dă `z`.",
        "",
        "## Surse pentru maparea germană",
        "",
        "- https://kbdlayout.info/KBDGR/ — layout-ul Windows de-DE (KBDGR.DLL)",
        "- https://en.wikipedia.org/wiki/German_keyboard_layout — QWERTZ, umlauturi, AltGr",
        "- `config/cradio.keymap` — sursa de adevăr pentru bindings (branch `irinelturturea-colemak`)",
        "",
        "Regenerare după orice modificare de keymap:",
        "",
        "```sh",
        "python3 tools/gen_cradio_layout_doc.py",
        "```",
        "",
    ]

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"scris {OUT.relative_to(REPO)} ({len(out)} linii), {len(layers)} layere, {len(combos)} combos")


if __name__ == "__main__":
    main()

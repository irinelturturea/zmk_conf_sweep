# cradio 34 — keymap for a German host (Colemak-DH)

`config/cradio.keymap`, branch `irinelturturea-colemak`, keymap at commit `bbb8320` · generated 2026-09-30 by `tools/gen_cradio_layout_doc.py`.

Cells show **only the character that actually comes out**, assuming the host runs a **German (QWERTZ, de-DE) keyboard layout**. The firmware sends key *usages* in the US order and the host translates them through its own layout — which is why a keymap label is not what you see on screen: **Z and Y are swapped**, the umlauts sit on punctuation positions, and some symbols need **AltGr**.

`..` = no action (`&none`) · `==` = passthrough (`&trans`, falls through to layer 0) · `L2` = toggles layer 2 · `Spc`/`Ent`/`BkSp` = Space/Enter/Backspace · `Up`/`Dn`/`Lt`/`Rt` = arrow keys.

Held modifiers (home-row mods) are on the `Hold:` line under each layer.

## Key positions (0-33)

```

+--+--+--+--+--+  +--+--+--+--+--+
|0 |1 |2 |3 |4 |  |5 |6 |7 |8 |9 |
+--+--+--+--+--+  +--+--+--+--+--+
|10|11|12|13|14|  |15|16|17|18|19|
+--+--+--+--+--+  +--+--+--+--+--+
|20|21|22|23|24|  |25|26|27|28|29|
+--+--+--+--+--+  +--+--+--+--+--+
 +--+--+--+--+
 |30|31|32|33|
 +--+--+--+--+

```

---

## Layer 0 — `default_layer`

*Default Layer*

```

+----+----+----+----+----+  +----+----+----+----+----+
| q  | w  | f  | p  | g  |  | j  | l  | u  | y  | ;  |
+----+----+----+----+----+  +----+----+----+----+----+
| a  | r  | s  | t  | d  |  | h  | n  | e  | i  | o  |
+----+----+----+----+----+  +----+----+----+----+----+
| z  | x  | c  | v  | b  |  | k  | m  | ,  | .  | /  |
+----+----+----+----+----+  +----+----+----+----+----+
  +----+----+----+----+
  |Spc |Tab |Esc |Spc |
  +----+----+----+----+

```

`Hold: 20 LCtrl · 21 LGui · 22 LAlt · 23 LShft · 26 RShft · 27 RAlt · 28 RGui · 29 RCtrl · 30 L4 · 31 L2 · 32 L4 · 33 L3`

---

## Layer 1 — `qwertz`

```

+----+----+----+----+----+  +----+----+----+----+----+
| q  | w  | e  | r  | t  |  | y  | u  | i  | o  | p  |
+----+----+----+----+----+  +----+----+----+----+----+
| a  | s  | d  | f  | g  |  | h  | j  | k  | l  | ö  |
+----+----+----+----+----+  +----+----+----+----+----+
| z  | x  | c  | v  | b  |  | n  | m  | ,  | .  | -  |
+----+----+----+----+----+  +----+----+----+----+----+
  +----+----+----+----+
  |Spc |Tab |Esc |Ent |
  +----+----+----+----+

```

`Hold: 20 LCtrl · 21 LGui · 22 LAlt · 23 LShft · 26 RShft · 27 RAlt · 28 RGui · 29 RCtrl · 30 L4 · 31 L2 · 32 L4 · 33 L3`

**Intentional:** layer 1 keeps the letters in the **US** arrangement (QWERTY key usages), not in the Colemak-DH positions — for a US host or software that expects a US layout. On a German host it therefore produces `q w e r t y u i o p`. It is not a German QWERTZ layer.

---

## Layer 2 — `function_layer`

*Function Layer*

```

+----+----+----+----+----+  +----+----+----+----+----+
| .. | .. | .. | .. | .. |  | .. | .. | .. | .. | .. |
+----+----+----+----+----+  +----+----+----+----+----+
| .. | .. | Up | .. | .. |  | .. | Lt | Dn | Up | Rt |
+----+----+----+----+----+  +----+----+----+----+----+
| .. | Lt | Dn | Rt | .. |  | .. | .. | .. | .. | .. |
+----+----+----+----+----+  +----+----+----+----+----+
  +----+----+----+----+
  |Del | .. |Ent | .. |
  +----+----+----+----+

```

---

## Layer 3 — `symbol_layer`

*Symbol Layer*

```

+----+----+----+----+----+  +----+----+----+----+----+
| @  | _  | [  | ]  | ^  |  | !  | <  | >  | =  | &  |
+----+----+----+----+----+  +----+----+----+----+----+
| \  | /  | {  | }  | *  |  | ?  | (  | )  | -  | :  |
+----+----+----+----+----+  +----+----+----+----+----+
| '  | $  | |  | ~  | `  |  | +  | %  | "  | #  | ;  |
+----+----+----+----+----+  +----+----+----+----+----+
  +----+----+----+----+
  | == | == | == | .. |
  +----+----+----+----+

```

The symbols follow the arrangement of **Neo2** (the *Mod3* layer of the German ergonomic Neo layout, see neo-layout.org), not the AltGr positions of a regular German keyboard: programming symbols sit on the top row, grouped by frequency. The umlauts (ä ö ü ß) are in layer 4.

---

## Layer 4 — `nr_layer`

*Number and F Layer*

```

+----+----+----+----+----+  +----+----+----+----+----+
| F9 |F10 |F11 |F12 | == |  | ä  | 7  | 8  | 9  | ß  |
+----+----+----+----+----+  +----+----+----+----+----+
| F5 | F6 | F7 | F8 | == |  | ö  | 4  | 5  | 6  | 0  |
+----+----+----+----+----+  +----+----+----+----+----+
| F1 | F2 | F3 | F4 | == |  | ü  | 1  | 2  | 3  | == |
+----+----+----+----+----+  +----+----+----+----+----+
  +----+----+----+----+
  | == |Ent | .. |BkSp|
  +----+----+----+----+

```

---

## Layer 5 — `bt_layer`

*Bluetooth Layer*

```

+----+----+----+----+----+  +----+----+----+----+----+
|BT0 |BT1 |BT2 |BT3 | .. |  | .. | .. | .. | .. | .. |
+----+----+----+----+----+  +----+----+----+----+----+
| .. | .. | .. | .. | .. |  | .. | .. | .. | .. | .. |
+----+----+----+----+----+  +----+----+----+----+----+
| .. | .. |BT+ |BT- | .. |  | .. | .. | .. | .. | .. |
+----+----+----+----+----+  +----+----+----+----+----+
  +----+----+----+----+
  | .. | .. |CLR | .. |
  +----+----+----+----+

```

---

## Combos (physical positions — independent of the host layout)

| Combo | Positions | Effect |
|---|---|---|
| `toggle_nav` | 0, 1, 2, 3 | `&tog 2` |
| `toggle_qwertz` | 6, 7, 8, 9 | `&tog 1` |
| `toggle_bt` (+80ms) | 30, 31, 32, 33 | `&tog 5` |

- **toggle_nav**: QWFP (left hand, top row) toggles layer 2 (nav/arrows); 50 ms default timeout.
- **toggle_qwertz**: L U Z , (right hand, top row — mirror of QWFP) toggles layer 1 (qwertz).
- **toggle_bt**: all four thumbs together toggle layer 5 (Bluetooth) — a deliberate chord, practically impossible to hit by accident.

---

## German layout gotchas

| In the keymap | On a German host |
|---|---|
| `kp Y` / `kp Z` | **z / y** — swapped |
| `kp SEMI` | **ö** |
| `kp SINGLE_QUOTE` | **ä** |
| `kp LEFT_BRACKET` | **ü** |
| `kp MINUS` | **ß** (Shift: ?) |
| `kp SLASH` | **-** (Shift: _) |
| `kp EQUAL` | **´** dead key (Shift: `) |
| `kp GRAVE` | **^** dead key (Shift: °) |
| `kp NUHS` | **'** (Shift: #) |
| `kp RBKT` | **+** (Shift: *) |
| `kp NUBS` | **<** (Shift: >, AltGr: |) |
| `kp LS(N6)` | **&** |
| `kp LS(N7)` | **/** |
| `kp LS(N8)` | **(** |
| `kp LS(N0)` | **=** |
| `kp LS(COMMA)` | **;** |
| `kp LS(DOT)` | **:** |
| `kp RA(N7)` | **{** |
| `kp RA(N8)` / `kp RA(N9)` | **[ / ]** |
| `kp RA(N0)` | **}** |
| `kp RA(Q)` | **@** |
| `kp RA(MINUS)` | **\\** |
| `kp RA(NUBS)` | **|** |

**Layer 1 (`qwertz`) is intentional**: it keeps the letters in the **US** arrangement (QWERTY key usages), not the Colemak-DH positions — for a US host or software that expects US. On a German host it produces `q w e r t y u i o p`.

**The symbols** in layer 3 follow the arrangement of **Neo2** (the Mod3 layer of the German ergonomic Neo layout), not the AltGr positions of a regular German keyboard. The umlauts (ä ö ü ß) live in layer 4.

## Sources

- https://kbdlayout.info/KBDGR/ — Windows de-DE layout (KBDGR.DLL)
- https://en.wikipedia.org/wiki/German_keyboard_layout — QWERTZ, umlauts, AltGr
- https://neo-layout.org/ — the Neo layout (Neo2), source for the symbol layer
- `config/cradio.keymap` — source of truth for the bindings

Regenerate after any keymap change: `python3 tools/gen_cradio_layout_doc.py` — writes both `cradio-layout-de.md` and `cradio-layout-de.html` (print/PDF source).

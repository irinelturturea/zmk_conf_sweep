# cradio 34 — keymap pentru host german (Colemak-DH)

`config/cradio.keymap`, branch `irinelturturea-colemak`, keymap la commit `bbb8320` · generat 2026-09-30 cu `tools/gen_cradio_layout_doc.py`.

În tabele stă **doar caracterul care iese efectiv**, presupunând că sistemul folosește tastatură **germană (QWERTZ)**. Firmware-ul trimite coduri de tastă în ordinea tastaturii US, iar sistemul le traduce prin layout-ul german — de aceea ce scrie în keymap nu e ce vezi pe ecran: **Z și Y sunt inversate**, umlautele stau pe poziții de punctuație, o parte din simboluri cer **AltGr**.

`×` = nicio acțiune (`&none`) · `↓` = passthrough (`&trans`, cade pe layer 0) · `L2` = comută layer 2 · `Spc`/`Ent`/`BkSp` = Space/Enter/Backspace.
Modificatorii ținuți (home-row mods) sunt pe linia *Ținut* de sub fiecare layer.

## Pozițiile tastelor (0-33)

```

┌──┬──┬──┬──┬──┐  ┌──┬──┬──┬──┬──┐
│0 │1 │2 │3 │4 │  │5 │6 │7 │8 │9 │
├──┼──┼──┼──┼──┤  ├──┼──┼──┼──┼──┤
│10│11│12│13│14│  │15│16│17│18│19│
├──┼──┼──┼──┼──┤  ├──┼──┼──┼──┼──┤
│20│21│22│23│24│  │25│26│27│28│29│
└──┴──┴──┴──┴──┘  └──┴──┴──┴──┴──┘
 ┌──┬──┬──┬──┐
 │30│31│32│33│
 └──┴──┴──┴──┘

```

---

## Layer 0 — `default_layer`

*Default Layer*

```

┌────┬────┬────┬────┬────┐  ┌────┬────┬────┬────┬────┐
│ q  │ w  │ f  │ p  │ g  │  │ j  │ l  │ u  │ y  │ ;  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ a  │ r  │ s  │ t  │ d  │  │ h  │ n  │ e  │ i  │ o  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ z  │ x  │ c  │ v  │ b  │  │ k  │ m  │ ,  │ .  │ /  │
└────┴────┴────┴────┴────┘  └────┴────┴────┴────┴────┘
  ┌────┬────┬────┬────┐
  │Spc │Tab │Esc │Spc │
  └────┴────┴────┴────┘

```

Ținut (hold): 20 LCtrl · 21 LGui · 22 LAlt · 23 LShft · 26 RShft · 27 RAlt · 28 RGui · 29 RCtrl · 30 L4 · 31 L2 · 32 L4 · 33 L3

---

## Layer 1 — `qwertz`

```

┌────┬────┬────┬────┬────┐  ┌────┬────┬────┬────┬────┐
│ q  │ w  │ e  │ r  │ t  │  │ y  │ u  │ i  │ o  │ p  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ a  │ s  │ d  │ f  │ g  │  │ h  │ j  │ k  │ l  │ ö  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ z  │ x  │ c  │ v  │ b  │  │ n  │ m  │ ,  │ .  │ -  │
└────┴────┴────┴────┴────┘  └────┴────┴────┴────┴────┘
  ┌────┬────┬────┬────┐
  │Spc │Tab │Esc │Ent │
  └────┴────┴────┴────┘

```

Ținut (hold): 20 LCtrl · 21 LGui · 22 LAlt · 23 LShft · 26 RShft · 27 RAlt · 28 RGui · 29 RCtrl · 30 L4 · 31 L2 · 32 L4 · 33 L3

---

## Layer 2 — `function_layer`

*Function Layer*

```

┌────┬────┬────┬────┬────┐  ┌────┬────┬────┬────┬────┐
│ ×  │ ×  │ ×  │ ×  │ ×  │  │ ×  │ ×  │ ×  │ ×  │ ×  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ ×  │ ×  │ ↑  │ ×  │ ×  │  │ ×  │ ←  │ ↓  │ ↑  │ →  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ ×  │ ←  │ ↓  │ →  │ ×  │  │ ×  │ ×  │ ×  │ ×  │ ×  │
└────┴────┴────┴────┴────┘  └────┴────┴────┴────┴────┘
  ┌────┬────┬────┬────┐
  │Del │ ×  │Ent │ ×  │
  └────┴────┴────┴────┘

```

---

## Layer 3 — `symbol_layer`

*Symbol Layer*

```

┌────┬────┬────┬────┬────┐  ┌────┬────┬────┬────┬────┐
│ @  │ _  │ [  │ ]  │ ^  │  │ !  │ <  │ >  │ =  │ &  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ \  │ /  │ {  │ }  │ *  │  │ ?  │ (  │ )  │ -  │ :  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ '  │ $  │ |  │ ~  │ `  │  │ +  │ %  │ "  │ #  │ ;  │
└────┴────┴────┴────┴────┘  └────┴────┴────┴────┴────┘
  ┌────┬────┬────┬────┐
  │ ↓  │ ↓  │ ↓  │ ×  │
  └────┴────┴────┴────┘

```

---

## Layer 4 — `nr_layer`

*Number and F Layer*

```

┌────┬────┬────┬────┬────┐  ┌────┬────┬────┬────┬────┐
│ F9 │F10 │F11 │F12 │ ↓  │  │ ä  │ 7  │ 8  │ 9  │ ß  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ F5 │ F6 │ F7 │ F8 │ ↓  │  │ ö  │ 4  │ 5  │ 6  │ 0  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ F1 │ F2 │ F3 │ F4 │ ↓  │  │ ü  │ 1  │ 2  │ 3  │ ↓  │
└────┴────┴────┴────┴────┘  └────┴────┴────┴────┴────┘
  ┌────┬────┬────┬────┐
  │ ↓  │Ent │ ×  │BkSp│
  └────┴────┴────┴────┘

```

---

## Layer 5 — `bt_layer`

*Bluetooth Layer*

```

┌────┬────┬────┬────┬────┐  ┌────┬────┬────┬────┬────┐
│BT0 │BT1 │BT2 │BT3 │ ×  │  │ ×  │ ×  │ ×  │ ×  │ ×  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ ×  │ ×  │ ×  │ ×  │ ×  │  │ ×  │ ×  │ ×  │ ×  │ ×  │
├────┼────┼────┼────┼────┤  ├────┼────┼────┼────┼────┤
│ ×  │ ×  │BT+ │BT- │ ×  │  │ ×  │ ×  │ ×  │ ×  │ ×  │
└────┴────┴────┴────┴────┘  └────┴────┴────┴────┴────┘
  ┌────┬────┬────┬────┐
  │ ×  │ ×  │CLR │ ×  │
  └────┴────┴────┴────┘

```

---

## Combos (poziții fizice — nu depind de layout-ul sistemului)

| Combo | Poziții | Efect |
|---|---|---|
| `toggle_nav` | 0, 1, 2, 3 | `&tog 2` |
| `toggle_qwertz` | 6, 7, 8, 9 | `&tog 1` |
| `toggle_bt` (+80ms) | 30, 31, 32, 33 | `&tog 5` |

- **toggle_nav**: QWFP (stanga, top row) = toggle layer 2 (nav/arrows) — 50ms default timeout
- **toggle_qwertz**: L U Z , (dreapta, top row, oglinda QWFP) = toggle qwertz
- **toggle_bt**: 4 thumbs = toggle layer 5 (BT) — intrare deliberata, aproape imposibil accidental

---

## Capcanele layout-ului german

| Ce scrie în keymap | Pe host german iese |
|---|---|
| `kp Y` / `kp Z` | **z / y** — inversate |
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

**Layer 1 (`qwertz`)** rescrie literele în ordinea Q W E R T Z U I O P ca poziții fizice. Pe un host german iese `q w e r t y u i o p` — Z și Y sunt inversate față de o tastatură germană fizică. În layer 0 swap-ul e aplicat corect (`kp Z` dă `y`, `kp Y` dă `z`).

## Surse

- https://kbdlayout.info/KBDGR/ — layout-ul Windows de-DE
- https://en.wikipedia.org/wiki/German_keyboard_layout — QWERTZ, umlaute, AltGr
- `config/cradio.keymap` — sursa de adevăr pentru bindings

Regenerare (după orice modificare de keymap): `python3 tools/gen_cradio_layout_doc.py` — scrie și `cradio-layout-de.md`, și `cradio-layout-de.html` (pentru print/PDF).

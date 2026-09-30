# cradio 34 — keymap grafic (Colemak-DH)

Layere din `config/cradio.keymap` (branch `irinelturturea-colemak`, keymap la commit `bbb8320`), generate cu `tools/gen_cradio_layout_doc.py` la 2026-09-30.

> **Premisa importantă:** toate coloanele «iese pe layout german» presupun că sistemul de operare e configurat cu **tastatură germană (QWERTZ, de-DE)**. Firmware-ul trimite coduri de tastă (usage HID, în ordinea tastaturii US), iar Windows/Linux le traduce prin layout-ul german — de aceea eticheta din keymap nu e ce vezi pe ecran. Consecințe: **Z și Y sunt inversate**, umlautele stau pe poziții de punctuație, iar o parte din simboluri cer **AltGr**.

Fiecare căsuță arată trei lucruri: numărul poziției (0-33), comportamentul ZMK, și caracterul care iese efectiv pe un sistem german. Legenda:

| Notație | Sens |
|---|---|
| `kp X` | tastă simplă |
| `kp LS(X)` | Shift + X |
| `kp RA(X)` | AltGr (Strg+Alt / Right Alt) + X |
| `mt MOD / X` | ținut = modificator (home-row mod, 300 ms, tap-preferred); apăsat scurt = X |
| `lt N / X` | ținut = layer N (momentary); apăsat scurt = X |
| `none` | nimic (nu cade nicăieri) |
| `trans` | transparent — cade pe layer 0 |
| `bt X` | acțiune Bluetooth (executată pe jumătatea centrală) |
| `▽` | valoarea moștenită de pe layer 0 |

---

## Layer 0 — `default_layer` (Default Layer)

```

┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐   ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ 0 kp Q             │ 1 kp W             │ 2 kp F             │ 3 kp P             │ 4 kp G             │   │ 5 kp J             │ 6 kp L             │ 7 kp U             │ 8 kp Z             │ 9 kp LS(COMMA)     │
│   q                │   w                │   f                │   p                │   g                │   │   j                │   l                │   u                │   y                │   ;                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│10 kp A             │11 kp R             │12 kp S             │13 kp T             │14 kp D             │   │15 kp H             │16 kp N             │17 kp E             │18 kp I             │19 kp O             │
│   a                │   r                │   s                │   t                │   d                │   │   h                │   n                │   e                │   i                │   o                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│20 mt LCtrl / Y     │21 mt LGui / X      │22 mt LAlt / C      │23 mt LShift / V    │24 kp B             │   │25 kp K             │26 mt RShift / M    │27 mt RAlt / COMMA  │28 mt RGui / DOT    │29 mt RCtrl / LS(N7)│
│   z                │   x                │   c                │   v                │   b                │   │   k                │   m                │   ,                │   .                │   /                │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘   └────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘
          ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┐
          │30 lt 4 / SPACE     │31 lt 2 / TAB       │32 lt 4 / ESC       │33 lt 3 / SPACE     │
          │   Space            │   Tab              │   Esc              │   Space            │
          └────────────────────┴────────────────────┴────────────────────┴────────────────────┘

```

### Detaliu pe poziții

| # | ZMK | iese pe layout german | observații |
|---|---|---|---|
| 0 | `&kp Q` | **q** |  |
| 1 | `&kp W` | **w** |  |
| 2 | `&kp F` | **f** |  |
| 3 | `&kp P` | **p** |  |
| 4 | `&kp G` | **g** |  |
| 5 | `&kp J` | **j** |  |
| 6 | `&kp L` | **l** |  |
| 7 | `&kp U` | **u** |  |
| 8 | `&kp Z` | **y** |  |
| 9 | `&kp LS(COMMA)` | **;** | Shift/AltGr citit pe poziția fizică germană |
| 10 | `&kp A` | **a** |  |
| 11 | `&kp R` | **r** |  |
| 12 | `&kp S` | **s** |  |
| 13 | `&kp T` | **t** |  |
| 14 | `&kp D` | **d** |  |
| 15 | `&kp H` | **h** |  |
| 16 | `&kp N` | **n** |  |
| 17 | `&kp E` | **e** |  |
| 18 | `&kp I` | **i** |  |
| 19 | `&kp O` | **o** |  |
| 20 | `&mt LCTRL Y` | **z** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 21 | `&mt LGUI X` | **x** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 22 | `&mt LALT C` | **c** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 23 | `&mt LSHFT V` | **v** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 24 | `&kp B` | **b** |  |
| 25 | `&kp K` | **k** |  |
| 26 | `&mt RSHFT M` | **m** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 27 | `&mt RALT COMMA` | **,** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 28 | `&mt RGUI DOT` | **.** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 29 | `&mt RCTRL LS(N7)` | **/** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 30 | `&lt 4 SPACE` | **Space** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 31 | `&lt 2 TAB` | **Tab** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 32 | `&lt 4 ESC` | **Esc** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 33 | `&lt 3 SPACE` | **Space** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |

---

## Layer 1 — `qwertz` (qwertz)

```

┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐   ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ 0 kp Q             │ 1 kp W             │ 2 kp E             │ 3 kp R             │ 4 kp T             │   │ 5 kp Z             │ 6 kp U             │ 7 kp I             │ 8 kp O             │ 9 kp P             │
│   q                │   w                │   e                │   r                │   t                │   │   y                │   u                │   i                │   o                │   p                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│10 kp A             │11 kp S             │12 kp D             │13 kp F             │14 kp G             │   │15 kp H             │16 kp J             │17 kp K             │18 kp L             │19 kp SEMI          │
│   a                │   s                │   d                │   f                │   g                │   │   h                │   j                │   k                │   l                │   ö                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│20 mt LCtrl / Y     │21 mt LGui / X      │22 mt LAlt / C      │23 mt LShift / V    │24 kp B             │   │25 kp N             │26 mt RShift / M    │27 mt RAlt / COMMA  │28 mt RGui / DOT    │29 mt RCtrl / SLASH │
│   z                │   x                │   c                │   v                │   b                │   │   n                │   m                │   ,                │   .                │   -                │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘   └────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘
          ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┐
          │30 lt 4 / SPACE     │31 lt 2 / TAB       │32 lt 4 / ESC       │33 lt 3 / RET       │
          │   Space            │   Tab              │   Esc              │   Enter            │
          └────────────────────┴────────────────────┴────────────────────┴────────────────────┘

```

### Detaliu pe poziții

| # | ZMK | iese pe layout german | observații |
|---|---|---|---|
| 0 | `&kp Q` | **q** |  |
| 1 | `&kp W` | **w** |  |
| 2 | `&kp E` | **e** |  |
| 3 | `&kp R` | **r** |  |
| 4 | `&kp T` | **t** |  |
| 5 | `&kp Z` | **y** |  |
| 6 | `&kp U` | **u** |  |
| 7 | `&kp I` | **i** |  |
| 8 | `&kp O` | **o** |  |
| 9 | `&kp P` | **p** |  |
| 10 | `&kp A` | **a** |  |
| 11 | `&kp S` | **s** |  |
| 12 | `&kp D` | **d** |  |
| 13 | `&kp F` | **f** |  |
| 14 | `&kp G` | **g** |  |
| 15 | `&kp H` | **h** |  |
| 16 | `&kp J` | **j** |  |
| 17 | `&kp K` | **k** |  |
| 18 | `&kp L` | **l** |  |
| 19 | `&kp SEMI` | **ö** |  |
| 20 | `&mt LCTRL Y` | **z** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 21 | `&mt LGUI X` | **x** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 22 | `&mt LALT C` | **c** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 23 | `&mt LSHFT V` | **v** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 24 | `&kp B` | **b** |  |
| 25 | `&kp N` | **n** |  |
| 26 | `&mt RSHFT M` | **m** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 27 | `&mt RALT COMMA` | **,** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 28 | `&mt RGUI DOT` | **.** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 29 | `&mt RCTRL SLASH` | **-** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 30 | `&lt 4 SPACE` | **Space** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 31 | `&lt 2 TAB` | **Tab** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 32 | `&lt 4 ESC` | **Esc** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |
| 33 | `&lt 3 RET` | **Enter** | ținut = modificator/layer, apăsat scurt = caracterul din coloana DE |

---

## Layer 2 — `function_layer` (Function Layer)

```

┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐   ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ 0 none             │ 1 none             │ 2 none             │ 3 none             │ 4 none             │   │ 5 none             │ 6 none             │ 7 none             │ 8 none             │ 9 none             │
│   —                │   —                │   —                │   —                │   —                │   │   —                │   —                │   —                │   —                │   —                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│10 none             │11 none             │12 kp UP_ARROW      │13 none             │14 none             │   │15 none             │16 kp LEFT          │17 kp DOWN          │18 kp UP            │19 kp RIGHT         │
│   —                │   —                │   ↑                │   —                │   —                │   │   —                │   ←                │   ↓                │   ↑                │   →                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│20 none             │21 kp LEFT          │22 kp DOWN_ARROW    │23 kp RIGHT         │24 none             │   │25 none             │26 none             │27 none             │28 none             │29 none             │
│   —                │   ←                │   ↓                │   →                │   —                │   │   —                │   —                │   —                │   —                │   —                │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘   └────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘
          ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┐
          │30 kp DEL           │31 none             │32 kp RET           │33 none             │
          │   Del              │   —                │   Enter            │   —                │
          └────────────────────┴────────────────────┴────────────────────┴────────────────────┘

```

### Detaliu pe poziții

| # | ZMK | iese pe layout german | observații |
|---|---|---|---|
| 0 | `&none` | **—** |  |
| 1 | `&none` | **—** |  |
| 2 | `&none` | **—** |  |
| 3 | `&none` | **—** |  |
| 4 | `&none` | **—** |  |
| 5 | `&none` | **—** |  |
| 6 | `&none` | **—** |  |
| 7 | `&none` | **—** |  |
| 8 | `&none` | **—** |  |
| 9 | `&none` | **—** |  |
| 10 | `&none` | **—** |  |
| 11 | `&none` | **—** |  |
| 12 | `&kp UP_ARROW` | **↑** |  |
| 13 | `&none` | **—** |  |
| 14 | `&none` | **—** |  |
| 15 | `&none` | **—** |  |
| 16 | `&kp LEFT` | **←** |  |
| 17 | `&kp DOWN` | **↓** |  |
| 18 | `&kp UP` | **↑** |  |
| 19 | `&kp RIGHT` | **→** |  |
| 20 | `&none` | **—** |  |
| 21 | `&kp LEFT` | **←** |  |
| 22 | `&kp DOWN_ARROW` | **↓** |  |
| 23 | `&kp RIGHT` | **→** |  |
| 24 | `&none` | **—** |  |
| 25 | `&none` | **—** |  |
| 26 | `&none` | **—** |  |
| 27 | `&none` | **—** |  |
| 28 | `&none` | **—** |  |
| 29 | `&none` | **—** |  |
| 30 | `&kp DEL` | **Del** |  |
| 31 | `&none` | **—** |  |
| 32 | `&kp RET` | **Enter** |  |
| 33 | `&none` | **—** |  |

---

## Layer 3 — `symbol_layer` (Symbol Layer)

```

┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐   ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ 0 kp RA(Q)         │ 1 kp LS(SLASH)     │ 2 kp RA(N8)        │ 3 kp RA(N9)        │ 4 kp GRAVE         │   │ 5 kp LS(N1)        │ 6 kp NUBS          │ 7 kp LS(NUBS)      │ 8 kp LS(N0)        │ 9 kp LS(N6)        │
│   @                │   _                │   [                │   ]                │   ^                │   │   !                │   <                │   >                │   =                │   &                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│10 kp RA(MINUS)     │11 kp LS(N7)        │12 kp RA(N7)        │13 kp RA(N0)        │14 kp LS(RBKT)      │   │15 kp LS(MINUS)     │16 kp LS(N8)        │17 kp LS(N9)        │18 kp SLASH         │19 kp LS(DOT)       │
│   \                │   /                │   {                │   }                │   *                │   │   ?                │   (                │   )                │   -                │   :                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│20 kp NUHS          │21 kp LS(N4)        │22 kp RA(NUBS)      │23 kp RA(RBKT)      │24 kp LS(EQUAL)     │   │25 kp RBKT          │26 kp LS(N5)        │27 kp LS(N2)        │28 kp LS(NUHS)      │29 kp LS(COMMA)     │
│   '                │   $                │   |                │   ~                │   `                │   │   +                │   %                │   "                │   #                │   ;                │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘   └────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘
          ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┐
          │30 trans            │31 trans            │32 trans            │33 none             │
          │   ▽                │   ▽                │   ▽                │   —                │
          └────────────────────┴────────────────────┴────────────────────┴────────────────────┘

```

### Detaliu pe poziții

| # | ZMK | iese pe layout german | observații |
|---|---|---|---|
| 0 | `&kp RA(Q)` | **@** | Shift/AltGr citit pe poziția fizică germană |
| 1 | `&kp LS(SLASH)` | **_** | Shift/AltGr citit pe poziția fizică germană |
| 2 | `&kp RA(N8)` | **[** | Shift/AltGr citit pe poziția fizică germană |
| 3 | `&kp RA(N9)` | **]** | Shift/AltGr citit pe poziția fizică germană |
| 4 | `&kp GRAVE` | **^** |  |
| 5 | `&kp LS(N1)` | **!** | Shift/AltGr citit pe poziția fizică germană |
| 6 | `&kp NUBS` | **<** |  |
| 7 | `&kp LS(NUBS)` | **>** | Shift/AltGr citit pe poziția fizică germană |
| 8 | `&kp LS(N0)` | **=** | Shift/AltGr citit pe poziția fizică germană |
| 9 | `&kp LS(N6)` | **&** | Shift/AltGr citit pe poziția fizică germană |
| 10 | `&kp RA(MINUS)` | **\** | Shift/AltGr citit pe poziția fizică germană |
| 11 | `&kp LS(N7)` | **/** | Shift/AltGr citit pe poziția fizică germană |
| 12 | `&kp RA(N7)` | **{** | Shift/AltGr citit pe poziția fizică germană |
| 13 | `&kp RA(N0)` | **}** | Shift/AltGr citit pe poziția fizică germană |
| 14 | `&kp LS(RBKT)` | ***** | Shift/AltGr citit pe poziția fizică germană |
| 15 | `&kp LS(MINUS)` | **?** | Shift/AltGr citit pe poziția fizică germană |
| 16 | `&kp LS(N8)` | **(** | Shift/AltGr citit pe poziția fizică germană |
| 17 | `&kp LS(N9)` | **)** | Shift/AltGr citit pe poziția fizică germană |
| 18 | `&kp SLASH` | **-** |  |
| 19 | `&kp LS(DOT)` | **:** | Shift/AltGr citit pe poziția fizică germană |
| 20 | `&kp NUHS` | **'** |  |
| 21 | `&kp LS(N4)` | **$** | Shift/AltGr citit pe poziția fizică germană |
| 22 | `&kp RA(NUBS)` | **|** | Shift/AltGr citit pe poziția fizică germană |
| 23 | `&kp RA(RBKT)` | **~** | Shift/AltGr citit pe poziția fizică germană |
| 24 | `&kp LS(EQUAL)` | **`** | Shift/AltGr citit pe poziția fizică germană |
| 25 | `&kp RBKT` | **+** |  |
| 26 | `&kp LS(N5)` | **%** | Shift/AltGr citit pe poziția fizică germană |
| 27 | `&kp LS(N2)` | **"** | Shift/AltGr citit pe poziția fizică germană |
| 28 | `&kp LS(NUHS)` | **#** | Shift/AltGr citit pe poziția fizică germană |
| 29 | `&kp LS(COMMA)` | **;** | Shift/AltGr citit pe poziția fizică germană |
| 30 | `&trans` | **▽** | transparent: cade pe layer 0 |
| 31 | `&trans` | **▽** | transparent: cade pe layer 0 |
| 32 | `&trans` | **▽** | transparent: cade pe layer 0 |
| 33 | `&none` | **—** |  |

---

## Layer 4 — `nr_layer` (Number and F Layer)

```

┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐   ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ 0 kp F9            │ 1 kp F10           │ 2 kp F11           │ 3 kp F12           │ 4 trans            │   │ 5 kp SINGLE_QUOTE  │ 6 kp N7            │ 7 kp N8            │ 8 kp N9            │ 9 kp MINUS         │
│   F9               │   F10              │   F11              │   F12              │   ▽                │   │   ä                │   7                │   8                │   9                │   ß                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│10 kp F5            │11 kp F6            │12 kp F7            │13 kp F8            │14 trans            │   │15 kp SEMI          │16 kp N4            │17 kp N5            │18 kp N6            │19 kp N0            │
│   F5               │   F6               │   F7               │   F8               │   ▽                │   │   ö                │   4                │   5                │   6                │   0                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│20 kp F1            │21 kp F2            │22 kp F3            │23 kp F4            │24 trans            │   │25 kp LEFT_BRACKET  │26 kp N1            │27 kp N2            │28 kp N3            │29 trans            │
│   F1               │   F2               │   F3               │   F4               │   ▽                │   │   ü                │   1                │   2                │   3                │   ▽                │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘   └────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘
          ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┐
          │30 trans            │31 kp RET           │32 none             │33 kp BSPC          │
          │   ▽                │   Enter            │   —                │   Backspace        │
          └────────────────────┴────────────────────┴────────────────────┴────────────────────┘

```

### Detaliu pe poziții

| # | ZMK | iese pe layout german | observații |
|---|---|---|---|
| 0 | `&kp F9` | **F9** |  |
| 1 | `&kp F10` | **F10** |  |
| 2 | `&kp F11` | **F11** |  |
| 3 | `&kp F12` | **F12** |  |
| 4 | `&trans` | **▽** | transparent: cade pe layer 0 |
| 5 | `&kp SINGLE_QUOTE` | **ä** |  |
| 6 | `&kp N7` | **7** |  |
| 7 | `&kp N8` | **8** |  |
| 8 | `&kp N9` | **9** |  |
| 9 | `&kp MINUS` | **ß** |  |
| 10 | `&kp F5` | **F5** |  |
| 11 | `&kp F6` | **F6** |  |
| 12 | `&kp F7` | **F7** |  |
| 13 | `&kp F8` | **F8** |  |
| 14 | `&trans` | **▽** | transparent: cade pe layer 0 |
| 15 | `&kp SEMI` | **ö** |  |
| 16 | `&kp N4` | **4** |  |
| 17 | `&kp N5` | **5** |  |
| 18 | `&kp N6` | **6** |  |
| 19 | `&kp N0` | **0** |  |
| 20 | `&kp F1` | **F1** |  |
| 21 | `&kp F2` | **F2** |  |
| 22 | `&kp F3` | **F3** |  |
| 23 | `&kp F4` | **F4** |  |
| 24 | `&trans` | **▽** | transparent: cade pe layer 0 |
| 25 | `&kp LEFT_BRACKET` | **ü** |  |
| 26 | `&kp N1` | **1** |  |
| 27 | `&kp N2` | **2** |  |
| 28 | `&kp N3` | **3** |  |
| 29 | `&trans` | **▽** | transparent: cade pe layer 0 |
| 30 | `&trans` | **▽** | transparent: cade pe layer 0 |
| 31 | `&kp RET` | **Enter** |  |
| 32 | `&none` | **—** |  |
| 33 | `&kp BSPC` | **Backspace** |  |

---

## Layer 5 — `bt_layer` (Bluetooth Layer)

```

┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐   ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ 0 bt BT_SEL 0      │ 1 bt BT_SEL 1      │ 2 bt BT_SEL 2      │ 3 bt BT_SEL 3      │ 4 none             │   │ 5 none             │ 6 none             │ 7 none             │ 8 none             │ 9 none             │
│   BT               │   BT               │   BT               │   BT               │   —                │   │   —                │   —                │   —                │   —                │   —                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│10 none             │11 none             │12 none             │13 none             │14 none             │   │15 none             │16 none             │17 none             │18 none             │19 none             │
│   —                │   —                │   —                │   —                │   —                │   │   —                │   —                │   —                │   —                │   —                │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤   ├────────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│20 none             │21 none             │22 bt BT_NXT        │23 bt BT_PRV        │24 none             │   │25 none             │26 none             │27 none             │28 none             │29 none             │
│   —                │   —                │   BT               │   BT               │   —                │   │   —                │   —                │   —                │   —                │   —                │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘   └────────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘
          ┌────────────────────┬────────────────────┬────────────────────┬────────────────────┐
          │30 none             │31 none             │32 bt BT_CLR_ALL    │33 none             │
          │   —                │   —                │   BT               │   —                │
          └────────────────────┴────────────────────┴────────────────────┴────────────────────┘

```

### Detaliu pe poziții

| # | ZMK | iese pe layout german | observații |
|---|---|---|---|
| 0 | `&bt BT_SEL 0` | **BT** |  |
| 1 | `&bt BT_SEL 1` | **BT** |  |
| 2 | `&bt BT_SEL 2` | **BT** |  |
| 3 | `&bt BT_SEL 3` | **BT** |  |
| 4 | `&none` | **—** |  |
| 5 | `&none` | **—** |  |
| 6 | `&none` | **—** |  |
| 7 | `&none` | **—** |  |
| 8 | `&none` | **—** |  |
| 9 | `&none` | **—** |  |
| 10 | `&none` | **—** |  |
| 11 | `&none` | **—** |  |
| 12 | `&none` | **—** |  |
| 13 | `&none` | **—** |  |
| 14 | `&none` | **—** |  |
| 15 | `&none` | **—** |  |
| 16 | `&none` | **—** |  |
| 17 | `&none` | **—** |  |
| 18 | `&none` | **—** |  |
| 19 | `&none` | **—** |  |
| 20 | `&none` | **—** |  |
| 21 | `&none` | **—** |  |
| 22 | `&bt BT_NXT` | **BT** |  |
| 23 | `&bt BT_PRV` | **BT** |  |
| 24 | `&none` | **—** |  |
| 25 | `&none` | **—** |  |
| 26 | `&none` | **—** |  |
| 27 | `&none` | **—** |  |
| 28 | `&none` | **—** |  |
| 29 | `&none` | **—** |  |
| 30 | `&none` | **—** |  |
| 31 | `&none` | **—** |  |
| 32 | `&bt BT_CLR_ALL` | **BT** |  |
| 33 | `&none` | **—** |  |

---

## Combos (poziții fizice — nu depind de layout-ul sistemului)

| Combo | Poziții | Efect | Nota din keymap |
|---|---|---|---|
| `toggle_nav` | 0, 1, 2, 3 | `&tog 2` | QWFP (stanga, top row) = toggle layer 2 (nav/arrows) — 50ms default timeout |
| `toggle_qwertz` | 6, 7, 8, 9 | `&tog 1` | L U Z , (dreapta, top row, oglinda QWFP) = toggle qwertz |
| `toggle_bt` | 30, 31, 32, 33 (timeout 80 ms) | `&tog 5` | 4 thumbs = toggle layer 5 (BT) — intrare deliberata, aproape imposibil accidental |

---

## Capcanele layout-ului german (de ce arată așa coloana «DE»)

| Ce scrie în keymap | Ce iese pe US | Ce iese pe DE |
|---|---|---|
| `kp Y` / `kp Z` | y / z | **z / y** (inversate) |
| `kp SEMI` | ; | **ö** |
| `kp SINGLE_QUOTE` | ' | **ä** |
| `kp LEFT_BRACKET` | [ | **ü** |
| `kp MINUS` | - | **ß** (Shift = ?) |
| `kp SLASH` | / | **-** (Shift = _) |
| `kp EQUAL` | = | **´** (dead key; Shift = `) |
| `kp GRAVE` | ` | **^** (dead key; Shift = °) |
| `kp NUHS` | \ | **'** (Shift = #) |
| `kp RBKT` | ] | **+** (Shift = *) |
| `kp NUBS` | \ | **<** (Shift = >, AltGr = |) |
| `kp LS(N6)` | ^ | **&** |
| `kp LS(N7)` | & | **/** |
| `kp LS(N8)` | * | **(** |
| `kp LS(N0)` | ) | **=** |
| `kp LS(COMMA)` | < | **;** |
| `kp LS(DOT)` | > | **:** |
| `kp RA(N7)` | { | **{** |
| `kp RA(N8)` / `kp RA(N9)` | ( / ) | **[ / ]** |
| `kp RA(N0)` | } | **}** |
| `kp RA(Q)` | @ | **@** |
| `kp RA(MINUS)` | _ | **\\** |
| `kp RA(NUBS)` | | | **|** |

**De ce există layer 1 (`qwertz`):** rescrie aranjarea literelor în ordinea Q W E R T Z U I O P (ca poziții fizice). **Atenție:** pe un host german poziția care trimite `Z` dă `y`, iar cea care trimite `Y` dă `z` — layer 1 iese deci `q w e r t y u i o p`, cu Z și Y inversate față de o tastatură germană fizică. În layer 0 (Colemak-DH) swap-ul e aplicat: poziția de sus-dreapta care trimite `Z` dă `y`, iar cea de jos-stânga care trimite `Y` dă `z`.

## Surse pentru maparea germană

- https://kbdlayout.info/KBDGR/ — layout-ul Windows de-DE (KBDGR.DLL)
- https://en.wikipedia.org/wiki/German_keyboard_layout — QWERTZ, umlauturi, AltGr
- `config/cradio.keymap` — sursa de adevăr pentru bindings (branch `irinelturturea-colemak`)

Regenerare după orice modificare de keymap:

```sh
python3 tools/gen_cradio_layout_doc.py
```

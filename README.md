# Single-Digit BCD Adder — Build Runner

An interactive, single-file build guide for a breadboard BCD adder: two cascaded 4-bit
binary adders with automatic +6 correction, a CD4511 decoder, a seven-segment display,
and an LED for the tens digit.

Built for EEL 3705 (Fundamentals of Digital Circuits, University of South Florida),
Hands-On Project 2.

### ▶ [Open the build runner](https://buttonoperator.github.io/bcd-adder-build-runner/)

One HTML file, no build step, no dependencies. Works offline once loaded — clone the repo and
open [`index.html`](index.html) directly if you would rather not rely on the network at the
bench.

---

## What the circuit does

Enter two BCD digits (0–9 each) on a DIP switch. The circuit adds them, detects any answer
past 9, corrects it by six, and shows the result as a decimal digit plus a tens LED.

| Chip | Part | Takes in | Puts out | Meaning |
|---|---|---|---|---|
| U1 | 74HC283 | `A3..A0`, `B3..B0` | `K`, `Z3..Z0` | raw binary sum, 0–18 |
| U3 | 74HC08 | `Z3`, `Z2`, `Z1` | `Z3·Z2`, `Z3·Z1` | two partial "past 9" tests |
| U4 | 74HC32 | those two, `K` | `C` | correct-by-six flag, and the tens digit |
| U2 | 74HC283 | `Z3..Z0`, `0 C C 0` | `S3..S0` | corrected ones digit, 0–9 |
| U5 | CD4511 | `S3..S0` | `a`–`g` | segment drive |

### The correction logic

```
C = K + Z3·Z2 + Z3·Z1
```

`C` answers one question: did the answer go past 9? There are two ways it can.

**The K term.** `K = 1` means the sum reached 16 or more. Two BCD digits cap at 18, so
`K = 1` means 16, 17 or 18 — all past 9. `K` alone is proof.

**The gate terms** catch 10 through 15, where `K` is still 0. `Z3` alone will not do: it is
high for 8 through 15, and 8 and 9 are valid. Qualifying it with `Z2` or `Z1` covers 10–15
and leaves 8 (`1000`) and 9 (`1001`) alone.

> `Err = S3S2 + S3S1` without the carry term is incomplete. 9 + 9 = 18 = `10010`, so the sum
> pins read `0010` — a valid-looking 2 — and the AND gates see nothing wrong. Only `K` knows.

U2's B inputs are strapped `0 C C 0`, which is `0110` (six) when `C` is high and `0000` when
it is low, so U2 computes `Z + 6C` with no extra gates. U2's carry out is left open: it
duplicates `C`, which already drives the tens LED.

### Test vectors

| Sum | U1: `K Z3Z2Z1Z0` | Why C | U2 adds | `S3..S0` | Display |
|---|---|---|---|---|---|
| 3 + 4 | `0 0111` | Z3 = 0, K = 0 → C = 0 | `0000` | `0111` | 7, LED off |
| 7 + 2 | `0 1001` | Z3 = 1 but Z2 = Z1 = 0 → C = 0 | `0000` | `1001` | 9, LED off |
| 5 + 5 | `0 1010` | Z3·Z1 = 1 → C = 1 | `0110` | `0000` | 0, LED on = 10 |
| 7 + 5 | `0 1100` | Z3·Z2 = 1 → C = 1 | `0110` | `0010` | 2, LED on = 12 |
| 9 + 9 | `1 0010` | gates see nothing, K = 1 → C = 1 | `0110` | `1000` | 8, LED on = 18 |

Those five exercise every path. `7 + 2 = 9` with the LED off is the one that catches AND
gates wired to the wrong sum bits.

---

## What the page does

- **30 steps, one at a time.** Each shows where on the board you are, what to do, and a table
  of exact pin-to-pin connections.
- **A live IC pin map.** Every package with every pin numbered and labelled by the net it
  carries. Pins light blue for the current step and green once wired.
- **A step-scoped breadboard diagram.** All 254 drawn wire elements carry their step index,
  so only the current step's connections are lit; completed wires dim, future wires ghost.
- **An interactive logic-level map.** Set any two BCD digits and it solves the whole circuit,
  showing what a meter should read at every pin — operands, `K` and `Z3..Z0`, both AND terms,
  `C`, `S3..S0`, and all seven segment drives. Lines stay dashed until you reach the step that
  wires them, so the map fills in as you build. A live seven-segment preview shows the digit,
  including the CD4511's tail-less 6 and 9.
- **Both diagrams side by side**, with the step list in a sticky rail beside them, so the whole
  build fits in one view. Independent diagram zoom (50–320%), whole-page zoom, full-window mode.
- **Progress saved** in `localStorage`, with per-step undo.
- Reference drawers: adder theory, signal flow schematic, pinouts, parts list,
  troubleshooting, and test vectors.

### Keyboard

| Key | Action |
|---|---|
| <kbd>←</kbd> <kbd>→</kbd> | previous / next step |
| <kbd>+</kbd> <kbd>−</kbd> | zoom the diagram |
| <kbd>0</kbd> | reset diagram zoom |
| <kbd>F</kbd> | full window |
| <kbd>Esc</kbd> | exit full window |

---

## Notes on the parts

**Use 74HC, not 74LS.** The CD4511 needs `VIH ≥ 3.5 V` at a 5 V supply, while 74LS guarantees
only `VOH ≥ 2.7 V`. A 74LS adder driving the decoder sits in the gap. If 74LS is all you have,
add 4.7 kΩ pull-ups on `S3..S0`.

**The display must be common cathode.** The CD4511 sources current on its segment outputs.

**Strap the CD4511's control pins.** `/LT` (3) and `/BL` (4) to +5 V, `LE` (5) to GND. Floating
CMOS inputs do not stay put. Grounding `/LT` momentarily lights all seven segments, which is a
one-wire test of the whole display subassembly.

**Tie off every unused gate input.** Four spare inputs on the 74HC08 and four on the 74HC32.

---

## Rebuilding

The page is generated. `index.html` is committed, so you only need this if you change a
diagram or a step.

```bash
python build.py
```

Requires Python 3 and nothing else. The build runs three generators and then verifies the
result before writing:

- every pin reference in the step data resolves to a real element in the pin map
- every breadboard step stamp falls inside the step range
- every step that lists connections actually draws wires
- required element IDs appear exactly once
- no stale references from earlier revisions survive

| File | Produces |
|---|---|
| `src/gen.py` | `bb.svg` — hole-accurate breadboard placement, wires stamped by step |
| `src/gen2.py` | `flow.svg` — signal flow schematic |
| `src/gen3.py` | `chips.svg` — IC pin map, every pin individually addressable |
| `src/build.py` | inlines all three into `src/template.html` → `index.html` |

`src/template.html` holds the step data, the page CSS, and the runner logic, with
`<!--SVG-->`, `<!--FLOW-->` and `<!--CHIPS-->` as the injection points.

See [WIRING.md](WIRING.md) for the full net list in plain text.

---

## License

MIT. See [LICENSE](LICENSE).

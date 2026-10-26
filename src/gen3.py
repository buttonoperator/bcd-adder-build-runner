# -*- coding: utf-8 -*-
"""Live IC pin map: every package, every pin, addressable by id.

Each package also carries a readout box underneath it. The page fills those in
with the logic levels that chip produces for the operands under test, and marks
them NOW once the step that wires the chip is done, or TARGET before that.
"""
import io

out = []
def e(s):
    out.append(s)

PITCH = 26.0
BW = 104.0          # body width
PADW, PADH = 23.0, 16.0
HEAD = 44.0
CHIP_Y = 40.0                    # one row, left to right in signal order
RO_Y = 330.0                     # readouts, aligned across the whole row
STEP_X = 175.0
ROW = 150.0                      # readout box width (body + both pad columns)
ROH = 50.0

CHIPS = [
    # ref, part, pins (1..n in order), column, y, readout y
    ('SW1', 'DIP switch',
     ['A0', 'A1', 'A2', 'A3', 'B0', 'B1', 'B2', 'B3',
      '+5', '+5', '+5', '+5', '+5', '+5', '+5', '+5'], 0, CHIP_Y, RO_Y),
    ('U1', '74HC283',
     ['Z1', 'B1', 'A1', 'Z0', 'A0', 'B0', '0', 'GND',
      'K', 'Z3', 'B3', 'A3', 'Z2', 'A2', 'B2', '+5'], 1, CHIP_Y, RO_Y),
    ('U3', '74HC08',
     ['Z3', 'Z2', 'Z3·Z2', 'Z3', 'Z1', 'Z3·Z1', 'GND',
      'n/c', '0', '0', 'n/c', '0', '0', '+5'], 2, CHIP_Y, RO_Y),
    ('U4', '74HC32',
     ['Z3·Z2', 'Z3·Z1', 'N3', 'N3', 'K', 'C', 'GND',
      'n/c', '0', '0', 'n/c', '0', '0', '+5'], 3, CHIP_Y, RO_Y),
    ('U2', '74HC283',
     ['S1', 'C', 'Z1', 'S0', 'Z0', '0', '0', 'GND',
      'n/c', 'S3', '0', 'Z3', 'S2', 'Z2', 'C', '+5'], 4, CHIP_Y, RO_Y),
    ('U5', 'CD4511',
     ['S1', 'S2', '/LT', '/BL', 'LE', 'S3', 'S0', 'GND',
      'e', 'd', 'c', 'b', 'a', 'g', 'f', '+5'], 5, CHIP_Y, RO_Y),
    ('DS1', '7-seg CC',
     ['e', 'd', 'CC', 'c', 'dp', 'b', 'a', 'CC', 'f', 'g'], 6, CHIP_Y, RO_Y),
]

def draw(ref, part, names, col, y, roy):
    x = 30.0 + col * STEP_X
    n = len(names)
    half = n // 2
    h = HEAD + half * PITCH + 10
    e('<g class="pkgwrap">')
    e('<rect class="cbody" id="c-%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6"/>'
      % (ref, x, y, BW, h))
    e('<path class="cnotch" d="M %.1f %.1f a 9 9 0 0 0 18 0"/>' % (x + BW / 2 - 9, y))
    e('<text class="cref" x="%.1f" y="%.1f">%s</text>' % (x + BW / 2, y + 22, ref))
    e('<text class="cpart" x="%.1f" y="%.1f">%s</text>' % (x + BW / 2, y + 35, part))
    for i in range(half):
        lp = i + 1                 # left column, top to bottom
        rp = n - i                 # right column, top to bottom
        py = y + HEAD + i * PITCH + PADH / 2 + 2
        # left
        e('<g class="pin" id="p-%s-%d">' % (ref, lp))
        e('<rect class="pad" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"/>'
          % (x - PADW - 1, py - PADH / 2, PADW, PADH))
        e('<text class="pnum" x="%.1f" y="%.1f">%d</text>' % (x - PADW / 2 - 1, py + 3.8, lp))
        e('<text class="pnet pnl" x="%.1f" y="%.1f">%s</text>' % (x + 7, py + 3.8, names[lp - 1]))
        e('</g>')
        # right
        e('<g class="pin" id="p-%s-%d">' % (ref, rp))
        e('<rect class="pad" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"/>'
          % (x + BW + 1, py - PADH / 2, PADW, PADH))
        e('<text class="pnum" x="%.1f" y="%.1f">%d</text>' % (x + BW + PADW / 2 + 1, py + 3.8, rp))
        e('<text class="pnet pnr" x="%.1f" y="%.1f">%s</text>' % (x + BW - 7, py + 3.8, names[rp - 1]))
        e('</g>')
    # stem from the package down to its readout
    e('<line class="rostem" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
      % (x + BW / 2, y + h, x + BW / 2, roy))
    # readout
    rx = x - PADW - 1
    e('<g class="ro" id="ro-%s">' % ref)
    e('<rect class="robox" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="7"/>'
      % (rx, roy, ROW, ROH))
    e('<rect class="robar" x="%.1f" y="%.1f" width="3.5" height="%.1f" rx="2"/>'
      % (rx, roy + 7, ROH - 14))
    e('<text class="rotag" id="rotag-%s" x="%.1f" y="%.1f">TARGET</text>'
      % (ref, rx + 11, roy + 15))
    e('<text class="rol1" id="rol1-%s" x="%.1f" y="%.1f"></text>' % (ref, rx + 11, roy + 30))
    e('<text class="rol2" id="rol2-%s" x="%.1f" y="%.1f"></text>' % (ref, rx + 11, roy + 43))
    e('</g>')
    e('</g>')
    return roy + ROH

maxb = 0
for ref, part, names, col, y, roy in CHIPS:
    maxb = max(maxb, draw(ref, part, names, col, y, roy))

W = 30 + (len(CHIPS) - 1) * STEP_X + BW + PADW + 40
svg = ('<svg id="cm" viewBox="0 0 %.0f %.0f" xmlns="http://www.w3.org/2000/svg" role="img" '
       'aria-label="Pin map of every IC in the build, with the logic levels each one produces">'
       % (W, maxb + 20)) + '\n'.join(out) + '</svg>'
io.open('chips.svg', 'w', encoding='utf-8').write(svg)
print('ok', len(svg), 'w', W, 'h', maxb + 20)

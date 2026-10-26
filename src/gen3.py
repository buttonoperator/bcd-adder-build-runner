# -*- coding: utf-8 -*-
"""Live IC pin map: every package, every pin, addressable by id."""
import io

out = []
def e(s):
    out.append(s)

PITCH = 26.0
BW = 104.0          # body width
PADW, PADH = 23.0, 16.0
HEAD = 44.0

CHIPS = [
    # ref, part, pins (1..n in order), x, y
    ('SW1', 'DIP switch',
     ['A0', 'A1', 'A2', 'A3', 'B0', 'B1', 'B2', 'B3',
      '+5', '+5', '+5', '+5', '+5', '+5', '+5', '+5'], 30, 40),
    ('U1', '74HC283',
     ['Z1', 'B1', 'A1', 'Z0', 'A0', 'B0', '0', 'GND',
      'K', 'Z3', 'B3', 'A3', 'Z2', 'A2', 'B2', '+5'], 205, 40),
    ('U3', '74HC08',
     ['Z3', 'Z2', 'Z3·Z2', 'Z3', 'Z1', 'Z3·Z1', 'GND',
      'n/c', '0', '0', 'n/c', '0', '0', '+5'], 380, 40),
    ('U4', '74HC32',
     ['Z3·Z2', 'Z3·Z1', 'N3', 'N3', 'K', 'C', 'GND',
      'n/c', '0', '0', 'n/c', '0', '0', '+5'], 555, 40),
    ('U2', '74HC283',
     ['S1', 'C', 'Z1', 'S0', 'Z0', '0', '0', 'GND',
      'n/c', 'S3', '0', 'Z3', 'S2', 'Z2', 'C', '+5'], 30, 330),
    ('U5', 'CD4511',
     ['S1', 'S2', '/LT', '/BL', 'LE', 'S3', 'S0', 'GND',
      'e', 'd', 'c', 'b', 'a', 'g', 'f', '+5'], 205, 330),
    ('DS1', '7-seg CC',
     ['e', 'd', 'CC', 'c', 'dp', 'b', 'a', 'CC', 'f', 'g'], 380, 330),
]

def draw(ref, part, names, x, y):
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
    e('</g>')
    return h

maxb = 0
for ref, part, names, x, y in CHIPS:
    hh = draw(ref, part, names, x, y)
    maxb = max(maxb, y + hh)

W = 555 + BW + PADW + 40
svg = ('<svg id="cm" viewBox="0 0 %.0f %.0f" xmlns="http://www.w3.org/2000/svg" role="img" '
       'aria-label="Pin map of every IC in the build, highlighted by step">'
       % (W, maxb + 24)) + '\n'.join(out) + '</svg>'
io.open('chips.svg', 'w', encoding='utf-8').write(svg)
print('ok', len(svg), 'w', W, 'h', maxb + 24)

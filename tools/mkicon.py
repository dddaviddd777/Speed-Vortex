"""Genera el logo de Speed Vortex (SVG) i les icones PNG a partir d'ell.
Ús: pip install resvg-py && python tools/mkicon.py .
"""
import sys, pathlib, resvg_py

out = pathlib.Path(sys.argv[1]) / 'icons'
out.mkdir(exist_ok=True)

VX, VY = 256, 196          # punt de fuga del túnel


def rings():
    s = []
    n = 9
    for i in range(n):
        t = (i + 1) / n
        r = 14 + 330 * t ** 2.2
        cy = VY + 70 * t ** 1.5
        col = '#6be3ff' if i % 2 else '#b46bff'
        op = 0.18 + 0.72 * t
        w = 2 + 16 * t ** 1.6
        s.append(f'<circle cx="{VX}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{col}" '
                 f'stroke-opacity="{op:.2f}" stroke-width="{w:.1f}"/>')
    import math
    for j in range(16):          # línies longitudinals del túnel, com la malla del joc
        a = j * math.pi / 8 + math.pi / 16
        x, y = VX + 520 * math.cos(a), VY + 70 + 520 * math.sin(a)
        s.append(f'<line x1="{VX}" y1="{VY}" x2="{x:.1f}" y2="{y:.1f}" stroke="#8fe9ff" '
                 f'stroke-opacity=".22" stroke-width="3"/>')
    return '\n  '.join(s)


def svg(rx):
    k, ox, oy = 150, 256, 372
    P = lambda u, v: f'{ox + u * k:.1f},{oy - v * k * .8:.1f}'
    apex, rw, notch, lw = P(0, 1), P(.55, -.4), P(0, -.1), P(-.55, -.4)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
<defs>
  <clipPath id="c"><rect width="512" height="512" rx="{rx}"/></clipPath>
  <radialGradient id="bg" cx="{VX}" cy="{VY}" r="400" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#ffe3c8"/>
    <stop offset=".06" stop-color="#ff9b6b"/>
    <stop offset=".22" stop-color="#5a2f8f"/>
    <stop offset=".6" stop-color="#1b1640"/>
    <stop offset="1" stop-color="#0f1226"/>
  </radialGradient>
  <linearGradient id="sl" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffe0c8"/><stop offset="1" stop-color="#ffb48a"/>
  </linearGradient>
  <linearGradient id="sr" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ff9b6b"/><stop offset="1" stop-color="#ff5f45"/>
  </linearGradient>
  <filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="rg" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.2"/></filter>
</defs>
<g clip-path="url(#c)">
  <rect width="512" height="512" fill="url(#bg)"/>
  <g filter="url(#rg)">
  {rings()}
  </g>
  <polygon points="{apex} {rw} {notch} {lw}" fill="#ff9b6b" opacity=".85" filter="url(#gl)"/>
  <polygon points="{apex} {notch} {lw}" fill="url(#sl)"/>
  <polygon points="{apex} {rw} {notch}" fill="url(#sr)"/>
</g>
</svg>'''


def png(src, size, name):
    data = resvg_py.svg_to_bytes(svg_string=src, width=size, height=size)
    (out / name).write_bytes(bytes(data))


rounded, full = svg(112), svg(0)
(out / 'icon.svg').write_text(rounded, encoding='utf-8')
for s in (192, 512):
    png(rounded, s, f'icon-{s}.png')
    png(full, s, f'icon-maskable-{s}.png')
png(full, 180, 'apple-touch-icon.png')
png(rounded, 32, 'favicon-32.png')
print(sorted(p.name for p in out.iterdir()))

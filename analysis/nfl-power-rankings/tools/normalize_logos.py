#!/usr/bin/env python3
"""Normalise the club-mark SVGs so they render consistently inside a disc.

Why this exists
---------------
Every mark downloaded from the NFL CDN is nominally 500x500, but they use very
different fractions of that canvas: the Bengals' ink spans 72% of it, the
Broncos' 96%. A plain `object-fit: contain` inside a fixed circle therefore
produces unequal visual weights — some logos touching the rim, others floating
in the middle — and no single CSS value fixes it.

The fix belongs in the asset: each file's `viewBox` is rewritten to its ink
bounds plus a small margin, leaving the artwork untouched. Afterwards every mark
occupies the same fraction of its own canvas, so any container that sizes them
equally shows them equally.

Measurement is done from **rendered pixels**, not from path data. The first
attempt at this walked SVG geometry and produced nonsense: cubic Bezier control
points routinely sit far outside the curve they steer, and this data also uses
implicit command repetition (`c` followed by several 6-number groups), so a
naive parse reports boxes well outside the canvas. Rendering each mark to a
known-size PNG and measuring ink is both simpler and exactly right:

*   ink = opaque and either non-white, or white *enclosed* by the mark. Exterior
      white is found by flood-filling from the border, so the white in a Colts
      horseshoe or a Bears "C" counts as part of the mark while the transparent
      background does not.

Usage
-----
    # 1. render each SVG to <size>x<size> PNGs (headless Chrome, one per file)
    # 2. measure and rewrite
    python3 tools/normalize_logos.py --png-dir /tmp/ink --check
    python3 tools/normalize_logos.py --png-dir /tmp/ink

`--check` reports the current fill without writing anything.
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import struct
import sys
import zlib

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_SVG_DIR = HERE.parent.parent.parent / "public" / "images" / "nfl"

# Leave 4% of canvas on each side so a square ink box does not sit flush
# against the edge of its container.
MARGIN = 0.04
# A pixel is "near white" at or above this on every channel.
WHITE = 246
# Alpha at or below this is treated as transparent.
ALPHA = 40
# Native canvas of every mark as downloaded, in SVG user units.
CANVAS = 500.0


# --- minimal PNG reader (no third-party libraries anywhere in this pipeline) ---


def read_png(path: pathlib.Path) -> tuple[int, int, int, list[bytes]]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG")
    pos = 8
    idat = bytearray()
    width = height = channels = 0
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        chunk_type = data[pos + 4 : pos + 8]
        chunk = data[pos + 8 : pos + 8 + length]
        if chunk_type == b"IHDR":
            width, height, depth, color, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
            if depth != 8 or interlace != 0:
                raise ValueError(f"{path}: only 8-bit non-interlaced PNGs are supported")
            channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color]
        elif chunk_type == b"IDAT":
            idat += chunk
        elif chunk_type == b"IEND":
            break
        pos += 12 + length

    raw = zlib.decompress(bytes(idat))
    stride = width * channels
    rows: list[bytes] = []
    previous = bytearray(stride)
    cursor = 0
    for _ in range(height):
        filter_type = raw[cursor]
        cursor += 1
        line = bytearray(raw[cursor : cursor + stride])
        cursor += stride
        if filter_type == 1:
            for x in range(channels, stride):
                line[x] = (line[x] + line[x - channels]) & 0xFF
        elif filter_type == 2:
            for x in range(stride):
                line[x] = (line[x] + previous[x]) & 0xFF
        elif filter_type == 3:
            for x in range(stride):
                left = line[x - channels] if x >= channels else 0
                line[x] = (line[x] + ((left + previous[x]) >> 1)) & 0xFF
        elif filter_type == 4:
            for x in range(stride):
                left = line[x - channels] if x >= channels else 0
                up = previous[x]
                up_left = previous[x - channels] if x >= channels else 0
                estimate = left + up - up_left
                da, db, dc = abs(estimate - left), abs(estimate - up), abs(estimate - up_left)
                predictor = left if (da <= db and da <= dc) else (up if db <= dc else up_left)
                line[x] = (line[x] + predictor) & 0xFF
        rows.append(bytes(line))
        previous = line
    return width, height, channels, rows


def ink_bounds(path: pathlib.Path) -> tuple[int, int, int, int] | None:
    """Bounding box of the mark's ink, in pixels."""
    width, height, channels, rows = read_png(path)
    opaque = bytearray(width * height)
    near_white = bytearray(width * height)

    for y, row in enumerate(rows):
        base = y * width
        for x in range(width):
            offset = x * channels
            if channels >= 3:
                r, g, b = row[offset], row[offset + 1], row[offset + 2]
                alpha = row[offset + 3] if channels == 4 else 255
            else:
                r = g = b = row[offset]
                alpha = row[offset + 1] if channels == 2 else 255
            if alpha <= ALPHA:
                continue
            index = base + x
            opaque[index] = 1
            if r >= WHITE and g >= WHITE and b >= WHITE:
                near_white[index] = 1

    # Flood-fill near-white pixels reachable from the border: that is backdrop.
    # Near-white pixels the fill cannot reach are enclosed detail and count.
    backdrop = bytearray(width * height)
    queue: collections.deque[int] = collections.deque()

    def seed(index: int) -> None:
        if near_white[index] and not backdrop[index]:
            backdrop[index] = 1
            queue.append(index)

    for x in range(width):
        seed(x)
        seed((height - 1) * width + x)
    for y in range(height):
        seed(y * width)
        seed(y * width + width - 1)
    while queue:
        index = queue.popleft()
        x, y = index % width, index // width
        if x > 0:
            seed(index - 1)
        if x < width - 1:
            seed(index + 1)
        if y > 0:
            seed(index - width)
        if y < height - 1:
            seed(index + width)

    min_x, min_y, max_x, max_y = width, height, -1, -1
    for y in range(height):
        base = y * width
        for x in range(width):
            index = base + x
            if opaque[index] and not backdrop[index]:
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
    if max_x < 0:
        return None
    return min_x, min_y, max_x, max_y


def square_viewbox(bounds: tuple[int, int, int, int]):
    """A generous square viewBox centred on the ink.

    The frame must NOT hug the artwork. If ink reaches the image edge the
    browser anti-aliases that boundary, and any white part of the mark then
    shows a square seam against the badge behind it. Wrapping each mark in a
    square that is at least as large as the original 500-unit canvas keeps the
    artwork strictly interior while holding size variation to a few percent.
    """
    min_x, min_y, max_x, max_y = bounds
    ink_w = max_x - min_x + 1
    ink_h = max_y - min_y + 1
    side = max(CANVAS, max(ink_w, ink_h) * (1 + 2 * MARGIN))
    return (min_x + max_x + 1) / 2 - side / 2, (min_y + max_y + 1) / 2 - side / 2, side


def strip_canvas_plates(svg: str) -> tuple[str, int]:
    """Remove full-canvas background plates.

    Eleven of the marks carry a `<path d="M0 0h500v500H0z"/>` (or an equivalent
    full-size `<rect>`) as a backdrop. They paint nothing useful once the mark
    sits on the widget's own disc, and a plate that carries a white fill would
    draw exactly the square seam this tool exists to prevent.
    """
    pattern = re.compile(
        r"<(?:path|rect)\b[^>]*?(?:d=\"M0[ ,]0h500v500H0z\"|width=\"500\"[^>]*?height=\"500\")[^>]*/?>",
        re.I,
    )

    def keep(match: re.Match[str]) -> str:
        tag = match.group(0)
        if tag.lower().startswith("<rect") and 'fill="none"' in tag:
            return tag
        return ""

    return pattern.sub(keep, svg), len(pattern.findall(svg))


def rewrite_viewbox(svg: str, x: float, y: float, side: float) -> str:
    value = f"{round(x, 2):g} {round(y, 2):g} {round(side, 2):g} {round(side, 2):g}"
    root = re.search(r"<svg\b[^>]*>", svg)
    if not root:
        raise ValueError("no <svg> root element")
    tag = root.group(0)
    if "viewBox" in tag:
        new_tag = re.sub(r'\bviewBox\s*=\s*"[^"]*"', f'viewBox="{value}"', tag)
    else:
        new_tag = tag[:-1] + f' viewBox="{value}">'
    return svg[: root.start()] + new_tag + svg[root.end() :]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--svg-dir", type=pathlib.Path, default=DEFAULT_SVG_DIR)
    parser.add_argument("--png-dir", type=pathlib.Path, default=None,
                        help="directory of <abbr>.png renders at the SVG's native size")
    parser.add_argument("--check", action="store_true", help="report only, write nothing")
    parser.add_argument("--force", action="store_true", help="rewrite already-square viewBoxes")
    args = parser.parse_args()

    if args.png_dir is None:
        parser.error("--png-dir is required (render each SVG first)")

    svgs = sorted(args.svg_dir.glob("*.svg"))
    if not svgs:
        print(f"error: no SVGs in {args.svg_dir}", file=sys.stderr)
        return 2

    failures = 0
    fills: list[tuple[str, float]] = []
    for svg_path in svgs:
        png_path = args.png_dir / f"{svg_path.stem}.png"
        if not png_path.exists():
            print(f"  {svg_path.stem:5} no render at {png_path}", file=sys.stderr)
            failures += 1
            continue
        bounds = ink_bounds(png_path)
        if bounds is None:
            print(f"  {svg_path.stem:5} render is empty", file=sys.stderr)
            failures += 1
            continue
        x, y, side = square_viewbox(bounds)
        fill = max(bounds[2] - bounds[0] + 1, bounds[3] - bounds[1] + 1) / side
        pad = min(
            (bounds[0] - x) / side, (bounds[1] - y) / side,
            (x + side - bounds[2]) / side, (y + side - bounds[3]) / side,
        )
        fills.append((svg_path.stem, fill))
        print(
            f"  {svg_path.stem:5} ink fills {fill:5.1%} of frame, "
            f"smallest margin {pad:5.1%}"
        )
        if not args.check:
            svg = svg_path.read_text(encoding="utf-8")
            svg, plates = strip_canvas_plates(svg)
            if plates:
                print(f"        removed {plates} full-canvas plate{'s' if plates > 1 else ''}")
            svg_path.write_text(rewrite_viewbox(svg, x, y, side), encoding="utf-8")

    if fills:
        values = sorted(f for _, f in fills)
        print(
            f"\nink span: min {values[0]:.1%}  median {values[len(values) // 2]:.1%}  "
            f"max {values[-1]:.1%}  (spread {values[-1] / values[0]:.2f}x)"
        )
    verb = "checked" if args.check else "normalised"
    print(f"{len(svgs) - failures} {verb}, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

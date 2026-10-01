#!/usr/bin/env python3
"""Static checks for editable, accessible diagram SVGs.

This catches structural mistakes and common geometry risks. It deliberately does
not claim to replace browser rendering or manual connector tracing.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SVG_NS = "http://www.w3.org/2000/svg"
KNOWN_RATIOS = {
    "16:9": 16 / 9,
    "4:3": 4 / 3,
    "3:4": 3 / 4,
    "1:1": 1.0,
}
DISCOURAGED = {
    "foreignObject": "viewer-dependent HTML layout",
    "filter": "filter/shadow effect",
    "linearGradient": "gradient fill",
    "radialGradient": "gradient fill",
    "animate": "animation in a static deliverable",
    "animateTransform": "animation in a static deliverable",
    "image": "embedded raster image",
}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def number(value: str | None) -> float | None:
    if value is None:
        return None
    match = re.match(r"\s*(-?(?:\d+(?:\.\d*)?|\.\d+))", value)
    return float(match.group(1)) if match else None


def parse_viewbox(raw: str | None) -> tuple[float, float, float, float] | None:
    if not raw:
        return None
    parts = re.split(r"[\s,]+", raw.strip())
    if len(parts) != 4:
        return None
    try:
        values = tuple(float(part) for part in parts)
    except ValueError:
        return None
    if values[2] <= 0 or values[3] <= 0:
        return None
    return values  # type: ignore[return-value]


def outside(value: float, low: float, high: float, tolerance: float = 0.5) -> bool:
    return value < low - tolerance or value > high + tolerance


def check_simple_geometry(
    element: ET.Element,
    viewbox: tuple[float, float, float, float],
    warnings: list[str],
) -> None:
    if element.get("transform"):
        return
    name = local_name(element.tag)
    min_x, min_y, width, height = viewbox
    max_x, max_y = min_x + width, min_y + height

    def warn_bounds(label: str, xs: list[float], ys: list[float]) -> None:
        if any(outside(x, min_x, max_x) for x in xs) or any(
            outside(y, min_y, max_y) for y in ys
        ):
            ident = element.get("id", "unnamed")
            warnings.append(f"{label} #{ident} may extend outside the viewBox")

    if name == "rect":
        x, y = number(element.get("x")) or 0, number(element.get("y")) or 0
        w, h = number(element.get("width")), number(element.get("height"))
        if w is not None and h is not None:
            warn_bounds("rect", [x, x + w], [y, y + h])
    elif name == "circle":
        cx, cy, radius = (
            number(element.get("cx")) or 0,
            number(element.get("cy")) or 0,
            number(element.get("r")),
        )
        if radius is not None:
            warn_bounds("circle", [cx - radius, cx + radius], [cy - radius, cy + radius])
    elif name == "ellipse":
        cx, cy = number(element.get("cx")) or 0, number(element.get("cy")) or 0
        rx, ry = number(element.get("rx")), number(element.get("ry"))
        if rx is not None and ry is not None:
            warn_bounds("ellipse", [cx - rx, cx + rx], [cy - ry, cy + ry])
    elif name == "line":
        values = [number(element.get(key)) for key in ("x1", "y1", "x2", "y2")]
        if all(value is not None for value in values):
            x1, y1, x2, y2 = values  # type: ignore[misc]
            warn_bounds("line", [x1, x2], [y1, y2])
    elif name in {"text", "tspan"}:
        x, y = number(element.get("x")), number(element.get("y"))
        if x is not None and y is not None:
            warn_bounds(name, [x], [y])


def text_content(element: ET.Element) -> str:
    return "".join(element.itertext()).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path, help="SVG file to validate")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as failures after printing the full report",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    try:
        raw = args.svg.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read {args.svg}: {exc}", file=sys.stderr)
        return 2

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        print(f"ERROR: invalid XML: {exc}", file=sys.stderr)
        return 2

    if local_name(root.tag) != "svg":
        errors.append("root element is not <svg>")
    if not root.tag.startswith(f"{{{SVG_NS}}}") and root.get("xmlns") != SVG_NS:
        errors.append("SVG namespace is missing")

    viewbox = parse_viewbox(root.get("viewBox"))
    if viewbox is None:
        errors.append("a valid positive viewBox is required")
    else:
        ratio = viewbox[2] / viewbox[3]
        profile, expected = min(KNOWN_RATIOS.items(), key=lambda item: abs(item[1] - ratio))
        if not math.isclose(ratio, expected, rel_tol=0.015, abs_tol=0.015):
            errors.append(
                f"viewBox ratio {ratio:.4f} does not match 16:9, 4:3, 3:4, or 1:1"
            )
        else:
            print(f"Canvas profile: {profile} ({viewbox[2]:g}×{viewbox[3]:g})")

    ids: dict[str, ET.Element] = {}
    for element in root.iter():
        ident = element.get("id")
        if ident:
            if ident in ids:
                errors.append(f"duplicate id: {ident}")
            ids[ident] = element

    titles = [element for element in root.iter() if local_name(element.tag) == "title"]
    descs = [element for element in root.iter() if local_name(element.tag) == "desc"]
    if root.get("role") != "img":
        errors.append('root must declare role="img"')
    if not titles or not text_content(titles[0]):
        errors.append("a non-empty <title> is required")
    if not descs or not text_content(descs[0]):
        errors.append("a non-empty <desc> is required")

    labelled = set((root.get("aria-labelledby") or "").split())
    for label, elements in (("title", titles), ("desc", descs)):
        if elements:
            ident = elements[0].get("id")
            if not ident:
                errors.append(f"<{label}> must have an id")
            elif ident not in labelled:
                errors.append(f"aria-labelledby must reference {label} id '{ident}'")

    if "Times New Roman" not in raw:
        warnings.append("Times New Roman fallback stack is not declared")
    if not any(font in raw for font in ("Songti SC", "SimSun", "STSong")):
        warnings.append("Songti/SimSun Chinese fallback stack is not declared")

    for element in root.iter():
        name = local_name(element.tag)
        if name in DISCOURAGED:
            warnings.append(f"<{name}> uses {DISCOURAGED[name]}")
        if viewbox is not None:
            check_simple_geometry(element, viewbox, warnings)

        for attr in ("marker-start", "marker-mid", "marker-end"):
            value = element.get(attr)
            if value:
                match = re.fullmatch(r"url\(#([^)]+)\)", value.strip())
                if not match:
                    errors.append(f"unsupported {attr} reference: {value}")
                elif match.group(1) not in ids:
                    errors.append(f"{attr} references missing id: {match.group(1)}")

        if name in {"path", "line", "polyline"} and any(
            element.get(attr) for attr in ("marker-start", "marker-end")
        ):
            source, target = element.get("data-from"), element.get("data-to")
            ident = element.get("id", "unnamed connector")
            if not source or not target:
                warnings.append(f"{ident} should declare data-from and data-to")
            else:
                if source not in ids:
                    errors.append(f"{ident} data-from references missing id: {source}")
                if target not in ids:
                    errors.append(f"{ident} data-to references missing id: {target}")
            if not element.get("data-relation"):
                warnings.append(f"{ident} should declare data-relation")

        if name == "text":
            content = re.sub(r"\s+", " ", text_content(element))
            has_tspans = any(local_name(child.tag) == "tspan" for child in element)
            cjk_count = len(re.findall(r"[\u3400-\u9fff]", content))
            if not has_tspans and (cjk_count > 24 or len(content) > 55):
                warnings.append(
                    f"long unwrapped text near id '{element.get('id', 'unnamed')}': {content[:40]!r}"
                )

    print(f"Elements with IDs: {len(ids)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    failed = bool(errors) or (args.strict and bool(warnings))
    if failed:
        print(
            f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)"
            + (" (strict mode)" if args.strict else "")
        )
        return 1

    print(f"PASS: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


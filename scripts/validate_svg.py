#!/usr/bin/env python3
"""Static checks for editable, accessible diagram SVGs.

This catches structural mistakes and common geometry risks:

- structure, ids, title/desc, viewBox profile, discouraged elements;
- ordered-flow sequence numbering and visible badges;
- connector endpoints that stop short of, or sink inside, their data-from /
  data-to node rectangles;
- text lines whose estimated width overflows, or crowds, the node rectangle.

It deliberately does not claim to replace browser rendering or manual connector
tracing. Width estimates assume serif CJK/Latin mixes and err on the wide side.
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


# ---------------------------------------------------------------------------
# Geometry checks: connector endpoints and text overflow
# ---------------------------------------------------------------------------

CONNECTOR_SNAP_TOLERANCE = 1.0  # units: endpoint must sit on the boundary
MIN_TEXT_PADDING = 20.0  # units at 1600×900 scale, each side


def parse_css_classes(root: ET.Element) -> dict[str, dict[str, str]]:
    """Extract `.class { prop: value; }` rules from inline <style> blocks."""
    css = "".join(
        element.text or ""
        for element in root.iter()
        if local_name(element.tag) == "style"
    )
    rules: dict[str, dict[str, str]] = {}
    for selector, body in re.findall(r"\.([\w-]+)\s*\{([^}]*)\}", css):
        props: dict[str, str] = {}
        for declaration in body.split(";"):
            if ":" in declaration:
                key, value = declaration.split(":", 1)
                props[key.strip()] = value.strip()
        rules.setdefault(selector, {}).update(props)
    return rules


def estimate_text_width(text: str, font_size: float, bold: bool) -> float:
    """Rough advance width for serif CJK/Latin mixes; errs on the wide side."""
    width = 0.0
    for char in text:
        code = ord(char)
        if (
            0x3000 <= code <= 0x303F
            or 0x3400 <= code <= 0x9FFF
            or 0xFF00 <= code <= 0xFFEF
        ):
            width += 1.0
        elif char == " ":
            width += 0.25
        elif char.isdigit():
            width += 0.5
        elif char.isupper():
            width += 0.68
        elif char.isalpha():
            width += 0.46
        elif char in ".,:;'":
            width += 0.28
        else:
            width += 0.5
    return width * font_size * (1.06 if bold else 1.0)


def resolve_font(
    element: ET.Element,
    css: dict[str, dict[str, str]],
    inherited: tuple[float, bool, str],
) -> tuple[float, bool, str]:
    size, bold, anchor = inherited
    for cls in (element.get("class") or "").split():
        rule = css.get(cls, {})
        if "font-size" in rule:
            size = number(rule["font-size"]) or size
        if rule.get("font-weight") in {"700", "bold", "800", "900"}:
            bold = True
        if "text-anchor" in rule:
            anchor = rule["text-anchor"]
    if element.get("font-size"):
        size = number(element.get("font-size")) or size
    if element.get("font-weight") in {"700", "bold", "800", "900"}:
        bold = True
    if element.get("text-anchor"):
        anchor = element.get("text-anchor") or anchor
    return size, bold, anchor


def node_rects(root: ET.Element) -> dict[str, tuple[float, float, float, float]]:
    """Map each <g id> to the bounds of its first direct <rect> child."""
    rects: dict[str, tuple[float, float, float, float]] = {}
    for group in root.iter():
        if local_name(group.tag) != "g" or not group.get("id"):
            continue
        if group.get("transform"):
            continue
        for child in group:
            if local_name(child.tag) == "rect" and child.get("width"):
                rects[group.get("id", "")] = (
                    number(child.get("x")) or 0.0,
                    number(child.get("y")) or 0.0,
                    number(child.get("width")) or 0.0,
                    number(child.get("height")) or 0.0,
                )
                break
    return rects


def check_text_overflow(
    root: ET.Element,
    rects: dict[str, tuple[float, float, float, float]],
    warnings: list[str],
) -> None:
    css = parse_css_classes(root)
    for group in root.iter():
        group_id = group.get("id")
        if local_name(group.tag) != "g" or group_id not in rects:
            continue
        rect_x, _rect_y, rect_w, _rect_h = rects[group_id]
        for text in group.iter():
            if local_name(text.tag) != "text":
                continue
            base = resolve_font(text, css, (16.0, False, "start"))
            base_x = number(text.get("x")) or 0.0
            lines: list[tuple[float, str, float, bool, str]] = []
            tspans = [child for child in text if local_name(child.tag) == "tspan"]
            if tspans:
                for tspan in tspans:
                    size, bold, anchor = resolve_font(tspan, css, base)
                    x = number(tspan.get("x"))
                    lines.append((base_x if x is None else x, (tspan.text or "").strip(), size, bold, anchor))
            else:
                lines.append((base_x, (text.text or "").strip(), *base))
            for x, content, size, bold, anchor in lines:
                if not content:
                    continue
                width = estimate_text_width(content, size, bold)
                if anchor == "middle":
                    left, right = x - width / 2, x + width / 2
                elif anchor == "end":
                    left, right = x - width, x
                else:
                    left, right = x, x + width
                pad_left = left - rect_x
                pad_right = rect_x + rect_w - right
                if pad_right < 0 or pad_left < 0:
                    warnings.append(
                        f"text overflows node '{group_id}': {content[:30]!r} "
                        f"(est. {width:.0f}u at {size:g}px; node width {rect_w:g}, "
                        f"overshoot {max(-pad_left, -pad_right):.0f}u)"
                    )
                elif min(pad_left, pad_right) < MIN_TEXT_PADDING:
                    warnings.append(
                        f"text too close to node edge in '{group_id}': {content[:30]!r} "
                        f"(padding {min(pad_left, pad_right):.0f}u < {MIN_TEXT_PADDING:g})"
                    )


def path_endpoints(d: str) -> list[tuple[float, float]]:
    """Return absolute vertex positions of a path (start of each command and its end)."""
    tokens = re.findall(r"[MmLlHhVvCcSsQqTtAaZz]|-?\d*\.?\d+(?:e-?\d+)?", d)
    points: list[tuple[float, float]] = []
    current = (0.0, 0.0)
    start = (0.0, 0.0)
    command = None
    index = 0

    def take(count: int) -> list[float]:
        nonlocal index
        values = [float(token) for token in tokens[index : index + count]]
        index += count
        return values

    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            command = token
            index += 1
            if command in "Zz":
                current = start
                points.append(current)
            continue
        if command is None:
            break
        if command == "M":
            current = tuple(take(2))  # type: ignore[assignment]
            start = current
            command = "L"
        elif command == "m":
            dx, dy = take(2)
            current = (current[0] + dx, current[1] + dy)
            start = current
            command = "l"
        elif command == "L":
            current = tuple(take(2))  # type: ignore[assignment]
        elif command == "l":
            dx, dy = take(2)
            current = (current[0] + dx, current[1] + dy)
        elif command == "H":
            current = (take(1)[0], current[1])
        elif command == "h":
            current = (current[0] + take(1)[0], current[1])
        elif command == "V":
            current = (current[0], take(1)[0])
        elif command == "v":
            current = (current[0], current[1] + take(1)[0])
        elif command == "C":
            values = take(6)
            current = (values[4], values[5])
        elif command == "c":
            values = take(6)
            current = (current[0] + values[4], current[1] + values[5])
        elif command in "SQ":
            values = take(4)
            current = (values[2], values[3])
        elif command in "sq":
            values = take(4)
            current = (current[0] + values[2], current[1] + values[3])
        elif command == "T":
            current = tuple(take(2))  # type: ignore[assignment]
        elif command == "t":
            dx, dy = take(2)
            current = (current[0] + dx, current[1] + dy)
        elif command == "A":
            values = take(7)
            current = (values[5], values[6])
        elif command == "a":
            values = take(7)
            current = (current[0] + values[5], current[1] + values[6])
        else:
            index += 1
            continue
        points.append(current)
    return points


def distance_to_rect_boundary(
    px: float, py: float, rect: tuple[float, float, float, float]
) -> tuple[float, bool]:
    """Distance from a point to the rect outline, plus whether the point is inside."""
    x, y, w, h = rect
    inside = x < px < x + w and y < py < y + h
    if inside:
        return min(px - x, x + w - px, py - y, y + h - py), True
    dx = max(x - px, 0.0, px - (x + w))
    dy = max(y - py, 0.0, py - (y + h))
    return math.hypot(dx, dy), False


def check_connector_endpoints(
    root: ET.Element,
    rects: dict[str, tuple[float, float, float, float]],
    warnings: list[str],
) -> None:
    for element in root.iter():
        name = local_name(element.tag)
        if name not in {"path", "line", "polyline"} or element.get("transform"):
            continue
        source, target = element.get("data-from"), element.get("data-to")
        if not source or not target:
            continue
        ident = element.get("id") or element.get("data-relation") or "unnamed connector"
        if name == "line":
            values = [number(element.get(key)) for key in ("x1", "y1", "x2", "y2")]
            if any(value is None for value in values):
                continue
            points = [(values[0], values[1]), (values[2], values[3])]  # type: ignore[list-item]
        elif name == "polyline":
            raw = re.findall(r"-?\d*\.?\d+", element.get("points") or "")
            if len(raw) < 4:
                continue
            coords = [float(value) for value in raw]
            points = [(coords[0], coords[1]), (coords[-2], coords[-1])]
        else:
            points = path_endpoints(element.get("d") or "")
            if len(points) < 2:
                continue
        for label, point, node_id in (("start", points[0], source), ("end", points[-1], target)):
            rect = rects.get(node_id)
            if rect is None:
                continue  # target is not a plain rect node; needs manual review
            distance, inside = distance_to_rect_boundary(point[0], point[1], rect)
            if inside and distance > CONNECTOR_SNAP_TOLERANCE:
                warnings.append(
                    f"connector '{ident}' {label} ({point[0]:g},{point[1]:g}) is {distance:.0f}u "
                    f"inside node '{node_id}' instead of on its boundary"
                )
            elif not inside and distance > CONNECTOR_SNAP_TOLERANCE:
                warnings.append(
                    f"connector '{ident}' {label} ({point[0]:g},{point[1]:g}) stops {distance:.0f}u "
                    f"short of node '{node_id}' boundary"
                )


def validate_ordered_flow(group: ET.Element, errors: list[str]) -> None:
    """Validate connector-level 1..N ordering and matching visible badges."""
    group_id = group.get("id", "unnamed ordered flow")
    connectors = [
        element
        for element in group.iter()
        if local_name(element.tag) in {"path", "line", "polyline"}
        and element.get("marker-end")
    ]
    if not connectors:
        errors.append(f"ordered flow '{group_id}' contains no directed connectors")
        return

    sequences: dict[int, str] = {}
    for connector in connectors:
        connector_id = connector.get("id", "unnamed connector")
        raw_sequence = connector.get("data-sequence")
        if raw_sequence is None:
            errors.append(
                f"ordered connector '{connector_id}' is missing data-sequence"
            )
            continue
        if not re.fullmatch(r"[1-9]\d*", raw_sequence):
            errors.append(
                f"ordered connector '{connector_id}' has invalid data-sequence: {raw_sequence!r}"
            )
            continue
        sequence = int(raw_sequence)
        if sequence in sequences:
            errors.append(
                f"ordered flow '{group_id}' repeats sequence {sequence} "
                f"on '{sequences[sequence]}' and '{connector_id}'"
            )
        sequences[sequence] = connector_id

    if sequences:
        expected = list(range(1, len(connectors) + 1))
        actual = sorted(sequences)
        if actual != expected:
            errors.append(
                f"ordered flow '{group_id}' must use contiguous 1..{len(connectors)} "
                f"sequences; found {actual}"
            )

    badges: dict[int, list[ET.Element]] = {}
    for element in group.iter():
        raw_label = element.get("data-sequence-label")
        if raw_label is None:
            continue
        if not re.fullmatch(r"[1-9]\d*", raw_label):
            errors.append(
                f"ordered flow '{group_id}' has invalid data-sequence-label: {raw_label!r}"
            )
            continue
        badges.setdefault(int(raw_label), []).append(element)

    for sequence in sequences:
        matches = badges.get(sequence, [])
        if not matches:
            errors.append(
                f"ordered flow '{group_id}' is missing visible badge {sequence}"
            )
        elif len(matches) > 1:
            errors.append(
                f"ordered flow '{group_id}' has multiple visible badges for sequence {sequence}"
            )
        elif text_content(matches[0]) != str(sequence):
            errors.append(
                f"badge {sequence} in ordered flow '{group_id}' must visibly contain '{sequence}'"
            )

    extra_badges = sorted(set(badges) - set(sequences))
    if extra_badges:
        errors.append(
            f"ordered flow '{group_id}' has badges without matching connectors: {extra_badges}"
        )


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

    ordered_groups = [
        element
        for element in root.iter()
        if element.get("data-ordered-flow") == "true"
    ]
    for group in ordered_groups:
        validate_ordered_flow(group, errors)
    if ordered_groups:
        print(f"Ordered flows: {len(ordered_groups)}")

    rects = node_rects(root)
    check_connector_endpoints(root, rects, warnings)
    check_text_overflow(root, rects, warnings)

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

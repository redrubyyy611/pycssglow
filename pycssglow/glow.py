"""Core CSS glow effect generators."""

from __future__ import annotations

import re


def _validate_color(color: str) -> str:
    """Validate and normalise a CSS color string.

    Accepts hex (#rgb / #rrggbb / #rrggbbaa), rgb(), rgba(), hsl(),
    hsla(), and named colours.  Raises ValueError for anything that
    doesn't look like a valid CSS colour token.
    """
    color = color.strip()
    if not color:
        raise ValueError("color must not be empty")

    hex_re = re.compile(r"^#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
    func_re = re.compile(
        r"^(rgba?|hsla?)\s*\(.+\)$",
        re.IGNORECASE,
    )
    named_re = re.compile(r"^[a-zA-Z]+$")

    if hex_re.match(color) or func_re.match(color) or named_re.match(color):
        return color

    raise ValueError(f"Invalid CSS color: {color!r}")


def _validate_number(value: float, name: str) -> float:
    """Ensure *value* is a real number and return it as a float."""
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a number, got {value!r}") from exc
    return result


def box_glow(
    color: str,
    blur: float = 10,
    spread: float = 0,
    x: float = 0,
    y: float = 0,
    inset: bool = False,
) -> str:
    """Return a CSS ``box-shadow`` value that produces a glow effect.

    Parameters
    ----------
    color:
        CSS color of the glow (e.g. ``"#ff0080"``, ``"rgba(0,255,128,0.8)"``).
    blur:
        Blur radius in pixels (default ``10``).
    spread:
        Spread radius in pixels (default ``0``).
    x:
        Horizontal offset in pixels (default ``0``).
    y:
        Vertical offset in pixels (default ``0``).
    inset:
        If ``True``, the shadow is rendered inside the element (default ``False``).

    Returns
    -------
    str
        A ready-to-use ``box-shadow`` CSS value string.

    Examples
    --------
    >>> box_glow("#00ffcc", blur=20, spread=5)
    '0px 0px 20px 5px #00ffcc'
    >>> box_glow("#ff0080", inset=True)
    'inset 0px 0px 10px 0px #ff0080'
    """
    color = _validate_color(color)
    blur = _validate_number(blur, "blur")
    spread = _validate_number(spread, "spread")
    x = _validate_number(x, "x")
    y = _validate_number(y, "y")

    prefix = "inset " if inset else ""
    return f"{prefix}{x:g}px {y:g}px {blur:g}px {spread:g}px {color}"


def text_glow(
    color: str,
    blur: float = 10,
    x: float = 0,
    y: float = 0,
) -> str:
    """Return a CSS ``text-shadow`` value that produces a glow effect.

    Parameters
    ----------
    color:
        CSS color of the glow.
    blur:
        Blur radius in pixels (default ``10``).
    x:
        Horizontal offset in pixels (default ``0``).
    y:
        Vertical offset in pixels (default ``0``).

    Returns
    -------
    str
        A ready-to-use ``text-shadow`` CSS value string.

    Examples
    --------
    >>> text_glow("#ffffff", blur=15)
    '0px 0px 15px #ffffff'
    """
    color = _validate_color(color)
    blur = _validate_number(blur, "blur")
    x = _validate_number(x, "x")
    y = _validate_number(y, "y")

    return f"{x:g}px {y:g}px {blur:g}px {color}"


# ---------------------------------------------------------------------------
# Preset neon colours
# ---------------------------------------------------------------------------

_NEON_PRESETS: dict[str, str] = {
    "blue": "#00f3ff",
    "green": "#39ff14",
    "pink": "#ff6ec7",
    "purple": "#bf5fff",
    "red": "#fe0000",
    "yellow": "#fff01f",
    "white": "#ffffff",
    "orange": "#ff6600",
    "cyan": "#00ffff",
}


def neon_glow(
    color: str,
    intensity: str = "medium",
    kind: str = "box",
) -> str:
    """Return a vivid neon glow CSS shadow value using preset parameters.

    Parameters
    ----------
    color:
        Either a named preset (``"blue"``, ``"green"``, ``"pink"``,
        ``"purple"``, ``"red"``, ``"yellow"``, ``"white"``, ``"orange"``,
        ``"cyan"``) or any valid CSS color string.
    intensity:
        One of ``"low"``, ``"medium"`` (default), or ``"high"``.
    kind:
        ``"box"`` (default) for ``box-shadow``, or ``"text"`` for
        ``text-shadow``.

    Returns
    -------
    str
        A layered CSS shadow value string that creates a vibrant neon glow.

    Examples
    --------
    >>> neon_glow("green")
    '0px 0px 5px #39ff14, 0px 0px 10px #39ff14, 0px 0px 20px #39ff14'
    """
    resolved = _NEON_PRESETS.get(color.lower(), color)
    resolved = _validate_color(resolved)

    intensities: dict[str, list[float]] = {
        "low": [4, 8],
        "medium": [5, 10, 20],
        "high": [5, 10, 20, 40, 80],
    }
    blurs = intensities.get(intensity)
    if blurs is None:
        raise ValueError(
            f"intensity must be one of {list(intensities)!r}, got {intensity!r}"
        )

    if kind == "text":
        layers = [text_glow(resolved, blur=b) for b in blurs]
    elif kind == "box":
        layers = [box_glow(resolved, blur=b) for b in blurs]
    else:
        raise ValueError(f"kind must be 'box' or 'text', got {kind!r}")

    return ", ".join(layers)


def multi_glow(shadows: list[dict]) -> str:
    """Combine multiple glow layers into a single CSS shadow value.

    Each element in *shadows* is a dict of keyword arguments forwarded
    to either :func:`box_glow` or :func:`text_glow` depending on the
    ``"kind"`` key (``"box"`` by default).

    Parameters
    ----------
    shadows:
        List of shadow specification dicts.  Each dict must contain at
        least a ``"color"`` key.  An optional ``"kind"`` key (``"box"``
        or ``"text"``) determines which generator is used.

    Returns
    -------
    str
        A comma-separated CSS shadow value string.

    Examples
    --------
    >>> multi_glow([
    ...     {"color": "#ff0080", "blur": 10},
    ...     {"color": "#00ffff", "blur": 20, "spread": 5},
    ... ])
    '0px 0px 10px 0px #ff0080, 0px 0px 20px 5px #00ffff'
    """
    if not shadows:
        raise ValueError("shadows list must not be empty")

    parts: list[str] = []
    for shadow in shadows:
        shadow = dict(shadow)
        kind = shadow.pop("kind", "box")
        if kind == "text":
            parts.append(text_glow(**shadow))
        elif kind == "box":
            parts.append(box_glow(**shadow))
        else:
            raise ValueError(f"kind must be 'box' or 'text', got {kind!r}")

    return ", ".join(parts)

# pycssglow

A Python library for generating CSS glow effects — `box-shadow` and
`text-shadow` values you can drop straight into your stylesheets or
inject with a CSS-in-Python workflow.

[![PyPI version](https://img.shields.io/pypi/v/pycssglow)](https://pypi.org/project/pycssglow/)
[![Python versions](https://img.shields.io/pypi/pyversions/pycssglow)](https://pypi.org/project/pycssglow/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Installation

```bash
pip install pycssglow
```

## Quick Start

```python
from pycssglow import box_glow, text_glow, neon_glow, multi_glow

# Simple box-shadow glow
print(box_glow("#ff0080", blur=20, spread=5))
# → '0px 0px 20px 5px #ff0080'

# Text-shadow glow
print(text_glow("#ffffff", blur=15))
# → '0px 0px 15px #ffffff'

# Vivid neon preset (layered shadows)
print(neon_glow("green"))
# → '0px 0px 5px #39ff14, 0px 0px 10px #39ff14, 0px 0px 20px #39ff14'

# Combine multiple layers manually
print(multi_glow([
    {"color": "#ff0080", "blur": 10},
    {"color": "#00ffff", "blur": 20, "spread": 5},
]))
# → '0px 0px 10px 0px #ff0080, 0px 0px 20px 5px #00ffff'
```

## API

### `box_glow(color, blur=10, spread=0, x=0, y=0, inset=False)`

Returns a CSS `box-shadow` value.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `color` | `str` | — | CSS color (hex, rgb(), named, …) |
| `blur` | `float` | `10` | Blur radius in px |
| `spread` | `float` | `0` | Spread radius in px |
| `x` | `float` | `0` | Horizontal offset in px |
| `y` | `float` | `0` | Vertical offset in px |
| `inset` | `bool` | `False` | Inner shadow |

### `text_glow(color, blur=10, x=0, y=0)`

Returns a CSS `text-shadow` value.

### `neon_glow(color, intensity="medium", kind="box")`

Returns a layered neon glow value.

- **color** – a named preset (`"blue"`, `"green"`, `"pink"`, `"purple"`,
  `"red"`, `"yellow"`, `"white"`, `"orange"`, `"cyan"`) or any CSS color.
- **intensity** – `"low"` (2 layers), `"medium"` (3 layers, default),
  `"high"` (5 layers).
- **kind** – `"box"` (default) or `"text"`.

### `multi_glow(shadows)`

Combines a list of shadow specification dicts into one CSS value.
Each dict is forwarded to `box_glow` or `text_glow` depending on the
optional `"kind"` key (`"box"` by default).

## CSS Usage Example

```css
.card {
  box-shadow: 0px 0px 20px 5px #ff0080;
}

.heading {
  text-shadow: 0px 0px 15px #ffffff;
}

.neon-button {
  box-shadow: 0px 0px 5px #39ff14, 0px 0px 10px #39ff14, 0px 0px 20px #39ff14;
}
```

## Development

```bash
# Install dependencies (requires Poetry)
poetry install

# Run tests
poetry run pytest
```

## License

[MIT](LICENSE) © Ruby
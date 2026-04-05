"""Tests for pycssglow."""

import pytest

from pycssglow import box_glow, multi_glow, neon_glow, text_glow
from pycssglow.glow import _validate_color


# ---------------------------------------------------------------------------
# _validate_color
# ---------------------------------------------------------------------------


class TestValidateColor:
    def test_hex_shorthand(self):
        assert _validate_color("#f00") == "#f00"

    def test_hex_full(self):
        assert _validate_color("#ff0080") == "#ff0080"

    def test_hex_with_alpha(self):
        assert _validate_color("#ff008080") == "#ff008080"

    def test_rgb_function(self):
        assert _validate_color("rgb(0, 255, 128)") == "rgb(0, 255, 128)"

    def test_rgba_function(self):
        assert _validate_color("rgba(0, 255, 128, 0.5)") == "rgba(0, 255, 128, 0.5)"

    def test_hsl_function(self):
        assert _validate_color("hsl(120, 100%, 50%)") == "hsl(120, 100%, 50%)"

    def test_named_color(self):
        assert _validate_color("red") == "red"
        assert _validate_color("transparent") == "transparent"

    def test_strips_whitespace(self):
        assert _validate_color("  #ff0080  ") == "#ff0080"

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            _validate_color("")

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="Invalid CSS color"):
            _validate_color("not a color!!!")


# ---------------------------------------------------------------------------
# box_glow
# ---------------------------------------------------------------------------


class TestBoxGlow:
    def test_defaults(self):
        result = box_glow("#ff0080")
        assert result == "0px 0px 10px 0px #ff0080"

    def test_custom_blur_and_spread(self):
        result = box_glow("#00ffcc", blur=20, spread=5)
        assert result == "0px 0px 20px 5px #00ffcc"

    def test_offsets(self):
        result = box_glow("#fff", x=3, y=-3)
        assert result == "3px -3px 10px 0px #fff"

    def test_inset(self):
        result = box_glow("#ff0080", inset=True)
        assert result.startswith("inset ")

    def test_invalid_color_raises(self):
        with pytest.raises(ValueError):
            box_glow("not-valid!!!")

    def test_invalid_blur_raises(self):
        with pytest.raises(ValueError, match="blur"):
            box_glow("#fff", blur="bad")


# ---------------------------------------------------------------------------
# text_glow
# ---------------------------------------------------------------------------


class TestTextGlow:
    def test_defaults(self):
        result = text_glow("#ffffff")
        assert result == "0px 0px 10px #ffffff"

    def test_custom_blur(self):
        result = text_glow("#ffffff", blur=15)
        assert result == "0px 0px 15px #ffffff"

    def test_with_offsets(self):
        result = text_glow("#fff", x=1, y=2)
        assert result == "1px 2px 10px #fff"

    def test_invalid_color_raises(self):
        with pytest.raises(ValueError):
            text_glow("bad!!!")


# ---------------------------------------------------------------------------
# neon_glow
# ---------------------------------------------------------------------------


class TestNeonGlow:
    def test_named_preset_green(self):
        result = neon_glow("green")
        assert "#39ff14" in result

    def test_named_preset_blue(self):
        result = neon_glow("blue")
        assert "#00f3ff" in result

    def test_custom_color(self):
        result = neon_glow("#abcdef")
        assert "#abcdef" in result

    def test_intensity_low_has_two_layers(self):
        result = neon_glow("pink", intensity="low")
        assert result.count(",") == 1  # 2 layers → 1 comma

    def test_intensity_medium_has_three_layers(self):
        result = neon_glow("pink", intensity="medium")
        assert result.count(",") == 2

    def test_intensity_high_has_five_layers(self):
        result = neon_glow("pink", intensity="high")
        assert result.count(",") == 4

    def test_kind_text(self):
        result = neon_glow("red", kind="text")
        # text-shadow values don't have a spread component
        parts = [p.strip() for p in result.split(",")]
        for part in parts:
            tokens = part.split()
            assert len(tokens) == 4  # x y blur color

    def test_invalid_intensity_raises(self):
        with pytest.raises(ValueError, match="intensity"):
            neon_glow("blue", intensity="ultra")

    def test_invalid_kind_raises(self):
        with pytest.raises(ValueError, match="kind"):
            neon_glow("blue", kind="border")


# ---------------------------------------------------------------------------
# multi_glow
# ---------------------------------------------------------------------------


class TestMultiGlow:
    def test_single_box_layer(self):
        result = multi_glow([{"color": "#ff0080", "blur": 10}])
        assert result == "0px 0px 10px 0px #ff0080"

    def test_two_box_layers(self):
        result = multi_glow(
            [
                {"color": "#ff0080", "blur": 10},
                {"color": "#00ffff", "blur": 20, "spread": 5},
            ]
        )
        assert result == "0px 0px 10px 0px #ff0080, 0px 0px 20px 5px #00ffff"

    def test_text_kind(self):
        result = multi_glow([{"color": "#fff", "blur": 8, "kind": "text"}])
        assert result == "0px 0px 8px #fff"

    def test_mixed_kinds(self):
        result = multi_glow(
            [
                {"color": "#fff", "blur": 5, "kind": "text"},
                {"color": "#fff", "blur": 10, "kind": "text"},
            ]
        )
        assert "," in result

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            multi_glow([])

    def test_invalid_kind_raises(self):
        with pytest.raises(ValueError, match="kind"):
            multi_glow([{"color": "#fff", "kind": "border"}])

    def test_does_not_mutate_input(self):
        shadows = [{"color": "#fff", "blur": 5, "kind": "box"}]
        original = dict(shadows[0])
        multi_glow(shadows)
        assert shadows[0] == original

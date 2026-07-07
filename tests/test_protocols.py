"""Tests for Samsung IR protocol encoder."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("infrared_protocols")

_PROTOCOLS_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "samsung_infrared"
    / "protocols.py"
)
_SPEC = importlib.util.spec_from_file_location(
    "samsung_infrared_protocols", _PROTOCOLS_PATH,
)
assert _SPEC is not None
assert _SPEC.loader is not None
protocols = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(protocols)


def test_samsung_command_timings() -> None:
    """Test Samsung command encoder timing shape."""
    command = protocols.SamsungCommand(data=0xE0E040BF, repeat_count=0)

    assert command.modulation == protocols.SAMSUNG_MODULATION
    timings = command.get_raw_timings()
    assert timings[:2] == [4500, -4500]
    assert len(timings) == 68
    assert timings[-2:] == [560, -560]


def test_repeats_add_inter_frame_space() -> None:
    """Test repeated frames contain the configured inter-frame space."""
    timings = protocols.SamsungCommand(
        data=0xE0E040BF, repeat_count=1,
    ).get_raw_timings()

    assert len(timings) == 137
    assert timings[66] == 560
    assert timings[67] == -560
    assert timings[68] == -10000
    assert timings[69:71] == [4500, -4500]

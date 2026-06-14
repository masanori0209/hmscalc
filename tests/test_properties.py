"""Property-based tests for hmscalc (Python 3.10+)."""

from __future__ import annotations

import sys

import pytest

if sys.version_info < (3, 10):
    pytest.skip("hypothesis requires Python 3.10+", allow_module_level=True)

from hypothesis import given, settings
from hypothesis import strategies as st

from hmscalc import HMSTime


@st.composite
def valid_hms_strings(draw: st.DrawFn) -> str:
    """Generate valid HMS duration strings."""
    hh = draw(st.integers(min_value=0, max_value=48))
    mm = draw(st.integers(min_value=0, max_value=59))
    ss = draw(st.integers(min_value=0, max_value=59))
    negative = draw(st.booleans())
    sign = "-" if negative else ""
    with_seconds = draw(st.booleans())
    if with_seconds:
        return f"{sign}{hh}:{mm:02}:{ss:02}"
    return f"{sign}{hh}:{mm:02}"


@given(valid_hms_strings())
@settings(max_examples=200)
def test_parse_str_roundtrip(time_str: str) -> None:
    """Parsing str(HMSTime(s)) reproduces the same value."""
    original = HMSTime(time_str.strip())
    assert HMSTime(str(original)) == original


@given(valid_hms_strings(), valid_hms_strings())
@settings(max_examples=100)
def test_add_sub_inverse(a: str, b: str) -> None:
    """(a + b) - b equals a at second precision."""
    left = HMSTime(a.strip())
    right = HMSTime(b.strip())
    assert (left + right) - right == left


@given(st.lists(valid_hms_strings(), min_size=1, max_size=8))
@settings(max_examples=50)
def test_sum_equals_fold(time_strings: list[str]) -> None:
    """HMSTime.sum matches left-fold addition."""
    times = [HMSTime(s.strip()) for s in time_strings]
    folded = times[0]
    for other in times[1:]:
        folded = folded + other
    assert HMSTime.sum(times) == folded

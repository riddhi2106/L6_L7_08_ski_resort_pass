from hypothesis import given, strategies as st
from processor import (
    parse_season_pass_validity,
    compute_trail_gradient,
    calculate_lift_access_tier
)


# Test 1: Date validation
@given(st.one_of(st.text(), st.none()))
def test_parse_season_pass_validity_no_crash(s):
    try:
        result = parse_season_pass_validity(s)
        assert isinstance(result, str)

    except ValueError:
        pass


# Test 2: Trail gradient calculation
@given(st.one_of(st.text(), st.none()))
def test_compute_trail_gradient_safe(s):
    try:
        result = compute_trail_gradient(s)
        assert isinstance(result, (int, float))

    except ValueError:
        pass


# Test 3: Lift access tier
@given(st.one_of(st.text(), st.none()))
def test_calculate_lift_access_tier_safe(s):
    try:
        result = calculate_lift_access_tier(s)
        assert result in [35.0, 60.0, 85.0, 110.0]

    except ValueError:
        pass


import pytest
from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


# ==========================================
# 1. INPUT VALIDATION
# ==========================================

def test_invalid_groups():
    with pytest.raises(ValueError):
        process_resort_bookings("invalid", 15.0)


def test_negative_facility_fee():
    with pytest.raises(ValueError):
        process_resort_bookings([], -10.0)


# ==========================================
# 2. GROUP AND PASS DURATION TESTS
# ==========================================

def test_inactive_group():
    groups = [{"is_active": False, "skiers": [{"age": 30}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result["status"] == "ZERO_SALES"


def test_season_pass():
    groups = [{
        "is_active": True,
        "duration": "season",
        "skiers": [{"age": 30}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 300.0


def test_half_day_pass():
    groups = [{
        "is_active": True,
        "duration": "half_day",
        "skiers": [{"age": 30}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 50.0


def test_default_full_day_duration():
    groups = [{
        "is_active": True,
        "skiers": [{"age": 30}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 80.0


def test_invalid_pass_duration():
    groups = [{
        "is_active": True,
        "duration": "weekly",
        "skiers": [{"age": 30}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_SALES"


# ==========================================
# 3. SKIER AGE AND DISCOUNT TESTS
# ==========================================

def test_invalid_skier_age():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 0}, {"age": -5}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["status"] == "ZERO_SALES"


def test_child_discount():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 10}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 48.0


def test_senior_discount():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 70}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 56.0


def test_regular_adult():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 30}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 80.0


# ==========================================
# 4. GEAR RENTAL AND LOCKER TESTS
# ==========================================

def test_gear_rental():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 30, "gear_rental": True}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 115.0


def test_lodge_locker_fee():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "includes_lodge_locker": True,
        "skiers": [{"age": 30}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 95.0


def test_empty_skiers_with_locker():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "includes_lodge_locker": True,
        "skiers": []
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 15.0


# ==========================================
# 5. BLACKOUT OVERRIDE TESTS
# ==========================================

def test_blackout_override_full_day():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 30, "blackout_override": True}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 40.0


def test_blackout_override_season():
    groups = [{
        "is_active": True,
        "duration": "season",
        "skiers": [{"age": 30, "blackout_override": True}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 150.0


def test_blackout_override_half_day():
    groups = [{
        "is_active": True,
        "duration": "half_day",
        "skiers": [
            {"age": 30, "blackout_override": True},
            {"age": 30}
        ]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_SALES"


def test_blackout_override_with_gear_rental():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [{"age": 30, "blackout_override": True,
                    "gear_rental": True}]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 75.0


# ==========================================
# 6. AUDIT AND ZERO SALES TESTS
# ==========================================

def test_audit_review():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [
            {"age": 0},
            {"age": 0},
            {"age": 0},
            {"age": 0},
            {"age": 0}
        ]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["status"] == "AUDIT_REVIEW"


def test_exactly_four_rejections():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [
            {"age": 0},
            {"age": 0},
            {"age": 0},
            {"age": 0}
        ]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["status"] == "ZERO_SALES"


def test_empty_groups():
    result = process_resort_bookings([], 15.0)
    assert result["status"] == "ZERO_SALES"


def test_multiple_skiers():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [
            {"age": 10},
            {"age": 30},
            {"age": 70}
        ]
    }]
    result = process_resort_bookings(groups, 15.0)
    assert result["total_revenue"] == 184.0


# ==========================================
# 7. CHAIRLIFT ANEMOMETER TESTS
# ==========================================

def test_no_wind_data():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_safe_wind_conditions():
    assert check_chairlift_anemometer([[20, 30, 40]]) == "SAFE_OPERATION"


def test_single_high_wind_gust():
    assert check_chairlift_anemometer([[50, 30, 50]]) == "SAFE_OPERATION"


def test_two_consecutive_high_gusts():
    assert check_chairlift_anemometer([[50, 55]]) == "SUSPEND_LIFT"


def test_gust_streak_resets():
    assert check_chairlift_anemometer(
        [[50, 30, 50, 55]]
    ) == "SUSPEND_LIFT"


def test_gusts_in_separate_lifts():
    assert check_chairlift_anemometer(
        [[50], [55]]
    ) == "SAFE_OPERATION"


def test_wind_exactly_45():
    assert check_chairlift_anemometer(
        [[45, 45, 45]]
    ) == "SAFE_OPERATION"


def test_empty_readings_inside_stream():
    assert check_chairlift_anemometer(
        [[], [20, 30]]
    ) == "SAFE_OPERATION"

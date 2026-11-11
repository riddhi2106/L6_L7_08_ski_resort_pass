
import math
import re
from datetime import datetime


def parse_season_pass_validity(date_str):
    if not isinstance(date_str, str):
        raise ValueError("Date must be a string")

    if not re.fullmatch(r"\d{4}/\d{2}/\d{2}", date_str):
        raise ValueError("Date must follow YYYY/MM/DD format")

    try:
        date = datetime.strptime(date_str, "%Y/%m/%d")
    except ValueError:
        raise ValueError("Invalid calendar date")

    year = date.year
    month = date.month
    day = date.day

    valid = year >= 2026

    return (
        f"Pass Expiry: {year:04d}-{month:02d}-{day:02d} "
        f"({'VALID' if valid else 'EXPIRED'})"
    )


def compute_trail_gradient(elevation_str):
    if not isinstance(elevation_str, str):
        raise ValueError("Input must be a string")

    try:
        parts = elevation_str.split(":")

        if len(parts) != 2:
            raise ValueError("Expected drop:distance")

        drop = float(parts[0])
        distance = float(parts[1])

        if not math.isfinite(drop) or not math.isfinite(distance):
            raise ValueError("Values must be finite")

        if drop < 0:
            raise ValueError("Drop cannot be negative")

        if distance <= 0:
            raise ValueError("Distance must be positive")

        gradient_pct = (drop / distance) * 100.0

        return round(gradient_pct, 2)

    except (TypeError, OverflowError) as e:
        raise ValueError("Invalid gradient input") from e


def calculate_lift_access_tier(zone_code):
    if not isinstance(zone_code, str):
        raise ValueError("Zone code must be a string")

    prefix = zone_code.strip().upper()[:3]

    zone_rates = {
        "BEG": 35.0,
        "INT": 60.0,
        "ADV": 85.0,
        "ALL": 110.0
    }

    if prefix not in zone_rates:
        raise ValueError("Invalid lift access zone")

    return zone_rates[prefix]


def main():
    print("==== Running parse_season_pass_validity ====")
    d_input = input("Enter pass expiry (YYYY/MM/DD): ")
    try:
        print(parse_season_pass_validity(d_input))
    except ValueError as e:
        print("Error:", e)

    print("\n==== Running compute_trail_gradient ====")
    e_input = input("Enter drop:distance (e.g. 250:1000): ")
    try:
        print("Gradient %:", compute_trail_gradient(e_input))
    except ValueError as e:
        print("Error:", e)

    print("\n==== Running calculate_lift_access_tier ====")
    z_input = input("Enter zone code (e.g. BEG, INT, ALL): ")
    try:
        print("Lift Pass Price: $", calculate_lift_access_tier(z_input))
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()

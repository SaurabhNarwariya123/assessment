"""Section 1 - Clean and normalize sensor readings"""


def clean_sensor_data(data):
    cleaned_data = []

    for value in data:
        try:
            if value is None:
                continue

            number = float(value)

            if number < 0:
                continue

            if number > 500:
                number = 500.0

            cleaned_data.append(number)

        except (ValueError, TypeError):
            continue

    return cleaned_data


# ---- Test cases ----
if __name__ == "__main__":
    # Test 1: mixed input
    data = [100, "200", None, -50, "abc", 600, 300.5]
    print("Test 1:", clean_sensor_data(data))
    assert clean_sensor_data(data) == [100.0, 200.0, 500.0, 300.5]

    # Test 2: empty list
    print("Test 2:", clean_sensor_data([]))
    assert clean_sensor_data([]) == []

    # Test 3: everything invalid
    print("Test 3:", clean_sensor_data([None, "xyz", -1, -999]))
    assert clean_sensor_data([None, "xyz", -1, -999]) == []

    print("All tests passed")

import math

MAX_READING = 500.0


def clean_sensor_data(data):
    if data is None:
        return []

    try:
        values = iter(data)
    except TypeError:
        return []

    cleaned = []
    for value in values:
        if value is None:
            continue
        try:
            number = float(value)
        except (ValueError, TypeError):
            continue

        if math.isnan(number) or number < 0:
            continue

        cleaned.append(min(number, MAX_READING))

    return cleaned

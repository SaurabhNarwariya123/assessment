import argparse
import csv
import json
import sys
from collections import defaultdict

from sensor_cleaning import clean_sensor_data

REQUIRED_COLUMNS = {"device_id", "status", "temperature"}
MAX_AVG_TEMPERATURE = 80.0


class TelemetryError(Exception):
    pass


def read_telemetry(csv_path):
    try:
        with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            columns = {name.strip() for name in (reader.fieldnames or [])}
            missing = REQUIRED_COLUMNS - columns
            if missing:
                raise TelemetryError(
                    f"CSV is missing required column(s): {', '.join(sorted(missing))}"
                )

            rows, skipped = [], 0
            for raw_row in reader:
                row = {
                    (key or "").strip(): (value or "").strip()
                    for key, value in raw_row.items()
                    if isinstance(value, str) or value is None
                }
                if not row.get("device_id"):
                    skipped += 1
                    continue
                rows.append(row)
    except FileNotFoundError:
        raise TelemetryError(f"File not found: {csv_path}") from None
    except PermissionError:
        raise TelemetryError(f"Permission denied: {csv_path}") from None
    except (UnicodeDecodeError, csv.Error) as error:
        raise TelemetryError(f"Could not parse {csv_path}: {error}") from None

    if not rows:
        raise TelemetryError("No usable records found in the CSV file.")
    return rows, skipped


def aggregate_by_device(rows):
    temperatures = defaultdict(list)
    totals = defaultdict(int)
    errors = defaultdict(int)

    for row in rows:
        device = row["device_id"]
        totals[device] += 1
        if row.get("status", "").upper() == "ERROR":
            errors[device] += 1
        temperatures[device].extend(clean_sensor_data([row.get("temperature")]))

    summary = []
    for device in sorted(totals):
        readings = temperatures[device]
        average = round(sum(readings) / len(readings), 2) if readings else None
        summary.append(
            {
                "device_id": device,
                "total_records": totals[device],
                "average_temperature": average,
                "error_count": errors[device],
            }
        )
    return summary


def filter_hot_devices(summary, limit=MAX_AVG_TEMPERATURE):
    return [
        device
        for device in summary
        if device["average_temperature"] is not None
        and device["average_temperature"] <= limit
    ]


def save_json(summary, json_path):
    try:
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(summary, json_file, indent=2)
            json_file.write("\n")
    except OSError as error:
        raise TelemetryError(f"Could not write {json_path}: {error}") from None


def print_table(summary):
    headers = ["Device", "Records", "Avg Temp (C)", "Errors"]
    rows = [
        [d["device_id"], d["total_records"], f"{d['average_temperature']:.2f}", d["error_count"]]
        for d in summary
    ]
    widths = [max(len(str(item)) for item in column) for column in zip(headers, *rows)]

    def line(cells):
        return " | ".join(str(cell).ljust(width) for cell, width in zip(cells, widths))

    print(line(headers))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(line(row))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Summarize device telemetry from a CSV file.")
    parser.add_argument("csv_path", nargs="?", default="device_telemetry.csv")
    parser.add_argument("-o", "--output", default="summary.json", help="JSON output path")
    parser.add_argument("--chart", metavar="PNG", help="also save a bar chart to this path")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        rows, skipped = read_telemetry(args.csv_path)
        summary = aggregate_by_device(rows)
        kept = filter_hot_devices(summary)
        removed = len(summary) - len(kept)

        if skipped:
            print(f"Note: skipped {skipped} row(s) with no device_id.")
        if removed:
            print(
                f"Note: excluded {removed} device(s) with average temperature "
                f"above {MAX_AVG_TEMPERATURE} (or no valid readings)."
            )
        if not kept:
            raise TelemetryError("No devices left after filtering; nothing to export.")

        save_json(kept, args.output)
        print_table(kept)
        print(f"\nSaved {len(kept)} device(s) to {args.output}")

        if args.chart:
            from plot_chart import create_chart

            create_chart(args.output, args.chart)
            print(f"Saved chart to {args.chart}")
    except TelemetryError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

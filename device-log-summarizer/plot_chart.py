import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_summary(json_path):
    try:
        with open(json_path, encoding="utf-8") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        raise SystemExit(f"Error: JSON file not found: {json_path}")
    except json.JSONDecodeError as error:
        raise SystemExit(f"Error: {json_path} is not valid JSON: {error}")
    if not data:
        raise SystemExit(f"Error: {json_path} contains no devices to plot.")
    return data


def create_chart(json_path, chart_path):
    summary = load_summary(json_path)
    devices = [item["device_id"] for item in summary]
    averages = [item["average_temperature"] for item in summary]

    fig, ax = plt.subplots(figsize=(max(6, len(devices) * 1.1), 5))
    bars = ax.bar(devices, averages, color="#3b7dd8")
    ax.bar_label(bars, fmt="%.1f", padding=3)

    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device")
    ax.set_ylabel("Average temperature (°C)")
    ax.set_ylim(0, max(averages) * 1.15)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    fig.tight_layout()
    fig.savefig(chart_path, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    json_file = sys.argv[1] if len(sys.argv) > 1 else "summary.json"
    png_file = sys.argv[2] if len(sys.argv) > 2 else "temperature_chart.png"
    create_chart(json_file, png_file)
    print(f"Saved chart to {png_file}")

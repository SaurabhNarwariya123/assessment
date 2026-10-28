# Device Log Summarizer

Reads `device_telemetry.csv`, aggregates per device, drops devices with average temperature > 80.0,
saves `summary.json`, prints a table and (optionally) draws a bar chart.

## Setup
```
pip install matplotlib
```

## Run
```
python device_summarizer.py                      # uses device_telemetry.csv -> summary.json
python device_summarizer.py data.csv -o out.json --chart chart.png
python plot_chart.py summary.json chart.png      # chart only, from existing JSON
python -m unittest discover -s tests             # tests
```

## Files
| File | Purpose |
|---|---|
| `first_section.py` | Section 1 standalone answer: `clean_sensor_data` + 3 test cases (`python first_section.py`) |
| `sensor_cleaning.py` | Hardened copy of the same function (NaN / non-iterable) used by the CLI |
| `device_summarizer.py` | CSV reading, aggregation, filtering, JSON export, table, CLI |
| `plot_chart.py` | matplotlib bar chart from the JSON |
| `tests/` | unit tests |
| `PROMPT_LOG.md` | how AI was used |

## Behaviour notes
- Temperatures go through `clean_sensor_data`: invalid / negative values are ignored in the average, values > 500 count as 500.
- Rows with no `device_id` are skipped (a note is printed).
- Missing file, wrong columns, empty file -> clear error message, exit code 1.

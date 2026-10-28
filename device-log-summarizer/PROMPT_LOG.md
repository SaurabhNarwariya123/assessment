# PROMPT_LOG

## Section 1 - Data cleaning
Written myself without AI (`first_section.py`). No prompt used.

## Section 2 - CSV, aggregation, JSON
Prompt:

> I am building a Device Log Summarizer CLI in Python. I want a simple, readable and reliable solution.
> Read `device_telemetry.csv` (`device_id`, `status`, `temperature`), group by device and calculate the total
> records, the average temperature and the number of ERROR records. Remove devices whose average temperature is
> above 80.0, save the rest to a JSON file and print a table in the terminal. Handle a missing file, bad CSV data
> and empty data without crashing. Keep the code modular with clear names and add simple tests. Explain your decisions.

## Section 3 - Chart
Initial prompt:

> Write a Python script that loads my JSON file (a list of objects with `device_id` and `average_temperature`)
> and creates a matplotlib bar chart comparing the average temperature of each device. Add a chart title, axis
> labels and make sure the device labels are readable. Save the chart as a PNG.

Bug in the first version:

> With long device names (e.g. `WAREHOUSE_SENSOR_01`) the x-axis labels overlapped and were unreadable. There was
> also no title, no axis labels and no values on the bars.

Follow-up prompt:

> The x-axis labels overlap when the device names are long. Rotate them 45 degrees and right-align them, make the
> figure wider based on the number of devices, and use `tight_layout()` so nothing is cut off. Also add a title,
> x and y axis labels, and show the average value above each bar.

# Output Layout

Use a deterministic output tree so the skill and downstream scripts can find artifacts reliably.

## Default Layout

```text
<output-dir>/
  <drug_name>/
    <timestamp>/
      <species>/
        <concentration>/
          detections/
            detections.json
          summaries/
            summary.json
            per_video_counts.csv
            time_series_counts.csv
          plots/
            time_curve.png
          visualizations/
            *.jpg
            *.png
          logs/
            pipeline.log
  global/
    all_results.csv
    grouped_summary.csv
```

## Layout Rules

- Keep generated artifacts separate from raw inputs.
- Mirror the input metadata hierarchy in the output tree.
- Put machine-readable summaries in `summaries/`.
- Put model overlay outputs in `visualizations/`.
- Put charts and analysis figures in `plots/`.
- Put script logs and failure details in `logs/`.

## Naming Rules

- Prefer stable lowercase names with underscores.
- Include timestamps only when repeated runs must coexist.
- If using timestamps, keep a run-level timestamp at the root rather than embedding it in every file name.

# Input / Output Contract

## Supported Inputs

The pipeline should accept:

- a root experiment directory
- a drug-specific subdirectory
- a timestamp-specific subdirectory
- a species-specific subdirectory
- a concentration-specific subdirectory containing videos

## Expected Input Layout

```text
<root>/
  <drug_name>/
    <timestamp>/
      <species>/
        <concentration>/
          *.mp4
          *.avi
          *.mov
```

The directory names are treated as metadata:

- `drug_name`
- `timestamp`
- `species`
- `concentration`

## Candidate Supported Video Types

- `.mp4`
- `.avi`
- `.mov`
- `.mkv`

Adjust this list once the SR-TOD backend constraints are confirmed.

## Required Script Contract

### `run_srtod_infer.py`

Input arguments should include:

- `--input-path`
- `--output-dir`
- `--frame-stride` or equivalent sampling control
- `--model-config` or equivalent backend selector
- optional runtime flags for device / thresholds

Expected outputs:

- `detections.json`
- `per_video_counts.csv`
- optional visualization outputs
- optional failure log

### `aggregate_results.py`

Inputs:

- `detections.json`

Outputs:

- `summary.json`
- `class_counts.csv`
- optional `per_video_counts.csv`
- optional `time_series_counts.csv`

### `run_analysis.py`

Inputs:

- `summary.json`
- `class_counts.csv`
- `time_series_counts.csv`

Outputs:

- plots under a plots directory
- optional analysis report files

## Suggested `detections.json` Shape

```json
{
  "input_path": "path/to/input",
  "videos": [
    {
      "drug_name": "drug_a",
      "timestamp": "2026-04-04T10-00",
      "species": "species_x",
      "concentration": "0.1",
      "file": "video001.mp4",
      "status": "ok",
      "frames": [
        {
          "frame_index": 10,
          "time_sec": 5.0,
          "count": 12
        }
      ]
    }
  ],
  "failures": []
}
```

## Suggested `summary.json` Shape

```json
{
  "total_videos": 20,
  "processed_videos": 19,
  "failed_videos": 1,
  "counts_by_species": {
    "species_x": 320
  },
  "counts_by_concentration": {
    "0.1": 120,
    "1.0": 200
  }
}
```

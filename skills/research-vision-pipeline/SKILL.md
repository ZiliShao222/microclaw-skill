---
name: research-vision-pipeline
description: Analyze experiment video directories via SR-TOD vision pipeline. Scans folders organized by drug, timestamp, species, and concentration, counts targets from extracted frames, and generates structured outputs with optional downstream analysis.
metadata:
  requires:
    bins:
      - ffmpeg
      - python3
    env:
      - SRTOD_MODEL_PATH
---

# Research Vision Pipeline

Structured research video-analysis workflow. Input is an experiment directory with nested metadata folders and videos; output is organized count results, summaries, and optional plots.

- Directory metadata (`drug_name`, `timestamp`, `species`, `concentration`) is treated as trusted input.
- This skill orchestrates deterministic local scripts; it is not for open-ended visual Q&A.

## Workflow

1. Validate the provided input path.
2. Expect a nested directory structure:
   - `<root>/<drug_name>/<timestamp>/<species>/<concentration>/*.mp4`
   - or the same layout with other supported video extensions
3. Parse `drug_name`, `timestamp`, `species`, and `concentration` from the path.
4. Collect supported video files.
5. Create the expected output directory structure.
6. Run the SR-TOD inference bridge script, which should extract frames and count targets.
7. Aggregate per-video and per-timepoint results into summary outputs.
8. If requested or configured, run downstream plotting or data-analysis scripts.
9. Return a concise summary with counts, output locations, and any failures.

## Script Boundaries

Use the local scripts in `scripts/` rather than re-implementing logic inline:

- `run_srtod_infer.py`
  Purpose: call the local SR-TOD vision backend on extracted video frames and emit structured per-video results.

- `aggregate_results.py`
  Purpose: merge per-video results into count tables and time-series summaries.

- `run_analysis.py`
  Purpose: generate time curves or downstream analysis artifacts from aggregated outputs.

## Expected Behavior

- Prefer deterministic scripts over ad-hoc one-off code.
- Keep all outputs inside a user-specified or default result directory.
- Record skipped files and failures explicitly.
- Return structured result locations, not only prose.
- Treat the species directory name as trusted input metadata.

## Required References

Read these before implementing or changing behavior:

- `references/input-output-contract.md`
- `references/output-layout.md`

## Error Handling

- If `SRTOD_MODEL_PATH` is not set or the model directory is empty, stop and inform the user.
- If `ffmpeg` is not installed, stop and suggest installing it.
- If a video cannot be decoded, record it in `failures[]` and continue with remaining videos.
- If the input directory does not match the expected `<root>/<drug>/<timestamp>/<species>/<concentration>/` layout, stop and explain the expected structure.

## Guardrails

- Do not guess labels if the local vision backend fails.
- Do not mix raw inputs and generated outputs in the same directory when avoidable.
- Do not silently drop unreadable files; report them.
- Do not invent analysis metrics that are not produced by scripts or configured logic.
- Do not override user-provided species metadata unless the user explicitly asks for validation.

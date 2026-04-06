# Research Vision Pipeline

This folder contains a first-pass design for a domain-specific OpenClaw skill
that orchestrates a research video-analysis workflow.

## Goal

Build a lightweight, domain-focused pipeline that:

1. Accepts a researcher-provided file or directory
2. Scans supported files and organizes inputs
3. Uses the directory structure as authoritative metadata for drug, timestamp, species, and concentration
4. Sends extracted video frames to a local SR-TOD-based vision pipeline
5. Extracts counts and per-video structured results
5. Writes organized outputs into a deterministic results directory
6. Calls fixed downstream analysis scripts for plotting or statistical analysis
7. Returns a concise summary plus result locations

## Architectural Direction

This design follows the spirit of DrugClaw:

- Narrow domain scope
- Explicit workflow steps
- Stable script boundaries
- Structured outputs

But it stays compatible with OpenClaw skill conventions:

- `SKILL.md` for trigger logic and orchestration guidance
- `references/` for contracts and conventions
- `scripts/` for deterministic execution

## Proposed Runtime Split

OpenClaw skill responsibilities:

- Detect when the workflow should trigger
- Validate the input path and output path
- Parse metadata from the directory structure
- Decide which script to run next
- Read structured results and summarize them

Local scripts responsibilities:

- File scanning and video discovery
- Frame extraction and SR-TOD inference bridge
- Result aggregation
- Plotting / data analysis

## Initial Workflow

1. Validate user input path
2. Expect an experiment directory structure like:
   - root / drug_name / timestamp / species / concentration / videos
3. Discover supported video files
4. Parse path metadata:
   - drug_name
   - timestamp
   - species
   - concentration
5. Create deterministic output directory structure
6. Run the SR-TOD bridge script for frame-based counting
7. Aggregate per-video and per-timepoint counts
8. Run downstream analysis / plotting script if requested or configured
9. Return:
   - total files processed
   - count summaries
   - output paths
   - failures / skipped files

## Initial Directory Structure

```text
research-vision-pipeline/
  SKILL_DESIGN.md
  skills/
    research-vision-pipeline/
      SKILL.md
      references/
        input-output-contract.md
        output-layout.md
      scripts/
        run_srtod_infer.py
        aggregate_results.py
        run_analysis.py
```

## First Decisions Locked In

- Use one main skill first, not a multi-agent graph
- Use scripts for deterministic heavy lifting
- Treat SR-TOD as a local model backend, not as skill logic
- Produce structured JSON artifacts before any final summary

## Next Steps

1. Confirm supported video extensions
2. Confirm frame extraction cadence and counting policy
3. Confirm SR-TOD invocation command or Python entrypoint
4. Confirm analysis outputs:
   - plots
   - CSV summaries
   - JSON summaries
5. Implement the three placeholder scripts

# LivEzee Assignment

Simple batch script to process call transcripts and generate:

- structured JSON output
- manager-friendly CSV output
- a short terminal summary

## Setup

1. Create and activate a virtual environment.

   macOS/Linux:

   - `python3 -m venv .venv`
   - `source .venv/bin/activate`

2. Install dependencies.

   - `pip install -r requirements.txt`

3. Create a `.env` file in the project root.

   - `GEMINI_API_KEY=your_api_key_here`

## How to run

- `python3 main.py`

Example output:

```text
Initializing Batch Process..
Processed: Thankamma Nair
Processed: Govindan Pillai

SUCCESS: 2 calls summarized in ./output/care_summary.csv
JSON output written to ./output/care_summary.json

Summary
- Calls processed: 2
- Calls with concerns flagged: 2
- Calls needing follow-up: 2
```

## Input format

Put transcript `.txt` files in [transcripts/](transcripts/).

Expected style:

- header lines like `Date:` and `Client:`
- free-text call notes
- optional `Follow-up:` section

## Output files

Generated in [output/](output/):

- [output/care_summary.json](output/care_summary.json): one structured JSON entry per transcript
- [output/care_summary.csv](output/care_summary.csv): flattened CSV view

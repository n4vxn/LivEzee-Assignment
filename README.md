# LivEzee Assignment

A Python script to process call transcripts and extract structured insights.

The script reads transcript files and generates:
- structured JSON output (one entry per transcript)
- manager-friendly CSV output for easy review
- a concise terminal summary of processed calls

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
Processed: Raman Kutty Menon
Processed: Saradha Krishnan
Processed: Thankamma Nair
Processed: Govindan Pillai
Processed: Mariamma Varghese

SUCCESS: 5 calls summarized in ./output/care_summary.csv
JSON output written to ./output/care_summary.json

Summary
- Calls processed: 5
- Calls with concerns flagged: 5
- Calls needing follow-up: 5
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

## Prompt used

```text
You are an elderly care assistant analyzing a call transcript.

Extract structured health and emotional insights.

Return ONLY a valid JSON object.
Do NOT include any text before or after the JSON.
Do NOT use markdown or code blocks.

STRICT JSON FORMAT:
{
  "physical_concerns": [],
  "mood_signal": "positive|neutral|concerned",
  "follow_up_actions": [],
  "priority": "low|medium|high"
}

Rules:

1. physical_concerns:
   - Include only clear health-related issues
   - Examples: pain, missed medication, high BP, mobility issues
   - Do NOT include vague statements

2. mood_signal:
   - positive → cheerful, stable
   - neutral → normal, no distress
   - concerned → sadness, anxiety, confusion, discomfort

3. priority:
   - high → urgent risk (severe symptoms, missed critical meds, confusion, fall risk)
   - medium → needs follow-up (mild pain, elevated BP, medication gaps)
   - low → stable, no issues

4. follow_up_actions:
   - Include actions mentioned OR clearly needed
   - Keep them short and practical

5. If no data is found for a field, return empty list [] (not null).

Transcript:
{text}
```

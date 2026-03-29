import re
import json

def extract_metadata(text):
    name_match = re.search(r"(?i)Client\s*:\s*(.*)", text)
    date_match = re.search(r"(?i)Date\s*:\s*(.*)", text)

    return {
        "client_name": name_match.group(1).strip() if name_match else "Unknown",
        "call_date": date_match.group(1).strip() if date_match else "Unknown"
    }

def get_llm_analysis(model, text):
    prompt = f"""
You are an elderly care assistant analyzing a call transcript.

Extract structured health and emotional insights.

Return ONLY a valid JSON object.
Do NOT include any text before or after the JSON.
Do NOT use markdown or code blocks.

STRICT JSON FORMAT:
{{
  "physical_concerns": [],
  "mood_signal": "positive|neutral|concerned",
  "follow_up_actions": [],
  "priority": "low|medium|high"
}}

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
"""
    response = model.models.generate_content(prompt)

    raw_json = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(raw_json)
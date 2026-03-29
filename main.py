import os
import json
import pandas as pd
from config import setup_client
from parser import extract_metadata, get_llm_analysis

def run_batch_process():
    model = setup_client()
    folder_path = "./transcripts"
    output_path = "./output/care_summary.csv"
    json_output_path = "./output/care_summary.json"
    json_results = []

    if not os.path.exists("./output"):
        os.makedirs("./output")

    print("Initializing Batch Process..")

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r') as f:
                content = f.read()
                
                # 1. Regex Metadata
                meta = extract_metadata(content)
                
                # 2. LLM Deep Dive
                try:
                    analysis = get_llm_analysis(model, content)

                    physical_concerns = analysis.get("physical_concerns", [])
                    follow_up_actions = analysis.get("follow_up_actions", [])

                    # Structured JSON entry (one per transcript)
                    json_results.append({
                        "transcript_file": filename,
                        "client": meta["client_name"],
                        "date": meta["call_date"],
                        "mood": analysis.get("mood_signal"),
                        "priority": analysis.get("priority"),
                        "physical_concerns": physical_concerns,
                        "follow_up_actions": follow_up_actions
                    })

                    print(f"Processed: {meta['client_name']}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    # 3. Write JSON output first
    with open(json_output_path, "w") as json_file:
        json.dump(json_results, json_file, indent=2)

    # 4. Convert JSON -> CSV
    with open(json_output_path, "r") as json_file:
        saved_json = json.load(json_file)

    csv_rows = []
    for entry in saved_json:
        csv_rows.append({
            "Client": entry.get("client", "Unknown"),
            "Date": entry.get("date", "Unknown"),
            "Mood": entry.get("mood", "unknown"),
            "Priority": entry.get("priority", "unknown"),
            "Concerns": ", ".join(entry.get("physical_concerns", [])),
            "Actions": " | ".join(entry.get("follow_up_actions", [])),
        })

    df = pd.DataFrame(csv_rows)
    df.to_csv(output_path, index=False)

    concerns_flagged = sum(1 for entry in saved_json if entry.get("physical_concerns"))
    needs_follow_up = sum(1 for entry in saved_json if entry.get("follow_up_actions"))

    print(f"\nSUCCESS: {len(saved_json)} calls summarized in {output_path}")
    print(f"JSON output written to {json_output_path}")

    # 5. Terminal summary
    print("\nSummary")
    print(f"- Calls processed: {len(saved_json)}")
    print(f"- Calls with concerns flagged: {concerns_flagged}")
    print(f"- Calls needing follow-up: {needs_follow_up}")

if __name__ == "__main__":
    run_batch_process()
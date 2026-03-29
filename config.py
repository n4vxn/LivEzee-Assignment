import os
from google import genai
from dotenv import load_dotenv

def setup_client():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Error: GEMINI_API_KEY not found in .env file.")

    return genai.Client(api_key=api_key)
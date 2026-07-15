import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Please check your .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = 'gemini-3.1-flash-lite' 

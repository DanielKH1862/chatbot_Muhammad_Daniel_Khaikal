import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv

# Muat environment variables dari file .env
load_dotenv()

# Konfigurasi API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY tidak ditemukan di environment variables")

genai.configure(api_key=api_key)  

# Pilih model
model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_text(prompt: str):
    response = model.generate_content(prompt)
    return response.text

def generate_text_http(prompt: str, model_name: str = "gemini-2.0-flash"):
    """Generate text using direct HTTP API call"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]
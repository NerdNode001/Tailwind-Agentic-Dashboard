import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_groq():
    key = os.getenv("GROQ_API_KEY")
    if not key or "xxxx" in key.lower():
        print("❌ GROQ_API_KEY is missing or still set to the placeholder in .env")
        return False
        
    print("Testing Groq API...")
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {key}"}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            print("✅ Groq API Key is VALID!")
            return True
        else:
            print(f"❌ Groq API Key rejected. Status: {res.status_code}. Message: {res.text}")
            return False
    except Exception as e:
        print(f"❌ Groq API connection failed: {e}")
        return False

if __name__ == "__main__":
    print("=== API Key Verification ===\n")
    groq_ok = test_groq()
    print("-" * 30)
    
    if groq_ok:
        print("\n🚀 GROQ KEY IS VALID! You are using DuckDuckGo for search (no API key needed).")
        print("\nBefore launching, ensure you installed the new search package:")
        print("Run: .venv\\Scripts\\pip install -r requirements.txt")
        print("\nThen to launch: .venv\\Scripts\\uvicorn main:app --reload")
    else:
        print("\n⚠️ Please fix your Groq API key in the .env file.")

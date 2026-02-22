
import google.generativeai as genai
import json
import os
import sys

def load_key():
    # 1. Try file
    try:
        with open('custom_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Try both keys just in case
            k = data.get("GEMINI_API_KEY") or data.get("api_key")
            if k and len(k) > 10: return k
    except: pass
    
    # 2. Prompt User
    print("\n⚠️ Không tìm thấy file 'custom_data.json'.")
    print("👉 Hãy dán API Key của bạn vào đây và nhấn Enter:")
    k = input(">>> ").strip()
    return k

def test_connection():
    try:
        import google.generativeai as genai
        print(f"📦 SDK Version: {genai.__version__}")
    except ImportError:
        print("❌ ERROR: google-generativeai not installed.")
        return

    api_key = load_key()
    if not api_key:
        print("❌ ERROR: Could not find API Key in custom_data.json")
        return

    print(f"🔑 Found API Key: {api_key[:10]}.......")
    
    # Configure
    genai.configure(api_key=api_key)

    # TEST 1: Basic Model Listing
    print("\n--- TEST 1: Listing Available Models (genai.list_models) ---")
    try:
        found_count = 0
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" ✅ {m.name}")
                found_count += 1
        
        if found_count == 0:
            print("⚠️ WARNING: API Call successful but NO models returned (Empty List). Key may be restricted?")
        else:
            print(f"🎉 Found {found_count} working models.")
            
    except Exception as e:
        print(f"❌ ERROR Listing Models: {e}")

    # TEST 2: Basic Generation (gemini-1.5-flash)
    print("\n--- TEST 2: Testing 'gemini-1.5-flash' ---")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Ping. Reply 'Pong' if you hear me.")
        print(f"✅ SUCCESS: {response.text}")
    except Exception as e:
        print(f"❌ FAIL: {e}")

if __name__ == "__main__":
    test_connection()

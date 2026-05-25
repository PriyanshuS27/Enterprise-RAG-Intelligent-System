#!/usr/bin/env python3
"""
Test which Groq models are available with the given API key
"""

import os
from groq import Groq

# Set API key
api_key = os.getenv('GROQ_API_KEY', 'your_groq_api_key_here')
client = Groq(api_key=api_key)

# List of models to test
models_to_test = [
    "mixtral-8x7b-32768",
    "llama-3.1-70b-versatile",
    "llama-3.3-70b-specdec",
    "gemma-7b-it",
    "llama2-70b-4096",
    "llama3-70b-8191",
    "llama-3-70b-8191",
    "llama-3.1-8b-instant",
    "whisper-large-v3-turbo",
]

print("=" * 70)
print("Testing Groq API Key: Available Models")
print("=" * 70)
print()

for model in models_to_test:
    try:
        print(f"Testing: {model}... ", end="", flush=True)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Hi"}
            ],
            max_tokens=10,
            temperature=0.1,
        )
        print("✅ WORKS!")
    except Exception as e:
        error_msg = str(e)
        if "decommissioned" in error_msg:
            print("❌ DECOMMISSIONED")
        elif "not found" in error_msg or "does not exist" in error_msg:
            print("❌ NOT FOUND")
        elif "not available" in error_msg:
            print("❌ NOT AVAILABLE")
        else:
            print(f"❌ ERROR: {error_msg[:50]}")

print()
print("=" * 70)

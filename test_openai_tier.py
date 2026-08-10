#!/usr/bin/env python3
"""
Quick script to test OpenAI API tier and rate limits
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("🔍 Testing OpenAI API connection and tier...")
print(f"API Key (first 20 chars): {os.getenv('OPENAI_API_KEY')[:20]}...")

try:
    # Make a simple API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say 'API connection successful!'"}
        ],
        max_tokens=10
    )
    
    print("\n✅ API call successful!")
    print(f"Response: {response.choices[0].message.content}")
    print(f"\nℹ️ If this worked without rate limit errors, your tier has been upgraded!")
    print(f"ℹ️ Check https://platform.openai.com/settings/organization/limits for details")
    
except Exception as e:
    print(f"\n❌ API call failed: {str(e)}")
    if "429" in str(e):
        print("\n⚠️ Still hitting rate limits. Tier upgrade may not have propagated yet.")
        print("⏱️ Wait 5-10 more minutes and try again.")
    else:
        print("\n⚠️ Different error - check your API key and account status.")

print("\n" + "="*60)


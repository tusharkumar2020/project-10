import os
import requests
import json
from requests.auth import HTTPBasicAuth

# Get the Watson API key and URL from environment variables
WATSON_API_KEY = os.getenv("WATSON_API_KEY")
WATSON_URL = os.getenv("WATSON_URL")

if not WATSON_API_KEY or not WATSON_URL:
    raise ValueError("WATSON_URL and WATSON_API_KEY environment variables must be set")

def analyze_text(text_to_analyze):
    url = f'{WATSON_URL}/v1/analyze?version=2019-07-12'
    myobj = {
        "text": text_to_analyze,
        "features": {
            "sentiment": {},
            "emotion": {},
            "keywords": {},
            "entities": {},
            "syntax": {"tokens": {"lemma": True, "part_of_speech": True}},
            "concepts": {}
        }
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=myobj, headers=headers, auth=HTTPBasicAuth('apikey', WATSON_API_KEY))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
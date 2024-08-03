import os
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import base64

# Get the Watson API key and URL from environment variables
WATSON_API_KEY = os.getenv("WATSON_API_KEY")
WATSON_URL = os.getenv("WATSON_URL")

if not WATSON_API_KEY or not WATSON_URL:
    raise ValueError("WATSON_URL and WATSON_API_KEY environment variables must be set")

# Encode the API key for Basic Authentication
auth = base64.b64encode(f"apikey:{WATSON_API_KEY}".encode()).decode()

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
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth}"
    }

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.post(url, json=myobj, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
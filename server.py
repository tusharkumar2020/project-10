from flask import Flask, render_template, request
import requests
import json
import os
from requests.auth import HTTPBasicAuth

# Initialize the Flask app
app = Flask(__name__)

# Function for sentiment analysis using Watson NLP
def sentiment_analyzer(text_to_analyze):
    # Get the Watson API key and URL from environment variables
    api_key = os.getenv('WATSON_API_KEY')
    url = os.getenv('WATSON_URL') + '/v1/analyze?version=2019-07-12'

    # Create the payload with the text to be analyzed
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
    # Set the headers with the required API key
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        # Make a POST request to the API with the payload and headers
        response = requests.post(url, json=myobj, headers=headers, auth=HTTPBasicAuth('apikey', api_key))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        # Parse the response from the API
        formatted_response = json.loads(response.text)

        # Extract the sentiment label and score from the response
        sentiment_label = formatted_response['sentiment']['document']['label']
        sentiment_score = formatted_response['sentiment']['document']['score']

        # Extract the emotions from the response
        emotions = formatted_response['emotion']['document']['emotion']

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sentiment_label = None
        sentiment_score = None
        emotions = {}

    # Return the sentiment and emotion data in a dictionary
    return {
        'sentiment_label': sentiment_label,
        'sentiment_score': sentiment_score,
        'emotions': emotions
    }

@app.route("/sentimentAnalyzer")
def sent_analyzer():
    ''' This code receives the text from the HTML interface and 
        runs sentiment analysis over it using sentiment_analyzer()
        function. The output returned shows the label and its confidence 
        score for the provided text.
    '''
    text_to_analyze = request.args.get('textToAnalyze')
    # Call sentiment_analyzer with the input text
    response = sentiment_analyzer(text_to_analyze)
    sentiment_label = response['sentiment_label']
    sentiment_score = response['sentiment_score']
    emotions = response['emotions']
    # Check if the label is None, indicating an error or invalid input
    if sentiment_label is None:
        return "Invalid input! Try again."
    else:
        # Render the result template with sentiment and emotion data
        return render_template('result.html', sentiment_label=sentiment_label, sentiment_score=sentiment_score, emotions=emotions)

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    ''' This functions executes the flask app and deploys it on localhost:5000
    '''
    app.run(debug=True)
''' This module provides the function for sentiment analysis
'''
import json
import requests


def sentiment_analyzer(text_to_analyze):
    ''' This function requests a sentiment analysis
        from IBM Watson's trained model
    '''
    url = (
        'https://sn-watson-sentiment-bert.labs.skills.network'
        '/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'
    )
    header = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}
    mytext = { "raw_document": { "text": text_to_analyze } }
    response = requests.post(url, headers = header, json = mytext, timeout = 5)
    formatted_response = json.loads(response.text)
    if response.status_code == 200:
        label = formatted_response['documentSentiment']['label']
        score = formatted_response['documentSentiment']['score']
    else:
        label = None
        score = None
    return {"label": label, "score": score}

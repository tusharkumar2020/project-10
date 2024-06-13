'''
Executing this function initiates the application of sentiment
analysis to be executed over the Flask channel and deployed on
localhost:5000.
'''
from flask import Flask, render_template, request
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

app = Flask("Sentiment Analyzer")

@app.route("/sentimentAnalyzer")
def sent_analyzer():
    """Endpoint to analyze sentiment of the provided text."""
    text_to_analyze = request.args.get('textToAnalyze')

    if not text_to_analyze:
        return "Invalid input! Please provide text to analyze."
    
    try:
        response = sentiment_analyzer(text_to_analyze)
        label = response.get('label')
        score = response.get('score')

        if not label or score is None:
            return "Invalid input or analysis failed. Try again."

        return f"The given text has been identified as {label.split('_')[1]} with a score of {score}."
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route("/")
def render_index_page():
    """Renders the index page."""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

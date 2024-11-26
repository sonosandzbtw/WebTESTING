from flask import Flask, render_template_string, request
import openai

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# If the key is not set, print a helpful error message
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set!")
# Initialize Flask app
app = Flask(__name__)

# Inline HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Created by Sandy! AI Gap Analysis Testing Version #1</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; }
        .container { max-width: 600px; margin: auto; padding: 20px; }
        h1, h3 { text-align: center; }
        textarea, input, button { width: 100%; padding: 10px; margin-bottom: 10px; }
        .results { margin-top: 20px; background-color: #e8f5e9; padding: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Created by Sandy!</h1>
        <h3>AI Gap Analysis Testing Version #1</h3>
        <form method="post">
            <label for="topic">What do you want to learn today?</label>
            <input type="text" id="topic" name="topic" required>

            <label for="concepts">Set the concepts you want to master:</label>
            <input type="text" id="concepts" name="concepts" required>

            <label for="explanation">Explain the concepts in your own words:</label>
            <textarea id="explanation" name="explanation" rows="4" required></textarea>

            <button type="submit">Analyze</button>
        </form>
        {% if results %}
        <div class="results">
            <h3>Gap Analysis Results:</h3>
            <p>{{ results }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    if request.method == "POST":
        # Retrieve user inputs
        topic = request.form.get("topic")
        concepts = request.form.get("concepts")
        explanation = request.form.get("explanation")

        # Construct the OpenAI API prompt
        prompt = f"Topic: {topic}\nConcepts: {concepts}\nExplanation: {explanation}\nAnalyze this explanation and highlight missing or unclear points."

        try:
            # Use the OpenAI ChatCompletion API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for cost-effective testing
                messages=[
                    {"role": "system", "content": "You are an AI assistant that helps users identify gaps in learning material."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200  # Limit the output to control costs
            )
            results = response['choices'][0]['message']['content'].strip()
        except Exception as e:
            results = f"Error with OpenAI API: {e}"

    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == "__main__":
    app.run(debug=True)
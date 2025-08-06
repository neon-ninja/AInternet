#!/usr/bin/env python3
from google import genai
from google.genai import types
import os
from flask import Flask, request
from pathvalidate import sanitize_filename
import dotenv
dotenv.load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

app = Flask(__name__)

os.makedirs("html", exist_ok=True)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    path = request.full_path.strip("?")
    filename = f"html/" + sanitize_filename(path) + ".html"
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            return f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"""You are a web server. A request has just come in on the path {path}.
            Respond with HTML/CSS/JS that is appropriate for that path.
            Only return the HTML/CSS/JS, nothing else.
            Do not include any comments or explanations.
            Try to make the web page as beautiful and functional as possible.
            Don't mention that this is a simulation, make it as realistic as possible.
        """,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        )
    ).text.strip("```html\n").strip("```")

    with open(filename, "w") as f:
        f.write(response)
    return response

if __name__ == '__main__':
    app.run(debug=True)

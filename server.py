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

def generate(path):
    filename = f"html/" + sanitize_filename(path) + ".html"
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            yield f.read()
            return

    html = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash-lite",
        contents=f"""You are a web server. A request has just come in on the path {path}.
            Respond with HTML/CSS/JS that is appropriate for that path.
            Only return the HTML/CSS/JS, nothing else.
            Do not include any comments or explanations.
            Try to make the web page as beautiful and functional as possible.
            Don't mention that this is a simulation, make it as realistic as possible.
            You can add relative links if appropriate, but if the user follows a relative link, you'll have to handle that too, so be sure to pass enough context for yourself to understand what you're doing in the URL.
        """,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        )
    ):
        if not chunk.text:
            continue
        chunk = chunk.text.removeprefix("```html\n").removesuffix("```")
        yield chunk
        html += chunk

    with open(filename, "w") as f:
        f.write(html)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    path = request.full_path.strip("?")
    return generate(path), {"Content-Type": "text/html"}

if __name__ == '__main__':
    app.run(debug=True)

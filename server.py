#!/usr/bin/env python3
from openai import OpenAI
import os
from flask import Flask, request
from pathvalidate import sanitize_filename
import dotenv
dotenv.load_dotenv()

# The client gets the API key from the environment variable `CEREBRAS_API_KEY`.
client = OpenAI(
    api_key=os.getenv("CEREBRAS_API_KEY"),
    base_url="https://api.cerebras.ai/v1",
)

app = Flask(__name__)

os.makedirs("html", exist_ok=True)

def generate(path):
    filename = f"html/" + sanitize_filename(path) + ".html"
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            yield f.read()
            return

    html = ""
    stream = client.chat.completions.create(
        model="llama3.1-8b",
        messages=[
            {
                "role": "user",
                "content": f"""You are a web server. A request has just come in on the path {path}.
            Respond with HTML/CSS/JS that is appropriate for that path.
            Only return the HTML/CSS/JS, nothing else.
            Do not include any comments or explanations.
            Try to make the web page as beautiful and functional as possible.
            Don't mention that this is a simulation, make it as realistic as possible.
            You can add relative links if appropriate, but if the user follows a relative link, you'll have to handle that too, so be sure to pass enough context for yourself to understand what you're doing in the URL.
        """
            }
        ],
        stream=True,
        max_tokens=4096,
        temperature=0.7
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            # Remove any markdown code block markers
            content = content.removeprefix("```html\n").removesuffix("```")
            yield content
            html += content

    with open(filename, "w") as f:
        f.write(html)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    path = request.full_path.strip("?")
    return generate(path), {"Content-Type": "text/html"}

if __name__ == '__main__':
    app.run(debug=True)

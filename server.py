#!/usr/bin/env python3
import os
from cerebras.cloud.sdk import Cerebras
import os
from flask import Flask, request
import dotenv
dotenv.load_dotenv()

client = Cerebras(
  api_key=os.environ.get("CEREBRAS_API_KEY"),
)

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    path = request.full_path.strip("?")
    result = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"""You are a web server. A request has just come in on the path {path}.
                Respond with HTML/CSS/JS that is appropriate for that path.
                Only return the HTML/CSS/JS, nothing else.
                Do not include any comments or explanations.
                Try to make the web page as beautiful and functional as possible.
                Don't mention that this is a simulation, make it as realistic as possible.
                You can add relative links if appropriate, but if the user follows a relative link, you'll have to handle that too, so be sure to pass enough context for yourself to understand what you're doing in the URL.
            """
        }],
        model="gpt-oss-120b",
    ).choices[0].message.content
    return result, {"Content-Type": "text/html"}

if __name__ == '__main__':
    app.run(debug=True)

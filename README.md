# AInternet - AI-Powered Web Server

This application creates a dynamic web server that generates HTML content for any requested path using the Cerebras AI API.

## Setup

### Prerequisites
- Python 3.7+
- Cerebras API account and API key

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Cerebras API key:
   ```bash
   export CEREBRAS_API_KEY=your_api_key_here
   ```
   
   Or create a `.env` file in the project root:
   ```
   CEREBRAS_API_KEY=your_api_key_here
   ```

### Usage

Run the server:
```bash
python server.py
```

The server will start on `http://localhost:5000` in debug mode.

Visit any path (e.g., `http://localhost:5000/about`, `http://localhost:5000/products/laptop`) and the AI will generate appropriate HTML content for that path.

## Features

- **Dynamic Content Generation**: AI generates HTML/CSS/JS based on the requested URL path
- **Caching**: Generated content is cached in the `html/` directory for faster subsequent requests
- **Streaming**: Content is streamed to the browser as it's generated
- **Beautiful Output**: AI is instructed to create attractive and functional web pages

## API Details

This application uses the Cerebras API with the `llama3.1-8b` model for content generation. The API is OpenAI-compatible and provides fast inference speeds.

## Migration from Gemini

This version has been updated to use Cerebras API instead of Google Gemini. Key changes:
- Environment variable changed from `GEMINI_API_KEY` to `CEREBRAS_API_KEY`
- Model changed from `gemini-2.5-flash-lite` to `llama3.1-8b`
- API client changed from Google GenAI to OpenAI-compatible client
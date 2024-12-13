# filepath: /c:/Users/storm/OneDrive/Desktop/Cryptic_AI/app.py
from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging
from waitress import serve # type: ignore

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400

        # Generate response using OpenAI's GPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": user_input}],
            max_tokens=150,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=['\n', 'User:', 'AI:']
        )

        ai_response = response.choices[0].message['content'].strip()
        return jsonify({'response': ai_response})
    except Exception as e:
        logging.exception("An error occurred while processing the request.")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
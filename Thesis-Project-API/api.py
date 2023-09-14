from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import time
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

# OpenAI API Endpoint and Key
# You might need to adjust this
# Replace with your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")
YOUR_SECRET_AUTH_KEY = os.getenv("YOUR_SECRET_AUTH_KEY")

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    
    if not data or "text" not in data or "auth_key" not in data:
        return jsonify({"error": "Invalid input"}), 400

    # You might want to handle authentication in a more secure manner
    if data["auth_key"] != YOUR_SECRET_AUTH_KEY:
        return jsonify({"error": "Invalid auth key"}), 401

    prompt = data["text"]
    response = generate_chat_completion(prompt)

    if response:
        return jsonify({"response": response})
    else:
        return jsonify({"error": "Failed to get response from API"}), 500

def generate_chat_completion(prompt):
    openai.api_key = OPENAI_API_KEY
    response_1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AIML Generator who takes in company description and generates AIML for the company's customer support chatbot. Add some greetings, partings, and start and end AIML tags."},
            {"role": "user", "content": prompt}
        ]
    )
    time.sleep(60)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AIML fixer. Fix the issues in the AIML if there are any and check the tags. Return AIML."},
            {"role": "user", "content": response_1.choices[0].message.content}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True,port=5000)

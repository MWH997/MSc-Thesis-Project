from flask import Flask, request, jsonify
import aiml
import openai
import os
from xml.etree import ElementTree
from flask_cors import CORS
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
import re
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

# Function to generate chat completion using OpenAI
def generate_chat_completion(chatbot_context, prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this value securely 

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a university admission assistant chatbot."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return set(synonyms)

def check_synonym_match(message):
    words = message.split()
    for word in words:
        synonyms = get_synonyms(word.lower())  # Convert word to lowercase
        for synonym in synonyms:
            response = kernel.respond(synonym)
            if response:
                return response
    return None

# Load AIML kernel
kernel = aiml.Kernel()
kernel.resetBrain()  # Resetting the kernel
kernel.learn("./university.xml")

@app.route('/')
def home():
    return jsonify({'response': "Welcome to the University Chatbot API"})

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'Message not provided'}), 400

    response = kernel.respond(message.upper())  # Convert message to uppercase for AIML
    
    # If AIML doesn't provide a satisfactory response, check for synonyms
    if not response:
        response = check_synonym_match(message.upper())  # Convert message to lowercase for synonym check

    if not response:
        response = search_aiml_file_for_response(message)

    # If still no response, fallback to OpenAI
    if not response:
        print("Using external API")
        with open("university.txt", "r") as file:
            description = file.read()
        
        response = generate_chat_completion(description, f"Context: {description}\nQuestion: {message}")
    
    response = response.replace('Â','')

    return jsonify({'response': response})

def search_aiml_file_for_response(message):
    with open("university.xml", "r") as f:
        content = f.read()
        max_score = -1
        best_template = None

        pattern = re.search(r'<pattern>(.*?)</pattern>\s*<template>(.*?)</template>', content, re.DOTALL | re.I)
        while pattern:
            aiml_pattern = pattern.group(1)
            aiml_template = pattern.group(2)

            # Sanitize the AIML pattern by escaping special regex characters
            sanitized_pattern = re.escape(aiml_pattern)

            try:
                for match in re.finditer(sanitized_pattern, message, re.DOTALL | re.I):
                    matched_string = match.group()
                    score = len(matched_string) / len(message)

                    # Update best score and best template if this score is higher
                    if score > max_score:
                        max_score = score
                        best_template = aiml_template.strip()
            except re.error:
                # Handle potential regex errors gracefully
                pass

            # Continue searching the rest of the file
            content = content[pattern.end():]
            pattern = re.search(r'<pattern>(.*?)</pattern>\s*<template>(.*?)</template>', content, re.DOTALL)

        return best_template


if __name__ == "__main__":
    app.run(debug=True, port=5002)

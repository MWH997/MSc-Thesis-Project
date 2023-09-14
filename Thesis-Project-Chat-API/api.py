from flask import Flask, request, jsonify
from flask_cors import CORS
import aiml
import os
import re

app = Flask(__name__)
CORS(app)

kernel = aiml.Kernel()

@app.route('/upload_aiml', methods=['POST'])
def upload_aiml():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    
    # If user does not select file, browser also
    # submits an empty part without filename
    if file.filename == 'aiml':
        return jsonify({'error': 'No selected file'}), 400

    if file:  # and allowed_file(file.filename):
        filepath = os.path.join("./", file.filename)
        file.save(filepath)
        kernel.resetBrain()  # Resetting the kernel
        kernel.learn(filepath)
        return jsonify({'message': 'AIML file uploaded and learned successfully'}), 200

@app.route('/ask', methods=['POST'])
def ask():
    message = request.json['message']
    response = kernel.respond(message)

    # If kernel doesn't have a satisfactory response, search the AIML file manually
    if not response:
        response = search_aiml_file_for_response(message)
        if not response:
            response = "I'm sorry, I don't understand that."

    return jsonify({"response": response})


def search_aiml_file_for_response(message):
    with open("aiml.xml", "r") as f:
        content = f.read()
        max_score = -1
        best_template = None

        pattern = re.search(r'<pattern>(.*?)</pattern>\s*<template>(.*?)</template>', content, re.DOTALL | re.I)
        while pattern:
            aiml_pattern = pattern.group(1)
            aiml_template = pattern.group(2)

            for match in re.finditer(aiml_pattern, message, re.DOTALL | re.I):
                matched_string = match.group()
                score = len(matched_string) / len(message)

                # Update best score and best template if this score is higher
                if score > max_score:
                    max_score = score
                    best_template = aiml_template.strip()

            # Continue searching the rest of the file
            content = content[pattern.end():]
            pattern = re.search(r'<pattern>(.*?)</pattern>\s*<template>(.*?)</template>', content, re.DOTALL)

        return best_template


if __name__ == '__main__':
    app.run(port=5001)

import os
import random
import json
from flask import Flask, jsonify, redirect, render_template, request, url_for, stream_with_context, json, Response
from flask_cors import CORS
from gpt import *


# Define the path to your JSON data folder
json_data_folder = 'json_data'
currentGameFile = {}

responseTemplate = {
    "response": "null"
}

app = Flask(__name__)
CORS(app)


@app.route('/')
def serve_random_json():
    return {'status': 'server up'}

# Define a route to receive JSON data, a message, modify the JSON data, and return it
@app.route('/get_response_grade', methods=['POST'])
def modify_json():
    print("request:", request.json)
    
    try:
        # Get the JSON data, message, and synopsis from the request
        request_data = request.json
        message = request_data.get('response', '')

        print("calling response function", message)
        
        # Pass the message, characterProfile, and game_synopsis to the function
        response = gradeResponse(message, responseTemplate)
        
        print("response:", response)
        response = jsonify(response)
        response.headers.add('Content-Type', 'application/json')
        return response
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/get_attributes', methods=['POST'])
def get_attributes():
    print("request:", request.json)
    
    try:
        # Get the JSON data, message, and synopsis from the request
        request_data = request.json
        message = request_data.get('message', '')
        quizData = request_data.get('quizData', '')
        
        print("calling response function", message)
        
        response = createAttributes(message, responseTemplate, VIDEO_TRANSCRIPT, quizData)
        
        # response = jsonify(response)
        print("response:", response)
        response = jsonify(response)
        response.headers.add('Content-Type', 'application/json')
        return response
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # app.run(host='192.168.50.109',debug=True)
    # app.run(host='172.26.112.93',debug=True)
    # app.run(debug=True)
    
    app.run(debug=True)
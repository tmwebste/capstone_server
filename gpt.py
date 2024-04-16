import os
import json
import random


import openai
import os
from dotenv import dotenv_values, load_dotenv
from data import *
from flask import jsonify

# Load the .env file
config = dotenv_values('.env')
load_dotenv()

# Access the specific key
# KEY = config.get('KEY')
KEY = os.getenv('KEY')

if KEY is None:
    print("API_KEY is not set.")
else:
    print("API_KEY is set.")

openai.api_key = KEY

responseTemplate = {
    "response": "null"
}

def createOneWord(request):
    instructions = f"{request}. Only respond with a single word and do not provide any explaination."
    chat_completion = openai.chat.completions.create(model="gpt-3.5-turbo", 
                                                    messages=[{"role": "user", 
                                                    "content": f"{instructions}"}]).choices[0].message.content
    return chat_completion


def exportjson(data):
    print("Dumping JSON file ")
    with open(f"json_data\data{random.randint(0,9999)}.json", 'w') as f:
        json.dump(data, f)


def createAttributes(messages, responseTemplate, transcript, quizData):
    attributes = {
                    'attribute1':{
                        'name':'example', 
                        'score': 0},
                    'attribute2':{
                        'name':'example', 
                        'score': 0},
                    'attribute3':{
                        'name':'example', 
                        'score': 0},
                    'attribute4':{
                        'name':'example', 
                        'score': 0},
                    'attribute5':{
                        'name':'example', 
                        'score': 0},
                    'attribute6':{
                        'name':'example', 
                        'score': 0},
                    'attribute7':{
                        'name':'example', 
                        'score': 0},
                    'attribute8':{
                        'name':'example', 
                        'score': 0}
                }
    
    print("Generating attributes")
    instructions = f'''You are an automated system that creates insights into personal attributes based on training 
        performance. Here is the reference training material: {transcript} and {quizData}.Based on the learners 
        input provided by the user please complete this template: {attributes}. replace all attribute names and 
        scores based on the learners quiz performance and writen response. The attributes should be assocated with 
        steaming milk, the values should vary in value between them. The attribute scores are float values
        between 0 and 1 ensure that all 8 attributes are created and the template is completed.'''

    try:
        chat_completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": f"{messages}"},
                {"role": "user", "content": f"Quiz data: {quizData}"},
            ],
             
        ).choices[0].message.content
        response = responseTemplate
        response['response'] = chat_completion
        # print(response)
        
        if (__name__ == "__main__" ):
            print(response)
        return response

    except Exception as e:
        print(f"Error in createAttributes: {e}")
        return {'error': str(e)}


#grade an open ended response
def gradeResponse(message, responseTemplate):
    print("Generating grade")
    instructions = f''' You are a teacher grading a short response question, the user is learning how to steam milk. 
        Your responsed should contain only a grade value between 0 and 100. valuate the content of the 
        response and respond with only a number. A 100 would be given to a response that demonstrates perfect understanding of the 
        content in the process. do not respond with any comments. Here is the response to grade{message}'''

    try:
        chat_completion = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": instructions},
                # {"role": "user", "content": f"{message}"},
            ],
             
        ).choices[0].message.content
        response = responseTemplate
        response['response'] = chat_completion
        
        return response

    except Exception as e:
        print(f"Error in gradeResponse: {e}")
        return {'error': str(e)}

if (__name__ == "__main__" ):
    print("main method")
    
    createAttributes(OLD_TRANSCRIPT, responseTemplate, VIDEO_TRANSCRIPT, SAMPLE_QUIZ)
    


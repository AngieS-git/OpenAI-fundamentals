import json
import os
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel
from flask import Flask, request, jsonify
from groq import Groq
load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

app = Flask(__name__)
Groq.api_key = Groq(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    data  = request.get_json()
    user_query = data.get('user_query')

    response = api_key.chat.completions.create(
         model="llama3-8b-8192", 
         messages=[
             {
                 "role": "system",
                 "content": "You are a simple chatbot just answering some simple queries."
             },
             {
              "role":"user",
              "content": {user_query}
             }
         ]
    )

    chatbot_response = response.choices[0].message.content

    return jsonify({'response': chatbot_response})

if __name__ == '__main__':
    app.run(debug=True)
import os
import json
import pytz
import datetime
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel
from flask import Flask, request, jsonify
from groq import Groq

load_dotenv

api_key = os.getenv('GROQ_API_KEY')

app = Flask(__name__)
#recipe_finder = Groq(api_key=api_key)

#Create Structures
class Ingredient(BaseModel):
    name: str
    quantity: str
    quantity_unit: Optional[str]

class Recipe(BaseModel):
    recipe_name: str
    ingredients: List[Ingredient]
    directions: List[str]

@app.route('/health', methods = ['GET'])
def check_connection():
    ph_tz = pytz.timezone('Asia/Singapore')
    server_time = datetime.datetime.now(ph_tz).strftime('%Y-%m-%d %I:%M:%S %p Philippine Time')

    upchk_msg = "Server Connection Established. Everything is running smoothly!"

    res_body = {
        "status": "OK",
        "message": upchk_msg,
        "server_time":server_time
    }

    return jsonify({"status":res_body})

if __name__ == '__main__':
    app.run(debug=True)
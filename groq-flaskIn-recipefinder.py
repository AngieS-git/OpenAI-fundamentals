import os
import json
import pytz
import datetime
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel
from flask import Flask, request, jsonify
from groq import Groq

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

app = Flask(__name__)
recipe_finder = Groq(api_key=api_key)

#Create Structures
class Ingredient(BaseModel):
    name: str
    quantity: str
    quantity_unit: Optional[str]

class Recipe(BaseModel):
    recipe_name: str
    ingredients: List[Ingredient]
    directions: List[str]

#checking established network
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

    return jsonify({"status":res_body}), 200

#main function of recipe finder
@app.route('/find', methods = ['POST'])
def find_recipe_chat(user_query: str) -> Recipe:
    data = request.get_json()
    user_query = data.get('user_query')

    #error if no user query is inputted
    if not user_query:
        return jsonify({"error": "No user query provided by the user. Please enter the food you want to find the recipe for."}), 400

    try:
        response = recipe_finder.chat.completions.create(
            model = "llama3-8b-8192",
            messages = [
                {
                    "role": "system",
                    "content": "You are a recipe finder ai bot that will send in json-format of the recipe to the user"
                    f"The JSON object must use the schmema: {json.dumps(Recipe.model_json_schema(), indent =2)}",
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            temperature=0,
            stream=False,
            response_format={"type": "json_object"}
        )

        recipe_find_response = response.choices[0].message.content

        #Better formatting of Recipe Results in JSON format
        recipe_result_find = {
            "Recipe": Recipe.recipe_name,
            "Ingredients": ingrdnt_format,
            "Directions": direct_format
        }

        for ingredient in Recipe.ingredients:
            ingrdnt_format = f"- {ingredient.name} {ingredient.quantity} {ingredient.quantity_unit or ''}"

        for step, direction in enumerate(Recipe.directions, start = 1):
            direct_format = f"{step}. {direction}"

        return jsonify(recipe_result_find)
    
    except Exception as e:
        return jsonify({"Error Message: Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
import os
import json
import pytz
import datetime
import base64
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel
from flask import Flask, request, jsonify
from groq import Groq
load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

app = Flask(__name__)
recipe_finder_client = Groq(api_key=api_key)

#Create Structures
class Ingredients(BaseModel):
    name: str
    quantity: str
    quantity_unit: Optional[str]

class Recipe(BaseModel):
    recipe_name: str
    ingredients: List[Ingredients]
    directions: List[str]

#Check if network is established
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

@app.route('/findrecipe', methods = ['POST'])
def find_recipe_chat() -> Recipe:
    data = request.get_json()
    user_image = data.get('user_image')
    base64_image = base64.b64encode(user_image.read()).decode('utf-8')

    #error if no user image is uploadsed
    if not user_image:
        return jsonify({"error": "No user image provided. Please upload the food you want to find the recipe for."}), 400

    try:
        response = recipe_finder_client.chat.completions.create(
            model = "llama-3.2-11b-vision-preview",
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": "You are a recipe finder ai bot that will send in json-format of the recipe to the user"
                    f"The JSON object must use the schmema: {json.dumps(Recipe.model_json_schema(), indent =2)}",
                        },
                        
                    ]
                },
                {
                    "role": "user",
                    "content": user_image
                }
            ],
            temperature=0,
            stream=False,
            response_format={"type": "json_object"}
        )

        #Recipe.model_validate_json(response.choices[0].message.content)
        recipe_data = json.loads(response.choices[0].message.content)

        recipe = Recipe(
            recipe_name=recipe_data.get("recipe_name", ""),
            ingredients=[
                Ingredient(
                    name=ingredient["name"],
                    quantity=ingredient["quantity"],
                    quantity_unit=ingredient.get("quantity_unit", None)
                )
                for ingredient in recipe_data.get("ingredients", [])
            ],
            directions=[
                direction if direction.strip().startswith(f"{step}.") else f"{step}. {direction}"
                for step, direction in enumerate(recipe_data.get("directions", []), start=1)
            ]
        )

        return jsonify(recipe.dict())
    except Exception as e:
        return jsonify({"Error Message: Internal Server Error"}), 500


if __name__ == '__main__':
    app.run(debug=True)

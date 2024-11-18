from typing import List, Optional
import json
import os
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
from groq import Groq

api_key = os.getenv('GROQ_API_KEY')

client = Groq(api_key=api_key)

class Ingredient(BaseModel):
    name: str
    quantity: str
    quantity_unit:Optional[str]

class Recipe(BaseModel):
    recipe_name:str
    ingredients: List[Ingredient]
    directions: List[str]

def get_recipe(recipe_name: str) -> Recipe:
    chat_completion = client.chat.completions.create(
         model="llama3-8b-8192", 
         messages=[
             {
                 "role": "system",
                 "content": "You are a recipe database that outputs recipes in JSON format.\n"
                 f"The JSON object must use the schmema: {json.dumps(Recipe.model_json_schema(), indent =2)}",
             },
             {
                 "role": "user",
                 "content": f"Fetch a recipe for {recipe_name}"
             }
         ],
         temperature=0,
         stream=False,
         response_format={"type": "json_object"},
    )
    return Recipe.model_validate_json(chat_completion.choices[0].message.content)

def print_recipe(recipe: Recipe):
    print("Recipe: ", recipe.recipe_name)

    print("\nIngredients: ")
    for ingredient in recipe.ingredients:
        print(
            f"- {ingredient.name} {ingredient.quantity} {ingredient.quantity_unit or ''}"
        )

    print("\nDirections: ")
    for step, direction in enumerate(recipe.directions, start=1):
        print(f"{step}. {direction}")

recipe = get_recipe("Blueberry Cupcake")        
print_recipe(recipe)
import os
from dotenv import load_dotenv
from groq import Groq
import base64
load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

client = Groq(api_key=api_key)

#First encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = r'D:\CODES\OpenAI\groq-vision\1_P4PdJq4ZKkcliA-N795DSA.jpg'

base64_image = encode_image(image_path)

pass_image_local = client.chat.completions.create(
    model = "llama-3.2-11b-vision-preview",
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "I am passing an image locally, can you give me the name of this Character?",
                },
                {
                    "type": "image_url" ,
                    "image_url":{
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
)

print(pass_image_local.choices[0].message.content)
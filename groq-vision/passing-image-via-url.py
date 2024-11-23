import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

client = Groq(api_key=api_key)

pass_image_url = client.chat.completions.create(
    model= "llama-3.2-11b-vision-preview",
    messages = [
        # {
        #     "role": "system",
        #     "content": "You are an AI bot image interpreter that will describe an image uploaded via url."
        # },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text":"What is this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Taka_Shiba.jpg"
                    }
                }
            ]
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None
)

print(pass_image_url.choices[0].message)
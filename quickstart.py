from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": """You are a Career Advisor for a user asking some career advise on any particular field. You are to provide comprehensive 
            roadmap of a particular job role that the user can have.
            """
        },
        {
            "role": "user",
            "content": """I'm a 4th year Computer Engineering student with a novice level understanding of Machine Learning, specifically Computer Vision
            focusing on pose estimation and natural language processing.
        """
        }
    ]
)

print(completion.choices[0].message)
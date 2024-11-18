from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=api_key)

completion = client.chat.completions.create(
    model="llama3-8b-8192",
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
    ],
    #Some additional parameters
    temperature=1.0, #the entropy
    max_tokens=1024,
    top_p=1, #1 meaning use all tokens in the vocabulary
    stop=None,
    stream=True
)

#previously: print(chat_completion.choices[0].message.content)

for chunk in completion:
    print(chunk.choices[0].delta.content, end="") #basically more structured results from gen ai compared to just chat completion
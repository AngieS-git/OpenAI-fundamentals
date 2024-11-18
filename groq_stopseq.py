from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

client = Groq(api_key=api_key)

stop_seq = client.chat.completions.create(
    model = "llama3-8b-8192",
    messages = [
        {
            "role": "system",
            "content":"You are an AI assistant performing basic tasks."
        },
        {
            "role": "user",
            "content":"Count to 10. Your response must begin with \"1, \". example is 1, 2, 3,...",
        }
    ],
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stop=", 6",
    stream=False
)

print(stop_seq.choices[0].message.content)
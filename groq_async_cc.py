from groq import AsyncGroq
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

async def main():
    client = AsyncGroq(api_key=api_key)

    chat_completion = await client.chat.completions.create(
        model="llama3-8b-8192", 
        messages = [
        {
                "role": "system",
                "content": "you are a helpful assistant."
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
    ],
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=True
    )

    #print(chat_completion.choices[0].message.content)
    async for chunk in chat_completion:
        print(chunk.choices[0].delta.content, end="")


asyncio.run(main())

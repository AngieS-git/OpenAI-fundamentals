from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": """You are a Career Advisor for a user asking some career advise on any particular field. You are to provide comprehensive 
            roadmap of a particular job role that the user can have, containing the necessary certifications or credentials that they can have
            to further improve their skills in the said field.
            """
        },
        {
            "role": "user",
            "content": """I'm a 4th year Computer Engineering student with a novice level understanding of Machine Learning, specifically Computer Vision
            focusing on pose estimation and natural language processing. I am interested in being a Machine Learning Developer. Can you give me some advice
            and a roadmap on how I can make the most figures in this industry?
        """
        }
    ]
)

print(completion.choices[0].message)
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ["GROQ_API_KEY"],
                base_url="https://api.groq.com/openai/v1")

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "My name is Alex."
        },
        {
            "role": "assistant",
            "content": "Nice to meet you, Alex."
        },
        {
            "role": "user",
            "content": "What is my name?"
        }
    ]
)

print(response)
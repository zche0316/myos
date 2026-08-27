import os

from dotenv import load_dotenv

from myos.llm.groq import GroqProvider

load_dotenv()

llm = GroqProvider(
    model="openai/gpt-oss-120b",
)

response = llm.generate(
    [
        {
            "role": "user",
            "content": "What is an AI agent?"
        }
    ]
)

print(response.input_tokens)
print(response.output_tokens)
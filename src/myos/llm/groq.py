import os

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from myos.llm.provider import LLMProvider
from myos.llm.models import LLMResponse


class GroqProvider(LLMProvider):

    def __init__(self, model: str):
        self.client = OpenAI(
            api_key=os.environ["GROQ_API_KEY"],
            base_url="https://api.groq.com/openai/v1",
        )
        self.model = model

    def generate(self, messages: list[ChatCompletionMessageParam]) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return LLMResponse(
            response.choices[0].message.content or "",
            model=response.model,
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            output_tokens=response.usage.completion_tokens if response.usage else 0,
        )
import os
import json

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from myos.llm.provider import LLMProvider
from myos.llm.models import LLMResponse
from myos.tools.models import ToolCall


class GroqProvider(LLMProvider):

    def __init__(self, model: str):
        self.client = OpenAI(
            api_key=os.environ["GROQ_API_KEY"],
            base_url="https://api.groq.com/openai/v1",
        )
        self.model = model

    def generate(
        self, 
        messages: list[ChatCompletionMessageParam],
        tools: list[dict] | None = None,
    ) -> LLMResponse:


        kwargs = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools

        response = self.client.chat.completions.create(**kwargs)   

        message = response.choices[0].message

        tool_calls = []

        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_calls.append(
                    ToolCall(
                        id=tool_call.id,
                        name=tool_call.function.name,
                        arguments=json.loads(tool_call.function.arguments),
                    )
                )
            
        return LLMResponse(
            content=message.content,
            model=response.model,
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            output_tokens=response.usage.completion_tokens if response.usage else 0,
            tool_calls=tool_calls,
            message=message.model_dump(
                exclude_none=True
            ),
        )
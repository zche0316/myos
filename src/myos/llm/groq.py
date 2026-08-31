import os
import json

from openai import OpenAI

from myos.llm.provider import LLMProvider
from myos.llm.models import LLMResponse
from myos.messages.models import ToolCall, Message, UserMessage, SystemMessage, AssistantMessage, ToolMessage


class GroqProvider(LLMProvider):

    def __init__(self, model: str):
        self.client = OpenAI(
            api_key=os.environ["GROQ_API_KEY"],
            base_url="https://api.groq.com/openai/v1",
        )
        self.model = model

    def _to_api_message(
        self,
        message: Message
    ) -> dict:

        if isinstance(message, dict):
            role = message.get("role")
            if role == "tool":
                return {
                    "role": "tool",
                    "content": message.get("content"),
                    "tool_call_id": message.get("tool_call_id"),
                }

            result = {
                "role": role,
                "content": message.get("content"),
            }

            if role == "assistant" and message.get("tool_calls"):
                result["tool_calls"] = [
                    {
                        "id": tool_call.get("id"),
                        "type": "function",
                        "function": {
                            "name": tool_call.get("function", {}).get("name"),
                            "arguments": tool_call.get("function", {}).get("arguments", "{}"),
                        },
                    }
                    for tool_call in message.get("tool_calls", [])
                ]

            return result

        if isinstance(message, UserMessage):
            result = {
                "role": "user",
                "content": message.content,
            }

        elif isinstance(message, SystemMessage):
            result = {
                "role": "system",
                "content": message.content,
            }

        elif isinstance(message, AssistantMessage):
            result = {
                "role": "assistant",
                "content": message.content,
            }

            if message.tool_calls:
                result["tool_calls"] = [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.name,
                            "arguments": json.dumps(tool_call.arguments),
                        },
                    }
                    for tool_call in message.tool_calls
                ]

        elif isinstance(message, ToolMessage):
            return {
                "role": "tool",
                "content": message.content,
                "tool_call_id": message.tool_call_id,
            }

        else:
            raise TypeError(
                f"Unsupported message type: {type(message)}"
            )

        return result


    def _from_api_message(
        self,
        message
    ) -> AssistantMessage:

        tool_calls = []

        if message.tool_calls:
            for tool_call in message.tool_calls:                    
                tool_calls.append(
                    ToolCall(
                        id=tool_call.id,
                        name=tool_call.function.name,
                        arguments=json.loads(tool_call.function.arguments)
                    )
                )

        return AssistantMessage(
            content=message.content,
            tool_calls=tool_calls,            
        )


    def generate(
        self, 
        messages: list[Message],
        tools: list[dict] | None = None,
    ) -> LLMResponse:
        
        # 1. MyOS Message → API Message
        api_messages = [
            self._to_api_message(message)
            for message in messages
        ]

        # 2. Prepare API request
        kwargs = {
            "model": self.model,
            "messages": api_messages,
        }

        if tools:
            kwargs["tools"] = tools

        # 3. Call Groq
        response = self.client.chat.completions.create(**kwargs)   

        # 4. API Message → MyOS AssistantMessage
        assistant_message = self._from_api_message(
            response.choices[0].message
        )

       # 5. Wrap into MyOS LLMResponse
        return LLMResponse(
            content=assistant_message.content,
            model=response.model,
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            output_tokens=response.usage.completion_tokens if response.usage else 0,
            tool_calls=assistant_message.tool_calls,
            message=assistant_message,
        )
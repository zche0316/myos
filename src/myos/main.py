import os

from dotenv import load_dotenv

from myos.llm.groq import GroqProvider
from myos.tools.calculator import calculate
from myos.tools.models import Tool
from myos.tools.registry import ToolRegistry

load_dotenv()

llm = GroqProvider(
    model="openai/gpt-oss-120b",
)

calculator_tool = Tool(
    name="calculator",
    description="Evaluate a mathematical expression.",
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The mathematical expression to evaluate.",
            }
        },
        "required": ["expression"],
    },
    function=calculate,
)

registry = ToolRegistry()
registry.register(calculator_tool)

messages = [
    {
        "role": "user",
        "content": "What is 12345 + 6789?",
    }
]

while True:
    response = llm.generate(messages=messages, tools=registry.schemas())
    print(f"Response: {response.content}")
    print(f"Tool Calls: {response.tool_calls}")

    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool = registry.get(tool_call.name)
            result = tool.function(**tool_call.arguments)
            messages.append({
                "role": "assistant",
                "content": f"Tool '{tool_call.name}' called with arguments {tool_call.arguments}. Result: {result}",
            })
            print(f"Tool '{tool_call.name}' called with arguments {tool_call.arguments}. Result: {result}")
            
    else:
        break
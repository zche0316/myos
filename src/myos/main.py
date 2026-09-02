import os

from dotenv import load_dotenv

from myos.llm.groq import GroqProvider
from myos.tools.calculator import calculate
from myos.tools.failing import failing_tool
from myos.tools.models import Tool
from myos.tools.registry import ToolRegistry
from myos.agent.runtime import AgentRuntime
from myos.messages.models import UserMessage, SystemMessage, AssistantMessage, ToolMessage

load_dotenv()

def main():

    llm = GroqProvider(
        model="openai/gpt-oss-120b"
    )

    failing_tool_instance = Tool(
        name="failing_tool",
        description=(
            "A tool that always fails."
        ),
        parameters={
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "description": "The value to fail with.",
                },
            },
            "required": ["value"],
        },
        function=failing_tool,
    )

    calculator_tool = Tool(
        name="calculator",
        description=(
            "Evaluates a mathematical expression."
        ),
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate.",
                },
            },
            "required": ["expression"],
        },
        function=calculate,
    )


    registry = ToolRegistry()

    registry.register(
        calculator_tool
    )
    registry.register(
        failing_tool_instance
    )

    agent = AgentRuntime(
        llm=llm,
        registry=registry,
    )


    answer = agent.run(
        messages=[
            UserMessage(
                content="Use the failing_tool with value hello."
            )
        ]
    )


    print()
    print("Final answer:")
    print(answer)


if __name__ == "__main__":
    main()
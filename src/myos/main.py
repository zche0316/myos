import os

from dotenv import load_dotenv

from myos.llm.groq import GroqProvider
from myos.tools.calculator import calculate
from myos.tools.models import Tool
from myos.tools.registry import ToolRegistry
from myos.agent.runtime import AgentRuntime
from myos.messages.models import UserMessage, SystemMessage, AssistantMessage, ToolMessage

load_dotenv()

def main():

    llm = GroqProvider(
        model="openai/gpt-oss-120b"
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


    agent = AgentRuntime(
        llm=llm,
        registry=registry,
    )


    answer = agent.run(
        messages=[
            UserMessage(
                content="What is 123454 * 567890?"
            )
        ]
    )


    print()
    print("Final answer:")
    print(answer)


if __name__ == "__main__":
    main()
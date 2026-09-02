from myos.agent.runtime import AgentRuntime
from myos.agent.session import AgentSession

from myos.llm.groq import GroqProvider
from myos.tools.models import Tool
from myos.tools.registry import ToolRegistry
from myos.tools.calculator import CalculatorTool
from myos.messages.models import UserMessage
import os
from dotenv import load_dotenv

load_dotenv()



llm = GroqProvider(
    model="openai/gpt-oss-120b",
)

tool_registry = ToolRegistry()


calculator_tool = Tool(
    name="calculator",
    description="A tool for performing calculations.",
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
    function=CalculatorTool().call,
)

tool_registry.register(calculator_tool)
    
runtime = AgentRuntime(
    llm=llm,
    registry=tool_registry,
    max_iterations=10,
)


session = AgentSession()

session.messages.append(
    UserMessage(
        content="My name is Chen.",
    )
)

answer = runtime.run(session)

print("\nRound 1: ")
print(answer)

session.messages.append(
    UserMessage(
        content="What is my name?",
    )
)

answer = runtime.run(session)
print("\nRound 2: ")
print(answer)

session.messages.append(
    UserMessage(
        content="What did I tell you at the beginning?",
    )
)

answer = runtime.run(session)
print("\nRound 3: ")
print(answer)

session.messages.append(
    UserMessage(
        content="What did I you answer me in the previous round?",
    )
)

answer = runtime.run(session)
print("\nRound 4: ")
print(answer)


print("\nFinal session history: ")

for i, message in enumerate(session.messages):
    print(i, message)
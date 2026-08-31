from typing import Any, Dict, List

from myos.llm.provider import LLMProvider
from myos.tools.registry import ToolRegistry
from myos.messages.models import Message, ToolMessage


class AgentRuntime:

    def __init__(
        self,
        llm: LLMProvider,
        registry: ToolRegistry,
        max_iterations: int = 10,
    ):
        self.llm = llm
        self.registry = registry
        self.max_iterations = max_iterations

    def run(
        self,
        messages: list[Message],
    ) -> str:

        for _ in range(self.max_iterations):

            response = self.llm.generate(
                messages=messages,
                tools=self.registry.schemas(),
            )

            print(
                f"[Runtime] LLM Response: "
                f"{response.content}"
            )

            print(
                f"[Runtime] Tool Calls: "
                f"{response.tool_calls}"
            )

            # 1. LLM 给出了最终答案
            if not response.tool_calls:
                return response.content or ""

            # 2. 保存 Assitant 的 Tool Call
            messages.append(
                response.message
            )

            # 3. 执行 Tool Calls
            for tool_call in response.tool_calls:

                tool = self.registry.get(
                    tool_call.name
                )

                if not tool:
                    raise RuntimeError(
                        f"Tool not found: {tool_call.name}"
                    )

                result = tool.function(
                    **tool_call.arguments
                )

                print(
                    f"[Runtime] Tool: "
                    f"{tool_call.name} returned: {result}"
                )

                # 4. 保存 Tool Result
                messages.append(
                    ToolMessage(
                        content=result,
                        tool_call_id=tool_call.id,
                    )
                )

                print("[Runtime] Messages:")
                for message in messages:
                    print(message)

        raise RuntimeError(
            "Maximum agent iterations reached."
        )
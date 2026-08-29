from typing import Any

from myos.llm.provider import LLMProvider
from myos.tools.registry import ToolRegistry


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
        messages: list[dict[str, Any]],
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

            # 1. 没有 Tool Call
            if not response.tool_calls:
                return response.content or ""

            # 2. 先加入 Assistant Tool Call Message
            messages.append(
                response.message
            )

            # 3. 执行所有 Tool Calls
            for tool_call in response.tool_calls:

                tool = self.registry.get(
                    tool_call.name
                )

                result = tool.function(
                    **tool_call.arguments
                )

                # 4. 加入真正的 Tool Message
                messages.append(
                    {
                        "role": "tool",
                        "content": str(result),
                        "tool_call_id": tool_call.id
                    }
                )

                print(
                    f"[Runtime] Tool "
                    f"{tool_call.name} "
                    f"returned: {result}"
                )

        raise RuntimeError(
            "Maximum agent iterations reached."
        )
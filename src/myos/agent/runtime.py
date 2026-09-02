from myos.llm.provider import LLMProvider
from myos.tools.models import ToolResult
from myos.tools.registry import ToolRegistry
from myos.agent.session import AgentSession
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


    def _execute_tool(
        self,
        tool_name: str,
        arguments: dict,
    ) -> ToolResult:

        tool = self.registry.get(tool_name)

        if not tool:
            return ToolResult(
                success=False,
                content=(
                    f"Tool {tool_name}"
                    f"is not registered."
                )
        )

        try:
            result = tool.function(**arguments)
            return ToolResult(
                success=True,
                content=result,
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=(
                    f"Tool execution failed:"
                    f"{type(e).__name__}: {e}"
                ),
            )

        
    def run(
        self,
        session: AgentSession,
    ) -> str:

        messages = session.messages

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

                messages.append(
                    response.message
                )
                
                return response.content or ""

            # 2. 保存 Assitant 的 Tool Call
            messages.append(
                response.message
            )

            # 3. 执行 Tool Calls
            for tool_call in response.tool_calls:

                tool_result = self._execute_tool(
                    tool_name=tool_call.name,
                    arguments=tool_call.arguments,
                )

                print(
                    f"[Runtime] Tool: "
                    f"{tool_call.name} "
                    f"success: {tool_result.success} "
                )

                print(
                    f"[Runtime] Tool Result: "
                    f"{tool_result.content}"
                )

                # 4. 保存 Tool Result
                messages.append(
                    ToolMessage(
                        content=tool_result.content,
                        tool_call_id=tool_call.id,
                    )
                )

                print("[Runtime] Messages:")
                for message in messages:
                    print(message)

        raise RuntimeError(
            "Maximum agent iterations reached."
        )
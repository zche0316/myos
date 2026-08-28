from myos.tools.models import Tool


class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name}")

        return self._tools[name]

    def schemas(self) -> list[dict]:
        return [tool.to_schema() for tool in self._tools.values()]
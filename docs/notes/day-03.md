# Day 3 — Tool Calling

## Goal

Let the LLM call registered tools and bring the results back into the agent loop.

## Implemented

- Tool abstraction
- Tool registry
- Tool schema generation
- Tool call representation
- Tool execution inside the runtime
- Tool result converted back into a message

## Tool Model

The tool definition is a simple contract:

```python
@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    function: Callable
```

The registry keeps all available tools and exposes their schemas to the LLM:

```python
class ToolRegistry:
    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def schemas(self) -> list[dict]:
        return [tool.to_schema() for tool in self._tools.values()]
```

## Runtime Flow

```text
UserMessage
    ↓
LLM
    ↓
AssistantMessage(tool_calls=[...])
    ↓
Runtime executes tool
    ↓
ToolMessage(content=result)
    ↓
LLM
    ↓
Final answer
```

The important idea is:

- the LLM decides which tool to call
- the runtime decides whether to execute it
- the tool result is sent back to the model as a message

## Tool Call Representation

The internal model uses a typed structure:

```python
@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]
```

This helps the runtime separate:

- tool name
- call id
- argument payload

## Execution Loop

Conceptually:

```python
response = llm.generate(messages, tools=registry.schemas())

if response.tool_calls:
    for tool_call in response.tool_calls:
        result = execute_tool(tool_call.name, tool_call.arguments)
        messages.append(ToolMessage(...))
```

The runtime does not blindly execute arbitrary code.
It only executes tools that were registered and exposed in the schema.

## Example

A calculator tool can be called like this:

```text
User: 123454 * 567890
```

The model may emit:

```text
tool_call = {
  "name": "calculator",
  "arguments": {"expression": "123454 * 567890"}
}
```

Then the runtime executes it and returns:

```text
70108292060
```

## Key Understanding

The LLM does not directly execute tools in Python.
It emits a structured tool call, and the application performs the actual function call.

This is the core boundary:

```text
LLM chooses tool
Runtime executes tool
Tool output returns to LLM
```

This keeps the model in the decision loop while the app remains in charge of side effects.

## Outcome

MyOS can now make the agent call registered tools, execute them safely, and feed the result back into the conversation for the next LLM step.

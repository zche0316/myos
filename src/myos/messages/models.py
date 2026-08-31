from dataclasses import dataclass, field
from typing import Literal, Any


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class Message:
    role: str = ""
    content: str | None = None


@dataclass
class UserMessage(Message):
    role: Literal["user"] = "user"


@dataclass
class SystemMessage(Message):
    role: Literal["system"] = "system"


@dataclass
class AssistantMessage(Message):
    role: Literal["assistant"] = "assistant"
    tool_calls: list[ToolCall] = field(default_factory=list)


@dataclass
class ToolMessage(Message):
    role: Literal["tool"] = "tool"
    tool_call_id: str = ""

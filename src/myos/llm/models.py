from typing import Any
from dataclasses import dataclass, field

from myos.messages.models import ToolCall, AssistantMessage

@dataclass
class LLMResponse:
    content: str | None
    model: str
    input_tokens: int
    output_tokens: int
    message: AssistantMessage
    tool_calls: list[ToolCall] = field(default_factory=list)


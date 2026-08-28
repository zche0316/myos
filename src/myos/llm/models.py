from dataclasses import dataclass, field

from myos.tools.models import ToolCall


@dataclass
class LLMResponse:
    content: str | None
    model: str
    input_tokens: int
    output_tokens: int
    tool_calls: list[ToolCall] = field(default_factory=list)


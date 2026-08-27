from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int


from dataclasses import dataclass, field
from uuid import uuid4

from myos.messages.models import Message

@dataclass
class AgentSession:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    messages: list[Message] = field(
        default_factory=list
    )
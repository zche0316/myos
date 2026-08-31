from abc import ABC, abstractmethod


from myos.llm.models import LLMResponse
from myos.messages.models import Message

class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self, 
        messages: list[Message],
        tools=None
    ) -> LLMResponse:
        """Generate a response from the LLM"""
        pass

    
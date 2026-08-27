from abc import ABC, abstractmethod

from openai.types.chat import ChatCompletionMessageParam

from myos.llm.models import LLMResponse

class LLMProvider(ABC):

    @abstractmethod
    def generate(self, messages: list[ChatCompletionMessageParam]) -> LLMResponse:
        """Generate a response from the LLM"""
        pass

    
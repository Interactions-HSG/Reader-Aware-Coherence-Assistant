from abc import ABC, abstractmethod


class LLMProvider(ABC):

    name = "llm_provider"
    @abstractmethod
    def ask_model(self,
                  query,
                  output_format=None, output_format_params={},
                  response_format=None):
        pass
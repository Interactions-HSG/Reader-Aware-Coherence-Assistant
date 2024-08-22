import requests

from arch.llm_providers import LLMProvider


class OllamaProvider(LLMProvider):
    name = "ollama"
    model = "gemma2"
    base_url = 'http://localhost:11434'

    def __init__(self, model="gemma2"):
        self.model = model

    def ask_model(self,
                  query,
                  output_format=None, output_format_params=None,
                  response_format=None):
        body = {
            "model": self.model,
            "prompt": query,
            "stream": False
        }
        r = requests.post(self.base_url + "/api/generate", json=body)
        return r.json()["response"]

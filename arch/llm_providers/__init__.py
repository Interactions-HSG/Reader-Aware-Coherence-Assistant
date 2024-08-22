# -*- coding: utf-8 -*-
#
from arch.llm_providers.abstract_llm_provider import LLMProvider
from arch.llm_providers.openai_provider import OpenAIClient
from arch.llm_providers.ollama_provider import OllamaProvider

__all__ = ['ProviderManager', 'openai_provider'
           ]

from utils import load_config


class MetaProviderManager(type):
    _instances = {}

    def __call__(self, *args, **kwds):
        # Check if there is no instance
        if self not in self._instances:
            # Create an unique instance
            uniqInstance = super().__call__(*args, **kwds)
            self._instances[self] = uniqInstance

        # Return the unique instance associated with the current object
        return self._instances[self]


class ProviderManager(metaclass=MetaProviderManager):
    dict = {}
    default_provider_name = "openai"

    def register(self, provider: LLMProvider):
        self.dict[provider.name] = provider

    def unregister(self, provider_name):
        del self.dict[provider_name]

    def set_default_provider(self, provider_name):
        self.default_provider_name = provider_name

    def is_registered(self, provider_name):
        return (provider_name in self.dict.keys())

    def get_provider(self):
        return self.dict[self.default_provider_name]



provider_manager = ProviderManager()
config = load_config()
llm_provider = config["LLM_PROVIDER"]
if llm_provider == "openai":
    oai_manager = OpenAIClient(config["LLM_API_KEY"], config["LLM_MODEL"])
    provider_manager.register(oai_manager)
    provider_manager.set_default_provider("openai")
elif llm_provider == "ollama":
    o_provider = OllamaProvider(config["LLM_MODEL"])
    provider_manager.register(o_provider)
    provider_manager.set_default_provider("ollama")





# "providers = ProviderManager()" -> providers = call to MetaProviderManager then call ProviderManager
# __call__ = when MetaProviderManager is called

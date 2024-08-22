import openai
from openai import OpenAI, AuthenticationError

from arch.llm_providers.abstract_llm_provider import LLMProvider
from ..ai_comm_utils import validate, SupportedOutputFormats
from flask import jsonify


# from . import ProviderManager

# import traceback


class OpenAIClient(LLMProvider):
    '''
        Client connected an LLM provider.

        This client connects to OpenAI API to communicate with ChatGPT.
        Note: prompts and responses should follow the specific documentation
        (https://platform.openai.com/docs/api-reference/messages/createMessage).

    '''

    name = "openai"

    delegate = None

    prompting_limit = 3
    system_role = "You are an assistant for analyzing coherence."
    model = "gpt-4o-mini"

    last_model_output = None

    def __init__(self, api_key, model="gpt-4o-mini"):
        self.model = model
        self.connect(api_key)
        openai.api_key = api_key

    def connect(self, key):
        self.delegate = OpenAI(api_key=key)

    def is_key_set(self):
        try:
            self.delegate.models.list()
        except AuthenticationError:
            # traceback.print_exc()
            return False
        else:
            return True

    def get_models_list(self):
        self.delegate.models.list()

    def ask_model(self,
                  query,
                  output_format=None, output_format_params=None,
                  response_format=None):
        """
        ask_model transforms a query into a prompt and sends it to the model

        This function transforms a query into a prompt understable by the 
        model. Then it sends this prompt to the associated model (delegate).
        Finally, it validates the model's output, and returns the formatted JSON
        response as result.

        By default, the system role is 'analyzing coherence', which relates to the
        main goal of this system: analyzing the coherence between user inputs and 
        selected reader profiles.

        By nature the GPT doesn't return deterministic responses (in terms of 
        format and content, for example). For this reason, this function operates 
        a validation step to ensure that GPT ouput respects any format asked in the
        prompt.
        
        Finally, it returns a formatted JSON response as a result the system 
        can rely on (in terms of format).
        """
        if output_format_params is None:
            output_format_params = {}
        try:
            v = False
            limit = self.prompting_limit
            while (not v) and (limit > -1):  # continue to ask gpt
                # Send the prompt to ChatGPT 
                response = self.delegate.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_role},
                        {"role": "user", "content": query}
                    ],
                    stream=False
                )

                # Extract the combined output from the response according to the 
                # OpenAI API documentation
                # old version: model_output = response["choices"][0]["message"]["content"]
                # new version (as of 20.08.2024):
                model_output = response.choices[0].message.content

                # Validate the output
                if output_format:
                    v = validate(model_output, output_format, params=output_format_params)
                else:
                    v = True
                # Decrement the limit
                limit -= 1

            last_model_output = model_output

            # Return the response as JSON
            return jsonify(self.create_response(
                textual_output=last_model_output,
                response_format=response_format
            ))
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return jsonify(self.create_response(
                textual_output="An error occurred while processing the request.",
                error_msg="Error calling OpenAI API",
                response_format=response_format))

    def create_response(self,
                        textual_output='', dict_data={}, error_msg='',
                        response_format=None):
        '''
        Create the response from openai.
        This function is designed to adapt to the prompt. Right now we don't know the prompt,
        but it is possible to access the prompt at runtime. 
        This is done by applying a technique called late binding. Late binding allows the function
        to defer defining the response format until the moment it is executed. With a late binding 
        to the response format, it's possible to access the prompt at runtime, just before formating
        the response.
        It allows the response format(a user defined format) to be flexibly defined according to the 
        runtime conditions and prompt characteristics.

        Parameters:
        - textual_output (str): Main textual content of the response.
        - dict_data (dict): Additional data provided in dictionary form.
        - error_msg (str): Error message in case there is an error during processing.
        - response_format (callable, optional): A callable that, if provided, formats the response 
        according to specific requirements.

        Returns:
        - dict: A dictionary containing the 'text', 'dict', and 'err' keys with values. 
        If 'response_format' is provided, returns the output of this callable, utilizing late 
        binding to adapt to the runtime prompt.

        '''

        if response_format:
            return response_format(
                text=textual_output,
                dict=dict_data,
                err=error_msg
            )

        return {
            "text": textual_output,
            "dict": dict_data,
            "err": error_msg
        }

# def import_main_execution():
#    global DEFAULT_PROVIDER_NAME
#
#    manager = ProviderManager()
#    if not manager.is_registered(DEFAULT_PROVIDER_NAME):
#        manager.register(OpenAIClient())
#        print('default_provider registered')
#
#    # if DEFAULT_OPENAI_PROVIDER is None:
#    #    DEFAULT_OPENAI_PROVIDER = OpenAIClient()
#    print('default_provider imported')


# def run_main_execution():
#    print('default_provider executed')


# designed to run independently, notice the 'if name == 'main' part here
# if __name__ == '__main__':
#   run_main_execution()
# else:
#   import_main_execution()

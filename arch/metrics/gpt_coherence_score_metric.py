#to score a piece of text 
from arch import *

#accept a p of text
import openai
import re, json

# Coherence range
KEYWORDS_MAX_LIST = 3
COHERENCE_RANGE_ON_SUM = [0, KEYWORDS_MAX_LIST]

def score(text, ref_text, provider, params={}):#the score is the value you get when apply the metric

    # Use OpenAI to get a response from the model
    # provider: the current llm provider
    # response = openai.ChatCompletion.create(**prompt)

    #1. extract the keywords from the reference text
    keywords = extract_key_terms(ref_text, KEYWORDS_MAX_LIST, provider)
    #print(keywords['dict'])

    #2. calculate the coherence scores
    dict_scores = calculate_coherence_scores(text, keywords['dict'], provider)
    #print(dict_scores)
    #3. calculate the final score
    value=None
    method='sum'
    if 'score_method' in params.keys():
        method=params['score_method']

    if method == 'sum':
        value=sum(dict_scores.values())
    elif method == 'blabla':
        pass
    else:
        raise KeyError

    return value

def dummyFct(text, keywords):
    #2. identify the coherence between keywords and the text
    prompt = f"Be the list of keywords: {keywords}\n" + \
        "Return a response limited to one decimal value from 0 to 10 that represents the coherence score " +\
        f"between the given keywords and the following text:\n{text}"
    # Use an appropriate model for text analysis
    response = openai.Completion.create(
        engine="gpt-4o-mini-instruct",
        prompt=prompt,
        max_tokens=150
    )

    print(response.choices[0])

    # Try to find all possible floats (and, hence, integers) in the response and
    # convert each into a float value
    value = [float(v) for v in re.findall(r'\d+\.?\d*', response.choices[0].text.strip())]
    # Return only the first float (or integrer) found (as a float)
    return value[0]


def extract_key_terms(text, length, provider):
    """
    This function takes a text paragraph and uses OpenAI's GPT model to extract key terms and concepts.

    Args:
    text (str): The text paragraph to be analyzed.
    provider (LLMProvider): current LLM Provider.
    
    Returns:
    str: The extracted key terms and concepts.
    """
    query = (
        f"Consider this paragraph: \"{text}\" \n"
        f"Abstract {length} concepts that relate to the main subject of this paragraph. "
        "Return only a list of keywords separated by commas."
    )
    output = provider.ask_model(
        query, 
        output_format = validate_list_of_words, output_format_params = {'strict':True},
        response_format = extract_list_of_words
    )

    # # Initialize the OpenAI API with the provided API key
    # openai.api_key = openai_api_key

    # # Define the prompt for extracting key terms and concepts
    # prompt = (
    #     f"Consider this paragraph: \"{text}\" \n\n"
    #     f"Abstract {length} concepts that relate to the main subject of this text and "
    #     "return only the list of concepts separated by commas."
    # ) #need regular expression to extract python list - lib(pattern)
    # prompt = (
    #     f"Consider this paragraph: \"{text}\" \n"
    #     f"Abstract {length} concepts that relate to the main subject of this paragraph. "
    #     "Return only a list of keywords separated by commas."
    # )

    # # Use an appropriate model for text analysis
    # response = openai.ChatCompletion.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": "You are an assistant for analyzing coherence."},
    #         {"role": "user", "content": prompt}
    #     ],

    # )
    
    #print(output)
    #gptOutput = output['text'] #response["choices"][0]["message"]["content"]

    return output


def validate_list_of_words(text, params={}):
    bStrict = True #by default
    if 'strict'in params.keys():bStrict = params['strict']

    #regular expression to search for a pattern within a string (gptOutput in 
    # this case), and specifically to extract text enclosed in square brackets    
    ex = re.search(r"\[(.*)\]", text)
    
    if ex: return True
    else: return not(bStrict)

def extract_list_of_words(text, dict={}, err=''):

    #regular expression to search for a pattern within a string (gptOutput in 
    # this case), and specifically to extract text enclosed in square brackets    
    ex = re.search(r"\[(.*)\]", text)

    # here we extract the words from the text to create a list (in the sens of 
    # Python).
    if ex:
        my_list = ex.group(1).split(',')
    else:
        my_list = text.split(',')

    # returns a copy of the list by striping each element
    return {'text': my_list, 'dict': [x.strip() for x in my_list], 'err':''}



def calculate_coherence_scores(text, keywords, provider):
    """
    This function takes a text paragraph and uses OpenAI's GPT model to extract key terms and concepts.

    Args:
    text (str): The text paragraph to be analyzed.
    provider (LLMProvider): The current provider.
    
    Returns:
    str: The extracted key terms and concepts.
    """
    query = (
        f"Consider this list of keywords:{','.join(keywords)}\n"
        f"Consider the paragraph: \"{text}\" \n"
        "Return only a json structure with keywords as keys and the calculated coherence score as values within [-1,0,1]."
    ) #need regular expression to extract python list - lib(pattern)

    output = provider.ask_model(
        query,
        output_format = validate_json_object, output_format_params = {'strict':True},
        response_format = extract_json_object
        )
        # return {
        #     "text": textual_output,
        #     "dict": dict_data,
        #     "err": error_msg
        # }


    # # Initialize the OpenAI API with the provided API key
    # openai.api_key = openai_api_key

    # # Define the prompt for computing coherence score according to COHERENCE_RANGE
    # prompt = (
    #     f"Consider this list of keywords:{','.join(keywords)}\n"
    #     f"Consider the paragraph: \"{text}\" \n"
    #     "Return only a json structure with keywords as keys and the calculated coherence score as values within [-1,0,1]."
    # ) #need regular expression to extract python list - lib(pattern)

    # # Use an appropriate model for text analysis
    # response = openai.ChatCompletion.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": "You are an assistant for analyzing coherence."},
    #         {"role": "user", "content": prompt}
    #     ],

    # )
    # gptOutput = response["choices"][0]["message"]["content"]
    #print(gptOutput)

    #print(output)

    my_dict = output['dict']
    # ex =re.search(r"\{(.*)\}",gptOutput) #change [] to {})
    # if ex:
    #     my_dict=json.loads(ex.group()) #json str for each keyword
    # else:
    #     my_dict=json.loads("{"+gptOutput+"}")
    return my_dict #here we extract a list of json str from response of GPT , [x.strip() for x in my_json]

def validate_json_object(text, params={}):
    #here we validate a list of json str from response of GPT
    bStrict = True #by default
    if 'strict'in params.keys():bStrict = params['strict']

    # JSON objects are enclosed in curly brackets.
    # Regular expression to search for a pattern within a string (GPT output in
    # this case), and specifically to extract text enclosed in curly brackets
    ex = re.search(r"\{(.*)\}",text) 
    
    if ex: return True
    else: return not(bStrict)

def extract_json_object(text, dict={}, err=''):
    #here we extract a list of json str from response of GPT

    # Find JSON object
    ex = re.search(r"\{(.*)\}",text.replace("\n", "")) 

    # here we extract the words from the text to create a list (in the sens of 
    # Python).
    if ex:
        my_dict=json.loads(ex.group()) #json str for each keyword
    else:
        my_dict=json.loads("{"+text+"}")

    # returns a copy of the list by striping each element
    return {'text': my_dict, 'dict': my_dict, 'err':''}




def import_main_execution():
    print('gpt_score2_metric imported')

def run_main_execution():
    # Example usage
    api_key = "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"  # Replace with your actual API key
    sample_text = """
    Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, 
    such as through variations in the solar cycle. But since the 1800s, human activities have been the main driver of 
    climate change, primarily due to burning fossil fuels like coal, oil and gas.
    """  # Replace with your text paragraph
    sample_text2 = """
    Approximately 65% of a garment's climate impact stems from fabric production. With 53 M tons of fibre produced every year and 87% ending in landfills, the fashion industry is polluting and wasting precious resources. Therefore, waste prevention and recapturing value become essential. 
    """
    k = extract_key_terms(sample_text2, 3, api_key)
    print(k)

    #v = score(sample_text, sample_text, api_key)
    #print(v)

# designed to run independently, notice the 'if name == 'main' part here
if __name__ == '__main__': run_main_execution()
else: import_main_execution()
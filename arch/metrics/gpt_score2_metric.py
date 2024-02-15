#to score a piece of text 


#accept a p of text
import openai
import re 

def score(text, ref_text, openai_api_key):#the score is the value you get when apply the metric

    # Use OpenAI to get a response from the model
    # openai.api_key = openai_api_key
    # response = openai.ChatCompletion.create(**prompt)

    #1. extract the keywords from the reference text
    keywords = extract_key_terms(ref_text, 15, openai_api_key)
    print(keywords)
    print(text)
    #2. identify the existence keywords in the text, and how many
    value = sum([re.search(k, text)!=None for k in keywords])

    return value

def dummyFct(text, keywords):
    #2. identify the coherence between keywords and the text
    prompt = f"Be the list of keywords: {keywords}\n" + \
        "Return a response limited to one decimal value from 0 to 10 that represents the coherence score " +\
        f"between the given keywords and the following text:\n{text}"
    # Use an appropriate model for text analysis
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150
    )

    print(response.choices[0])

    # Try to find all possible floats (and, hence, integers) in the response and
    # convert each into a float value
    value = [float(v) for v in re.findall(r'\d+\.?\d*', response.choices[0].text.strip())]
    # Return only the first float (or integrer) found (as a float)
    return value[0]


def extract_key_terms(text, length, openai_api_key):
    """
    This function takes a text paragraph and uses OpenAI's GPT model to extract key terms and concepts.

    Args:
    text (str): The text paragraph to be analyzed.
    openai_api_key (str): The OpenAI API key.
    
    Returns:
    str: The extracted key terms and concepts.
    """
    # Initialize the OpenAI API with the provided API key
    openai.api_key = openai_api_key

    # Define the prompt for extracting key terms and concepts
    prompt = (
        f"Return a list of the {length} most relevant keywords separated by commas " 
        "from the following paragraph:\n"
        f"{text}"
    )

    # Use an appropriate model for text analysis
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150
    )
    
    return [x.strip() for x in response.choices[0].text.split(',')]




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
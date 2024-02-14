#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

import openai
import json
import re  # Importing regular expressions for extracting the rating
#Regular expressions are a powerful tool for processing text. They allow you to specify a pattern of text to search for, which can be used for various tasks such as finding specific strings, validating input formats, replacing parts of a string, splitting strings, and more.

from . import gpt_score_metric, gpt_score2_metric


#reduce dimentionality
def dim_reduction_mean(ratings):
    arr = [x for x in ratings if x >= 0]
    return sum(arr)/len(arr)

def score_clauses(text, params = {}):

    # Check if API keys are provided in the parameters
    bUseOpenAI = 'openai_api_key' in params.keys()
    if bUseOpenAI:
        openai.api_key = params['openai_api_key']
    # ... Same for other type of API


    # Split the text into clauses or sentences
    clauses = text.split(". ")

    # Initialize a list to store scores
    scores = []

    for i, clause in enumerate(clauses):
        ratings = []

        # include all the metrics we want to compute
        # This metric will use OpenAI
        if bUseOpenAI:
            topic = 'a hip-hop artist'
            #ratings.append(gpt_score_metric.score(clause, topic, params['openai_api_key']))

        if bUseOpenAI:
            topic2 = 'a classic composer'
            #ratings.append(gpt_score_metric.score(clause, topic2, params['openai_api_key']))

        if 'ref_text'in params:
            ref_text = params['ref_text']
            v=gpt_score2_metric.score(clause, ref_text, params['openai_api_key']) #putting the score in the vector
            print(v)
            ratings.append(v)
            



        # Store the rating in the dictionary
        scores.append(dim_reduction_mean(ratings)) #diff functions that reduce the dimentionality

    # Return the scores as JSON
    return {'scores':scores, 'texts':clauses} #last steppppp(0130)



def import_main_execution():
    print('score_clauses imported')

def run_main_execution():
    # Example usage:
    text = "Approximately 65% of a garment's climate impact stems from fabric production. With 53 M tons of fibre produced every year and 87% ending in landfills, the fashion industry is polluting and wasting precious resources. Therefore, waste prevention and recapturing value become essential. Our research explores the development of a new circular design strategy (CDS) - Refashion, for service innovation through a design thinking process. Grounded in sustainable design strategies and advanced manufacturing technology, the Refashion CDS aims to enable multiple reutilization of fabric before fibre recycling. This is showcased via a proof-of-concept collection launched on the market in 2022, where three pre-designed multifunctional fabric blocks create 11 different garments, accompanied by a diagram showcasing the product-service system's closed-loop material flow."
    scores = score_clauses(text)
    print(scores)

# designed to run independently, notice the 'if name == 'main' part here
if __name__ == '__main__': run_main_execution()
else: import_main_execution()
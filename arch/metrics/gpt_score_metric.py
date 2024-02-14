#to score a piece of text 

#accept a p of text
import openai
import re 

def score(text, topic, openai_api_key):
    '''
    why write this function(-1)
    '''
    prompt = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please rate the clarity and understandability of the following clause on a scale of 1 to 10 for {topic}: {text}"} #the profile is part of the prompt 'for a hiphop artist'
            ]
        }

    # Use OpenAI to get a response from the model
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(**prompt)

    # Extract the numeric rating from the response using regular expressions
    match = re.search(r'\b\d+(?:\.\d+)?\b', response['choices'][0]['message']['content'])


    if match:
        return float(match.group())/10
    else:
        return -1




def import_main_execution():
    print('gpt_score_metric imported')

def run_main_execution():
    pass

# designed to run independently, notice the 'if name == 'main' part here
if __name__ == '__main__': run_main_execution()
else: import_main_execution()
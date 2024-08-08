from arch import *

import openai
import os

from reader_profile import fetch_abstract



if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)


# Server side
# Define a fetch route and use my_fetch function(defined in the reader_profile.py),to fetch data using personal_id
# @app.route('/fetchGS', methods=['POST'])
# def route_my_fetch():
#     personal_id = request.json.get('personal_id')
#     return fetch_abstract(personal_id)


# Define the route for POST request, this route is to handle the analysis of user input and abstract
# @app.route('/api/coherence-analysis2', methods=['POST'])
# def coherence_analysis2():
#     user_input = request.json.get('txt')
#     abstract = request.json.get('abstract')

#     try:
#         #coherence analysis between the two text
#         prompt = f"You are an assistant for analyzing coherence between user's text:\n\n{user_input}\n\n and the following abstracts: {abstract}. Find a section from the abstracts that matches the user's text."


#         response = openai.ChatCompletion.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are an assistant for analyzing coherence."},
#                 {"role": "user", "content": prompt}
#             ],

#         )

#         # Extract the combined_output and suggestions from the response
#         combined_output = response["choices"][0]["message"]["content"]
#         suggestions = "These are the suggestions." 

#         # Return the results as JSON
#         return jsonify({
#             "combinedOutput": combined_output,
#             "suggestions": suggestions
#         })
#     except Exception as e:
#         print(f"Error calling OpenAI API: {str(e)}")
#         return jsonify({
#             "combinedOutput": "An error occurred while processing the request.",
#             "suggestions": "No suggestions received."
#         })


# @app.route('/get_score', methods=['POST'])
# def get_score():
#     user_input = request.json.get('txt')
#     abstract = request.json.get('abstract')

#     dictScores = metrics.score_clauses(user_input, params={
#         'openai_api_key': openai.api_key,
#         'ref_text': abstract
#     })

#     print(dictScores)

#     return jsonify(dictScores)

@app.route('/test-srv', methods = ['POST', 'GET'])
def my_test_srv():
    selected_test = request.json.get('selected_test')

    if selected_test == 'coherence-analysis2':
        user_input = request.json.get('txt')
        abstract = request.json.get('abstract')

        try:
            #coherence analysis between the two text
            prompt = f"You are an assistant for analyzing coherence between user's text:\n\n{user_input}\n\n and the following abstracts: {abstract}. Find a section from the abstracts that matches the user's text."


            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an assistant for analyzing coherence."},
                    {"role": "user", "content": prompt}
                ],

            )

            # Extract the combined_output and suggestions from the response
            combined_output = response["choices"][0]["message"]["content"]
            suggestions = "These are the suggestions." 

            # create the response
            srv_response = create_response(
                textual_output= combined_output,
                dict_data = { "combinedOutput": combined_output, "suggestions": suggestions }
            )

            # Return the results as JSON
            return jsonify(srv_response)
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return jsonify(create_response(
                textual_output= '',
                dict_data= {
                "combinedOutput": "An error occurred while processing the request.",
                "suggestions": "No suggestions received."
                },
                error_msg= 'An error occurred while processing the request.'
            ))
    elif selected_test == 'fetchGS':
        personal_id = request.json.get('personal_id')
        # return a pre-formatted response
        return create_response( textual_output= fetch_abstract(personal_id) ) 
    elif selected_test == 'get_score':
        user_input = request.json.get('txt')
        abstract = request.json.get('abstract')

        dictScores = metrics.score_clauses(user_input, params={
            'openai_api_key': openai.api_key,
            'ref_text': abstract
        })

        print(dictScores)

        return jsonify(create_response(
            textual_output= dictScores,
            data= dictScores
        ))
           
    else:
        # return an error message
        return jsonify({"err":'ERROR! [TODO: write a more detailed message]'})
    
@app.route('/demo-srv', methods = ['POST']) #to test one function or another: 1)check which demo we want to ask 2)check the parameter according to the functions 3) prepare the prompts 4)send the prompt 5) return the responses
def my_demo_srv(): #new form with text area be selected_demo
    #check which demo we selected
    selected_demo = request.json.get('selected_demo')
    param1 = request.json.get('param1') #input
    param2 = request.json.get('param2') #nb_of_words



    response = ''
    if selected_demo == 'generate paragraph':
        #generateParagraph
        prompt = f"give me a paragraph in {param2} words, which relates to {param1}"
        output = ask_GPT(prompt)
        
        return output

    elif selected_demo == 'extract keywords':
        #extractKeywords
        # build the prompt
        prompt = f"Consider this paragraph: \"{param1}\" \nAbstract {param2} concepts that relate to the main subject of this paragraph. Return only a list of keywords separated by commas."
        output = ask_GPT(prompt)

        return output
        
    elif selected_demo == 'ask measure':
        #ask GPT to measure
        param3 = request.json.get('param3') #input
        metric = request.json.get('metric') #coherence score
        scale = request.json.get('scale') #scale

        # build the prompt
        prompt = f"Consider this list of keywords:{param1}\n Consider the paragraph:{param3}\n Return only a json structure with keywords as keys and the calculated {metric} as values within {scale}."
        output = ask_GPT(prompt)

        return output

    elif selected_demo == "validate response": #create new demo
        param3 = request.json.get('param3') #input

        # build the prompt
        prompt = f"How each keyword of the following list is coherent to computer science: {param1}.\n Return only a list of numbers in a range from 1 to 10 separated by commas."
        output = ask_GPT(prompt,
                output_format = SupportedOutputFormats.List_of_numbers_in_range,
                output_format_params = {
                    'aRange': [1,2,3, 4, 5, 6, 7, 8, 9, 10], 
                    'fctToNumber': int
                })

        return output

    else:
        #raise error
        response = '3'

    return jsonify(response)

def my_own_oFormat(text, params={}):
    return False



@app.route('/labeling-srv', methods = ['POST']) 
def create_labels(): #the protocol - a series of steps
    # 0. Retrieve the values sent to the server
    inputText = request.json.get('txt')
    personalIDs = (request.json.get('ids')).split(',')

    # 1. Retrieve the profiles
    profiles = fetch_profiles(personalIDs)

    # 2. Process the text
    # Nothing to do
    
    # 3. Ask measures
    js_scores = metrics.score_clauses(inputText, params={ #access through package metrics, score_clauses is a function
        'ref_text': " ".join(profiles), #we have the retrieved profile as parameter, now we join the list of abstract as profiles
        'openai_api_key': openai.api_key
    })

    # 4. Return the scores computed for the input text
    return jsonify(js_scores)



def ask_GPT(prompt,
    output_format = None, output_format_params = {},
    response_format = None,
    prompting_limit = 3,
    system_role = "You are an assistant for analyzing coherence.",
    model="gpt-4o-mini"):
    """
    ask_GPT sends a prompt to ChaGPT via OpenAI API

    This function sends a prompt to ChatGPT, using OpenAI API. Then it 
    validates the GPT output, and returns the formatted response.

    By default, the system role is 'analyzing coherence', which relates to the
    main goal of this system: analyzing the coherence between user inputs and 
    selected reader profiles.

    As this function uses OpenAI API to communicate with ChatGPT, the prompt and
    responses should follow the specific documentation(https://platform.openai.com/docs/api-reference/messages/createMessage).

    By nature the GPT doesn't return deterministic responses (in terms of 
    format and content, for example). For this reason, this function operates 
    a validation step to ensure that GPT ouput respects any format asked in the
    prompt.
    
    Finally, it returns a formatted response that the system could rely on (in 
    terms of format).
    """
    try:
        v = False
        limit = prompting_limit
        while (not v) and (limit>-1): #continue to ask gpt
            # Send the prompt to ChatGPT 
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}
                ],
            )

            # Extract the combined output from the response according to the 
            # OpenAI API documentation
            gptOutput = response["choices"][0]["message"]["content"]

            # Validate the output
            if output_format:
                v = validate(gptOutput, output_format, params=output_format_params)
            else:
                v = True
            # Decrement the limit
            limit -= 1

        # Return the response as JSON
        return jsonify(create_response(
            textual_output=gptOutput, 
            response_format=response_format
        ))
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return jsonify(create_response(
            textual_output="An error occurred while processing the request.",
            error_msg="Error calling OpenAI API",
            response_format=response_format))




def create_response(
    textual_output = '', dict_data = {}, error_msg = '',
    response_format = None):
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

def import_main_execution():
    print('app_server imported')

def run_main_execution():
    app.run(debug=True)

# designed to run independently, notice the 'if name == 'main' part here
if __name__ == '__main__': run_main_execution()
else: import_main_execution()

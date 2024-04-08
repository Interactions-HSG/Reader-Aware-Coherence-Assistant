from arch import *

import openai
import os

from reader_profile import fetch_abstract



if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)


# Server side
# Define a fetch route and use my_fetch function(defined in the reader_profile.py),to fetch data using personal_id
@app.route('/fetchGS', methods=['POST'])
def route_my_fetch():
    personal_id = request.json.get('personal_id')
    return fetch_abstract(personal_id)


# Define the route for POST request, this route is to handle the analysis of user input and abstract
@app.route('/api/coherence-analysis2', methods=['POST'])
def coherence_analysis2():
    user_input = request.json.get('txt')
    abstract = request.json.get('abstract')

    try:
        #coherence analysis between the two text
        prompt = f"You are an assistant for analyzing coherence between user's text:\n\n{user_input}\n\n and the following abstracts: {abstract}. Find a section from the abstracts that matches the user's text."


        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant for analyzing coherence."},
                {"role": "user", "content": prompt}
            ],

        )

        # Extract the combined_output and suggestions from the response
        combined_output = response["choices"][0]["message"]["content"]
        suggestions = "These are the suggestions." 

        # Return the results as JSON
        return jsonify({
            "combinedOutput": combined_output,
            "suggestions": suggestions
        })
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return jsonify({
            "combinedOutput": "An error occurred while processing the request.",
            "suggestions": "No suggestions received."
        })


@app.route('/get_score', methods=['POST'])
def get_score():
    user_input = request.json.get('txt')
    abstract = request.json.get('abstract')

    dictScores = metrics.score_clauses(user_input, params={
        'openai_api_key': openai.api_key,
        'ref_text': abstract
    })

    print(dictScores)

    return jsonify(dictScores)

@app.route('/demo-srv', methods = ['POST']) #to test one function or another: 1)check which demo we want to ask 2)check the parameter according to the functions 3) prepare the prompts 4)send the prompt 5) return the responses
def my_demo_srv(): #new form with text area be selected_demo
    #check which demo we selected
    selected_demo = request.json.get('selected_demo')
    param1 = request.json.get('param1') #input
    param2 = request.json.get('param2') #nb_of_words



    response = ''
    if selected_demo == 'generate paragraph':
        #generateParagraph

        # 3. Build the prompt and send it
        try:
            # build the prompt
            prompt = f"give me a paragraph in {param2} words, which relates to {param1}"
            # send the prompt to ChatGPT
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant for analyzing coherence."},
                    {"role": "user", "content": prompt}
                ],

            )

            # Extract the combined output and suggestions from the response
            gptOutput = response["choices"][0]["message"]["content"]

            # Return the results as JSON
            return jsonify({
                "gptOutput": gptOutput
            })
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return jsonify({
                "gptOutput": "An error occurred while processing the request.",
                "errOutput": "Error calling OpenAI API"
            })
    elif selected_demo == 'extract keywords':
        #extractKeywords

        # build the prompt
        prompt = f"Consider this paragraph: \"{param1}\" \nAbstract {param2} concepts that relate to the main subject of this paragraph. Return only a list of keywords separated by commas."
        output = ask_GPT(prompt)

        return output
        
        # # 3. Build the prompt and send it
        # try:
        #     # build the prompt
        #     prompt = f"Consider this paragraph: \"{param1}\" \nAbstract {param2} concepts that relate to the main subject of this paragraph. Return only a list of keywords separated by commas."
        #     print(prompt)
        #     # send the prompt to ChatGPT
        #     response = openai.ChatCompletion.create(
        #         model="gpt-3.5-turbo",
        #         messages=[
        #             {"role": "system", "content": "You are an assistant for analyzing coherence."},
        #             {"role": "user", "content": prompt}
        #         ],

        #     )

        #     # Extract the combined output and suggestions from the response
        #     gptOutput = response["choices"][0]["message"]["content"]

        #     # Return the results as JSON
        #     return jsonify({
        #         "gptOutput": gptOutput
        #     })
        # except Exception as e:
        #     print(f"Error calling OpenAI API: {str(e)}")
        #     return jsonify({
        #         "gptOutput": "An error occurred while processing the request.",
        #         "errOutput": "Error calling OpenAI API"
        #     })

    elif selected_demo == 'ask measure':
        #ask GPT to measure
        param3 = request.json.get('param3') #input
        metric = request.json.get('metric') #coherence score
        scale = request.json.get('scale') #scale

        # build the prompt
        prompt = f"Consider this list of keywords:{param1}\n Consider the paragraph:{param3}\n Return only a json structure with keywords as keys and the calculated {metric} as values within {scale}."
        output = ask_GPT(prompt)

        return output

        # # 3. Build the prompt and send it
        # try:
        #     # build the prompt
        #     prompt = f"Consider this list of keywords:{param1}\n Consider the paragraph:{param3}\n Return only a json structure with keywords as keys and the calculated {metric} as values within {scale}."
        #     print(prompt)
        #     # send the prompt to ChatGPT
        #     response = openai.ChatCompletion.create(
        #         model="gpt-3.5-turbo",
        #         messages=[
        #             {"role": "system", "content": "You are an assistant for analyzing coherence."},
        #             {"role": "user", "content": prompt}
        #         ],

        #     )

        #     # Extract the combined output and suggestions from the response
        #     gptOutput = response["choices"][0]["message"]["content"]

        #     # Return the results as JSON
        #     return jsonify({
        #         "gptOutput": gptOutput
        #     })
        # except Exception as e:
        #     print(f"Error calling OpenAI API: {str(e)}")
        #     return jsonify({
        #         "gptOutput": "An error occurred while processing the request.",
        #         "errOutput": "Error calling OpenAI API"
        #     })
    elif selected_demo == "validate response": #create new demo
        param3 = request.json.get('param3') #input

        # build the prompt
        prompt = f"How each keyword of the following list is coherent to computer science: {param1}.\n Return only a list of numbers in a range from 1 to 10 separated by commas."
        output = ask_GPT(prompt,
                output_format = 'list_of_numbers_in_range', output_format_params = {
                    'aRange': [1,2,3, 4, 5, 6, 7, 8, 9, 10], 
                    'fctToNumber': int
                })

        return output

        # try:
        #     # build the prompt
        #     prompt = f"How each keyword of the following list is coherent to computer science: {param1}.\n Return only a list of numbers in a range from 1 to 10 separated by commas."
        #     # send the prompt to ChatGPT
        #     v = False
        #     limit = 3
        #     while (not v) and (limit>-1): #continue to ask gpt
        #         response = openai.ChatCompletion.create(
        #             model="gpt-3.5-turbo",
        #             messages=[
        #                 {"role": "system", "content": "You are an assistant for analyzing coherence."},
        #                 {"role": "user", "content": prompt}
        #             ],

        #         )

        #         # Extract the combined output and suggestions from the response
        #         gptOutput = response["choices"][0]["message"]["content"]
        #         # Check the validation of the response
        #         # print(gptOutput)
        #         v = validate(gptOutput,output_format='list_of_numbers_in_range', params={
        #             'aRange': [1,2,3, 4, 5, 6, 7, 8, 9, 10], 
        #             'fctToNumber': int
        #         })
        #         limit -= 1
            
        #     # print(limit+1) 
        #     if limit == -1:
        #         raise Exception("Reach the limit of prompting, fail to find validated result")
        #     # Return the results as JSON
        #     return jsonify({
        #         "gptOutput": gptOutput,
        #         "valid":limit>-1 #we select the strict validate
        #     })
        # except Exception as e:
        #     print(f"Error calling OpenAI API: {str(e)}")
        #     return jsonify({
        #         "gptOutput": "An error occurred while processing the request.",
        #         "errOutput": "Error calling OpenAI API"
        #     })

    else:
        #raise error
        response = '3'

    return jsonify(response)





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
    prompting_limit = 3,
    system_role = "You are an assistant for analyzing coherence.",
    model="gpt-3.5-turbo"):
    try:
        v = False
        limit = prompting_limit
        while (not v) and (limit>-1): #continue to ask gpt
            # send the prompt to ChatGPT 
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}
                ],

            )

            # Extract the combined output and suggestions from the response
            gptOutput = response["choices"][0]["message"]["content"]

            # Validate the output
            if output_format:
                v = validate(gptOutput, output_format, params=output_format_params)
            else:
                v = True
            # Decrement the limit
            limit -= 1

        # Return the results as JSON
        return jsonify({
            "gptOutput": gptOutput
        })
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return jsonify({
            "gptOutput": "An error occurred while processing the request.",
            "errOutput": "Error calling OpenAI API"
        })


def import_main_execution():
    print('app_server imported')

def run_main_execution():
    app.run(debug=True)

# designed to run independently, notice the 'if name == 'main' part here
if __name__ == '__main__': run_main_execution()
else: import_main_execution()

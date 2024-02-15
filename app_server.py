from arch import *

import openai
import json
import os

from reader_profile import my_fetch



if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)



# Configure your OpenAI API key

api_key = json.load(open('config.json'))["CHATGPT_API_KEY"]  # Replace with your actual API key
openai.api_key = api_key



# Server side
# Define a fetch route and use my_fetch function(defined in the reader_profile.py),to fetch data using personal_id
@app.route('/fetchGS', methods=['POST'])
def route_my_fetch():
    personal_id = request.json.get('personal_id')
    return my_fetch(personal_id)


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
    param1 = request.json.get('param1')
    param2 = request.json.get('param2')


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

        # 3. Build the prompt and send it
        try:
            # build the prompt
            prompt = f"Consider this paragraph: \"{param1}\" \nAbstract {param2} concepts that relate to the main subject of this paragraph. Return only a list of keywords separated by commas."
            print(prompt)
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


    else:
        #raise error
        response = '3'

    return jsonify(response)



def import_main_execution():
    print('app_server imported')

def run_main_execution():
    app.run(debug=True)

# designed to run independently, notice the 'if name == 'main' part here
if __name__ == '__main__': run_main_execution()
else: import_main_execution()

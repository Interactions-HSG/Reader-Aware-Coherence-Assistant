#server script
#configure the server-side code to handle the /api/coherence-analysis endpoint
#this file handles the http requests and responses for your web app
from arch import *

import openai
import os

from reader_profile import my_fetch


if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)


# Configure your OpenAI API key
api_key = "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"  # Replace with your actual API key
openai.api_key = api_key


# Server side
# Define a fetch route and use my_fetch function(defined in the reader_profile.py),to fetch data using personal_id
@app.route('/fetchGS', methods=['POST'])
def route_my_fetch():
    personal_id = request.json.get('personal_id')
    return my_fetch(personal_id)


'''@app.route('/api/coherence-analysis', methods=['POST'])
def coherence_analysis():
    user_input = request.json.get('txt')
    #combine the profiles,write the prompt(s)
    selected_profile = request.json.get('profile')

    try:
        # Construct the prompt based on the selected profile and user input
        if selected_profile == 'Layman':
            prompt = (f"Identify complex terms in this technical text and suggest simpler alternatives for a general audience:\n\n"
          f"{user_input}")

        elif selected_profile == 'Simon':
            prompt = f"You are an assistant for analyzing coherence between user's text:\n\n{user_input}\n\n and {selected_profile}. Find a section that matches the two."
        else:
            # Handle other profiles here if needed
            pass    


    #try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant for analyzing coherence."},
                {"role": "user", "content": prompt}
            ],

        )

        # Extract the combined output and suggestions from the response
        combined_output = response["choices"][0]["message"]["content"]
        suggestions = "These are the suggestions."  # Replace with your own logic

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
        })'''

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

        # Extract the combined output and suggestions from the response
        combined_output = response["choices"][0]["message"]["content"]
        suggestions = "These are the suggestions."  # Replace with your own logic

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

# Serve merged abstracts when Simon profile is selected
'''@app.route('/merged-abstracts/simon', methods=['GET'])
def serve_simon_merged_abstracts():
    # Define the path to the Simon's merged abstracts file
    simon_merged_abstracts_path = os.path.join(merged_abstracts_dir, 'simon_abstracts.txt')
    
    return send_from_directory(merged_abstracts_dir, 'simon_abstracts.txt')
'''

def import_main_execution():
    print('app_server imported')

def run_main_execution():
    app.run(debug=True)

# designed to run independently, notice the 'if name == 'main' part here
if __name__ == '__main__': run_main_execution()
else: import_main_execution()
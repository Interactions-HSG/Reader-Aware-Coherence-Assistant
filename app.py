#server script
#configure the server-side code to handle the /api/coherence-analysis endpoint
#this file handles the http requests and responses for your web app

from arch import *

import openai
# Configure your OpenAI API key
OPENAI_API_KEY = ""  # Replace with your actual API key
openai.api_key = OPENAI_API_KEY


import os

import app_server

import app_client






# if this file is run directly(i.e it is the main script), it will start the app and debug
if __name__ == '__main__':
    app.run(debug=True)

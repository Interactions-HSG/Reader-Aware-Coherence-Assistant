#server script
#configure the server-side code to handle the /api/coherence-analysis endpoint
#this file handles the http requests and responses for the web app
from arch import *

import os

from reader_profile import my_fetch



if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)




# Client side, define the route (entry point)
@app.route('/newTest')
def my_newTest():
        return render_template('ui.html')
# Define the route that render HTML template 
@app.route('/newTest2')
def my_newTest2():
        return render_template('ui_2.html')
#create the route for a new form computing the score
@app.route('/newTest3')
def my_newTest3():
        return render_template('ui_3.html')

@app.route('/test', methods=['GET', 'POST'])
def my_test():
    if request.method == 'GET':
        return '''
        <html>
        <head><meta name="Content-Type" value="application/json" /></head>
        <body>
            <form action="/test" method="post" enctype="application/json">
                <input type="text" name="txt" id="txt" />
                <input type="submit" />
            </form>
        </body>
        </html>
        '''
    else:  # The method is POST
        if 'txt' in request.form:
            user_input = request.form['txt']
            selected_profile = request.form['profile']
            url = 'http://localhost:5000/api/coherence-analysis'
            data = {'txt': user_input,'profile':selected_profile}
            response = rq.post(url, json=data)

            return response.json()

    return "Invalid request"

#add a route for testing two functions for demo
@app.route('/demo', methods=['GET', 'POST']) 
def my_demo():
    return render_template('demo.html')


def import_main_execution():
    print('app_client imported')

def run_main_execution():
    app.run(debug=True)

# designed to run independently, notice the 'if name == 'main' part here
if __name__ == '__main__': run_main_execution()
else: import_main_execution()
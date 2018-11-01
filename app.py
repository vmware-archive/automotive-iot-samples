from flask import Flask
from flask_cors import CORS
from flask import request

# Initiating the flask app
app = Flask(__name__)
# CORS wrapper to allow cross domain requests
CORS(app)



@app.route('/post_example', methods=['POST'])
def post_example():
    """
    Sample post request route.
    """
    # data sent through the post request 
    req_data = request.get_json()

    # Getting the value for the message field
    message = req_data["message"]

    # Return message
    return "Someone said: " + str(message) + "\n"



if __name__ == '__main__':
    app.run(debug=True, port=2000) #run app in debug mode on port 2000

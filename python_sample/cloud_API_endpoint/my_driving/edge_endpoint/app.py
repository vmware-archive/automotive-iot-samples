from flask import Flask
from flask_cors import CORS
from flask import request
from flask import json
from db import write_event


# Initiating the flask app
app = Flask(__name__)
# CORS wrapper to allow cross domain requests
CORS(app)



@app.route('/add_event', methods=['POST'])
def add_event():
    """
    Recieve the data to write to the DB
    """
    # data sent through the post request 
    event_data = request.get_json()

    # Write to DB
    write_event(event_data)

    return "Called /post_example \n"





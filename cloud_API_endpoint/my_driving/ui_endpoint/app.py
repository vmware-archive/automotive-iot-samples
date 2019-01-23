from flask import Flask
from flask_cors import CORS
from flask import request
from flask import json
from app.db import write_event, read_last_event, read_events


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


@app.route('/events', methods=['GET'])
def get_events():
    """
    retrieve the last event (max timestamp)
    and returns json containing values.
    """
    # get last event (in terms of timestamp)
    rows = read_events()
    res_data = []
    for row in rows:
        res_data.append({
            "client_side_id": row[0],
            "user": row[1],
            "event_type": row[2],
            "event_timestamp": row[3],
            "gps_coord": row[4]
        })

    response = app.response_class(
		response=json.dumps(res_data),
		status=200,
		mimetype='application/json'
		)
    
    return response




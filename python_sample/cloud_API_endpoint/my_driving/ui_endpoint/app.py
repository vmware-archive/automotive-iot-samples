from flask import Flask
from flask_cors import CORS
from flask import request
from flask import json
from db import read_events


# Initiating the flask app
app = Flask(__name__)
# CORS wrapper to allow cross domain requests
CORS(app)


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
            "event_timestamp": row[2],
            "distance": row[3],
            "fuel": row[4]
        })

    response = app.response_class(
		response=json.dumps(res_data),
		status=200,
		mimetype='application/json'
		)
    
    return response




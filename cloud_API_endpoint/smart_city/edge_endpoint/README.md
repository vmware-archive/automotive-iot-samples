# Smart City Edge API Endpoint

This directory contains the API connected to the edge device. The edge device sends the driving events through post requests to this endpoint. The requests are then stored in the SQLite3 DB in `data/cloud_db.db`.

### Setup the environment

1. Initialise the python virtual environment: (Only if never initialiazed before)

    ```
    python3 -m venv venv
    ```

2. Activate virtual environment:

    ```
    . venv/bin/activate
    ```

3. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

4. Start the endpoint:

    ```
    python -m flask run --host=0.0.0.0 --port=2002
    ```

Note that this command does NOT allow for hot reloading. You will have to restart the server after modifying the app.

Alternatively, you could use docker to run this sepcific service:

1. Build the image:

    ```
    docker build -t smart_city_edge_API .
    ```

2. Start the container:

    ```
    docker run -it --rm -v <absolute/path/to/cloud_db.db>:/cloud_db.db -p 2002:2002 smart_city_edge_API
    ```


### Test the endpoint

1. Once the endpoint is running, you can make a POST request from the command line using `curl`:

    ```
    curl -d '{"event_type": "SPEEDING", "event_timestamp": 1541181513, "gps_coord": "37.7992520359445,-122.41955459117891"}' -H "Content-Type: application/json" -X POST http://localhost:2002/add_event
    ```

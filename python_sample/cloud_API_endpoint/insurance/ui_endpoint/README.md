# Insurance UI REST API

This directory contains the API that serves the events stored in `data/cloud_db.db` to the frontend.

To run this APi endpoint in development mode, follow the instructions bellow:

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
    python -m flask run --host=0.0.0.0 --port=3000
    ```

Alternatively, you could use docker to run this sepcific service:

1. Build the image:

    ```
    docker build -t insurance_UI_API .
    ```

2. Start the container:

    ```
    docker run -it --rm -v <absolute/path/to/cloud_db.db>:/cloud_db.db -p 3000:3000 insurance_UI_API
    ```

Next, you should run the ReactJS frontend to display the data served by this API.
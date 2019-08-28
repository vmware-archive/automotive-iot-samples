# My Driving REST API Endpoint

This directory contains the two endpoints and the User Interface for the My Driving use case of our automotive IoT sample. This directory is contains four subdirectories.

- data

    Contains the SQLite3 database file containing the events produced by the edge device. Note that this directory will be created when the API in `edge_endpoint/` is first started.

- edge_endpoint

    Contains the API connected to the edge device. The edge device sends the driving events through post requests to this endpoint. The requests are then stored in the SQLite3 DB in `data/cloud_db.db`.

- react-ui

    Contains the ReactJS frontend that displays the drive events in a web-based user interface.

- ui_endpoint

    Contains the API that serves the events stored in `data/cloud_db.db` to the frontend.

Each directory contains the information required to run the service for *development* purposes. If you wish to run the three applications all together, we recommend you use the docker-compose file located in the top level directory.
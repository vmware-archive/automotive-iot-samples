# Automotive IoT Sample Cloud Endpoints

## Introduction

This repository contains the cloud endpoints for the Automotive IoT Sample. With this sample, we show case three different possible usecases for an automotive IoT application. The usecases are listed bellow:

**Three Usecases:**

- Insurance

    Simulating an hypothetical evil insurance company that spies on it's client's driving habits.

- My Driving

    A personal record of driving habit and drive logs. A user could review their driving habits and miles driven.

- Smart City

    A hypothetical smart city that wants to track anonimous driving data to understand the state of its roads and congetions.

The purpose of these endpoints is to collect and display data collected by the edge application running an a raspberry PI. Each usecase in this directory contains three different parts.

- `edge_endpoint`

    Contains the API connected to the edge device. The edge device sends the driving events through post requests to this endpoint. The endpoint then stores those events in a SQLite3 database.


- `react-ui`

    Contains the ReactJS frontend that displays the drive events in a web-based user interface.


- `ui_endpoint`

    Contains the API that serves the events stored in the SQLite3 database to the frontend.

## How to run

If you have docker and docker-compose installed on your machine, the following command will run all services at once.

```
docker-compose up -d
```

To stop all services:

```
docker-compose down
```

After all services are started, you can start populating each service's database with test data with a simple curl command. For example, to add a driving event to the each usecase, use the commands bellow.

### Insurance

```
curl -d '{"client_side_id": "abcd1234566", "user": "Someone", "event_type": "SPEEDING", "event_timestamp": 1541181513, "gps_coord": "37.7992520359445,-122.41955459117891"}' -H "Content-Type: application/json" -X POST http://localhost:2000/add_event
```

With test data in the database, you should be able to view the data in the insurance's dashboard. In a browser, open `localhost:4000`. The event should appear in the table.

### My Driving

```
curl -d '{"client_side_id": "abcd1234566", "user": "someone", "event_type": "SPEEDING", "event_timestamp": 1541181513, "gps_coord": "37.7992520359445,-122.41955459117891"}' -H "Content-Type: application/json" -X POST http://localhost:2001/add_event
```

View the dashboard at `localhost:4001`.

### Smart City

```
curl -d '{"event_type": "SPEEDING", "event_timestamp": 1541181513, "gps_coord": "37.7992520359445,-122.41955459117891"}' -H "Content-Type: application/json" -X POST http://localhost:2002/add_event
```

Note that the smart city API does not accept `client_side_id` and `user` since the smart city uses anonimized data.

View the dashboard at `localhost:4002`.

Instruction to run the different services in development mode is in each service's directory.
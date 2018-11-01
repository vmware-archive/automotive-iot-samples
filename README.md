# IoT REST API Endpoint

### Setup the environment

1. Clone repository:
```
git clone https://gitlab.eng.vmware.com/acourouble/IoT_cloud_API_endpoint
```

2. Change directory:
```
cd IoT_cloud_API_endpoint
```

3. Initialise the python virtual environment:
```
python3 -m venv venv
```

4. Activate virtual environment:
```
. venv/bin/activate
```

5. Install dependencies:
```
pip install -r requirements.txt
```

### Start the REST API endpoint

First make sure that your virtusal environment is activated. Your command prompt should start with `(venv)`

1. If the virtual environment is not activated yet, you need to activate it first:
```
. venv/bin/activate
```

2. Now we are ready to start the endpoint:
```
python app.py
```

### Make a POST request

1. Once the endpoint is running, you can make a POST request from the command line using `curl`:
```
curl -d '{"message":"Hello World!"}' -H "Content-Type: application/json" -X POST http://localhost:2000/post_example
```

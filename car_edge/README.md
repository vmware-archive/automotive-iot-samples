# IoT REST API Endpoint

### Setup the environment

1. Clone repository:
```
git clone https://gitlab.eng.vmware.com/mbhandaru/car_edge
```

2. Change directory:
```
cd car_edge
```

3. Python3
3a. If you do not have python3, install it.
    For Mac OSX, installing a package manager such as homebrew (see https://docs.python-guide.org/starting/install3/osx/)
    > brew install python3

4a. Set up python virtual environment:
```
python3 -m venv venv
```

4b. Activate virtual environment:
```
. venv/bin/activate
```

5. Upgrade pip
pip install --upgrade pip

6. Install dependencies:
```
pip install -r requirements.txt
```

7. Follow instructions to run the cloud endpoints
```
git clone https://gitlab.eng.vmware.com/acourouble/IoT_cloud_API_endpoint
```

8. Back to current directory
```
python edge.py
```
9. Last but not least, behavior can be modified by editting the
   config.yaml file and restarting as shown in step 8

10.


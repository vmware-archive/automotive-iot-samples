# IoT REST API Endpoint

### Setup the environment


1. Python3
    If you do not have python3, install it.
    For Mac OSX, installing a package manager such as homebrew (see https://docs.python-guide.org/starting/install3/osx/)

```    
brew install python3
```

2. Set up python virtual environment:

```
python3 -m venv venv
```

3. Activate virtual environment:

```
. venv/bin/activate
```

4. Upgrade pip

```
pip install --upgrade pip
```

5. Install dependencies:

```
pip install -r requirements.txt
```

8. Back to current directory

```
python edge.py
```

9. Last but not least, behavior can be modified by editting the
   config.yaml file and restarting as shown in step 8
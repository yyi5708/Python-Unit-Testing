# SWEN352-Activity-2

The Python code for Activity #2: Unit Testing with Mocking in Python.

## Verify Python Version

The code in this activity has only been verified on Python 3.9.  Use this command to test
which version of Python is running on your machine.

### Windows:
```shell
python --version
```

### MacOS:
```shell
python3 --version
```


## Install Python 3.9

If you have a different version of Python you must install v3.9.

### Windows:
TBD

### MacOS:
```shell
brew install python@3.9
```
This installs an executable called `python3.9`; you will use this for the next step.


## Setup Virtual Environment

This section describes how to setup your Python virtual environment.

### Windows:
```shell
python -m venv venv
```

### MacOS:
```shell
python3.9 -m venv venv
source venv/bin/activate
```
This establishes Path variables that link `python` to the Python 3.9 binary.

## Running the Tests

Run the Python unittest module:

```shell
python -m unittest discover
```

# NFL Events
* Overview
* Repo content
* Setup
* Missing


## Overview:
A function  to return a list of NFL events in JSON dynamical. Collects data from 2 endpoints:
* https://delivery.chalk247.com/scoreboard/NFL/<YYYY-MM-DD>/<YYYY-
MM-DD>.json?api_key=<api_key>
* https://delivery.chalk247.com/team_rankings/NFL.json?api_key=<api_key>

## Repo content:
* main.py: Main python code. 
* env_file: Environment variables. This should moved to a .env file and an api_key added.
* .flake: bypass default flake8 settings. 
* response_sample: json response samples from the above mentioned points.

## Setup:
Clone the repo locally and cd to it. Make sure python 3.9+ is installed.
Then follow these steps:

* Create a virtual environment in the repo:
`$ python3 -m venv venv`

* Activate the venv:
`$ source venv/bin/activate`

* Install python requirements:
`$ pip install -r requirements.txt`

* Move env_file to .env and add api_key there:
`$ mv env_file .env`

* To test the function, run the following: 
```
# start a python shell
$ python
>>> from main import run_main
>>> data = {
...     'league': 'NFL',
...     'start_date': '2021-1-12',
...     'end_date': '2021-1-17'
...     }
>>> 
>>> x = run_main(**data)
>>> x
```

## Missing:
Technically a lot is missing: 
* Exceptions are not handled, they could be handled in the clientsession.
* We should check for status, that we got a 200 status. 
* Add timeout for async calls. 
* Add test cases ( possibly pytest ). 

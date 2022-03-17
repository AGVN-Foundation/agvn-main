# A-GVN | Automated Governing System
![](AGVN_white.svg)

# Backend
This project contains everything in the backend of the A-GVN services, including the web server, databases, logic.

[![.github/workflows/django.yml](https://github.com/COMP3900-9900-Capstone-Project/Backend/actions/workflows/django.yml/badge.svg)](https://github.com/COMP3900-9900-Capstone-Project/Backend/actions/workflows/django.yml)

## Frontend
To access Frontend, go to [Frontend](https://github.com/COMP3900-9900-Capstone-Project/Frontend).

## Pyenv
We use `pyenv` to manage python versions throughout the Backend repo.

[Install dependencies](https://github.com/pyenv/pyenv/wiki)
`sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev`

[Install pyenv](https://github.com/pyenv/pyenv-installer)
`curl https://pyenv.run | bash`

Install Python 3.8
`pyenv install 3.8.5`

Use the command `python` in a directory with `.python_version` like `Backend/webserver'.

## Automatic Installation of Dependencies
Install anaconda and `pip install -r requirements.txt` for all subdirs.

## Pipenv : Manual Installation, If something goes wrong
Run `pipenv install --python 3.8` to install the venv for the this project's environment.

Run `pipenv shell` in /Backend. Will activate the venv.
It is also possible to use the standard `venv` with requirements.txt. 

Run `pipenv lock --requirements > requirements.txt` first then activate `venv` and install requirments manually.

## Microservice Architecture
The main server `/webserver` utilizes other always-on servers such as `gcoin`, `emailserver` and `chatbot` to deliver its complete service.

## To start server
To run main server `/webserver`: `python3 webserver/manage.py runserver`

To run the other servers: `python3 server.py` in each server's repository


## When database is changed or new apps is added
`python3 webserver/manage.py makemigrations`

`python3 webserver/manage.py migrate`

## Testing
Using django-pytest module to integrate pytest with django settings.
Run `pytest` on `/Backend/webserver`.
Note: need to setup postgres database for github actions.

## Docker
A 'hypervirtualization' container. By containerizing the backend, the app be run on any system by simply installing required dependencies on a pseudo OS.

Run docker compose to build the app in the container.
`docker-compose run web`

After building, run:
`docker-compose run web python manage.py migrate` to ensure all models have been migrated.

To start the server:
`docker-compose up`

NOTE: Change 'HOST' in `settings.py` to `db`, change it back if you want to run it locally. Also supports HTTP only.

#### Docker Requirement
Why use docker for a web server?
- don't have to install an entire VM, works on all hosts with Docker capability

## GitHub Actions
Every time you push code to this repository, specific github actions may run.

The .github/workflows contains scripts that ensure any errors in new code show up right away.
If the tests don't completely pass, then do not merge to master.

Only when there is a green tick, should you merge request to master.

## Chatbot
When using chatbot on a non-cuda compatible machine, be sure to install the cpu only version of pytorch with `conda install pytorch torchvision torchaudio cpuonly -c pytorch`.


## A-GVN :: Policies
A-GVN can introduce new policies based on the current initiative and recent sentiment.

## A-GVN :: Departments
Each department is attached to one or more policy types. A-GVN assumes that departments in the future will be run autonomously.


## A-GVN :: Actions
A-GVN can take direct actions when faced with relevant events.
These include:
- An environmental disaster
- International disaster
- Lower level political disaster -> act to change lower level constitution
- Higher level -> changes to its own code

For the backend, A-GVN simply sends a 'blog post' about its action, given an 'action prompt' completed by GPT-2. This is rendered on the frontend.

#### Action Prompts
- Environment: river flooding, coastal flooding, coastal erosion, storms, cyclone, drought, earthquake, tornado, plague, coral bleaching, oil/toxic resource spill, acid rain, high particulate air
- International: trade war, foreign incursion, citizen hostage, diplomatic emergency, war, international law violation, international crime
- Physical: terrorist activity, massacre, hostage situation
- Epidemology: disease breakout, pandemic
- Industry: nuclear meltdown, factory disaster
- Political: mass revolt, mass riots, party overthrow


#### GPT-2
Generative Pretrained Transformer 2 is a transformer model by OpenAI.
Requirements:
Transformers and Pytorch CPU.

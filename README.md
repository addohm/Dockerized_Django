# Dockerized_Django

Why?  Containerized Django is hard, frusterating, and makes you want to just go the easy route and start a VM.  If you're running docker, or even researching containerization, you're probably already starting to understand the benefits of containerization.  This project was born out of curiosity for me, to see if I could successfully create a single stack that could successfully host a django project from both development and production environments. 

This stack utilizes a postgres backend and an nginx front end by utilizing the proxy_pass function.  

## Instructions

### Development:
`python -m venv env`
`source env/bin/activate`
`pip install --upgrade pip`
`pip install -r requirements.txt`
Edit the `.env.example` file and replace all the fields as appropriate
Save as `.env`
Edit the `docker-compose.yaml` if you chose to define the project name, and apply the project name there as well as the container names  You will aos need to change the `project` directory name to whatever you decided your project name will be.
Save it as is.

### Deployment:



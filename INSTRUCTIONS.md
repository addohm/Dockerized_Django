## Instructions
The steps listed below in Local Development can all be done as-is after cloning this repository and you will be greeted with a very basic `Hello world!" html response. It is not required but we all like to make sure things work before we do work, right?

### Local Development:
* `python -m venv env`
* `source env/bin/activate`
* `pip install --upgrade pip`
* `pip install -r requirements.txt`
* Edit the `.env.example` file and replace all the fields as appropriate
* Save as `.env`
* `python manage.py migrate`
* `python manage.py createsuperuser`
* `python manage.py runserver 8001 --settings=project.settings.development`
* Visit http://0.0.0.0:8001/ in your browser to verify its running

Following this, must first develop your project locally as you normally would.  Use this file structure as a base.  Feel free to do the standard things expected and get your project in a state which you're ready to test and troubleshoot it in a containerized state.  This project comes with the base django project and an initial app to get you started.  Adding further apps is all still very standard.  

This package comes with a few other things I like to use in Django projects like `gunicorn`, `python-decouple`, `django-debug-toolbar` & `django-jazzmin`. Feel free to add to the package requirements, just don't foret to update the requirements.txt.  

If you need to add environment variables, add to the `.env` file and retrieve any variables using `python-decouple` or other means.  This will still use `sqlite3` as a development database which will be cleaned up later with provided scripts.  

From here forward we will be working more closely with environment variables.  To name some key ones we use during development - `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_USERNAME` & `DJANGO_SUPERUSER_PASSWORD`.

### Containerized Development:
NOTE: When developing in the continerized state, the project will start to use the postgres server.

* Edit the `docker-compose.yaml` if you chose to define the project name, and apply the project name there as well as the container names.  Leave the `project` folder name as is.  There will be instructions on how to modify that later.
* Save it as is.
* `docker-compose --file=docker-compose.yaml up`
* Visit http://0.0.0.0:8001/ in your browser to verify its running



### Deployment:



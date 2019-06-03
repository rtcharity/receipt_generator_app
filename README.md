## Local installation

```
git clone https://github.com/david-mears/rc4-mock-up
cd rc4-mock-up
python -m venv path/to/new/virtual/environment
pip install -r requirements.txt
```
Check that the virtual environment is using python 3.6 or higher.
Set the environment variables (SECRET_KEY)

## To run tests and see test coverage

Make sure your virtual environment is activated, then:
```
python manage.py test
```

To run a specific test file:
```
python manage.py test functional_tests.test_create_donation
```

...where 'test_create_donation.py' is the filename.

You may need to install geckodriver to use tests on Firefox.

As of 29th May 2019 a lot of tests produce a ConnectionAbortedError as a result of a Python bug which will be fixed in 3.7.4 (scheduled June 24).
https://github.com/python/cpython/pull/9713

Occasionally the part of the test which manually creates a new charity has a Server Error for no reason I can discern. Re-running the test often 'fixes' this.

## Local database setup with sqlite3

projectname/settings.py will detect whether you are local or on Azure hosting so that there is no need to manually specify a new database configuration for local development.

Make sure your virtual environment is activated, then:
```
python manage.py migrate
```

This migrate command creates an empty database.

If admin site css is missing, `python3.6 manage.py collectstatic`

## Run local server

Make sure your virtual environment is activated, then:
```
python manage.py runserver
```
(Add `8080` to command if using Amazon Web Services IDE.)

You may need to add the host url to ALLOWED_HOSTS in settings.py if not using localhost.

## To enable the admin side of the site

`cd` to rc4-mockup/projectname
```
python manage.py createsuperuser
```

Define the required details for the admin account. Anyone who can edit the source code of the website and deploy can create an admin account in this way.

## Hosting on Azure

Environment variables you will need to set:

- SENDGRID_API_KEY
(from https://app.sendgrid.com/settings/api_keys which is protected by log in details)
- SECRET_KEY (specific to each Django project)
- DATABASE_NAME e.g. testdb
- DATABASE_USER e.g. manager@your-database-server
- DATABASE_PASSWORD e.g. supersecretpassword
- DATABASE_HOST  e.g. your-database-server.postgres.database.azure.com

Azure should set this automatically:
- WEBSITE_SITE_NAME

These resources may be useful:
https://docs.microsoft.com/en-us/azure/app-service/containers/tutorial-python-postgresql-app
https://docs.microsoft.com/en-us/azure/app-service/containers/quickstart-docker-go

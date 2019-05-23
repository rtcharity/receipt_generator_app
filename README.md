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
cd rc4-mockup/projectname
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
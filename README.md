## Local installation

```
git init
git pull https://github.com/david-mears/rc4-mock-up
cd projectname/
pip install -r requirements.txt
python3.6 manage.py migrate
```

Migrate creates empty database.

If admin site css is missing, `python3.6 manage.py collectstatic`

## Run local server

`cd` to rc4-mockup/projectname
```
python3.6 manage.py runserver
```
Add `8080` to command if using AWS.

You may need to add the host url to ALLOWED_HOSTS in settings.py.

## To enable the admin side of the site

`cd` to rc4-mockup/projectname
```
python3.6 manage.py createsuperuser
```

Define the required details for the admin account. Anyone who can edit the source code of the website and deploy can create an admin account in this way.
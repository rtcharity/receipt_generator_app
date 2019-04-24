## Local installation

```
git init
git pull https://github.com/david-mears/rc4-mock-up
virtualenv ./elasticb-virt
source ./elasticb-virt/bin/activate
cd projectname/
pip install -r requirements.txt
```

## Run local server

`cd` to rc4-mockup/projectname
```
python3.6 manage.py runserver
```
Add `8080` to command if using AWS.

## To enable the admin side of the site

`cd` to rc4-mockup/projectname
```
python3.6 manage.py createsuperuser
```

Define the required details for the admin account. Anyone who can edit the source code of the website and deploy can create an admin account in this way.

Admin app (url: /admin) is where you can add new charities (e.g. RC Forward) or update their details (e.g. signature). Receipt Generator app (url: /) is where you go to create receipts.
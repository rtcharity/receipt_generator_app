## To use the admin side of the site

```
python3.6 manage.py createsuperuser
```

Define the required details for the admin account. Warning: anyone who can edit
the source code of the website can create an admin account in this way.

Admin app (url: /admin) is where you can add new charities (e.g. RC Forward)
or update their details (e.g. signature). Receipt Generator app (url: none yet)
is where you go to create receipts. The admin app currently only interfaces with
charities (can't view donors etc).
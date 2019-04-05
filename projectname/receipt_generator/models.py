from django.db import models

class Donor(models.Model):
    first_name = models.CharField(max_length=50)
    middle_initials = models.CharField(max_length=10)
    last_name = models.CharField(max_length=50)
    address = models.TextField

class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    date_received = models.DateField("The date the gift was received")
    amount = models.DecimalField(
        "The amount received",
        max_digits=6,
        decimal_places=2
        )
    currency = models.CharField(
        "Currency abbreviation (e.g. USD/CAD)",
        max_length=3
        )

# The charity which receives the gift first (i.e. not the destination charity.)
# In the first iteration of this web app, the charity will
# always be RC Forward.
class Charity(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField
    logo = models.FileField(upload_to='logos')
    signature = models.FileField(upload_to='signatures')
    
    

from django.db import models

class Donor(models.Model):
    first_name = models.CharField(max_length=50)
    middle_initials = models.CharField(max_length=10)
    last_name = models.CharField(max_length=50)
    address = models.TextField(
        default='')
    email = models.EmailField(
        "Email address to receive tax receipts.",
        default='',
        unique=True
        )
        
    def __str__(self):
        return '%s %s %s' % (self.first_name, self.middle_initials, self.last_name)

# The charity which receives the gift first (i.e. not the destination charity.)
# In the first release of this web app, the charity will
# always be RC Forward.
class Charity(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField
    logo = models.FileField(upload_to='logos')
    signature = models.FileField(upload_to='signatures')
    registration = models.CharField(
        "IRS/CRA registration number",
        max_length=100
        )
    email = models.EmailField(
        "Email address to receive copies of tax receipts.",
        default=''
        )
        
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = 'Charities'

class Donation(models.Model):
    charity = models.ForeignKey(
        Charity, on_delete=models.CASCADE,
        default=1)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    date_received = models.DateField("The date the gift was received")
    amount = models.DecimalField(
        "The amount received",
        max_digits=14,
        decimal_places=2
        )
    currency = models.CharField(
        "Currency abbreviation (e.g. USD/CAD)",
        max_length=3
        )

# This class exists in order to maintain unique receipt ids for each time
# the user generates a receipt, and to associate receipts with donors/donations.
class Receipt(models.Model):
    STORAGE_DIR_NAME = 'receipts'
    
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    receipt_pdf = models.FileField(upload_to=STORAGE_DIR_NAME)
    
    

from django.db import models

class Donor(models.Model):
    first_name = models.CharField(max_length=50)
    middle_initials = models.CharField(
        max_length=10,
        blank=True,
        default=''
        )
    last_name = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    email = models.EmailField(
        "Email address to receive tax receipts.",
        unique=True,
        )
        
    def __str__(self):
        if self.middle_initials:
            return '%s %s %s' % (self.first_name, self.middle_initials, self.last_name)
        else:
            return '%s %s' % (self.first_name, self.last_name)

# The charity which receives the gift first (i.e. not the destination charity.)
# In the first release of this web app, the charity will
# always be RC Forward.
class Charity(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    logo = models.FileField(upload_to='logos')
    signature = models.FileField(upload_to='signatures')
    registration = models.CharField(
        "IRS/CRA registration number",
        max_length=100
        )
    email = models.EmailField(
        "Email address to receive copies of tax receipts.",
        )
    revenue_agency = models.CharField(
        "Revenue agency, e.g. IRS or CRA",
        max_length=3,
        )
    earmark_options = models.TextField(
        "Earmarking options (separated by a new line)",
        blank=True,
        )
        
    def __str__(self):
        return self.name
        
    def list_earmark_options(self, text):
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            cleaned_lines.append(line.replace('\r', ''))
        return cleaned_lines
        
    class Meta:
        verbose_name_plural = 'Charities'

class Donation(models.Model):
    charity = models.ForeignKey(
        Charity, on_delete=models.CASCADE,
        )
    donor = models.ForeignKey(
        Donor, on_delete=models.CASCADE,
        )
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
    earmark = models.CharField(
            "Earmarked for (can be blank)",
            blank=True,
            max_length = 50,
        )
        
    def __str__(self):
        return 'donation on %s by %s' % (self.date_received, self.donor)


# This class exists in order to maintain unique receipt ids for each time
# the user generates a receipt, and to associate receipts with donors/donations.
class Receipt(models.Model):
    STORAGE_DIR_NAME = 'receipts'
    
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    receipt_pdf = models.FileField(upload_to=STORAGE_DIR_NAME)
    
    def __str__(self):
        return 'Receipt for %s' % (self.donation)

    
    

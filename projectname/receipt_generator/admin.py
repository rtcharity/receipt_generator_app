from django.contrib import admin

from .models import Donation, Donor, Charity, Receipt

admin.site.register(Donation)
admin.site.register(Donor)
admin.site.register(Charity)
admin.site.register(Receipt)
from flatpickr import DatePickerInput
from django import forms
from django.shortcuts import get_object_or_404

from .models import Donor, Charity, Donation

class DonorForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First Name",
        })
    )
    middle_initials = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Middle Initials"
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Last Name"
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Address"
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email"
        })
    )
    
    def process(self, pk=False):
        data = self.cleaned_data
        if pk:
            donor = get_object_or_404(Donor, pk=pk)
            donor.first_name = data['first_name']
            donor.middle_initials = data['middle_initials']
            donor.last_name = data['last_name']
            donor.address = data['address']
            donor.email = data['email']
            donor.save()
        else:
            donor = Donor(
                first_name = data['first_name'],
                middle_initials = data['middle_initials'],
                last_name = data['last_name'],
                address = data['address'],
                email = data['email'],
            )
            donor.save()
        return donor

class DonationForm(forms.Form):
    CHARITY_CHOICES = []
    for charity in Charity.objects.all():
        CHARITY_CHOICES.append((charity.id, charity))
    charity = forms.ChoiceField(
        widget=forms.Select(attrs={
            "class": "form-control",
        }),
        choices=CHARITY_CHOICES,
    )
    DONOR_CHOICES = []
    for donor in Donor.objects.all():
        DONOR_CHOICES.append((donor.id, donor))
    donor = forms.ChoiceField(
        widget=forms.Select(attrs={
            "class": "form-control",
        }),
        choices=DONOR_CHOICES,
    )
    date_received = forms.DateField(
        widget=DatePickerInput(attrs={
            "class": "form-control",
        })
    )
    amount = forms.DecimalField(
        # max_length=14,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
        })
    )
    CURRENCY_CHOICES = [('CAD', 'CAD'), ('USD', 'USD')]
    currency = forms.ChoiceField(
        widget=forms.Select(attrs={
            "class": "form-control",
        }),
        choices=CURRENCY_CHOICES
    )
    
    def process(self, pk=False):
        data = self.cleaned_data
        if pk:
            donation = get_object_or_404(Donation, pk=pk)
            donation.charity = Charity.objects.get(pk=data['charity'])
            donation.donor = Donor.objects.get(pk=data['donor'])
            donation.date_received = data['date_received']
            donation.amount = data['amount']
            donation.currency = data['currency']
            donation.save()
        else:
            donation = Donation(
                charity = Charity.objects.get(pk=data['charity']),
                donor = Donor.objects.get(pk=data['donor']),
                date_received = data['date_received'],
                amount = data['amount'],
                currency = data['currency'],
            )
            donation.save()
        return donation
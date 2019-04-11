from flatpickr import DatePickerInput
from django import forms

from .models import Donor

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
    
class DonationForm(forms.Form):
    all_donors = Donor.objects.all()
    DONOR_CHOICES = []
    for donor in all_donors:
        DONOR_CHOICES.append((donor.id, donor))
    donor = forms.ChoiceField(
        widget=forms.Select(attrs={
            "class": "form-control",
        }),
        choices=DONOR_CHOICES
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
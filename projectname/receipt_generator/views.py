from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views import generic
from django.forms.models import model_to_dict

from .forms import DonorForm, DonationForm
from .models import Donor, Donation, Receipt, Charity

def receipt_generator_index(request):
    context = {
        'welcome_message': 'Hello Swirled!'
    }
    return render(request, 'receipt_generator/index.html', context)
    
def add_donor(request):
    if request.method == 'GET':
        context = {
            'form': DonorForm()
        }
        return render(request, 'receipt_generator/add_donor.html', context)
    elif request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            new_donor = Donor(
                first_name = request.POST['first_name'],
                middle_initials = request.POST['middle_initials'],
                last_name = request.POST['last_name'],
                address = request.POST['address'],
                email = request.POST['email'],
            )
            try:
                new_donor.save()
            except Exception as e:
                return render(request, 'receipt_generator/add_donor.html', {
                    'error_message': e.__cause__,
                    'form': form
                })
            else:
                return render(request, 'receipt_generator/list_donors.html', {
                    'success_message': "Successfully saved new donor!",
                    'donors': get_list_or_404(Donor),
                })
        else:
            return render(request, 'receipt_generator/add_donor.html', {
                    'error_message': "Invalid form",
                    'form': form
                })

def edit_donor(request, pk):
    if request.method == 'GET':
        donor = get_object_or_404(Donor, pk=pk)
        context = {
            'form': DonorForm(model_to_dict(donor)),
            'donor': donor
        }
        return render(request, 'receipt_generator/edit_donor.html', context)
    elif request.method == 'POST':
        donor = get_object_or_404(Donor, pk=pk)
        form = DonorForm(request.POST)
        if form.is_valid():
            donor.first_name = request.POST['first_name']
            donor.middle_initials = request.POST['middle_initials']
            donor.last_name = request.POST['last_name']
            donor.address = request.POST['address']
            donor.email = request.POST['email']
            try:
                donor.save()
            except Exception as e:
                return render(request, ('receipt_generator/edit_donor.html'), {
                    'error_message': e.__cause__,
                    'form': form,
                    'donor': donor,
                })
            else:
                return render(request, 'receipt_generator/view_donor.html', {
                    'success_message': "Successfully saved new donor information!",
                    'form': DonorForm(model_to_dict(donor)),
                    'donor': donor,
                })
        else:
            return render(request, 'receipt_generator/edit_donor.html', {
                    'error_message': "Invalid form",
                    'form': form,
                    'donor': donor,
                })

def add_donation(request):
    if request.method == 'GET':
        context = {
            'form': DonationForm()
        }
        return render(request, 'receipt_generator/add_donation.html', context)
    elif request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            new_donation = Donation(
                charity = Charity.objects.get(pk=request.POST['charity']),
                donor = Donor.objects.get(pk=request.POST['donor']),
                date_received = request.POST['date_received'],
                amount = request.POST['amount'],
                currency = request.POST['currency'],
            )
            try:
                new_donation.save()
            except Exception as e:
                return render(request, 'receipt_generator/add_donation.html', {
                    'error_message': e.__cause__,
                    'form': form
                })
            else:
                return render(request, 'receipt_generator/edit_donation.html', {
                    'success_message': "Successfully saved new donation!",
                    'form': DonationForm(model_to_dict(new_donation)),
                    'donation': new_donation,
                })
        else:
            return render(request, 'receipt_generator/add_donation.html', {
                    'error_message': "Invalid form",
                    'form': form
                })
 
def edit_donation(request, pk):
    if request.method == 'GET':
        donation = get_object_or_404(Donation, pk=pk)
        context = {
            'form': DonationForm(model_to_dict(donation)),
            'donation': donation
        }
        return render(request, 'receipt_generator/edit_donation.html', context)
    elif request.method == 'POST':
        donation = get_object_or_404(Donation, pk=pk)
        form = DonationForm(request.POST)
        if form.is_valid():
            donation.charity = Charity.objects.get(pk=request.POST['charity'])
            donation.donor = Donor.objects.get(pk=request.POST['donor'])
            donation.date_received = request.POST['date_received']
            donation.amount = request.POST['amount']
            donation.currency = request.POST['currency']
            try:
                donation.save()
            except Exception as e:
                return render(request, ('receipt_generator/edit_donation.html'), {
                    'error_message': e.__cause__,
                    'form': form,
                    'donation': donation,
                })
            else:
                return render(request, 'receipt_generator/edit_donation.html', {
                    'success_message': "Successfully saved new donation information!",
                    'form': DonationForm(model_to_dict(donation)),
                    'donation': donation,
                })
        else:
            return render(request, 'receipt_generator/edit_donation.html', {
                    'error_message': "Invalid form",
                    'form': form,
                    'donation': donation,
                })
    
def view_receipt(request, pk):
    context = {
        'receipt': get_object_or_404(Receipt, pk=pk)
    }
    return render(request, 'receipt_generator/view_receipt.html', context)
    
def list_donors(request):
    context = {
        'donors': get_list_or_404(Donor)
    }
    return render(request, 'receipt_generator/list_donors.html', context)

def view_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    context = {
        'donor': donor,
        'form': DonorForm(model_to_dict(donor)),
        'donations': Donation.objects
            .filter(donor=donor.id)
            .order_by('-date_received')
    }
    return render(request, 'receipt_generator/view_donor.html', context)



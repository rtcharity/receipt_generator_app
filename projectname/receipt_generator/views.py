from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.forms.models import model_to_dict

from .services import CreateReceipt
from .forms import DonorForm, DonationForm
from .models import Donor, Donation, Receipt, Charity

def receipt_generator_index(request):
    context = {}
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
            try:
                new_donor = form.process()
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
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'GET':
        context = {
            'form': DonorForm(model_to_dict(donor)),
            'donor': donor
        }
        return render(request, 'receipt_generator/edit_donor.html', context)
    elif request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            try:
                donor = form.process(pk)
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
            # try:
            new_donation = form.process()
            # except Exception as e:
            #     return render(request, 'receipt_generator/add_donation.html', {
            #         'error_message': e.__cause__,
            #         'form': form
            #     })
            # else:
            return render(request, 'receipt_generator/view_donation.html', {
                'success_message': "Successfully saved new donation information!",
                'donation': new_donation,
                'form': DonationForm(model_to_dict(new_donation))
            })
        else:
            return render(request, 'receipt_generator/add_donation.html', {
                    'error_message': "Invalid form",
                    'form': form
                })
 
def edit_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    if request.method == 'GET':
        context = {
            'form': DonationForm(model_to_dict(donation)),
            'donation': donation
        }
        return render(request, 'receipt_generator/edit_donation.html', context)
    elif request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            try:
                donation = form.process(pk)
            except Exception as e:
                return render(request, ('receipt_generator/edit_donation.html'), {
                    'error_message': e.__cause__,
                    'form': form,
                    'donation': donation,
                })
            else:
                return render(request, 'receipt_generator/view_donation.html', {
                    'success_message': "Successfully saved new donation information!",
                    'donation': donation,
                    'form': DonationForm(model_to_dict(donation))
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

def view_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    context = {
        'donation': donation,
        'form': DonationForm(model_to_dict(donation))
    }
    return render(request, 'receipt_generator/view_donation.html', context)

def add_receipt(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    donation_form = DonationForm(model_to_dict(donation))
    # try:
    receipt = CreateReceipt.execute({
        'donation_pk': pk
    })
    # except Exception as e:
    #     return render(request, ('receipt_generator/add_donation.html'), {
    #                 'error_message': 'Something went wrong!',
    #                 'donation_form': donation_form,
    #             })
    context = {
        'success_message': 'Receipt generated and sent successfully',
        'donation': donation,
        'donation_form': donation_form,
        'receipt': receipt
    }
    return render(request, 'receipt_generator/add_receipt.html', context)
    
     # TODO:
     # Check that they are not reloading the page and
     # accidentally emailing people.
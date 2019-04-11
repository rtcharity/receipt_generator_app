from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from .forms import DonorForm
from django.views import generic
from django.forms.models import model_to_dict

from .models import Donor, Donation, Receipt

def receipt_generator_index(request):
    context = {
        'welcome_message': 'Hello World!'
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
            print(request.POST)
            try:
                new_donor = Donor(
                    first_name = request.POST['first_name'],
                    middle_initials = request.POST['middle_initials'],
                    last_name = request.POST['last_name'],
                    address = request.POST['address'],
                    email = request.POST['email'],
                )
            except KeyError:
                return render(request, 'receipt_generator/add_donor.html', {
                    'error_message': "Error message.",
                    'form': form
                })
            else:
                new_donor.save()
                return HttpResponseRedirect(reverse('receipt_generator:list_donors'))
        else:
            return render(request, 'receipt_generator/add_donor.html', {
                    'error_message': "Error message.",
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
            try:
                donor.first_name = request.POST['first_name']
                donor.middle_initials = request.POST['middle_initials']
                donor.last_name = request.POST['last_name']
                donor.address = request.POST['address']
                donor.email = request.POST['email']
            except KeyError:
                return render(request, 'receipt_generator/edit_donor.html', {
                    'error_message': "Error message.",
                    'form': form,
                    'donor': donor,
                })
            else:
                donor.save()
                return render(request, 'receipt_generator/edit_donor.html', {
                    'error_message': "Error message.",
                    'form': form,
                    'donor': donor,
                })
        else:
            return render(request, 'receipt_generator/edit_donor.html', {
                    'error_message': "Error message.",
                    'form': form,
                    'donor': donor,
                })

def add_donation(request):
    context = {}
    return render(request, 'receipt_generator/add_donation.html', context)

def edit_donation(request, pk):
    context = {
        'donation': get_object_or_404(Donation, pk=pk)
    }
    return render(request, 'receipt_generator/edit_donation.html', context)
    
def receipt_view(request, pk):
    context = {
        'receipt': get_object_or_404(Receipt, pk=pk)
    }
    return render(request, 'receipt_generator/receipt_view.html', context)
    
def list_donors(request):
    context = {
        'donors': get_list_or_404(Donor)
    }
    return render(request, 'receipt_generator/list_donors.html', context)
    


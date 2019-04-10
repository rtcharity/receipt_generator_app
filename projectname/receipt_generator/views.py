from django.http import Http404
from django.shortcuts import render
from .models import Donor, Donation, Receipt

def receipt_generator_index(request):
    context = {
        'welcome_message': 'Hello World!'
    }
    return render(request, 'receipt_generator/index.html', context)
    
def add_donor(request):
    context = {}
    return render(request, 'receipt_generator/add_donor.html', context)

def edit_donor(request, pk):
    try:
        donor = Donor.objects.get(pk=pk)
    except Donor.DoesNotExist:
        raise Http404("Donor does not exist")
    context = {
        'donor': donor
    }
    return render(request, 'receipt_generator/edit_donor.html', context)
    
def add_donation(request):
    context = {}
    return render(request, 'receipt_generator/add_donation.html', context)

def edit_donation(request, pk):
    try:
        donation = Donation.objects.get(pk=pk)
    except Donation.DoesNotExist:
        raise Http404("Donation does not exist")
    context = {
        'donation': donation
    }
    return render(request, 'receipt_generator/edit_donation.html', context)
    
def view_receipt(request, pk):
    try:
        receipt = Receipt.objects.get(pk=pk)
    except Receipt.DoesNotExist:
        raise Http404("Receipt does not exist")
    context = {
        'receipt': receipt
    }
    return render(request, 'receipt_generator/view_receipt.html', context)
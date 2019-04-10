from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
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
    context = {
        'donor': get_object_or_404(Donor, pk=pk)
    }
    return render(request, 'receipt_generator/edit_donor.html', context)
    
def add_donation(request):
    context = {}
    return render(request, 'receipt_generator/add_donation.html', context)

def edit_donation(request, pk):
    context = {
        'donation': get_object_or_404(Donation, pk=pk)
    }
    return render(request, 'receipt_generator/edit_donation.html', context)
    
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
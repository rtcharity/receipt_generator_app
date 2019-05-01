from django.utils import timezone
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

from .services import CreateReceipt
from .forms import DonorForm, DonationForm, CharityChoiceForm, DonorChoiceForm
from .models import Donor, Donation, Receipt, Charity

@login_required
def receipt_generator_index(request):
    context = {}
    return render(request, 'receipt_generator/index.html', context)

@login_required
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
                    'error_message': 'Something went wrong! %s' % e.__cause__,
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

@login_required
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
                    'error_message': 'Something went wrong! %s' % e.__cause__,
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

@login_required
def add_donation(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/choose_charity')
    elif request.method == 'POST':
        charity = get_object_or_404(Charity, pk=request.POST['charity'])
        form = DonationForm(charity, request.POST)
        if form.is_valid():
            try:
                new_donation = form.process()
            except Exception as e:
                 return render(request, 'receipt_generator/add_donation.html', {
                     'error_message': 'Something went wrong! %s' % e.__cause__,
                     'form': form
                 })
            else:
                return render(request, 'receipt_generator/view_donation.html', {
                    'success_message': "Successfully saved new donation information!",
                    'donation': new_donation,
                    'donations': [new_donation]
                })
        else:
            return render(request, 'receipt_generator/add_donation.html', {
                    'error_message': "Invalid form",
                    'form': form
                })

@login_required 
def edit_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    if request.method == 'GET':
        context = {
            'form': DonationForm(donation.charity, model_to_dict(donation)),
            'donation': donation
        }
        return render(request, 'receipt_generator/edit_donation.html', context)
    elif request.method == 'POST':
        form = DonationForm(donation.charity, request.POST)
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
                    'form': DonationForm(donation.charity, model_to_dict(donation))
                })
        else:
            return render(request, 'receipt_generator/edit_donation.html', {
                    'error_message': "Invalid form",
                    'form': form,
                    'donation': donation,
                })

@login_required    
def view_receipt(request, pk):
    context = {
        'receipt': get_object_or_404(Receipt, pk=pk)
    }
    return render(request, 'receipt_generator/view_receipt.html', context)
    
@login_required
def list_donors(request):
    if request.method == 'GET':
        order_by = request.GET.get('order_by', 'last_name')
        donors = Donor.objects.all().order_by(order_by)
        if request.GET.get('sort') == 'descend':
            donors = donors.reverse()
        context = {
            'donors': donors,
            'form': DonorChoiceForm(),
        }
        return render(request, 'receipt_generator/list_donors.html', context)
    elif request.method == 'POST':
        return HttpResponseRedirect('/donor/%s' % request.POST['donor'])

@login_required
def view_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    donations = Donation.objects.filter(donor=donor.id).order_by('-date_received')
    last_year = timezone.now().year - 1
    context = {
        'donor': donor,
        'form': DonorForm(model_to_dict(donor)),
        'donations': donations,
        'last_year': last_year,
        'annual_donations': donations.filter(date_received__year=last_year)
    }
    return render(request, 'receipt_generator/view_donor.html', context)

@login_required
def view_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    context = {
        'donations': [donation],
        'donation': donation,
    }
    return render(request, 'receipt_generator/view_donation.html', context)

@login_required
def add_receipt(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    donation_form = DonationForm(donation.charity, model_to_dict(donation))
    
    try:
        receipt = CreateReceipt.execute({
            'donation_pk': pk
        })
    except Exception as e:
        return render(request, ('receipt_generator/add_donation.html'), {
            'error_message': 'Something went wrong!',
            'donation_form': donation_form,
        })
    else:
        context = {
            'success_message': 'Receipt generated and sent successfully',
            'donation': donation,
            'donation_form': donation_form,
            'receipt': receipt
        }
        return render(request, 'receipt_generator/add_receipt.html', context)
        
@login_required
def choose_charity(request):
    if request.method == 'GET':
        context = {
            'form': CharityChoiceForm()
        }
        return render(request, 'receipt_generator/choose_charity.html', context)
    elif request.method == 'POST':
        form = CharityChoiceForm(request.POST)
        if form.is_valid():
            try:
                charity = get_object_or_404(Charity, pk=request.POST['charity'])
                form = DonationForm(charity=charity)
                context = {
                    'form': form
                    }
                return render(request, 'receipt_generator/add_donation.html', context)
            except Exception as e:
                print('ARGH')
                return render(request, ('receipt_generator/choose_charity.html'), {
                    'error_message': e.__cause__,
                    'form': form,
                })
        else:
            return render(request, 'receipt_generator/choose_charity.html', {
                    'error_message': "Invalid form",
                    'form': form,
                })

@login_required
def list_donations(request):
    order_by = request.GET.get('order_by', 'date_received')
    donations = Donation.objects.all().order_by(order_by)
    if request.GET.get('sort') == 'descend':
        donations = donations.reverse()
    context = {
        'donations': donations,
    }
    return render(request, 'receipt_generator/list_donations.html', context)
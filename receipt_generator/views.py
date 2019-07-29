from django.utils import timezone
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.forms.models import model_to_dict
from django.contrib import messages

from .services import CreateReceipt
from .forms import DonorForm, DonationForm, CharityChoiceForm, DonorChoiceForm
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
                messages.error(request, 'Something went wrong! %s' % e.__cause__)
                return render(request, 'receipt_generator/add_donor.html', {
                    'form': form
                })
            else:
                return HttpResponseRedirect('/donor?success=true')
        else:
            messages.error(request, "Invalid form. Error: %s" % form.errors)
            return render(request, 'receipt_generator/add_donor.html', {
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
                messages.error(request, 'Something went wrong! %s' % e.__cause__)
                return render(request, ('receipt_generator/edit_donor.html'), {
                    'form': form,
                    'donor': donor,
                })
            else:
                return HttpResponseRedirect('/donor/%s?new_donor_success=true' % donor.id)
        else:
            messages.error(request, "Invalid form. Error: %s" % form.errors)
            return render(request, 'receipt_generator/edit_donor.html', {
                    'form': form,
                    'donor': donor,
                })

def add_donation(request):
    if request.method == 'GET':
        if request.GET.get('charity'):
            charity = get_object_or_404(Charity, pk=request.GET['charity'])
            context = {
                'form': DonationForm(charity=charity)
            }
            return render(request, 'receipt_generator/add_donation.html', context)
        else:
            return HttpResponseRedirect('/choose_charity')
    elif request.method == 'POST':
        charity = get_object_or_404(Charity, pk=request.POST['charity'])
        form = DonationForm(charity, request.POST)
        if form.is_valid():
            try:
                new_donation = form.process()
            except Exception as e:
                messages.error(request, 'Something went wrong! %s' % e.__cause__)
                return render(request, 'receipt_generator/add_donation.html', {
                    'form': form
                })
            else:
                return HttpResponseRedirect('/donation/%s?new_donation_success=true' % new_donation.id)
        else:
            messages.error(request, "Invalid form. Error: %s" % form.errors)
            return render(request, 'receipt_generator/add_donation.html', {
                'form': form
            })

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
                messages.error(request, 'Something went wrong! %s' % e.__cause__)
                return render(request, ('receipt_generator/edit_donation.html'), {
                    'form': form,
                    'donation': donation,
                })
            else:
                return HttpResponseRedirect('/donation/%s?edit_success=true' % donation.id)
        else:
            messages.error(request, "Invalid form. Error: %s" % form.errors)
            return render(request, 'receipt_generator/edit_donation.html', {
                    'form': form,
                    'donation': donation,
                })
     
def view_receipt(request, pk):
    context = {
        'receipt': get_object_or_404(Receipt, pk=pk)
    }
    return render(request, 'receipt_generator/view_receipt.html', context)
     
def list_donors(request):
    if request.method == 'GET':
        order_by = request.GET.get('order_by', 'last_name')
        donors = Donor.objects.all().order_by(order_by)
        if request.GET.get('sort') == 'descend':
            donors = donors.reverse()
        if request.GET.get('success') and request.GET.get('success') == 'true':
            messages.success(request, "New donor has been successfully saved!")
        context = {
            'donors': donors,
            'form': DonorChoiceForm(),
        }
        return render(request, 'receipt_generator/list_donors.html', context)
    elif request.method == 'POST':
        return HttpResponseRedirect('/donor/%s' % request.POST['donor'])
 
def view_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    donations = Donation.objects.filter(donor=donor.id).order_by('-date_received')
    last_year = timezone.now().year - 1
    annual_donations = donations.filter(date_received__year=last_year)
    totals = {}
    for donation in annual_donations:
        if donation.currency not in totals.keys():
            totals[donation.currency] = 0
        totals[donation.currency] += donation.amount
    total_message = []
    for currency in totals.keys():
        total_message.append('%s - %s' % (currency, totals[currency]))
    if len(annual_donations) == 0:
        total_message.append('No donations for this period.')
    context = {
        'donor': donor,
        'form': DonorForm(model_to_dict(donor)),
        'donations': donations,
        'last_year': last_year,
        'annual_donations': annual_donations,
        'total_message': total_message,
    }
    if request.GET.get('new_donor_success') and request.GET.get('new_donor_success') == 'true':
        messages.success(request, "Successfully saved new donor information!")
    return render(request, 'receipt_generator/view_donor.html', context)
 
def view_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    if request.GET.get('edit_success') and request.GET.get('edit_success') == 'true':
        messages.success(request, "Successfully saved new donation information!")
    if request.GET.get('new_donation_success') and request.GET.get('new_donation_success') == 'true':
        messages.success(request, "Successfully saved new donation information!")
    if request.GET.get('new_receipt_success') and request.GET.get('new_receipt_success') == 'true':
        messages.success(request, "Receipt generated and sent")
    context = {
        'donations': [donation],
        'donation': donation,
    }
    return render(request, 'receipt_generator/view_donation.html', context)

def add_receipt(request, pk):
    if request.method == 'POST':
        donation = get_object_or_404(Donation, pk=pk)
        donation_form = DonationForm(donation.charity, model_to_dict(donation))
        try:
            receipt = CreateReceipt.execute({
                'donation_pk': pk
            })
        except Exception as e:
            messages.error(request, 'Something went wrong! %s' % e.__cause__)
            return render(request, ('receipt_generator/add_donation.html'), {
                'donation_form': donation_form,
            })
        else:
            return HttpResponseRedirect('/donation/%s?new_receipt_success=true' % donation.id)
 
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
                return HttpResponseRedirect('/donation/add?charity=%s' % request.POST['charity'])
            except Exception as e:
                messages.error(request, 'Something went wrong! %s' % e.__cause__)
                return render(request, ('receipt_generator/choose_charity.html'), {
                    'form': form,
                })
        else:
            messages.error(request, "Invalid form. Error: %s" % form.errors)
            return render(request, 'receipt_generator/choose_charity.html', {
                    'form': form,
                })
 
def list_donations(request):
    order_by = request.GET.get('order_by', 'date_received')
    donations = Donation.objects.all().order_by(order_by)
    if request.GET.get('sort') == 'descend':
        donations = donations.reverse()
    context = {
        'donations': donations,
    }
    return render(request, 'receipt_generator/list_donations.html', context)
from django.shortcuts import render

def receipt_generator_index(request):
    context = {
        'welcome_message': 'Hello World!'
    }
    return render(request, 'index.html', context)
    
def add_donor(request):
    context = {}
    return render(request, 'add_donor.html', context)
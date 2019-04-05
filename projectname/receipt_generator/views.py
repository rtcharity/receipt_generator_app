from django.shortcuts import render

def receipt_generator_index(request):
    context = {
        'welcome_message': 'Hello World!'
    }
    return render(request, 'index.html', context)
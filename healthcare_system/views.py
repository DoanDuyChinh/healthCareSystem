from django.shortcuts import render

def csrf_failure(request, reason=""):
    context = {'reason': reason}
    return render(request, '403_csrf.html', context)

def home_view(request):
    """View for the home/introduction page"""
    return render(request, 'home.html')

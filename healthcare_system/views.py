from django.shortcuts import render

def csrf_failure(request, reason=""):
    context = {'reason': reason}
    return render(request, '403_csrf.html', context)

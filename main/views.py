from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    """Home page view"""
    return render(request, 'main/home.html')


@login_required
def profile(request):
    """Account profile view"""
    return render(request, 'main/profile.html')

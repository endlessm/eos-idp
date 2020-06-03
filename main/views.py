from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


@login_required
def home(request):
    """Home page view"""
    return render(request, 'main/home.html')


@login_required
def profile(request):
    """Account profile view"""
    context = {
        'title': _('Profile'),
    }
    return render(request, 'main/profile.html', context=context)

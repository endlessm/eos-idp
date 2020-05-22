from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


@login_required
def index(request):
    """Home page view"""
    context = {
        'title': 'Endless Account',
    }
    return render(request, 'main/index.html', context=context)


class LoginView(auth_views.LoginView):
    template_name = 'main/login.html'

    # For some reason, LoginView doesn't set a title in the context
    extra_context = {
        'title': _('Login'),
    }


class LogoutView(auth_views.LogoutView):
    template_name = 'main/logout.html'

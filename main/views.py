from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import UpdateView

from .forms import ProfileForm


@login_required
def home(request):
    """Home page view"""
    return render(request, 'main/home.html')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Update current user

    Normally django's model views find a model instance from a database
    query using the URL parameters. This overrides get_object() to
    simply always use the currently logged in user.
    """
    def get_object(self, queryset=None):
        return self.request.user


class ProfileView(SuccessMessageMixin, UserUpdateView):
    template_name = 'main/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('main:profile')
    success_message = _('Profile updated')


profile = ProfileView.as_view()

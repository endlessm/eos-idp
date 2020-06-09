from django import forms

from .models import User


class SignupForm(forms.Form):
    """Tweak the field order for the allauth signup form

    If you have email required, then it will be put first in the field
    order, but I think that if username is required, that should go
    first. Not to mention that username is autofocused regardless.
    """
    field_order = [
        'username',
        'email',
        'email2',  # ignored when not present
        'password1',
        'password2'  # ignored when not present
    ]

    def signup(self, request, user):
        pass


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]

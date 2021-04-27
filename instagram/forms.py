from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')




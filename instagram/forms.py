from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Posts


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['picture', 'caption']


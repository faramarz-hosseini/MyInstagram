from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


# Create your views here.
@login_required
def activity_feed(request):
    return render(request, template_name='instagram/activity_feed.html', context={'title': 'Home!'})


class RegisterView(View):
    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data['username']
            messages.success(request, f"An account was successfully created for {user_name}. Log in below.")
            return redirect('login_page')

    def get(self, request):
        form = NewUserForm
        return render(request, template_name='instagram/register.html', context={'register_form': form})

from urllib import request
from django.shortcuts import redirect, render
from .forms import SignupForm
from django.contrib.auth import authenticate,login
from django.urls import reverse


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Use 'password1' here
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/accounts/profile')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})
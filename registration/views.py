from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate

from labs.forms import SignUpForm


def home(request):
    return render(request, 'registration/home.html')


def home_logout(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() # load the profile instance created by the signal

            user.profile.full_name = form.cleaned_data.get('full_name')
            user.profile.department = form.cleaned_data.get('department')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('user_home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

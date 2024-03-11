from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile


def register(request):

    if request.method == "GET":

        form = RegistrationForm()
        return render(request, 'user/registration.html', {'form': form})
    
    elif request.method == "POST":

        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(user=user)
            # user_profile.user_id = user.id
            user_profile.save()
            return redirect('/')
        else:
            error = "You put wrong information. Please try again. DETAILS:"
            return render(request, 'user/registration.html', {'form': form, 'error': error})


def login_user(request):

    if request.method == "GET":

        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    
    elif request.method == "POST":

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')


def redirect_to_login(request):
    """Redirect to the note details view."""
    return redirect(reverse("user:login_user"))
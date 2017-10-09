# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from users import SignUpForm, ProfileForm
from django.urls import reverse
from django.views import generic
from accounts.models import UserProfile
import logging

logger = logging.getLogger(__name__)


def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def success(request):
    return render(request, 'accounts/login_success.html', {})


def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = request.user.userprofile
            profile.university = form.cleaned_data['university']
            profile.location = form.cleaned_data['location']
            profile.save()
            return redirect('success')
    else:
        form = ProfileForm()
    return render(request, 'accounts/profile.html', {'form': form})

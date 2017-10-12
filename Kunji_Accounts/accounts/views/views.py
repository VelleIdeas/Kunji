# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import logging
from accounts.forms.login_form import LoginForm
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib import messages


logger = logging.getLogger(__name__)


def sign_up_view(request):
    return render(request, 'accounts/signup.html', {})


def authenticate_user(request, username, password):
    logger.info('authenticate_user')
    logger.debug("username:" + str(username))
    user = authenticate(username=username, password=password)
    logger.debug('user:' + str(user))
    logger.debug(request.COOKIES.get(getattr(settings, 'SESSION_COOKIE_NAME'), None))
    if user is not None:
        if user.is_active:
            login(request, user)
            logger.debug("User login successful: %s" % username)
            logger.debug(request.session.session_key)
        else:
            logger.info('inactive user')
            return None
    return user


def user_login(request):
    logger.info('login')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        username = request.POST.get('username', None)

        if login_form.is_valid():
            username = request.POST.get('username').strip()
            password = request.POST.get('password')
            user = authenticate_user(
                request,
                username,
                password
            )

            if user:
                return success(request)
            else:
                error_msg = "Your username and/or password do not match."
                logger.debug(error_msg)
                form = login_form
                site = request.POST.get('site', '')
                logger.debug('site:' + str(site))
                target = request.POST.get('target', '')
                logger.debug('target:' + str(target))
                return render(request, 'accounts/login.html', locals())
        else:
            logger.debug('invalid login form')
            form = login_form
            site = request.POST.get('site', '')
            logger.debug('site:' + str(site))
            target = request.POST.get('target', '')
            logger.debug('target:' + str(target))
            return render(request, 'accounts/login.html', locals())
    else:
        logger.info('cookie %s', request.COOKIES)
        site = request.GET.get('site', '')
        user_id = request.session.get('_auth_user_id')
        if not user_id:
            logger.info("Anonymous user")
            logger.debug('site:' + str(site))
            form = LoginForm()
            storage = messages.get_messages(request)
            return render(request, 'accounts/login.html', locals())


def success(request):
    return render(request, 'accounts/login_success.html', {})


@login_required
def create_profile_view(request):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'accounts/profile.html', context)

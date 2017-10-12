from django.conf.urls import url

from api.views.user_register import create_user

urlpatterns = [
    url(r'^createUser/$', create_user),
]
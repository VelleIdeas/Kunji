from django.conf.urls import include, url
from views import create_user


urlpatterns = [
    url(r'^createUser/$', create_user),
]
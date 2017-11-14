from django.conf.urls import url

from api.views.user_register import create_user, create_profile
from accounts.views.views import logout

urlpatterns = [
    url(r'^createUser/$', create_user),
    url(r'^logOut/$', logout),
    url(r'^save_profile/$', create_profile)
]
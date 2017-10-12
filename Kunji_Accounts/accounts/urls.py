from django.conf.urls import url
from accounts.views import views
from accounts.views import *

urlpatterns = [
    url(r'^signup/?$', views.sign_up_view, {}, 'signup'),
    url(r'^login/?$', views.user_login, {}, 'login'),
    url(r'^success/?$', views.success, {}, 'success'),
    url(r'^profile/?$', views.create_profile_view, {}, 'create_profile'),
    url(r'^signup/blank_page/$', blank_page, name='blank_page'),
]

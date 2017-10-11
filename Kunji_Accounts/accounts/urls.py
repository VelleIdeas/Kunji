from django.conf.urls import url
from accounts.views import views

urlpatterns = [
    url(r'^signup/?$', views.sign_up_view, {}, 'signup'),
    url(r'^profile/?$', views.create_profile, {}, 'profile'),
    url(r'^success/?$', views.success, {}, 'success'),
]

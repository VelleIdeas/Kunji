from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^upload-paper/$', views.upload_paper),
    url(r'^get-papers/$', views.get_papers),
]
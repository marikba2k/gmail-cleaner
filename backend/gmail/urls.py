from django.urls import path
from . import views

urlpatterns = [
    path("oauth/start/", views.oauth_start, name="oauth_start"),
    path("oauth/callback/", views.oauth_callback, name="oauth_callback"),
    path("oauth/disconnect/", views.disconnect, name="oauth_disconnect"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("oauth/start/", views.oauth_start, name="oauth_start"),
    path("oauth/callback/", views.oauth_callback, name="oauth_callback"),
    path("oauth/disconnect/", views.disconnect, name="oauth_disconnect"),
    
    path("api/gmail/profile/", views.gmail_profile, name="gmail_profile"),
    path("api/gmail/inbox-sample/", views.inbox_sample, name="inbox_sample"),
    path("api/rules/<int:rule_id>/preview/", views.preview_rule, name="preview_rule"),

]

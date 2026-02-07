import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
import os

from .models import GoogleCredential

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


if os.getenv("DJANGO_DEBUG", "0") == "1":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def _build_flow(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
    )
    flow.redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI
    return flow


@login_required
def oauth_start(request):
    flow = _build_flow(request)

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    request.session["google_oauth_state"] = state
    return redirect(authorization_url)


@login_required
def oauth_callback(request):
    state = request.session.get("google_oauth_state")
    if not state:
        return redirect("/dashboard/")

    flow = _build_flow(request)
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    creds = flow.credentials
    payload = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }

    GoogleCredential.objects.update_or_create(
        user=request.user,
        defaults={"credentials_json": json.dumps(payload)},
    )

    return redirect("/dashboard/")


@login_required
def disconnect(request):
    GoogleCredential.objects.filter(user=request.user).delete()
    return redirect("/dashboard/")

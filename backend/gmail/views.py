import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
import os

from .models import GoogleCredential
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .services import get_gmail_service
from .models import Rule

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

login_required
def gmail_profile(request):
    svc = get_gmail_service(request.user)
    profile = svc.users().getProfile(userId="me").execute()
    return JsonResponse({"emailAddress": profile.get("emailAddress")})

@login_required
def inbox_sample(request):
    svc = get_gmail_service(request.user)

    # Search inbox, newest first
    res = svc.users().messages().list(userId="me", q="in:inbox", maxResults=10).execute()
    msgs = res.get("messages", [])

    items = []
    for m in msgs:
        msg = svc.users().messages().get(
            userId="me",
            id=m["id"],
            format="metadata",
            metadataHeaders=["Subject", "From", "Date"],
        ).execute()

        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        items.append({
            "id": m["id"],
            "from": headers.get("From"),
            "subject": headers.get("Subject"),
            "date": headers.get("Date"),
        })

    return JsonResponse({"count": len(items), "items": items})

@require_GET
@login_required
def preview_rule(request, rule_id):
    rule = Rule.objects.get(id=rule_id, user=request.user)
    svc = get_gmail_service(request.user)

    res = svc.users().messages().list(
        userId="me",
        q=rule.query,
        maxResults=10,
    ).execute()

    msgs = res.get("messages", [])
    total = res.get("resultSizeEstimate", 0)

    return JsonResponse({
        "rule": rule.name,
        "query": rule.query,
        "estimated_matches": total,
        "sample_count": len(msgs),
    })
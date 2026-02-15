import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .models import GoogleCredential

def get_gmail_service(user):
    rec = GoogleCredential.objects.get(user=user)
    data = json.loads(rec.credentials_json)

    creds = Credentials(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        token_uri=data.get("token_uri"),
        client_id=data.get("client_id"),
        client_secret=data.get("client_secret"),
        scopes=data.get("scopes"),
    )

    return build("gmail", "v1", credentials=creds, cache_discovery=False)

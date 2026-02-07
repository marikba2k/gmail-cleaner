from django.shortcuts import render
from gmail.models import GoogleCredential


def home(request):
    return render(request, "home.html")

def dashboard(request):
    connected = False
    if request.user.is_authenticated:
        connected = GoogleCredential.objects.filter(user=request.user).exists()
    return render(request, "dashboard.html", {"connected": connected})
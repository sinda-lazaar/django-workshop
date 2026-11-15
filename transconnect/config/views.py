
from django.shortcuts import render


def index(request):
    return render(request, "home.html")


def homeWithName(request, nom):
    return render(request, "home.html", {"nom": nom})

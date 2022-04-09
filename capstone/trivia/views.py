from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def index(request):
    # Return the front page
    return render(request, "index.html")


def test(request):
    return HttpResponse("fdfdsfsdfsdfsdf")

def register(request):
    if request.method == "GET":
        return render(request, "register.html")

def login(request):
    pass

def logout(request):
    pass
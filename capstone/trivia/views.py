from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.urls import reverse
from .models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    # Return the front page
    return render(request, "index.html")


def test(request):
    return HttpResponse("fdfdsfsdfsdfsdf")

def register(request):
    if request.method == "GET":
        
        return render(request, "register.html")

    if request.method == "POST":

        # Verify Password is above minimum length
        if len(request.POST["pw"]) < 6:
            return render(request, "register.html", {"error": "Password must be at least 6 characters"})

        # Check password matches confirmation
        if request.POST["pw"] != request.POST["pwverify"]:
            return render(request, "register.html", {"error": "Passwords did not match"})
        else:
            password = request.POST["pw"]
            username = request.POST["username"]

        # Check username is unique, and if so create the account, then log in the user
        try: 
            user = User.objects.create_user(username, password)
            user.save()
        except:
            return render(request, "register.html", {"error": "Username already taken"})
        else:
            login(user)
            return HttpResponseRedirect(reverse("index"))


def login(request):
    pass

def logout(request):
    pass
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.urls import reverse
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import requests
from random import seed, random, randrange

# Seed RNG
seed()

# Create your views here.
def index(request):
    # Return the front page
    return render(request, "index.html")

def triviagame(request):
    return render(request, "trivia.html")

@csrf_exempt
@login_required
def createquestions(request):
    if request.method == "POST":

        # Validate json is valid
        # Note - find a better way to write this
        contentcheck = 0
        while contentcheck == 0:
            json = artworkquestion.createquestion()
            contentcheck = artworkquestion.checkvalid(json)

        # Parse question from API response
        question = artworkquestion.format(json)

        url = artworkquestion.createurl(json)

        return JsonResponse(json, safe=False)

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
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

def loginview(request):
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["loginusername"]
        password = request.POST["loginpw"]
        user = authenticate(request, username=username, password=password)      

        # Check if authentication was successful and if so, log in the current user
        if user is not None:
            login(request, login)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

def logoutview(request):
    #Logout the current user
    logout(request)
    return HttpResponseRedirect(reverse("index"))

class artworkquestion:
    
    def createquestion():
        # Select a random number from 0 to 90000 
        artid = randrange(1, 90000)
        # Enter id into api call
        url = "https://api.artic.edu/api/v1/artworks/{0}".format(artid)
        response = requests.get(url)
        json = response.json()
        return json

    def checkvalid(json):
        #Check the returned json is valid and that the year range is a single number (for question purposes)
        try:
            artworkid = (json["data"]["id"])
        except:
            return 0
        else:
            if json["data"]["date_start"] != json["data"]["date_end"]:
                return 0
            else:
                return 1

    def format(json):
        choice = randrange(1, 3)
        if choice == 1:
            question = {
                "artist": json["data"]["artist_title"]
            }
            return question
        if choice == 2:
            question = {
                "country": json["data"]["place_of_origin"]
            }
            return question
        if choice == 3:
            question = {
                "year": json["data"]["date_start"]
            }

    def createurl(json):
        iiif = json["config"]["iiif_url"]
        imageid = json["data"]["image_id"]
        suffix = "/full/300,/0/default.jpg"
        url = "{0}/{1}{2}".format(iiif, imageid, suffix)
        return url

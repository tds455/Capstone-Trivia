from nturl2path import url2pathname
from unicodedata import name
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
from random import seed, random, randrange, randint

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

        # Parse POST data
        data = json.loads(request.body)
        topics = data["topics"]
        totalqs = data["totalqs"]
        totalqs = int(totalqs)

        # Create list of questions, looping for total number of questions 
        # and picking a selected category at random each time

        questions = []

        for x in range(totalqs):
            i = randrange(0, len(topics))
            if topics[i] == "Art":
                contentcheck = 0
                while contentcheck == 0:
                    question = artworkquestion.createquestion()
                    contentcheck = artworkquestion.checkvalid(question)
                question = artworkquestion.format(question, x)
                questions.append(question)

            if topics[i] == "Sports":
                contentcheck = 0
                while contentcheck == 0:
                    question = sportsquestion.createquestion()
                    contentcheck = sportsquestion.checkvalid(question)
                question = sportsquestion.format(question, x)
                
        print(questions)
        return JsonResponse(questions, safe=False)

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

    def format(json, id):
        url = artworkquestion.createurl(json)
        choice = randrange(1, 4)
        if choice == 1:
            question = {
                "number": id,
                "url": url,
                "type": 1,
                "title" : json["data"]["title"],
                "year": json["data"]["date_start"],
                "country": json["data"]["place_of_origin"],
                "question" : "Which artist painted this artwork",
                "answer": json["data"]["artist_title"]
            }
            return question
        if choice == 2:
            question = {
                "number": id,
                "url": url,
                "type": 2,
                "title" : json["data"]["title"],
                "year": json["data"]["date_start"],
                "artist": json["data"]["artist_title"],
                "question": "Which country is this artwork from",
                "answer": json["data"]["place_of_origin"]
            }
            return question
        if choice == 3:
            question = {
                "number": id,
                "url": url,
                "type": 3,
                "title" : json["data"]["title"],
                "country": json["data"]["place_of_origin"],
                "artist": json["data"]["artist_title"],
                "question": "In which year was this artwork painted",
                "answer": json["data"]["date_start"]
            }
            return question

    def createurl(json):
        iiif = json["config"]["iiif_url"]
        imageid = json["data"]["image_id"]
        suffix = "/full/300,/0/default.jpg"
        url = "{0}/{1}{2}".format(iiif, imageid, suffix)
        return url

class sportsquestion:

    def createquestion():
        # Select a random number from 0 to 90000 
        sportid = randrange(1, 1000)
        # Enter id into api call
        url = "https://sports.api.decathlon.com/sports/{0}".format(sportid)
        response = requests.get(url)
        json = response.json()
        return json

    def checkvalid(json):
        try:
            url = json["data"]["attributes"]["icon"]
        except:
            return 0
        else:
            if url == None:
                return 0
            if json["data"]["attributes"]["description"] == None:
                return 0
            else:
                return 1

    def format(json, id):
        choice = randrange(1, 3)
        if choice == 1:
            question = {
                "number": id,
                "url": json["data"]["attributes"]["icon"],
                "type": 1,
                "title" : json["data"]["attributes"]["name"],
                "description" : json["data"]["attributes"]["description"],
                "question" : "What is the name of this sport?",
                "answer": json["data"]["attributes"]["name"]
            }
            print(question)
            return question

        if choice == 2:
            question = {
                "number": id,
                "url": json["data"]["attributes"]["icon"],
                "type": 1,
                "title" : json["data"]["attributes"]["name"],
                "description" : json["data"]["attributes"]["description"],
                "question" : "Based on the description, what is the name of this sport?",
                "answer": json["data"]["attributes"]["name"]
            }
            print(question)
            return question

    
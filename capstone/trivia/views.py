from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.urls import reverse
from .models import User, Userstats, IDcache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import requests
from random import seed, random, randrange, randint, choice

# Seed RNG
seed()

# Views
def profileview(request):
    # Get user profile to access ID
    user = request.user

    # Retrieve user scores and serialise to pass into template
    try:
        query = Userstats.objects.get(userid=user.id)
        userscores = query.serialise()
    except:
        return render(request, "profile.html")
    else:
        if request.method == "GET":

            return render(request, "profile.html", {"userscores": userscores})
        
        if request.method == "POST":

            # Check that the testuser is not logged in

            if user.username == "Testuser":
                return render(request, "profile.html", {"userscores": userscores, "error": "Testuser password cannot be changed"})

            # Take user input, validate, then use it to update password record
            if len(request.POST["pw"]) < 6:
                return render(request, "profile.html", {"userscores": userscores, "error": "Password must be at least 6 characters"})

            # Check password matches confirmation
            if request.POST["pw"] != request.POST["pwverify"]:
                return render(request, "profile.html", {"userscores": userscores, "error": "Passwords did not match"})

            query = User.objects.get(username = user.username)
            query.set_password = request.POST["pw"]
            query.save()
            return render(request, "profile.html", {"userscores": userscores})



    

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
            user = User.objects.create_user(username=username, password=password)
            user.save()

        except:
            return render(request, "register.html", {"error": "Username already taken"})
        else:
            # Log in the user, then create them a stats table
            login(request, user)
            stats = Userstats.objects.create(userid = user.id)
            stats.save()
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
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

def logoutview(request):
    #Logout the current user
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def index(request):
    # Return the front page
    return render(request, "index.html")

def triviagame(request):
    return render(request, "trivia.html")

# API Routes
@csrf_exempt
@login_required
def updatescores(request):
    if request.method == "POST":
        # Retrieve submitted scores
        data = json.loads(request.body)

        # Get user profile to access ID
        user = request.user

        # Access and update user's score recrods 
        query = Userstats.objects.get(userid=user.id)
        query.score += data["score"]
        query.artrating += data["art"]
        query.sportsrating += data["sports"]
        query.worldrating += data["world"]
        query.animalrating += data["animals"]
        query.movierating += data["movies"]
        query.gamesplayed += 1
        query.save()

        # Retrieve updated values in dictionary format and return to user
        userscores = query.serialise()
        return JsonResponse(userscores, safe=False)

    if request.method == "GET":

        # Get user profile to access ID and request score values
        user = request.user
        query = Userstats.objects.get(userid=user.id)

        # Return user's current stats 
        userscores = query.serialise()
        return JsonResponse(userscores, safe=False)

@csrf_exempt
@login_required
def createquestions(request):
    if request.method == "POST":

        # Parse POST data
        data = json.loads(request.body)
        topics = data["topics"]
        totalqs = data["totalqs"]
        fast = data["fast"]
        totalqs = int(totalqs)

        # Create list of questions, looping for total number of questions 
        # and picking a selected category at random each time

        questions = []

        for x in range(totalqs):
            i = randrange(0, len(topics))
            if topics[i] == "Art":
                if fast == 1:
                    question = artworkquestion.createfastquestion()
                else:
                    contentcheck = 0
                    while contentcheck == 0:
                        question = artworkquestion.createquestion()
                        contentcheck = artworkquestion.checkvalid(question)
                question = artworkquestion.format(question, x)
                questions.append(question)

            if topics[i] == "Sports":
                if fast == 1:
                    question = sportsquestion.createfastquestion()
                else:
                    contentcheck = 0
                    while contentcheck == 0:
                        question = sportsquestion.createquestion()
                        contentcheck = sportsquestion.checkvalid(question)
                question = sportsquestion.format(question, x)
                questions.append(question)

            if topics[i] == "World":
                if fast == 1:
                    question = countryquestion.createfastquestion()
                else:
                    contentcheck = 0
                    while contentcheck == 0:
                        question = countryquestion.createquestion()
                        contentcheck = countryquestion.checkvalid(question)
                question = countryquestion.format(question, x)
                questions.append(question)

            if topics[i] == "Animal":
                # zoo-animal-api includes a rand function, no validity checks or random functions are required
                question = animalquestion.createquestion()
                question = animalquestion.format(question, x)
                questions.append(question)

            if topics[i] == "Movie":
                # movie-quote-api includes a rand function, no validity checks or random functions are required
                question = quotequestion.createquestion()
                question = quotequestion.format(question, x)
                questions.append(question)

        print(questions)
        return JsonResponse(questions, safe=False)

    else:
        pass
# Objects

class artworkquestion:
    
    def createquestion():
        # Select a random number from 0 to (max)90000 
        artid = randrange(0, 90000)
        # Enter id into api call
        url = "https://api.artic.edu/api/v1/artworks/{0}".format(artid)
        response = requests.get(url)
        json = response.json()
        return json

    def createfastquestion():
        # Take a random url from the IDCache model
        query = list(IDcache.objects.filter(category = "art"))
        query = choice(query)
        id = query.APIID
        url = "https://api.artic.edu/api/v1/artworks/{0}".format(id)
        response = requests.get(url)
        json = response.json()
        return json

    def checkvalid(json):
        #Check the returned json is valid and that the year range is a single number (for question purposes)
        try:
            datestart = json["data"]["date_start"]
        except:
            return 0
        else:
            if datestart != json["data"]["date_end"]:
                return 0
            else:
                # Cache successful ID
                apiID = json["data"]["id"]
                query = IDcache.objects.get_or_create(APIID=apiID, category="art")
                return 1

    def format(json, id):
        url = artworkquestion.createurl(json)
        choice = randrange(1, 4)
        if choice == 1:
            question = {
                "number": id,
                "url": url,
                "category": "arts",
                "type": 1,
                "title" : json["data"]["title"],
                "year": json["data"]["date_start"],
                "country": json["data"]["place_of_origin"],
                "question" : "Which artist painted this artwork",
                "answer": json["data"]["artist_title"]
            }

        if choice == 2:
            question = {
                "number": id,
                "url": url,
                "category": "arts",
                "type": 2,
                "title" : json["data"]["title"],
                "year": json["data"]["date_start"],
                "artist": json["data"]["artist_title"],
                "question": "Which country is this artwork from",
                "answer": json["data"]["place_of_origin"]
            }

        if choice == 3:
            question = {
                "number": id,
                "url": url,
                "category": "arts",
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
        # Select a random number from 0 to (max)1000  
        sportid = randrange(1, 200)
        # Enter id into api call
        url = "https://sports.api.decathlon.com/sports/{0}".format(sportid)
        response = requests.get(url)
        json = response.json()
        return json

    def createfastquestion():
        # Take a random url from the IDCache model
        query = list(IDcache.objects.filter(category = "sports"))
        query = choice(query)
        id = query.APIID
        url = "https://sports.api.decathlon.com/sports/{0}".format(id)
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
                # Cache successful ID
                apiID = json["data"]["id"]
                query = IDcache.objects.get_or_create(APIID=apiID, category="sports")
                return 1

    def format(json, id):
        choice = randrange(1, 3)

        # Strip any instances of the sport name in the description
        description = str(json["data"]["attributes"]["description"])
        title = str(json["data"]["attributes"]["name"])
        description = description.replace(title, "SPORT")
        description = description.replace(title.lower(), "SPORT")

        if choice == 1:
            question = {
                "number": id,
                "category": "sports",
                "url": json["data"]["attributes"]["icon"],
                "type": 1,
                "title" : title,
                "description" : description,
                "question" : "Based on the picture, what is the name of this sport?",
                "answer": json["data"]["attributes"]["name"]
            }


        if choice == 2:
            question = {
                "number": id,
                "category": "sports",
                "url": json["data"]["attributes"]["icon"],
                "type": 2,
                "title" : title,
                "description" : description,
                "question" : "Based on the description, what is the name of this sport?",
                "answer": json["data"]["attributes"]["name"]
            }

        return question

class countryquestion:
    
    def createquestion():
        # Select a random number from 0 to (max)1000  
        worldid = randrange(1, 1000)
        # Enter id into api call
        url = "https://restcountries.com/v2/callingcode/{0}".format(worldid)
        response = requests.get(url)
        json = response.json()
        return json

    def createfastquestion():
        # Take a random url from the IDCache model
        query = list(IDcache.objects.filter(category = "country"))
        query = choice(query)
        id = query.APIID
        url = "https://restcountries.com/v2/callingcode/{0}".format(id)
        response = requests.get(url)
        json = response.json()
        return json

    def checkvalid(json):
        try:
            url = json[0]["flags"]["png"]
        except:
            return 0
        else:
            if url == None:
                return 0
            else:
                # Cache successful ID
                apiID = json[0]["callingCodes"][0]
                query = IDcache.objects.get_or_create(APIID=apiID, category="country")
                return 1

    def format(json, id):
        choice = randrange(1, 4)

        # Which country in REGION speaks LANGUAGE_CODE
        if choice == 1:
            question = {
                "number": id,
                "category": "world",
                "url": json[0]["flags"]["png"],
                "type": 1,
                "region" : json[0]["region"],
                "question": "Which country speaks this language",
                "language" : json[0]["languages"][0]["name"],
                "answer": json[0]["name"]
            }


        # Which country in REGION uses CURRENCY
        if choice == 2:
            question = {
                "number": id,
                "category": "world",
                "url": json[0]["flags"]["png"],
                "type": 2,
                "region" : json[0]["region"],
                "question": "Which country uses this currency",
                "currency" : json[0]["currencies"][0]["name"],
                "answer": json[0]["name"]
            }



        # Which country in REGION has population of POPULATION?
        if choice == 3:
            question = {
                "number": id,
                "category": "world",
                "url": json[0]["flags"]["png"],
                "type": 3,
                "region" : json[0]["region"],
                "question": "Which country has this population",
                "population" : json[0]["population"],
                "answer": json[0]["name"]
            }

        return question

class animalquestion:

    #zoo-animal-api already has a rand function, so checkvalid and random functions are not required
    def createquestion():
        response = requests.get("https://zoo-animal-api.herokuapp.com/animals/rand")
        json = response.json()
        return json

    def format(json, id):
        choice = randrange(1, 4)

        if choice == 1:
            question = {
                "number": id,
                "category": "animal",
                "url": json["image_link"],
                "type": 1,
                "diet": json["diet"],
                "question": "Which animal matches the above picture and has this diet",
                "answer": json["name"]
            }

        if choice == 2:
            question = {
                "number": id,
                "category": "animal",
                "url": json["image_link"],
                "type": 2,
                "habitat": json["habitat"],
                "question": "Which animal matches the above picture and has this habitat",
                "answer": json["name"]
            }

        if choice == 3:
            question = {
                "number": id,
                "category": "animal",
                "url": json["image_link"],
                "type": 3,
                "location": json["geo_range"],
                "question": "Which animal matches the above picture and lives in ",
                "answer": json["name"]
            }
        
        return question
        
        
class quotequestion:

    #movie-quote-api already has a rand function, so checkvalid and random functions are not required
    def createquestion():
        response = requests.get("https://movie-quote-api.herokuapp.com/v1/quote/?censored")
        json = response.json()
        return json

    def format(json, id):
        choice = randrange(1, 3)

        if choice == 1:
            question = {
                "number": id,
                "category": "quote",
                "type": 1,
                "movie": json["show"],
                "quote": json["quote"],
                "person": json["role"],
                "question": "In which movie was this quote said?",
                "answer": json["show"]
            }

        if choice == 2:
            question = {
                "number": id,
                "category": "quote",
                "type": 2,
                "movie": json["show"],
                "quote": json["quote"],
                "person": json["role"],
                "question": "In this movie, which person said this quote",
                "answer": json["role"]
            }

        return question

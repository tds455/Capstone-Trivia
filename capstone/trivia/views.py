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
def index(request):
    # Return the front page
    return render(request, "index.html")

def triviagame(request):
    # Return /triviagame.
    return render(request, "trivia.html")

def about(request):
    # Return about page
    return render(request, "about.html")

def profileview(request):
    # Return profile view
    # Get user profile to access ID
    user = request.user

    # Retrieve user scores and serialise to pass into template
    try:
        query = Userstats.objects.get(userid=user.id)
        userscores = query.serialise()
    except:
        # Return unathenticated profile page
        return render(request, "profile.html")
    else:
        # Return profile page with user stats
        if request.method == "GET":

            return render(request, "profile.html", {"userscores": userscores})
        
        if request.method == "POST":
            # Update userstats

            # Check that the testuser is not logged in
            # Testuser is the sample account for demo usage.
            # Users should not be able to change it's details

            if user.username == "Testuser":
                return render(request, "profile.html", {"userscores": userscores, "error": "Testuser password cannot be changed"})

            # Take user input, validate, then use it to update password record
            if len(request.POST["pw"]) < 6:
                return render(request, "profile.html", {"userscores": userscores, "error": "Password must be at least 6 characters"})

            # Check password matches confirmation
            if request.POST["pw"] != request.POST["pwverify"]:
                return render(request, "profile.html", {"userscores": userscores, "error": "Passwords did not match"})

            # Update user's password and return profile page
            query = User.objects.get(username = user.username)
            query.set_password = request.POST["pw"]
            query.save()
            return render(request, "profile.html", {"userscores": userscores})


def register(request):
    if request.method == "GET":
        # Return register page

        return render(request, "register.html")

    if request.method == "POST":
        # Process and validate user's input

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
            # Return register page with appropiate error message
            return render(request, "register.html", {"error": "Username already taken"})
        else:
            # Log in the user, then create them a stats table
            login(request, user)
            stats = Userstats.objects.create(userid = user.id)
            stats.save()
            return HttpResponseRedirect(reverse("index"))

def loginview(request):
    if request.method == "GET":
        # Return login page
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
            # Return login page with appropiate error message
            return render(request, "login.html", {"error": "Invalid username or password"})

def logoutview(request):
    #Logout the current user
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# API Routes
@csrf_exempt
@login_required
def updatescores(request):
    if request.method == "PUT":
        # Update user's scores

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
        fast = int(data["fast"])
        totalqs = int(totalqs)

        # Create list of questions, looping for total number of questions 
        # and picking a selected category from user selected topics each time

        questions = []
        # Create list of questions and add each serialised question to the list

        for x in range(totalqs):
            i = randrange(0, len(topics))
            if topics[i] == "Art":
                question = artworkquestion()
                question.createquestion(fast, x)
                question = question.serialise()
                questions.append(question)

            if topics[i] == "Sports":
                question = sportsquestion()
                question.createquestion(fast, x)
                question = question.serialise()
                questions.append(question)

            if topics[i] == "World":
                question = countryquestion()
                question.createquestion(fast, x)
                question = question.serialise()
                questions.append(question)

            if topics[i] == "Animal":
                # zoo-animal-api includes a rand function, no validity checks or random functions are required
                question = animalquestion()
                question.createquestion(x)
                question = question.serialise()
                questions.append(question)

            if topics[i] == "Movie":
                # movie-quote-api includes a rand function, no validity checks or random functions are required
                question = quotequestion()
                question.createquestion(x)
                question = question.serialise()
                questions.append(question)
                
        # Return list of serialised questions 
        return JsonResponse(questions, safe=False)
  
    else:
        pass

    
# Objects

class artworkquestion:

    def __init__(self):
        # Create an empty question
        self.postid = 0
        self.url = ""
        self.category = ""
        self.type = 0
        self.title = ""
        self.year = ""
        self.country = ""
        self.artist = ""
        self.question = ""
        self.answer = ""
    
    def createquestion(self, fast, postid):
        # To enable fastmode and use cached API routes, pass 1 as an argument with createquestion()

        if fast == 1:
            # Take a random url from the IDCache model
            query = list(IDcache.objects.filter(category = "art"))
            query = choice(query)

            # Take ID and add it to API call string
            id = query.APIID
            url = "https://api.artic.edu/api/v1/artworks/{0}".format(id)

            # Parse and return response
            response = requests.get(url)
            json = response.json()

        else:
            contentcheck = 0
            while contentcheck == 0:    
                # Select a random number from 0 to (max)90000 (reasonable upper limit for accessing artic API)
                artid = randrange(0, 90000)

                # Enter id into api call
                url = "https://api.artic.edu/api/v1/artworks/{0}".format(artid)

                # Parse response and validate contents
                response = requests.get(url)
                json = response.json()
                contentcheck = self.checkvalid(json)

        # Format object contents into a question.   
        self.format(json, postid)
            

    def checkvalid(self, json):        
        #Check the returned json is valid and that the year range is a single number (for question purposes)
        try:
            # Check artwork has a date of creation
            datestart = json["data"]["date_start"]
        except:
            return 0
        else:
            # Check artwork has only single date of creation and not a range
            if datestart != json["data"]["date_end"]:
                return 0
            else:
                # Cache successful ID inside IDcache model
                apiID = json["data"]["id"]
                query = IDcache.objects.get_or_create(APIID=apiID, category="art")
                return 1

    def format(self, json, postid):
        # Parse JSON contents and store inside object

        # Construct URL from JSON contents 
        # https://api.artic.edu/docs/#iiif-image-api
        url = self.createurl(json)

        # Randomly select a number to decide question type
        choice = randrange(1, 4)
        if choice == 1:
            self.postid = postid
            self.url = url
            self.category = "arts"
            self.type = 1
            self.title = json["data"]["title"]
            self.year = json["data"]["date_start"]
            self.country = json["data"]["place_of_origin"]
            self.question = "Which artist painted this artwork"
            self.answer = json["data"]["artist_title"]

        if choice == 2:
            self.postid = postid
            self.url = url
            self.category = "arts"
            self.type = 2
            self.title = json["data"]["title"]
            self.year = json["data"]["date_start"]
            self.artist = json["data"]["artist_title"]
            self.question = "Which country is this artwork from"
            self.answer = json["data"]["place_of_origin"]

        if choice == 3:

            self.postid = postid
            self.url = url
            self.category = "arts"
            self.type = 3
            self.title = json["data"]["title"]
            self.country = json["data"]["place_of_origin"]
            self.artist = json["data"]["artist_title"]
            self.question = "In which year was this artwork painted"
            self.answer = json["data"]["date_start"]
            


    def createurl(self, json):
        # https://api.artic.edu/docs/#iiif-image-api
        # Construct URL from JSON details
        iiif = json["config"]["iiif_url"]
        imageid = json["data"]["image_id"]
        suffix = "/full/300,/0/default.jpg"
        url = "{0}/{1}{2}".format(iiif, imageid, suffix)
        return url

    def serialise(self):
        # Take current question object and return a dictionary
        question = {
            "number": self.postid,
            "url": self.url,
            "category": self.category,
            "type": self.type,
            "title": self.title,
            "country": self.country,
            "year": self.year,
            "artist": self.artist,
            "question": self.question,
            "answer": self.answer
        }

        return question


class sportsquestion:

    def __init__(self):
        self.postid = 0
        self.url = ""
        self.category = "sports"
        self.type = 0
        self.title = ""
        self.description = ""
        self.question = ""
        self.answer = ""

    def createquestion(self, fast, postid):
        if fast == 1:
            # Take a random url from the IDCache model
            query = list(IDcache.objects.filter(category = "sports"))
            query = choice(query)
            id = query.APIID
            url = "https://sports.api.decathlon.com/sports/{0}".format(id)
            response = requests.get(url)
            json = response.json()

        else:

            contentcheck = 0
            while contentcheck == 0:
                # Select a random number from 0 to (max)1000  
                sportid = randrange(1, 200)
                # Enter id into api call
                url = "https://sports.api.decathlon.com/sports/{0}".format(sportid)
                response = requests.get(url)
                json = response.json()

                # Validate JSON contents are suitable for formatting into question
                contentcheck = self.checkvalid(json)
        
        self.format(json, postid)

    def checkvalid(self, json):
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

    def format(self, json, postid):
       
        # Strip any instances of the sport name in the description
        description = str(json["data"]["attributes"]["description"])
        title = str(json["data"]["attributes"]["name"])
        description = description.replace(title, "SPORT")
        description = description.replace(title.lower(), "SPORT")

        # Randomly select a question type
        choice = randrange(1, 3)
        if choice == 1:
            self.number = postid,
            self.category = "sports"
            self.url = json["data"]["attributes"]["icon"]
            self.type = 1
            self.title = title,
            self.description = description,
            self.question = "Based on the picture, what is the name of this sport?",
            self.answer = json["data"]["attributes"]["name"]

        if choice == 2:
            self.number = postid,
            self.category = "sports"
            self.url = json["data"]["attributes"]["icon"]
            self.type = 2
            self.title = title,
            self.description = description,
            self.question = "Based on the description, what is the name of this sport?",
            self.answer = json["data"]["attributes"]["name"]
    
    def serialise(self):
        # Take current question object and return a dictionary
        question = {
            "number": self.postid,
            "category": self.category,
            "url": self.url,
            "type": self.type,
            "title" : self.title,
            "description" : self.description,
            "question" : self.question,
            "answer": self.answer
        }

        return question


class countryquestion:

    def __init__(self):
        self.postid = 0
        self.category = "world"
        self.url = ""
        self.type = 0
        self.region = ""
        self.language = ""
        self.currency = ""
        self.population = ""
        self.question = ""
        self.answer = ""

    def createquestion(self, fast, postid):
        if fast == 1:
            # Take a random url from the IDCache model
            query = list(IDcache.objects.filter(category = "country"))
            query = choice(query)
            id = query.APIID
            url = "https://restcountries.com/v2/callingcode/{0}".format(id)
            response = requests.get(url)
            json = response.json()

        else:
            # Validate contents of return to ensure they can be formatted into a question
            contentcheck = 0
            while contentcheck == 0:
                # Select a random number from 0 to (max)1000  
                worldid = randrange(1, 1000)
                # Enter id into api call
                url = "https://restcountries.com/v2/callingcode/{0}".format(worldid)
                response = requests.get(url)
                json = response.json()
                contentcheck = self.checkvalid(json)
        
        self.format(json, postid)


    def checkvalid(self, json):
        try:
            # Check JSON has contains an image URL
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

    def format(self, json, postid):
        # Randomly select a type from 1 to 3
        choice = randrange(1, 4)

        if choice == 1:
            self.postid = postid
            self.url = json[0]["flags"]["png"]
            self.type = 1
            self.region = json[0]["region"]
            self.question = "Which country speaks this language"
            self.answer = json[0]["name"]
            self.language = json[0]["languages"][0]["name"]
            

        # Which country in REGION uses CURRENCY
        if choice == 2:
            self.postid = postid
            self.url = json[0]["flags"]["png"]
            self.type = 2
            self.region = json[0]["region"]
            self.question = "Which country speaks this language"
            self.answer = json[0]["name"]
            self.currency = json[0]["currencies"][0]["name"]
            

        # Which country in REGION has population of POPULATION?
        if choice == 3:
            self.postid = postid
            self.url = json[0]["flags"]["png"]
            self.type = 3
            self.region = json[0]["region"]
            self.question = "Which country speaks this language"
            self.answer = json[0]["name"]
            self.population = json[0]["population"]
            
    def serialise(self):
        # Take current question object and return a dictionary
        question = {
            "number": self.postid,
            "category": self.category,
            "url": self.url,
            "type": self.type,
            "region" : self.region,
            "question": self.question,
            "language" : self.language,
            "currency" : self.currency,
            "population" : self.population,
            "answer": self.answer
            }

        return question

class animalquestion:

    def __init__(self):
        self.postid = 0
        self.url = ""
        self.category = "animal"
        self.type = 0
        self.diet = ""
        self.habitat = ""
        self.location = ""
        self.question = ""
        self.answer = ""

    #zoo-animal-api already has a rand function, so checkvalid and random functions are not required
    def createquestion(self, postid):
        response = requests.get("https://zoo-animal-api.herokuapp.com/animals/rand")
        json = response.json()
        
        self.format(json, postid)

    def format(self, json, postid):
        # Pick a random value and update object values according to appriopiate question type
        choice = randrange(1, 4)

        if choice == 1:
            self.postid = postid
            self.url = json["image_link"]
            self.type = 1
            self.question = "Which animal matches the above picture and has this diet"
            self.answer = json["name"]
            self.diet = json["diet"]

        if choice == 2:
            self.postid = postid
            self.url = json["image_link"]
            self.type = 2
            self.question = "Which animal matches the above picture and has this habitat"
            self.answer = json["name"]
            self.habitat = json["habitat"]
            
        if choice == 3:
            self.postid = postid
            self.url = json["image_link"]
            self.type = 3
            self.question = "Which animal matches the above picture and lives in "
            self.answer = json["name"]
            self.location = json["geo_range"]
            
    def serialise(self):
        # Take current question object and return a dictionary
        question = {
            "number": self.postid,
            "url": self.url,
            "category": self.category,
            "type": self.type,
            "diet": self.diet,
            "habitat": self.habitat,
            "location": self.location,
            "question": self.question,
            "answer": self.answer
        }
        
        return question
        
        
class quotequestion:

    def __init__(self):
        self.postid = 0
        self.category = "quote"
        self.type = 0
        self.movie = ""
        self.quote = ""
        self.person = ""
        self.question = ""
        self.answer = ""

    # movie-quote-api already has a rand function, so checkvalid and random functions are not required
    def createquestion(self, postid):
        response = requests.get("https://movie-quote-api.herokuapp.com/v1/quote/?censored")
        json = response.json()
        
        self.format(json, postid)

    def format(self, json, postid):
        # Take a random value and return one of two questions
        choice = randrange(1, 3)

        if choice == 1:
            self.postid = postid,
            self.type = 1
            self.movie = json["show"]
            self.quote = json["quote"]
            self.person = json["role"]
            self.question = "In which movie was this quote said?"
            self.answer = json["show"]
            
        if choice == 2:
            self.postid = postid,
            self.type = 2
            self.movie = json["show"]
            self.quote = json["quote"]
            self.person = json["role"]
            self.question = "In this movie, which person said this quote"
            self.answer = json["show"]


    def serialise(self):
        # Take current question object and return a dictionary
        question = {
                "number": self.postid,
                "category": self.category,
                "type": self.type,
                "movie": self.movie,
                "quote": self.quote,
                "person": self.person,
                "question": self.question,
                "answer": self.answer,
            }
        
        return question




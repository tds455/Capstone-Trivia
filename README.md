# Trivia
Welcome to Trivia, my CS50W final project.<br>
Trivia is a web application that pulls data from public APIs, parses the responses and formats them into questions.<br>
Trivia uses a combination of a Python backend running Django and a Javascript frontend to create a responsive, reactive website. <br>


## Demo

## Distinctiveness and Complexity

### Technology

Trivia was created to match the specification provided by the [CS50W Capstone project](https://cs50.harvard.edu/web/2020/projects/final/capstone/), utilising Django for the backend and Javascript for the frontend.  <br>
I wanted the website to use a combination of Django views to serve important features (account creation, static pages) while having the actual Trivia app/game be completely responsive, contained within a single .html file. <br>

I seperated my views.py file into three categories

####**Views**
Views provide html templates and values directly from the Django backend.  These are used for the user management views (profile, loginview, logoutview, register), the index page and the about page, which gives a condensed description of the trivia app.<br>
They also handle accessing /triviagame, but all rendering in done inside trivia.html and trivia.js, and no values are passed from Django.<br>
####**API routes**
Two API routes exist - createquestions and updatescores.
createquestions will take a POST request containing the information provided by the triviagame form (topics, total questions, fastmode enable) and return the requested questions in JSON format.<br>
updatescores, upon recieving a GET request, will return the currently logged in user's current score.<br>
A POST request containing the user's updated rating and score changes will update the Userstats object of the currently logged in user.<br>
####**Objects**
There is one object for each question topic, containing two essential functions - createquestion and format. <br>
createquestion will make an API call to the public API associated with that topic and return a JSON. <br>
format will take the contents of the JSON file, parse them and return a dictionary containing a question, answer and all other relevant information.<br>

Some objects contain other functions: checkvalid, createfastquestion and createurl. <br>
checkvalid will check the JSON is suitable for being used as a question, making sure it contains all the information required. <br>
createfastquestion will pull an ID from the IDcache model that has previously been used successfully, to avoid having to make random API calls until a viable response is recieved. <br>
createurl is specific to the artworkquestion object, and constructs an image URL from information provided in the API response. <br>




### Files

### Mobile-responsive

### Caching

### Django models
 
## Design

### Reactive design

### Files



### User information and statistics

## Requirements

## Installation 

# How to run

# Additional Information
# Trivia
Welcome to Trivia, my CS50W final project.<br>
Trivia is a web application that pulls data from public APIs, parses the responses and formats them into questions.<br>
Trivia uses a combination of a Python backend running Django and a Javascript frontend to create a responsive, reactive website. <br>

## Key features

- Object-Oriented Programming
- Reactive design (within /triviagame)
- Django web API
- Use of Django backend to retrieve data from public APIs which then serves content to a Javascript frontend


## Demo

Trivia is available at https://tshaw.me

Note that site may change over time and the trivia app may not always be available.

## Installation and how to run

- Create virtual environment

        virtualenv env

- Install requirements

        pip install -r requirements.txt

- Start Django server

        python manage.py runserver

Note: If hosting a public server or deploying Trivia in a production environment, open 

    capstone/settings.py

And remove the secret key, replacing it with your own

## CS50W - Specification

**Note - the below section is a detailed overview of the capstone project as required by CS50W. **

### Distinctiveness and Complexity

Trivia was created to match the specification provided by the [CS50W Capstone project](https://cs50.harvard.edu/web/2020/projects/final/capstone/), utilising Django for the backend and Javascript for the frontend.  <br>
However, unlike the other CS50W projects, Trivia was an original project with no distribution code or instruction provided.  <br>
I wanted to make use of public APIs and create a website that took the data from multiple APIs, parsed and formatted it then presented to the user.  I decided the best way to do this was to make a quiz or trivia website. <br>


I wanted the website to use a combination of Django views to serve important features (account creation, static pages) while having the actual Trivia app/game be completely reactive, contained within a single .html file. <br>
While accessing /triviagame, no page reloads will be attempted or required, users can access the full functionality and loop through the quiz multiple times while all the data is displayed and controlled from trivia.js

#### Caching and models

Trivia primarily uses Django models to cache valid API route subdirectories. <br>  
While some APIs automatically return a random JSON, others do not, requiring the application to randomly select API routes until it finds a valid one. <br>
On top of this, the Art Institute of Chicago API has tens of thousands of records, many of which are missing information Trivia requires to create questions. <br>
Using the IDCache model, Trivia will reconstruct a valid URL requiring only one request to be made for each question when the fastmode setting is enabled. <br>
When the fastmode setting is disabled, Trivia will store the successful request url subdirectories inside the IDCache model before returning the questions. <br>

Creating IDcache was required due to extensive loading times and risk of throttling from making too many requests to certain APIs.  By implementing the fastmode feature before working on the design elements, which required extensive testing of the application, I was able to build up a large database of valid urls that should prevent questions from being repeated <br>
<br>
Two other models exist - the default User model provided by Django (unmodified), and Userstats, which tracks the user's scores and ratings for each category, as well as the total number of games played.
<br>
A user's score can only increase, while ratings will adjust both positively and negatively after each game. <br>
The user's score will be displayed in the top right corner of the screen while accessing Trivia, while ratings can be found on /profile. <br>
A player's scores and ratings can be accessed from calling /updatescores <br> 

#### Mobile-responsive

In order to make Trivia display responsively based on device screen size, I made use of various parts of the Bootstrap framework.<br>

I decided to display the Trivia questions and results using bootstrap cards, and immediately ran into issues with card-group and card-deck, which while perfect for my needs are not compatible with reactive design, with content being pushed from trivia.js without a page reload required.<br>

I instead used card-columns, intended to be used for cards of various different sizes, but by fixing the card sizes with additional css attributes I was able to cause the cards to display in rows of 3, regardless of device screen size.<br>

I also limited the dimensions of images using max-width and max-height attributes, allowing images to display at their intended aspect ratio without overflowing the div boundaries and causing display issues.<br>

## Files
Please see below for a description of all files I created. <br>

    trivia/views.py

#### views.py
I seperated my views.py file into three categories<br>

##### **Views**
Views provide html templates and values directly from the Django backend.  These are used for the user management pages (profile, loginview, logoutview, register), the index page and the about page, which gives a condensed description of the trivia app.<br>
They also handle accessing /triviagame, but all rendering is done inside trivia.html and trivia.js, and no values are passed from Django.<br>
##### **API routes**
Two API routes exist - createquestions and updatescores.
createquestions will take a POST request containing the information provided by the triviagame form (topics, total questions, fastmode enable) and return the requested questions in JSON format.<br>
updatescores, upon recieving a GET request, will return the currently logged in user's current score.<br>
A PUT request containing the user's updated rating and score changes will update the Userstats object of the currently logged in user.<br>
##### **Objects**
There is one object for each question topic, containing two essential functions - createquestion and format. <br>
createquestion will make an API call to the public API associated with that topic and return a JSON. <br>
format will take the contents of the JSON file, parse them and return a dictionary containing a question, answer and all other relevant information.<br>

Some objects contain other functions: checkvalid, createfastquestion and createurl. <br>
checkvalid will check the JSON is suitable for being used as a question, making sure it contains all the information required. <br>
createfastquestion will pull an ID from the IDcache model that has previously been used successfully, to avoid having to make random API calls until a viable response is recieved. <br>
createurl is specific to the artworkquestion object, and constructs an image URL from information provided in the API response. <br>

    trivia/static/trivia.js

#### trivia.js

Trivia.js serves as Trivia's frontend, containing the following functions

##### defaultview
Called automatically when the DOM has completed loading, defaultview clears all HTML div elements except for #default view, in order to display the form used to set up a new trivia game.

defaultview will also make a GET request to /updatescores, in order to display the user's current total score in the navbar

##### quizview
quizview is called from an eventlistener on the Submit button in the trivia form, and will update views to show a loading screen while the form contents are processed and the backend API is called.
quizview will validate the form contents, returning an error if requirements are not met, before create a FETCH POST request to /createquestions.

quizview will call the appropiate function for each returned question, before appending them to the #quizview element inside trivia.html.

#### checkanswers
checkanswers is called from the submit button inside the quizview element.  It will initialise variables for containing the player's scores, and check the user's submitted answers against those returned from the backend API, which checkanswers takes as it's sole argument.

checkanswers will use .toLowerCase() in it's comparison, to remove case sensitivity from answers.  

After iterating through the provided answers, checkanswers will call displayscores

#### displayscores
displayscores takes as arguments the user's submitted answers, the questions response from /createquestions and the ratings / results arrays created in checkanswers which detail the rating changes and result for each question.

displayscores will then parse this information and create a html element showing the overall results and change, before creating a further element for each question showing the question, provided answer, correct answer and if the user was correct or not.

A PUT request to /updatescores will then be made to update the user's score and ratings on the backend.

#### TOPICquestion
trivia.js contains a function for each topic, that will parse the JSON response and create a HTML element containing a formatted question, depending on the type of question requested and the information provided.
These questions will then be returned to the quizview function

    trivia/static/styles.css

#### styles.css

Contains css classes used to modify how various elements inside Trivia are displayed.

    trivia/templates

#### trivia.html

Contains various HTML elements controlled by Trivia.js, including the initial Trivia form used to create a new quiz.

#### Other HTML files
about.html - provides a condensed description of trivia<br>
index.html - serves as a frontpage for trivia, allowing access to all other features<br>
layout.html - layout.html is extended into all other html files, and adds the navbar and `<head>` <br>
login.html - allows users to login <br>
profile.html - displays the user's profile, scores and ratings, and allows the user to update their password <br>
register.html - create a new account. <br>


## APIs used
[Art Institute of Chicago](https://api.artic.edu/docs/)<br>
[Decathlon Sports](https://developers.decathlon.com/sports/)<br>
[REST Countries](https://restcountries.com/)<br>
[Zoo Animal API](https://zoo-animal-api.herokuapp.com/)<br>
[Movie Quote API](https://movie-quote-api.herokuapp.com/)<br>

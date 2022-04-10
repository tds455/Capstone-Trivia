document.addEventListener('DOMContentLoaded', function() {
    

    // document.querySelector('#newpost-form').addEventListener('submit', create_post);

    document.getElementById("triviasubmit").addEventListener("click", quizview);
    defaultview()
    });

// These are currently hardcoded, but they could instead be created from form input
var alltopics = ["Art", "Music", "History", "Sports", "Science"]
var questionvals = ["0", "0", "0", "0", "0", "6", "9", "12"]

function defaultview() {
    document.querySelector('#defaultview').style.display = 'block';
    document.querySelector('#quizview').style.display = 'none';
}

function quizview() {
    // Update views
    document.querySelector('#defaultview').style.display = 'none';
    document.querySelector('#quizview').style.display = 'block';

    // Process form input
    let form = document.getElementById("triviadata").elements;

    // create list of selected topics
    topics = []

    for (let i = 0; i < alltopics.length; i++) {
        if (form[i]["checked"] == true) {
            topics.push(alltopics[i]) 
        }
    }

    // Check selected amount of questions
    totalqs = ""

    for (let i = 5; i <= questionvals.length; i++)
        if (form[i]["checked"] == true) {
            totalqs = questionvals[i]
        }

    // Create POST request
    fetch('/createquestions', {
        method: 'POST',
        body: JSON.stringify({
            totalqs: totalqs,
            topics: topics
        })
    })
    .then(response => response.json())
    // Take response, format each question into HTML and add to HTML div
    .then(questions => {
        questions.forEach(question => {
        console.log(question);
        element = artquestion(question);
        document.querySelector('#quizview').appendChild(element);
        });
        })
    .then(questions => {
        const finalelement = document.createElement('div');
        finalelement.innerHTML = `
        <button class="btn btn-outline-dark" type="button"> Submit </button>
        `
        document.querySelector('#quizview').appendChild(finalelement);
    })
    // Wait for response before continuing


    // Update HTML views

}

function artquestion(question) {
    // Create HTML element containing question code
    console.log("artquestion")
    const element = document.createElement('div');
    element.innerHTML = `
    <div class="card border-primary mb-3 text-center col-sm" style="max-width: 18rem;">
    <img class="card-img-top" src="${question['url']}" alt="Artwork">
    <div class="card-body">
    <h5 class="card-title">${question['question']}"</h5>
    <div class="form-group">
    <label for="answer${question['number']}">Answer</label>
    <input type="text" class="form-control" id="answer${question['number']}">
    </div>
    </div>
    </div
    `
     return element
}

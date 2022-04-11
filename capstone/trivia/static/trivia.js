document.addEventListener('DOMContentLoaded', function() {
    

    // document.querySelector('#newpost-form').addEventListener('submit', create_post);

    document.getElementById("triviasubmit").addEventListener("click", quizview);
    defaultview()
    });

// These are currently hardcoded, but they could instead be created from form input
var alltopics = ["Art", "Music", "World", "Sports", "Science"]
var questionvals = ["0", "0", "0", "0", "0", "6", "9", "12"]

function defaultview() {
    document.querySelector('#defaultview').style.display = 'block';
    document.querySelector('#quizview').style.display = 'none';
    document.querySelector('#loadingview').style.display = 'none';
}

function quizview() {
    // Update views
    document.querySelector('#defaultview').style.display = 'none';
    document.querySelector('#loadingview').style.display = 'block';
    document.querySelector('#quizview').style.display = 'none';

    // Process form input
    let form = document.getElementById("triviadata").elements;

    // create list of selected topics
    topics = []

    // create array of question info to be checked for answers later
    quizquestions = []

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
        quizquestions.push(question)

        if (question['category'] == "arts") {
            element = artquestion(question);
        }
        if (question['category'] == "sports") {
            element = sportsquestion(question);
        }
        
        document.querySelector('#quizview').appendChild(element);
        });
        })
    .then(questions => {
        const submitelement = document.createElement('div');
        submitelement.innerHTML = `
        <button class="btn btn-outline-dark" id="answersubmit" type="button"> Submit </button>
        `
        submitelement.addEventListener('click', () => checkanswers(quizquestions));
        document.querySelector('#quizview').appendChild(submitelement);

        // Update HTML views
        document.querySelector('#loadingview').style.display = 'none';
        document.querySelector('#quizview').style.display = 'block';
    })
}

function artquestion(question) {
    // Create HTML element containing question code
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
    </div>
    `
    return element
}

function sportsquestion(question) {
    // Create HTML element containing question code
    const element = document.createElement('div');
    if (question["type"] == "1") {
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
        </div>
        `
    }
    if (question["type"] == "2") {
        element.innerHTML = `
        <div class="card border-primary mb-3 text-center col-sm" style="max-width: 18rem;">
        <p> Description: ${question['description']} </p>
        <div class="card-body">
        <h5 class="card-title">${question['question']}"</h5>
        <div class="form-group">
        <label for="answer${question['number']}">Answer</label>
        <input type="text" class="form-control" id="answer${question['number']}">
        </div>
        </div>
        </div>
        `
    }

    return element

}

function checkanswers(questions) {
    document.querySelector('#defaultview').style.display = 'none';
    document.querySelector('#quizview').style.display = 'none';
    document.querySelector('#loadingview').style.display = 'none';
    document.querySelector('#resultsview').style.display = 'block';

    let answers = document.getElementById("quizviewform").elements;
    results = []
    score = 0
    for (let i = 0; i < (answers.length - 1); i++) {
        if (answers[i]["value"] == questions[i]["answer"]) {
            results[i] = "Correct";
            score += 1
        }
        else {
            results[i] = "Incorrect"
        }
    
    }
    // Display results in HTML
    for (let i = 0; i < (results.length); i++)  {
        const element = document.createElement('div');
        element.innerHTML = `
        <div class="card mt-5 mb-5 w-50">
        <div class="card-header">
        Question: ${questions[i]['question']}
        </div>
        <ul class="list-group list-group-flush">
            <li class="list-group-item">Your answer: ${answers[i]['value']}</li>
            <li class="list-group-item">Correct answer: ${questions[i]['answer']}</li>
            <li class="list-group-item">You were ${results[i]} !</li>
        </ul>
        </div>
        `
        document.querySelector('#resultsview').appendChild(element);
    }
    

}
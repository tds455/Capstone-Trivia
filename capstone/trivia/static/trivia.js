document.addEventListener('DOMContentLoaded', function() {
    

    // document.querySelector('#newpost-form').addEventListener('submit', create_post);

    document.getElementById("triviasubmit").addEventListener("click", quizview);
    defaultview()
    });

// These are currently hardcoded, but they could instead be created from form input
var alltopics = ["Art", "Animal", "World", "Sports", "Movie"]
var questionvals = ["0", "0", "0", "0", "0", "6", "9", "12"]

function defaultview() {
    document.querySelector('#defaultview').style.display = 'block';
    document.querySelector('#quizview').style.display = 'none';
    document.querySelector('#loadingview').style.display = 'none';
    document.querySelector('#quizviewbutton').style.display = 'none';
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

    for (let i = 5; i < questionvals.length; i++)
        if (form[i]["checked"] == true) {
            totalqs = questionvals[i]
        }
        
    // Check if fastmode is ticked
    if (form[8]["checked"] == true) {
        fast = 1
    }
    else {
        fast = 0
    }

    // Create POST request
    fetch('/createquestions', {
        method: 'POST',
        body: JSON.stringify({
            totalqs: totalqs,
            topics: topics,
            fast: fast
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
        if (question['category'] == "world") {
            element = worldquestion(question);
        }
        if (question['category'] == "animal") {
            element = animalquestion(question);
        }
        if (question['category'] == "quote") {
            element = quotequestion(question);
        }
        
        document.querySelector('#quizview').appendChild(element);
        });
        })
    .then(questions => {
        const submitelement = document.createElement('div');
        submitelement.innerHTML = `
        <button class="btn btn-lg btn-block btn-dark" id="answersubmit" type="button"> Submit </button>
        `
        submitelement.addEventListener('click', () => checkanswers(quizquestions));
        document.querySelector('#quizviewbutton').appendChild(submitelement);

        // Update HTML views
        document.querySelector('#loadingview').style.display = 'none';
        document.querySelector('#quizview').style.display = 'block';
        document.querySelector('#quizviewbutton').style.display = 'block';
    })
}

function artquestion(question) {
    // Create HTML element containing question code
    const element = document.createElement('div');
    element.innerHTML = `
    <div class="card border-primary mt-3 text-center quizcard">
    <img class="card-img-top quizimg" src="${question['url']}" alt="Artwork">
    <div class="card-body">
    <h5 class="card-title">${question['question']}</h5>
    <div class="quizinput form-group">
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
        <div class="card border-primary mt-3 text-center quizcard">
        <img class="card-img-top quizimg" src="${question['url']}" alt="Sport">
        <div class="card-body">
        <h5 class="card-title">${question['question']}"</h5>
        <div class="quizinput form-group">
        <label for="answer${question['number']}">Answer</label>
        <input type="text" class="form-control" id="answer${question['number']}">
        </div>
        </div>
        </div>
        `
    }
    if (question["type"] == "2") {
        element.innerHTML = `
        <div class="card border-primary mt-3 text-center quizcard">
        <div class="card-body">
        <h5 class="card-title">${question['question']}"</h5>
        <p> Description: ${question['description']} </p>
        <div class="quizinput form-group">
        <label for="answer${question['number']}">Answer</label>
        <input type="text" class="form-control" id="answer${question['number']}">
        </div>
        </div>
        </div>
        `
    }
    return element
}

function animalquestion(question) {
    // Create HTML element containing question code
    const element = document.createElement('div');
    if (question["type"] == "1") {
        element.innerHTML = `
        <div class="card border-primary mt-3 text-center quizcard">
        <img class="card-img-top animalquizimg" src="${question['url']}" alt="animal">
        <div class="card-body">
        <h5 class="card-title">${question['question']}</h5>
        <p>${question['diet']}</p>
        <div class="quizinput form-group">
        <label for="answer${question['number']}">Answer</label>
        <input type="text" class="form-control" id="answer${question['number']}">
        </div>
        </div>
        </div>
        `
    }
    if (question["type"] == "2") {
        element.innerHTML = `
        <div class="card border-primary mt-3 text-center quizcard">
        <img class="card-img-top animalquizimg" src="${question['url']}" alt="animal">
        <div class="card-body">
        <h5 class="card-title">${question['question']}</h5>
        <p>${question['habitat']}</p>
        <div class="quizinput form-group">
        <label for="answer${question['number']}">Answer</label>
        <input type="text" class="form-control" id="answer${question['number']}">
        </div>
        </div>
        </div>
        `
    }
    if (question["type"] == "3") {
        element.innerHTML = `
        <div class="card border-primary mt-3 text-center quizcard">
        <img class="card-img-top animalquizimg" src="${question['url']}" alt="animal">
        <div class="card-body">
        <h5 class="card-title">${question['question']}${question['location']}</h5>
        <div class="quizinput form-group">
        <label for="answer${question['number']}">Answer</label>
        <input type="text" class="form-control" id="answer${question['number']}">
        </div>
        </div>
        </div>
        `
    }

    return element
}

function worldquestion(question) {
    // Create HTML element containing question code
    const element = document.createElement('div');
    if (question["type"] == "1") {
        element.innerHTML = `
        <div class="card border-primary mt-3 text-center quizcard">
        <img class="worldquizimg card-img-top" src="${question['url']}" alt="flag">
        <div class="card-body">
        <h5 class="card-title">Which country in ${question['region']} with the above flag speaks ${question['language']}</h5>
        <div class="quizinput form-group">
        <label for="answer${question['number']}">Answer</label>
        <input type="text" class="form-control" id="answer${question['number']}">
        </div>
        </div>
        </div>
        `
    }
    if (question["type"] == "2") {
        element.innerHTML = `
        <div class="card border-primary mt-3 text-center quizcard">
        <img class="worldquizimg card-img-top" src="${question['url']}" alt="flag">
        <div class="card-body">
        <h5 class="card-title">Which country in ${question['region']} with the above flag uses the ${question['currency']}</h5>
        <div class="quizinput form-group">
        <label for="answer${question['number']}">Answer</label>
        <input type="text" class="form-control" id="answer${question['number']}">
        </div>
        </div>
        </div>
        `
    }
    if (question["type"] == "3") {
        element.innerHTML = `
        <div class="card border-primary mt-3 text-center quizcard">
        <img class="worldquizimg card-img-top" src="${question['url']}" alt="flag">
        <div class="card-body">
        <h5 class="card-title">Which country in ${question['region']} with the above flag has a population of ${question['population']}</h5>
        <div class="quizinput form-group">
        <label for="answer${question['number']}">Answer</label>
        <input type="text" class="form-control" id="answer${question['number']}">
        </div>
        </div>
        </div>
        `
    }

    return element
}

function quotequestion(question) {
    // Create HTML element containing question code
    const element = document.createElement('div');
    if (question["type"] == "1") {
        element.innerHTML = `
        <div class="card border-primary mt-3 text-center quizcard">
        <div class="card-body">
        <h5 class="card-title">In which movie did ${question['person']} say "${question['quote']}"</h5>
        <div class="quizinput form-group">
        <label for="answer${question['number']}">Answer</label>
        <input type="text" class="form-control" id="answer${question['number']}">
        </div>
        </div>
        </div>
        `
    }
    if (question["type"] == "2") {
        element.innerHTML = `
        <div class="card border-primary mt-3 text-center quizcard">
        <div class="card-body">
        <h5 class="card-title">In ${question['movie']} who said the following "${question['quote']}"</h5>
        <div class="quizinput form-group">
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
    document.querySelector('#quizviewbutton').style.display = 'none';

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
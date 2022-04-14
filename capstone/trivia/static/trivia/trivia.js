document.addEventListener('DOMContentLoaded', function() {
    
    try {
    document.getElementById("triviasubmit").addEventListener("click", quizview);
    defaultview()
    }
    catch (error) {
        return
    }

    

    });

// These are currently hardcoded, but they could instead be created from form input
var alltopics = ["Art", "Animal", "World", "Sports", "Movie"]
var questionvals = ["0", "0", "0", "0", "0", "6", "9", "12"]

function defaultview() {
    document.getElementById("triviasubmit").addEventListener("click", quizview);
    document.querySelector('#defaultview').style.display = 'block';
    document.querySelector('#loadingview').style.display = 'none';
    document.querySelector('#quizview').style.display = 'none';
    document.querySelector('#quizviewbutton').style.display = 'none';
    document.querySelector('#resultsview').style.display = 'none';
    document.querySelector('#scoreview').style.display = 'none';
    document.querySelector('#resultsbutton').style.display = 'none';
    document.querySelector('#quizview').innerHTML = ``;
    document.querySelector('#quizviewbutton').innerHTML = ``;
    document.querySelector('#resultsview').innerHTML = ``;
    document.querySelector('#scoreview').innerHTML = ``;
    document.querySelector('#resultsbutton').innerHTML = ``;

    // Retrieve and display latest score
    fetch('/updatescores', {
        method: 'GET',
        })
    .then(response => response.json())
    .then(stats => {
        document.querySelector('#userscore').innerHTML =
        `
            <a class="nav-link">Total score: ${stats['score']}</a>
        `
    })
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

    // validate form input

    // If no categories have been selected, return an error message
    if (topics.length == 0) {
        document.querySelector('#loadingview').style.display = 'none';
        document.querySelector('#resultsview').style.display = 'block';

        document.querySelector('#resultsview').innerHTML = `
        <div class="container">
        <div class="header mt-5 text-center">
        <p class="error">Please select one or more categories</p>
        </div>
        </div>
        `
        const element = document.createElement('div');
        element.innerHTML = `
        <div class="col-md-4 text-center mx-auto">
        <button class="btn btn-lg btn-block btn-dark text-center" id="triviareturn" type="button"> Start again </button>
        </div>
        `
        element.addEventListener('click', () => defaultview());
        document.querySelector('#resultsview').appendChild(element);
    }
    // Continue processing form
    else {

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
        <h5 class="card-title">Which country in ${question['region']} with the above flag has a population of ${question['population']} people</h5>
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
    document.querySelector('#scoreview').style.display = 'block';
    document.querySelector('#quizviewbutton').style.display = 'none';
    document.querySelector('#resultsbutton').style.display = 'block';

    let answers = document.getElementById("quizviewform").elements;

    // Initialise score and rating values
    let score = 0;
    let artrating = 0;
    let animalrating = 0;
    let worldrating = 0;
    let sportsrating = 0;
    let movierating = 0;

    let ratings = [];
    let results = [];



    for (let i = 0; i < (answers.length - 1); i++) {

        // Check if an answer was provided, and if not set it as an empty string
        if (answers[i]['value'] != "") {
            answer = answers[i]['value']
        }
        else {
            answer = ""
        }

        // Create string with correct answer.  
        questionanswer = String(questions[i]['answer'])
     
        // Check if question matches answer, increasing score and ratings or decreasing ratings appropiately
        // Scores can only increase, while ratings will go up and down with each answer
        // Convert strings to lowercase to remove case sensitivity
        if (answer.toLowerCase() == questionanswer.toLowerCase()) {
            results[i] = "Correct";
            score += 5
            if (questions[i]['category'] == "arts") {
                artrating += 5;
            }
            if (questions[i]['category'] == "sports") {
                sportsrating += 5;
            }
            if (questions[i]['category'] == "world") {
                worldrating += 5;
            }
            if (questions[i]['category'] == "animal") {
                animalrating += 5;
            }
            if (questions[i]['category'] == "quote") {
                movierating += 5;
            }
        }
        else {
            results[i] = "Incorrect"
            if (questions[i]['category'] == "arts") {
                artrating -= 5;
            }
            if (questions[i]['category'] == "sports") {
                sportsrating -= 5;
            }
            if (questions[i]['category'] == "world") {
                worldrating -= 5;
            }
            if (questions[i]['category'] == "animal") {
                animalrating -= 5;
            }
            if (questions[i]['category'] == "quote") {
                movierating -= 5;
            }            
        }
    
    }

    // Call displayscores function to display information in page
    ratings.push(score, artrating, sportsrating, worldrating, animalrating, movierating)
    displayscores(ratings, questions, answers, results)

}

function displayscores(ratings, questions, answers, results) {

    // Display scores updates
    const scores = document.createElement('div')
    scores.innerHTML = `
    <div class="container-fluid w-100">
    <div class="header mt-5 text-center">
        <h1>Scores and ratings</h1>
        <ul class="list-group list-group-flush">
        <li class="list-group-item">Score: ${ratings[0]}</li>
        <li class="list-group-item">Art rating change: ${ratings[1]}</li>
        <li class="list-group-item">Sports rating change: ${ratings[2]}</li>
        <li class="list-group-item">Geography rating change: ${ratings[3]}</li>
        <li class="list-group-item">Animals rating change: ${ratings[4]}</li>
        <li class="list-group-item">Movie / TV shows rating change: ${ratings[5]}</li>

    </div>
    </div>
    <div class="card-columns">
    `
    document.querySelector('#scoreview').appendChild(scores);


    // Display results in HTML
    for (let i = 0; i < (results.length); i++)  {
        const element = document.createElement('div');
        element.innerHTML = `
        <div class="card border-primary mt-3 text-center resultscard">
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

    const submitelement = document.createElement('div');
    submitelement.innerHTML = `
    <button class="btn btn-lg btn-block btn-dark" id="resultsback" type="button"> Play again </button>
    `
    submitelement.addEventListener('click', () => defaultview());
    document.querySelector('#resultsbutton').appendChild(submitelement);

    window.scrollTo(0,0);

    // Create POST request to update scores, then display new score in top corner
    fetch('/updatescores', {
        method: 'PUT',
        body: JSON.stringify({
            score: ratings[0],
            art: ratings[1],
            sports: ratings[2],
            world: ratings[3],
            animals: ratings[4],
            movies: ratings[5],
            })
        })
    .then(response => response.json())
    .then(stats => {
        document.querySelector('#userscore').innerHTML =
        `
            <a class="nav-link">Total score: ${stats['score']}</a>
        `
    })

}
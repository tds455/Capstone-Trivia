document.addEventListener('DOMContentLoaded', function() {
    

    // document.querySelector('#newpost-form').addEventListener('submit', create_post);

    document.getElementById("triviasubmit").addEventListener("click", quizview);
    defaultview()
    });

// These are currently hardcoded, but it could instead be created from form input
var alltopics = ["Art", "Music", "History", "Sports", "Science"]
var questionvals = ["0", "0", "0", "0", "0", "6", "9", "12"]

function defaultview() {
    document.querySelector('#defaultview').style.display = 'block';
    document.querySelector('#quizview').style.display = 'none';
}

function quizview() {
    // Update views
    document.querySelector('#defaultview').style.display = 'block';
    document.querySelector('#quizview').style.display = 'none';

    // Process form input
    let form = document.getElementById("triviadata").elements;

    // create list of selected topics
    topics = []

    for (let i = 0; i < alltopics.length; i++) {
        if (form[i]["checked"] == true) {
            topics.push(alltopics[i]) 
        }
    }
    console.log(topics)

    // Check selected amount of questions

    for (let i = 5; i <= questionvals.length; i++)
        if (form[i]["checked"] == true) {
            totalqs = questionvals[i]
        }
    console.log(totalqs)

    // Create POST request
    console.log("success")
    body = "testing"
    fetch('/createquestions', {
        method: 'POST',
        body: JSON.stringify({
            body: body
        })
    })

    // Wait for response before continuing


    // Update HTML views

}


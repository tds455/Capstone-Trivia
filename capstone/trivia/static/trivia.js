document.addEventListener('DOMContentLoaded', function() {

    // document.querySelector('#newpost-form').addEventListener('submit', create_post);

    document.getElementById("triviaform").addEventListener("click", quizview);
    document.getElementById("triviasubmit").addEventListener("click", apitest);
    quizview()
    });

function defaultview() {
    document.querySelector('#defaultview').style.display = 'block';
    document.querySelector('#quizview').style.display = 'none';
}

function quizview() {
    document.querySelector('#defaultview').style.display = 'none';
    document.querySelector('#quizview').style.display = 'block';
}

function apitest() {
    console.log("success")
    body = "testing"
    fetch('/createquestions', {
        method: 'POST',
        body: JSON.stringify({
            body: body
        })
    })
}
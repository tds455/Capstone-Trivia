document.addEventListener('DOMContentLoaded', function() {

    // document.querySelector('#newpost-form').addEventListener('submit', create_post);

    document.getElementById("triviaform").addEventListener("click", quizview);
    defaultview()
    });

function defaultview() {
    document.querySelector('#defaultview').style.display = 'block';
    document.querySelector('#quizview').style.display = 'none';
}

function quizview() {
    document.querySelector('#defaultview').style.display = 'none';
    document.querySelector('#quizview').style.display = 'block';
}
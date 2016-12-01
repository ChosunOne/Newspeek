$(document).ready(function () {
    $("#button").click(function () {
        $("#frame").attr("src", "http://www.google.com/");
    });
});

function loadArticle() {
    var el = document.getElementById('frame1');
    el.src = document.getElementById("article1").value;
    alert("I did something!");
}


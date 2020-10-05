$(document).ready(function(){
console.log( "ready!" );
var titles = document.querySelectorAll(".title");
var results = document.querySelectorAll(".result");
for (i=0; i<titles.length; i++) {
    titles[i].addEventListener("click", function(){
        for (i=0; i<results.length; i++) {
            if (results[i].style.display ==""){
                results[i].style.display = "none";
            }
            else {
                results[i].style.display = "";
            }
        };
    });    
};
});


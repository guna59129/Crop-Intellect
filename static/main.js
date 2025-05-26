function openExplore() {
    var url = '/explorenow';
    window.location.href = url;
}

function predict() {
    console.log("Predict button clicked");
    var form = document.getElementById("prediction-form");
    var formData = new FormData(form);

    fetch("/explorenow", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())  
    .then(data => {
        
        var prediction = data.prediction;
        
        prediction = prediction.charAt(0).toUpperCase() + prediction.slice(1);
        
        document.getElementById("prediction-result").innerHTML = "<div class='pred'><h1>Best Suitable  Crop: " + prediction + "</h1></div>";
    })
    .catch(error => {
        console.error("Error:", error);
        
    });
}

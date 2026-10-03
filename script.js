console.log("ArgoMatrix-AI loaded successfully.");

function validateScore(value) {

    if (value < 0 || value > 10) {

        alert("Please enter a value between 0 and 10.");

        return false;
    }

    return true;
}
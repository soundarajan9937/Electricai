// ===============================
// Dashboard
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    let profile = JSON.parse(localStorage.getItem("profile"));

    if (profile && profile.name) {

        document.getElementById("welcomeUser").innerHTML =
            "Welcome, " + profile.name;

    } else {

        document.getElementById("welcomeUser").innerHTML =
            "Welcome, User";

    }

});

// ===============================
// Toggle Payment Apps Grid Display
// ===============================
function togglePaymentMethods() {
    const appsGrid = document.getElementById("paymentButtonsGrid");
    if (appsGrid.style.display === "none") {
        appsGrid.style.display = "flex";
    } else {
        appsGrid.style.display = "none";
    }
}
// ===============================
// Load Settings
// ===============================

window.onload = function () {

    let profile = JSON.parse(localStorage.getItem("profile"));

    if (profile) {

        document.getElementById("email").value = profile.email || "";
        document.getElementById("currentPassword").value = profile.password || "";

    }

};

// ===============================
// Save Settings (Change Password)
// ===============================

async function saveSettings() {

    let profile = JSON.parse(localStorage.getItem("profile"));

    if (!profile) {
        alert("Session error. Please login again.");
        return;
    }

    let password = document.getElementById("password").value.trim();
    let confirm = document.getElementById("confirm").value.trim();

    if (password === "" || confirm === "") {

        alert("Please enter a new password.");
        return;

    }

    if (password !== confirm) {

        alert("Passwords do not match.");
        return;

    }

    // Update profile object
    profile.password = password;

    try {
        const response = await fetch("http://127.0.0.1:5000/update_profile", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(profile)
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem("profile", JSON.stringify(profile));
            document.getElementById("currentPassword").value = password;
            document.getElementById("password").value = "";
            document.getElementById("confirm").value = "";
            alert("✅ Password Changed Successfully!");
        } else {
            alert("❌ Failed to update password on server: " + data.message);
        }
    } catch (error) {
        console.error("Backend sync failed:", error);
        alert("❌ Cannot connect to Flask Server.");
    }

}

// ===============================
// Logout Function
// ===============================

function logout() {

    localStorage.removeItem("profile");
    window.location.href = "login.html";

}
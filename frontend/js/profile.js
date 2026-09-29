// ===============================
// Load Profile
// ===============================

window.onload = function () {

    let profile = JSON.parse(localStorage.getItem("profile"));

    if (profile != null) {

        document.getElementById("name").value = profile.name || "";
        document.getElementById("email").value = profile.email || "";
        document.getElementById("phone").value = profile.phone || "";
        document.getElementById("meter").value = profile.meter || "";
        document.getElementById("address").value = profile.address || "";

    } else {

        document.getElementById("name").value = "";
        document.getElementById("email").value = "";
        document.getElementById("phone").value = "";
        document.getElementById("meter").value = "";
        document.getElementById("address").value = "";

    }

};

// ===============================
// Save Profile
// ===============================

async function saveProfile() {

    let profile = {
        name: document.getElementById("name").value.trim(),
        email: document.getElementById("email").value.trim(),
        phone: document.getElementById("phone").value.trim(),
        meter: document.getElementById("meter").value.trim(),
        address: document.getElementById("address").value.trim()
    };

    if (profile.name === "" || profile.email === "") {
        alert("Name and Email are required.");
        return;
    }

    // Save to localStorage so it reflects across the dashboard instantly
    localStorage.setItem("profile", JSON.stringify(profile));

    // Also attempt to update the backend database if applicable
    try {
        const response = await fetch(`${API_BASE_URL}/update_profile`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(profile)
        });

        const data = await response.json();
        if (response.ok) {
            alert("✅ Profile Updated Successfully!");
        } else {
            alert("✅ Profile updated locally: " + data.message);
        }
    } catch (error) {
        console.error("Backend sync failed:", error);
        alert("✅ Profile Updated Successfully!");
    }

}
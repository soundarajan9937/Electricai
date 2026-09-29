document.querySelector("form").addEventListener("submit", async function (e) {

    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Please fill all fields.");
        return;
    }

    try {

        const response = await fetch(`${API_BASE_URL}/login`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("✅ " + data.message);

            // Save user profile details to localStorage for the dashboard
            const profile = {
                name: data.name,
                email: data.email,
                phone: data.phone,
                meter: data.meter,
                address: data.address,
                password: data.password
            };
            localStorage.setItem("profile", JSON.stringify(profile));

            window.location.href = "dashboard.html";

        } else {

            alert("❌ " + data.message);

        }

    } catch (error) {

        console.error(error);

        alert("Cannot connect to Flask Server.");

    }

});

// ===============================
// Toggle Password Visibility Eye Symbol
// ===============================
function togglePasswordVisibility() {
    const passwordField = document.getElementById("password");
    const toggleIcon = document.getElementById("togglePasswordIcon");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        toggleIcon.classList.remove("fa-eye-slash");
        toggleIcon.classList.add("fa-eye");
    }
}
// =====================================================
// ELECTRIC AI - LOGIN
// =====================================================

document.querySelector("form").addEventListener("submit", async function (e) {

    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Please fill all fields.");
        return;
    }

    try {

        console.log("=================================");
        console.log("⚡ ELECTRIC AI LOGIN");
        console.log("=================================");

        console.log("Backend:", API_BASE_URL);
        console.log("Login URL:", API_BASE_URL + "/login");

        const response = await fetch(
            API_BASE_URL + "/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

        console.log("Response status:", response.status);

        const data = await response.json();

        console.log("Backend response:", data);

        if (response.ok) {

            alert("✅ " + data.message);

            const profile = {
                name: data.name,
                email: data.email,
                phone: data.phone,
                meter: data.meter,
                address: data.address,
                password: data.password
            };

            localStorage.setItem(
                "profile",
                JSON.stringify(profile)
            );

            localStorage.setItem(
                "userEmail",
                data.email || email
            );

            localStorage.setItem(
                "userMeter",
                data.meter || ""
            );

            localStorage.setItem(
                "userName",
                data.name || ""
            );

            console.log("✅ Login successful.");

            window.location.href = "dashboard.html";

        } else {

            alert(
                "❌ " +
                (data.message || "Login failed.")
            );
        }

    } catch (error) {

        console.error("❌ LOGIN CONNECTION ERROR");
        console.error(error);

        alert(
            "Cannot connect to Flask Server."
        );
    }

});


// =====================================================
// PASSWORD VISIBILITY
// =====================================================

function togglePasswordVisibility() {

    const passwordField =
        document.getElementById("password");

    const toggleIcon =
        document.getElementById("togglePasswordIcon");

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
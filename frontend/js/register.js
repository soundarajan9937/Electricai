document.getElementById("registerForm").addEventListener("submit", async function (e) {

    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const meter = document.getElementById("meter").value.trim();
    const address = document.getElementById("address").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (
        name === "" ||
        email === "" ||
        phone === "" ||
        meter === "" ||
        address === "" ||
        password === "" ||
        confirmPassword === ""
    ) {
        alert("Please fill all fields.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    try {

        const response = await fetch(`${API_BASE_URL}/register`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name,
                email: email,
                phone: phone,
                meter: meter,
                address: address,
                password: password
            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("✅ " + data.message);

            window.location.href = "login.html";

        } else {

            alert("❌ " + data.message);

        }

    } catch (error) {

        console.error(error);

        alert("Cannot connect to Flask Server.");

    }

});

// ===============================
// Toggle Password Field Visibility
// ===============================
function toggleFieldVisibility(fieldId, iconId) {
    const targetField = document.getElementById(fieldId);
    const targetIcon = document.getElementById(iconId);

    if (targetField.type === "password") {
        targetField.type = "text";
        targetIcon.classList.remove("fa-eye");
        targetIcon.classList.add("fa-eye-slash");
    } else {
        targetField.type = "password";
        targetIcon.classList.remove("fa-eye-slash");
        targetIcon.classList.add("fa-eye");
    }
}
const fileInput = document.getElementById("fileInput"); 
const preview = document.getElementById("previewImage"); 
 
fileInput.addEventListener("change", function () { 
 
    const file = this.files[0]; 
 
    if (file) { 
        preview.src = URL.createObjectURL(file); 
    } 
 
}); 
 
function analyzeMeter() { 
 
    if (fileInput.files.length === 0) { 
 
        alert("Please upload a meter image."); 
        return; 
 
    } 
 
    const file = fileInput.files[0]; 
 
    // Clear old data 
    localStorage.removeItem("meterImage"); 
    localStorage.removeItem("meter_reading"); 
    localStorage.removeItem("bill_amount"); 
    localStorage.removeItem("meterImageURL"); 
 
    const reader = new FileReader(); 
 
    reader.onload = function (e) { 
 
        // Save uploaded image
        localStorage.setItem("meterImage", e.target.result); 
 
        // Backend URL
        const BACKEND_URL =
            "https://electric-ai-backend-sound.onrender.com";
 
        // Uploaded image URL
        const imageURL =
            BACKEND_URL + "/uploads/" + encodeURIComponent(file.name);
 
        // Save backend image URL
        localStorage.setItem("meterImageURL", imageURL);
 
        console.log("Image saved to localStorage");
        console.log("Backend image URL:", imageURL);
 
        // Open processing page 
        window.location.href = "processing.html"; 
 
    }; 
 
    reader.onerror = function () { 
 
        alert("Failed to read image."); 
 
    }; 
 
    reader.readAsDataURL(file); 
 
}
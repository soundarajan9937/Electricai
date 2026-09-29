console.log("processing.js loaded");

const status = document.getElementById("status");

// Prevent duplicate requests
let processingStarted = false;

window.onload = async function () {

    if (processingStarted) {
        console.log("Already processing...");
        return;
    }

    processingStarted = true;

    console.log("window.onload fired");

    document.getElementById("step1").innerHTML = "✅ Upload Received";

    try {

        const imageData = localStorage.getItem("meterImage");

        if (!imageData) {
            alert("No uploaded image found.");
            window.location.href = "upload_meter.html";
            return;
        }

        status.innerHTML = "Preparing image...";

        const blob = await (await fetch(imageData)).blob();

        const formData = new FormData();
        formData.append("image", blob, "meter.jpg");

        status.innerHTML = "Detecting Electricity Meter...";
        document.getElementById("step2").innerHTML = "⏳ Detecting Meter...";

        console.log("Sending request to Flask...");

        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: "POST",
            body: formData
        });

        console.log("HTTP Status:", response.status);

        if (!response.ok) {
            throw new Error("Backend Error: " + response.status);
        }

        const data = await response.json();

        console.log("Response Data:", data);

        if (!data.success) {
            alert(data.message);
            return;
        }

        localStorage.setItem("meter_reading", data.meter_reading);
        localStorage.setItem("bill_amount", data.bill_amount);

        document.getElementById("step2").innerHTML = "✅ Meter Detected";

        status.innerHTML = "Reading Meter...";
        document.getElementById("step3").innerHTML = "✅ OCR Completed";

        await new Promise(resolve => setTimeout(resolve, 700));

        status.innerHTML = "Calculating Bill...";
        document.getElementById("step4").innerHTML = "✅ Bill Calculated";

        await new Promise(resolve => setTimeout(resolve, 700));

        status.innerHTML = "Generating Report...";
        document.getElementById("step5").innerHTML = "✅ Report Generated";

        await new Promise(resolve => setTimeout(resolve, 700));

        status.innerHTML = "Opening Result Page...";

        console.log("Redirecting to result page...");

        window.location.replace("result.html");

    }
    catch (err) {

        console.error("ERROR:", err);

        alert(err.message);

        processingStarted = false;
    }

};
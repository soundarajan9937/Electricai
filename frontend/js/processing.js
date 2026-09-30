console.log("processing.js loaded");

const status = document.getElementById("status");

let processingStarted = false;

window.onload = async function () {

    if (processingStarted) {
        console.log("Already processing...");
        return;
    }

    processingStarted = true;

    console.log("======================================");
    console.log("⚡ ELECTRIC AI - PROCESSING");
    console.log("======================================");

    try {

        document.getElementById("step1").innerHTML =
            "⏳ Preparing uploaded image...";

        const imageData = localStorage.getItem("meterImage");

        if (!imageData) {
            console.error("No meterImage found in localStorage.");

            alert("No uploaded image found.");

            window.location.href = "upload_meter.html";
            return;
        }

        console.log("Image found in localStorage.");

        status.innerHTML = "Preparing image...";

        // Convert Base64 image to Blob
        const imageResponse = await fetch(imageData);
        const blob = await imageResponse.blob();

        console.log("Image converted to Blob.");
        console.log("Image size:", blob.size);

        // Create FormData
        const formData = new FormData();

        formData.append(
            "image",
            blob,
            "meter.jpg"
        );

        document.getElementById("step1").innerHTML =
            "✅ Upload Received";

        // -----------------------------------------
        // STEP 2 - SEND TO BACKEND
        // -----------------------------------------

        status.innerHTML =
            "Detecting Electricity Meter...";

        document.getElementById("step2").innerHTML =
            "⏳ Detecting Meter...";

        console.log(
            "Sending request to:",
            API_BASE_URL + "/upload"
        );

        const response = await fetch(
            API_BASE_URL + "/upload",
            {
                method: "POST",
                body: formData
            }
        );

        console.log(
            "Backend HTTP Status:",
            response.status
        );

        // -----------------------------------------
        // READ BACKEND RESPONSE
        // -----------------------------------------

        const responseText = await response.text();

        console.log("Raw Backend Response:");
        console.log(responseText);

        let data;

        try {
            data = JSON.parse(responseText);
        } catch (error) {

            throw new Error(
                "Backend returned an invalid response."
            );
        }

        console.log("Parsed Backend Response:");
        console.log(data);

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Backend Error: HTTP " + response.status
            );
        }

        if (!data.success) {

            throw new Error(
                data.message ||
                "Meter analysis failed."
            );
        }

        // -----------------------------------------
        // STEP 3 - GET RESULTS
        // -----------------------------------------

        console.log(
            "Meter Reading:",
            data.meter_reading
        );

        console.log(
            "Bill Amount:",
            data.bill_amount
        );

        // Save result
        localStorage.setItem(
            "meter_reading",
            data.meter_reading ?? ""
        );

        localStorage.setItem(
            "bill_amount",
            data.bill_amount ?? ""
        );

        // Save backend image if returned
        if (data.image) {

            let imageURL;

            if (
                data.image.startsWith("http://") ||
                data.image.startsWith("https://")
            ) {

                imageURL = data.image;

            } else {

                imageURL =
                    API_BASE_URL +
                    "/uploads/" +
                    encodeURIComponent(data.image);
            }

            localStorage.setItem(
                "meterImageURL",
                imageURL
            );

            console.log(
                "Backend Image URL:",
                imageURL
            );
        }

        // -----------------------------------------
        // STEP 4 - UPDATE PROCESSING SCREEN
        // -----------------------------------------

        document.getElementById("step2").innerHTML =
            "✅ Meter Detected";

        await new Promise(
            resolve => setTimeout(resolve, 700)
        );

        status.innerHTML =
            "Reading Meter...";

        document.getElementById("step3").innerHTML =
            "✅ OCR Completed";

        await new Promise(
            resolve => setTimeout(resolve, 700)
        );

        status.innerHTML =
            "Calculating Bill...";

        document.getElementById("step4").innerHTML =
            "✅ Bill Calculated";

        await new Promise(
            resolve => setTimeout(resolve, 700)
        );

        status.innerHTML =
            "Generating Report...";

        document.getElementById("step5").innerHTML =
            "✅ Report Generated";

        await new Promise(
            resolve => setTimeout(resolve, 700)
        );

        status.innerHTML =
            "Opening Result Page...";

        console.log(
            "Redirecting to result.html..."
        );

        window.location.replace(
            "result.html"
        );

    }

    catch (err) {

        console.error(
            "======================================"
        );

        console.error(
            "❌ PROCESSING ERROR"
        );

        console.error(
            "======================================"
        );

        console.error(err);

        status.innerHTML =
            "❌ Processing Failed";

        alert(
            err.message ||
            "Something went wrong while processing the image."
        );

        processingStarted = false;
    }

};
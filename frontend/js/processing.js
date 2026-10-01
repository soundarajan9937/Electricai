console.log("processing.js loaded");

const status = document.getElementById("status");

let processingStarted = false;


// ============================================================
// PROCESS METER IMAGE
// ============================================================

window.onload = async function () {

    if (processingStarted) {
        return;
    }

    processingStarted = true;

    console.log("======================================");
    console.log("⚡ ELECTRIC AI - PROCESSING");
    console.log("======================================");


    try {

        // ====================================================
        // CLEAR OLD RESULT
        // ====================================================

        localStorage.removeItem("meter_reading");
        localStorage.removeItem("bill_amount");
        localStorage.removeItem("meterImageURL");


        // ====================================================
        // GET NEW IMAGE
        // ====================================================

        const imageData =
            localStorage.getItem("meterImage");

        if (!imageData) {

            alert("No uploaded image found.");

            window.location.href =
                "upload_meter.html";

            return;
        }


        console.log(
            "✅ New uploaded image found."
        );


        // ====================================================
        // STEP 1
        // ====================================================

        const step1 =
            document.getElementById("step1");

        if (step1) {

            step1.innerHTML =
                "⏳ Preparing uploaded image...";
        }

        status.innerHTML =
            "Preparing image...";


        // ====================================================
        // BASE64 → BLOB
        // ====================================================

        const imageResponse =
            await fetch(imageData);

        if (!imageResponse.ok) {

            throw new Error(
                "Unable to read uploaded image."
            );
        }


        const blob =
            await imageResponse.blob();


        console.log(
            "Image size:",
            blob.size,
            "bytes"
        );


        // ====================================================
        // FORM DATA
        // ====================================================

        const formData =
            new FormData();


        formData.append(
            "image",
            blob,
            "meter.jpg"
        );


        // ====================================================
        // STEP 2
        // ====================================================

        status.innerHTML =
            "Detecting Electricity Meter...";


        const step2 =
            document.getElementById("step2");

        if (step2) {

            step2.innerHTML =
                "⏳ Detecting Meter...";
        }


        // ====================================================
        // BACKEND URL
        // ====================================================

        const uploadURL =
            API_BASE_URL + "/upload";


        console.log(
            "Sending image to:",
            uploadURL
        );


        // ====================================================
        // SEND IMAGE
        // ====================================================

        const response =
            await fetch(
                uploadURL,
                {
                    method: "POST",
                    body: formData
                }
            );


        console.log(
            "Backend HTTP status:",
            response.status
        );


        // ====================================================
        // READ BACKEND RESPONSE
        // ====================================================

        const responseText =
            await response.text();


        console.log(
            "Backend response:",
            responseText
        );


        let data;

        try {

            data =
                JSON.parse(
                    responseText
                );

        } catch (error) {

            throw new Error(
                "Backend returned invalid JSON."
            );
        }


        // ====================================================
        // BACKEND ERROR
        // ====================================================

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Meter analysis failed."
            );
        }


        if (!data.success) {

            throw new Error(
                data.message ||
                "Meter analysis failed."
            );
        }


        // ====================================================
        // VERIFY ACTUAL READING
        // ====================================================

        if (
            data.meter_reading === undefined ||
            data.meter_reading === null ||
            String(data.meter_reading).trim() === ""
        ) {

            throw new Error(
                "Backend did not return a meter reading."
            );
        }


        if (
            data.bill_amount === undefined ||
            data.bill_amount === null
        ) {

            throw new Error(
                "Backend did not return a bill amount."
            );
        }


        // ====================================================
        // GET ACTUAL VALUES
        // ====================================================

        const actualReading =
            String(
                data.meter_reading
            ).trim();


        const actualBill =
            String(
                data.bill_amount
            ).trim();


        console.log(
            "======================================"
        );

        console.log(
            "✅ ACTUAL BACKEND RESULT"
        );

        console.log(
            "Meter Reading:",
            actualReading
        );

        console.log(
            "Bill Amount:",
            actualBill
        );

        console.log(
            "======================================"
        );


        // ====================================================
        // SAVE ONLY NEW BACKEND RESULT
        // ====================================================

        localStorage.setItem(
            "meter_reading",
            actualReading
        );


        localStorage.setItem(
            "bill_amount",
            actualBill
        );


        // ====================================================
        // SAVE IMAGE
        // ====================================================

        localStorage.setItem(
            "meterImageURL",
            data.image_id
                ? API_BASE_URL +
                  "/image/" +
                  encodeURIComponent(
                      data.image_id
                  )
                : ""
        );


        // ====================================================
        // STEP 2 COMPLETE
        // ====================================================

        if (step2) {

            step2.innerHTML =
                "✅ Meter Detected";
        }


        // ====================================================
        // STEP 3
        // ====================================================

        status.innerHTML =
            "Reading Meter...";


        const step3 =
            document.getElementById("step3");


        if (step3) {

            step3.innerHTML =
                "⏳ Reading Meter...";
        }


        await new Promise(
            resolve =>
                setTimeout(
                    resolve,
                    500
                )
        );


        if (step3) {

            step3.innerHTML =
                "✅ OCR Completed";
        }


        // ====================================================
        // STEP 4
        // ====================================================

        status.innerHTML =
            "Calculating Bill...";


        const step4 =
            document.getElementById("step4");


        if (step4) {

            step4.innerHTML =
                "⏳ Calculating Bill...";
        }


        await new Promise(
            resolve =>
                setTimeout(
                    resolve,
                    500
                )
        );


        if (step4) {

            step4.innerHTML =
                "✅ Bill Calculated";
        }


        // ====================================================
        // STEP 5
        // ====================================================

        status.innerHTML =
            "Generating Report...";


        const step5 =
            document.getElementById("step5");


        if (step5) {

            step5.innerHTML =
                "⏳ Generating Report...";
        }


        await new Promise(
            resolve =>
                setTimeout(
                    resolve,
                    500
                )
        );


        if (step5) {

            step5.innerHTML =
                "✅ Report Generated";
        }


        // ====================================================
        // REDIRECT
        // ====================================================

        status.innerHTML =
            "Opening Result Page...";


        await new Promise(
            resolve =>
                setTimeout(
                    resolve,
                    500
                )
        );


        window.location.replace(
            "result.html"
        );

    }

    catch (error) {

        console.error(
            "======================================"
        );

        console.error(
            "❌ PROCESSING ERROR"
        );

        console.error(
            error
        );

        console.error(
            "======================================"
        );


        status.innerHTML =
            "❌ Processing Failed";


        alert(
            error.message ||
            "Something went wrong."
        );


        processingStarted = false;
    }

};
window.onload = function () {

    // Load uploaded image
    const image = localStorage.getItem("meterImage");

    if (image) {
        document.getElementById("meterImage").src = image;
    } else {
        document.getElementById("meterImage").src = "images/meter.png";
    }

    // Load reading and bill
    const reading = localStorage.getItem("meter_reading");
    const bill = localStorage.getItem("bill_amount");

    console.log("Reading:", reading);
    console.log("Bill:", bill);

    document.getElementById("reading").innerText =
        reading || "Not Found";

    document.getElementById("bill").innerText =
        bill ? "₹" + bill : "₹0";
};


// ==========================
// Save Analysis to History
// ==========================
function saveHistory() {

    const reading = localStorage.getItem("meter_reading");
    const bill = localStorage.getItem("bill_amount");
    const image = localStorage.getItem("meterImage");

    if (!reading || !bill) {
        alert("No analysis available.");
        return;
    }

    let history = JSON.parse(localStorage.getItem("history")) || [];

    // Prevent duplicate save
    const exists = history.some(item =>
        item.reading === reading &&
        item.bill === bill
    );

    if (!exists) {

        history.push({
            image: image,
            reading: reading,
            bill: bill,
            date: new Date().toLocaleString(),
            status: "Verified"
        });

        localStorage.setItem("history", JSON.stringify(history));

        alert("Analysis saved successfully!");

    } else {

        alert("This analysis is already saved.");

    }

    window.location.href = "history.html";
}


// ==========================
// Download Report
// ==========================
function downloadReport() {

    const reading = localStorage.getItem("meter_reading") || "N/A";
    const bill = localStorage.getItem("bill_amount") || "0";

    const report = `
AI Electricity Bill Analyzer
----------------------------

Meter Reading : ${reading}
Estimated Bill : ₹${bill}
Status : Verified

Generated on:
${new Date().toLocaleString()}
`;

    const blob = new Blob([report], { type: "text/plain" });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;
    a.download = "Electricity_Report.txt";

    document.body.appendChild(a);

    a.click();

    document.body.removeChild(a);

    URL.revokeObjectURL(url);
}
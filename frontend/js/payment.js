// ==============================
// Load Bill Amount
// ==============================

window.onload = function () {

    const bill = localStorage.getItem("bill_amount") || "0";

    document.getElementById("billAmount").innerHTML = "₹" + bill;

    document.getElementById("payBtn").innerHTML = "Pay ₹" + bill;

};


// ==============================
// Pay Now
// ==============================

function payNow() {

    const method =
        document.querySelector('input[name="payment"]:checked').value;

    const bill = localStorage.getItem("bill_amount") || "0";

    const name =
        document.querySelector('input[placeholder="Card Holder Name"]').value.trim();

    const card =
        document.querySelector('input[placeholder="Card Number"]').value.trim().replace(/\s/g, "");

    const expiry =
        document.querySelector('input[placeholder="MM/YY"]').value.trim();

    const cvv =
        document.querySelector('input[placeholder="CVV"]').value.trim();


    // Validate Card Only

    if (method === "Card") {

        if (name === "" || card === "" || expiry === "" || cvv === "") {

            alert("Please fill all card details.");

            return;
        }

        if (card.length !== 16 || isNaN(card)) {

            alert("Enter a valid 16-digit Card Number.");

            return;
        }

        const expiryPattern = /^(0[1-9]|1[0-2])\/\d{2}$/;

        if (!expiryPattern.test(expiry)) {

            alert("Enter Expiry Date in MM/YY format.");

            return;
        }

        if (cvv.length !== 3 || isNaN(cvv)) {

            alert("Enter a valid 3-digit CVV.");

            return;
        }

    }


    // Generate Transaction ID

    const transactionId =
        "TXN" + Math.floor(Math.random() * 1000000000);


    // Payment Object

    const payment = {

        transactionId: transactionId,

        amount: bill,

        method: method,

        status: "Paid",

        date: new Date().toLocaleString()

    };


    // Save Payment History

    let payments =
        JSON.parse(localStorage.getItem("paymentHistory")) || [];

    payments.push(payment);

    localStorage.setItem(
        "paymentHistory",
        JSON.stringify(payments)
    );


    // Save Bill Status

    localStorage.setItem("bill_status", "Paid");


    // Success

    alert(

        "✅ Payment Successful!\n\n" +

        "Transaction ID : " + transactionId +

        "\nPayment Method : " + method +

        "\nAmount Paid : ₹" + bill

    );


    window.location.href = "payment_history.html";

}


// ==============================
// Download Receipt
// ==============================

function downloadReceipt() {

    const bill =
        localStorage.getItem("bill_amount") || "0";

    const method =
        document.querySelector('input[name="payment"]:checked').value;

    const receipt = `

AI ELECTRICITY BILL ANALYZER

----------------------------

Payment Successful

Amount : ₹${bill}

Payment Method : ${method}

Status : Paid

Date : ${new Date().toLocaleString()}

Thank You.

`;

    const blob =
        new Blob([receipt], { type: "text/plain" });

    const url =
        URL.createObjectURL(blob);

    const a =
        document.createElement("a");

    a.href = url;

    a.download = "Payment_Receipt.txt";

    document.body.appendChild(a);

    a.click();

    document.body.removeChild(a);

    URL.revokeObjectURL(url);

}
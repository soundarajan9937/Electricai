window.onload = function () {

    const history = JSON.parse(localStorage.getItem("history")) || [];

    const tbody = document.getElementById("historyBody");

    tbody.innerHTML = "";

    if (history.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align:center;">
                    No History Available
                </td>
            </tr>
        `;

        return;
    }

    history.slice().reverse().forEach((item) => {

        tbody.innerHTML += `

        <tr>

            <td>
                <img
                    src="${item.image}"
                    width="90"
                    height="70"
                    style="border-radius:8px;object-fit:cover;">
            </td>

            <td>${item.date}</td>

            <td>${item.reading}</td>

            <td>₹${item.bill}</td>

            <td class="paid">Verified</td>

            <td>
                <button onclick="viewHistory('${item.date}')">
                    View
                </button>
            </td>

        </tr>

        `;

    });

};


// Search History
const search = document.getElementById("searchInput");

search.addEventListener("keyup", function () {

    const filter = this.value.toLowerCase();

    const rows = document.querySelectorAll("#historyBody tr");

    rows.forEach(function (row) {

        const text = row.innerText.toLowerCase();

        row.style.display = text.includes(filter) ? "" : "none";

    });

});


// View Selected Record
function viewHistory(date) {

    const history = JSON.parse(localStorage.getItem("history")) || [];

    const item = history.find(record => record.date === date);

    if (!item) return;

    localStorage.setItem("meterImage", item.image);
    localStorage.setItem("meter_reading", item.reading);
    localStorage.setItem("bill_amount", item.bill);

    window.location.href = "result.html";

}
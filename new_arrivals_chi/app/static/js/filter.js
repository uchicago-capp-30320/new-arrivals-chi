/**
   Implements filtering mechanisim for table

   Resource 1: https://www.w3schools.com/howto/howto_js_filter_table.asp

   Resource 2: https://stackoverflow.com/questions/51187477/how-to-filter-a-html-table-using-simple-javascript
*/

function filterTable() {
    var suppliesDropdown = document.getElementById("supplies");
    var neighborhoodDropdown = document.getElementById("neighborhood");
    var organizationDropdown = document.getElementById("organization");
    var hoursDropdown = document.getElementById("hours");

    var tableBody = document.querySelector("#healthTable tbody");

    var supplies = suppliesDropdown.value;
    var neighborhood = neighborhoodDropdown.value;
    var organization = organizationDropdown.value;
    var hours = hoursDropdown.value;

    var rows = tableBody.querySelectorAll("tr");
    rows.forEach(function(row) {
        var cells = row.querySelectorAll("td");
        var showRow = true;

        if (supplies) {
            var services = cells[0].textContent.toLowerCase().split(', ');
            if (!services.some(service => service.includes(supplies.toLowerCase()))) {
                showRow = false;
            }
        }

        if (neighborhood && cells[1].textContent !== neighborhood) {
            showRow = false;
        }
        if (organization && cells[2].textContent !== organization) {
            showRow = false;
        }
        if (hours) {
            var hrs = cells[3].textContent.toLowerCase();
            if (!hrs.includes(hours)) {
                showRow = false;
            }
        }

        if (showRow) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    var suppliesDropdown = document.getElementById("supplies");
    var neighborhoodDropdown = document.getElementById("neighborhood");
    var organizationDropdown = document.getElementById("organization");
    var hoursDropdown = document.getElementById("hours");

    suppliesDropdown.addEventListener("change", filterTable);
    neighborhoodDropdown.addEventListener("change", filterTable);
    organizationDropdown.addEventListener("change", filterTable);
    hoursDropdown.addEventListener("change", filterTable);

    filterTable();
});

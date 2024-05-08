/**
   Implements filtering mechanisim for table

   Resource 1: https://www.w3schools.com/howto/howto_js_filter_table.asp

   Resource 2: https://stackoverflow.com/questions/51187477/how-to-filter-a-html-table-using-simple-javascript
*/

function filterTable() {
    var suppliesDropdown = document.getElementById("street_address");
    var neighborhoodDropdown = document.getElementById("zip_code");
    var organizationDropdown = document.getElementById("city");
    var hoursDropdown = document.getElementById("state");

    var tableBody = document.querySelector("#healthTable tbody");

    var supplies = suppliesDropdown.value;
    var neighborhood = neighborhoodDropdown.value;
    var organization = organizationDropdown.value;
    var hours = hoursDropdown.value;

    var rows = tableBody.querySelectorAll("tr");
    rows.forEach(function(row) {
        var cells = row.querySelectorAll("td");
        var showRow = true;

        if (supplies && cells[0].textContent !== supplies) {
            showRow = false;
        }
        if (neighborhood && cells[1].textContent !== neighborhood) {
            showRow = false;
        }
        if (organization && cells[2].textContent !== organization) {
            showRow = false;
        }
        if (hours && cells[3].textContent !== hours) {
            showRow = false;
        }

        if (showRow) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    var suppliesDropdown = document.getElementById("street_address");
    var neighborhoodDropdown = document.getElementById("zip_code");
    var organizationDropdown = document.getElementById("city");
    var hoursDropdown = document.getElementById("state");

    suppliesDropdown.addEventListener("change", filterTable);
    neighborhoodDropdown.addEventListener("change", filterTable);
    organizationDropdown.addEventListener("change", filterTable);
    hoursDropdown.addEventListener("change", filterTable);

    filterTable();
});

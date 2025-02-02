var machineID;
var OptionsID;
function updateStatus() {
  machineID = document.querySelector('input[name="machine"]:checked').value;
  OptionsID = document.querySelector('input[name="options"]:checked').value;
  console.log(`Selected machine: ${machineID}`);
  console.log(`Selected options: ${OptionsID}`);
  getTableData(machineID, OptionsID);
}
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('input[type="radio"]').forEach((radio) => {
    radio.addEventListener("change", updateStatus);
    // updateStatus.call(radio); // Gọi updateStatus ban đầu để thiết lập trạng thái
  });
});
function getMachineInfor() {
  fetch("/machines")
    .then((response) => response.json())
    .then((data) => {
      const machineSection = document.getElementById("machine-id-section");
      data.forEach((machine, index) => {
        const radioInput = document.createElement("input");
        machineID = machine.name;
        radioInput.type = "radio";
        radioInput.name = "machine";
        radioInput.id = machine.name;
        radioInput.value = machine.name; // Set the value to machine name
        radioInput.className = "machine-id";
        if (index === 0) {
          radioInput.checked = true; // Set the first radio button as checked
        }

        const radioLabel = document.createElement("label");
        radioLabel.htmlFor = machine.name;
        radioLabel.className = "radio-label";
        radioLabel.innerHTML = `${machine.name}<br>${machine.ip}`;
        OptionsID = document.querySelector(
          'input[name="options"]:checked'
        ).value;
        radioInput.addEventListener("change", () => {
          machineID = document.querySelector(
            'input[name="machine"]:checked'
          ).value;
          getTableData(machineID, OptionsID); // Call getTableData with appropriate OptionsID

          console.log(`Selected machine: ${machineID}`);
        });

        machineSection.appendChild(radioInput);
        machineSection.appendChild(radioLabel);
      });

      // Trigger table update for the initially selected machine
      getTableData(machineID, OptionsID);
    });
}

function getTableData(machineID, OptionsID) {
  // print the machineID
  document.getElementById("fixture-name").textContent =
    "Machine ID: " + machineID;
  url_string = "/data/" + machineID;
  // Fetch JSON data and generate table rows

  fetch(url_string)
    .then((response) => response.json())
    .then((data) => {
      const tableBody = document.getElementById("table-body");
      tableBody.innerHTML = ""; // Clear existing rows
      let index = 0;
      const selectedData = data[OptionsID];
      selectedData.forEach((row) => {
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
          <th>${++index}</th>
          <th>${row.component}</th>
          <th>${row.counter}</th>
          <th><input type="checkbox" class="row-checkbox"></th>
        `;
        newRow.addEventListener("click", () => {
          const checkbox = newRow.querySelector('input[type="checkbox"]');
          checkbox.checked = !checkbox.checked;
        });
        tableBody.appendChild(newRow);
      });
    });
}

function deleteSelected() {
  const checkboxes = document.querySelectorAll(".row-checkbox:checked");
  const selectedRows = [];

  checkboxes.forEach((checkbox) => {
    const row = checkbox.closest("tr");
    const cells = row.querySelectorAll("th");
    const rowData = {
      machineID: machineID,
      OptionsID: OptionsID,
      component: cells[1].innerText,
    };
    console.log("Selected row:", rowData);
    selectedRows.push(rowData);
    // row.remove();
  });
  // Send API request to delete selected rows
  fetch("/delete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(selectedRows),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  getTableData(machineID, OptionsID);
}
function deleteAll() {
  const rowData = {
    machineID: machineID,
    OptionsID: OptionsID,
  };
  console.log("Selected row:", rowData);

  // Gửi yêu cầu API với chuỗi "delete all"
  fetch("/delete-all", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(rowData),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
// Call getMachineInfor to initialize the machine list and table
getMachineInfor();

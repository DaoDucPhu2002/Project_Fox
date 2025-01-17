// Fetch JSON data and generate radio buttons
fetch("machine.json")
  .then((response) => response.json())
  .then((data) => {
    const machineSection = document.getElementById("machine-id-section");
    data.forEach((machine, index) => {
      const radioInput = document.createElement("input");
      radioInput.type = "radio";
      radioInput.name = "machine";
      radioInput.id = machine.name;
      radioInput.className = "machine-id";
      if (index === 0) {
        radioInput.checked = true; // Set the first radio button as checked
      }

      const radioLabel = document.createElement("label");
      radioLabel.htmlFor = machine.name;
      radioLabel.className = "radio-label";
      radioLabel.innerHTML = `${machine.name}<br>${machine.ip}`;

      machineSection.appendChild(radioInput);
      machineSection.appendChild(radioLabel);
    });
  });

// Fetch JSON data and generate table rows
fetch("data.json")
  .then((response) => response.json())
  .then((data) => {
    const tableBody = document.getElementById("table-body");
    data.forEach((row) => {
      const newRow = document.createElement("tr");
      newRow.innerHTML = `
                        <th>${row.column1}</th>
                        <th>${row.column2}</th>
                        <th>${row.column3}</th>
                        <th><input type="checkbox"></th>
                    `;
      newRow.addEventListener("click", () => {
        const checkbox = newRow.querySelector('input[type="checkbox"]');
        checkbox.checked = !checkbox.checked;
      });
      tableBody.appendChild(newRow);
    });
  });

// Test Add Row
function addRow() {
  const tableBody = document.getElementById("table-body");
  const newRow = document.createElement("tr");
  newRow.innerHTML = `
                <th>1</th>
                <th>2</th>
                <th>3</th>
                <th><input type="checkbox"></th>
            `;
  newRow.addEventListener("click", () => {
    const checkbox = newRow.querySelector('input[type="checkbox"]');
    checkbox.checked = !checkbox.checked;
  });
  tableBody.appendChild(newRow);
}

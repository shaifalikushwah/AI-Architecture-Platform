document
    .getElementById("propertyForm")
    .addEventListener("submit", function(event) {

        event.preventDefault();

        const propertyData = {
            property_type: document.getElementById("propertyType").value,
            length: document.getElementById("length").value,
            width: document.getElementById("width").value,
            floors: document.getElementById("floors").value
        };

        console.log(propertyData);

        alert("Property details submitted successfully");
    });
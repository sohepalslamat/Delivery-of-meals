// Getting DOM Element
const requestForm = document.getElementById("request-form");
const name = document.getElementById("name");
const address = document.getElementById("address");

// Add Event Listeners
requestForm.addEventListener("submit", submitForm);

function submitForm(e) {
  if (name.value == "" || address.value == "") {
    e.preventDefault();
  }
}

// Make Textarea resize according to its content
const mealDesc = document.getElementById("mealDesc");

mealDesc.addEventListener("input", e => {
  e.target.style.height = e.target.scrollHeight + "px";
});
/* ======================================================= */

// Add file name to html
const mealImageName = document.getElementById("mealImageName");
const mealImage = document.getElementById("mealImage");
const mealImagePlus = document.getElementById("meal-image-plus");

mealImage.addEventListener("change", e => {
  if (e.target.value) {
    mealImageName.innerText = e.target.value.split("\\").reverse()[0];
    mealImagePlus.innerHTML = "&#10004;";
    mealImagePlus.className = "active";
  } else {
    mealImageName.innerText = "برجاء إضافة صورة";
    mealImagePlus.innerText = "+";
    mealImagePlus.className = "plus";
  }
});
/* ======================================================= */

// Validate

// Getting DOM Element
const updateForm = document.getElementById("update-meal-form");
const mealName = document.getElementById("mealName");

// Add Event Listeners
updateForm.addEventListener("submit", submitForm);

function submitForm(e) {
  if (mealName.value == "" ) {
    e.preventDefault();
  }
}

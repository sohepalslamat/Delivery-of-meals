// Make Textarea resize according to its content
const mealDesc = document.getElementById("mealDesc");

mealDesc.addEventListener("input", e => {
  e.target.style.height = e.target.scrollHeight + "px";
});
/* ======================================================= */

// Add file name to html
const mealImageName = document.getElementById("mealImageName");
const mealImage = document.getElementById("mealImage");

mealImage.addEventListener("change", e => {
  mealImageName.innerText =
    e.target.value.split("\\").reverse()[0] || "برجاء إضافة صورة";
});

/* Functions */

/* function displayEditForm() {
  const editForm = document.getElementById("edit-form");
  const isHide = editForm.getAttribute("data-hide");

  if (isHide === "true") {
    editForm.classList.add("edit-form-hide");
  } else {
    editForm.classList.remove("edit-form-hide");
  }
} */

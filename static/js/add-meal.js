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

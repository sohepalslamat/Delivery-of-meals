renderMeals();
displayEditForm();

// Handle edit form
const addMealCancel = document.getElementById("add-meal-cancel");
addMealCancel.addEventListener("click", e => {
  e.preventDefault();

  const editForm = document.getElementById("edit-form");
  editForm.setAttribute("data-hide", "true");
  displayEditForm();
});

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
async function getData() {
  const data = await fetch("../static/db.json").then(data => data.json());

  return data;
}

async function renderMeals() {
  const mealsContainer = document.getElementsByClassName("meals-container")[0];

  // Get Data
  const data = await getData();

  data.forEach(mel => {
    // Create Meal container
    const meal = document.createElement("div");
    meal.id = mel.id;
    meal.className = "meal";

    // Create Meal Name
    const mealName = document.createElement("p");
    mealName.innerText = mel.mealName;
    meal.appendChild(mealName);

    // Create Meal Image
    const mealImage = document.createElement("img");
    mealImage.src = mel.mealImage;
    meal.appendChild(mealImage);

    // Create div container for buttons;
    const btnContainer = document.createElement("div");
    meal.appendChild(btnContainer);

    // Create Delete Button
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "delete-btn";
    deleteBtn.innerText = "حـــذف";
    btnContainer.appendChild(deleteBtn);

    // Create Edit Button
    const editBtn = document.createElement("button");
    editBtn.className = "edit-btn";
    editBtn.innerText = "تعديـــل";
    editBtn.addEventListener("click", e => {
      // get id of meal
      const id = e.target.parentNode.parentNode.id;
      addValuesToEditForm(id);

      const editForm = document.getElementById("edit-form");
      editForm.setAttribute("data-hide", "false");
      displayEditForm();
    });

    btnContainer.appendChild(editBtn);

    // Add meal to HTML
    mealsContainer.appendChild(meal);
  });
}

function displayEditForm() {
  const editForm = document.getElementById("edit-form");
  const isHide = editForm.getAttribute("data-hide");

  if (isHide === "true") {
    editForm.classList.add("edit-form-hide");
  } else {
    editForm.classList.remove("edit-form-hide");
  }
}

async function addValuesToEditForm(mealId) {
  // Get Meal
  const data = await getData();
  const meal = data.filter(meal => {
    return meal.id == mealId;
  })[0];

  if (meal) {
    const mealName = document.getElementById("mealName");
    const mealDesc = document.getElementById("mealDesc");
    const price = document.getElementById("price");
    const mealImageName = document.getElementById("mealImageName");

    // Add values of selected meal
    mealName.value = meal.mealName;
    mealDesc.value = meal.mealDesc;
    price.value = meal.price;
    mealImageName.innerText = meal.mealImage.split("/").reverse()[0];
  }
}

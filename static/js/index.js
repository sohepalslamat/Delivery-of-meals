// Allow only integer number for amount input
const amount = document.getElementById("amount");

amount.addEventListener("keydown", e => handleInValidInput(e));
/* ======================================================= */

/* FUNCTIONS */
function handleInValidInput(e) {
  const inValid = [107, 109, 110, 69];

  if (inValid.includes(e.keyCode)) {
    e.preventDefault();
  }
}

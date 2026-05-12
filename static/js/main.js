/* jshint esversion: 6 */

// Hidden message toggle

const noMessageToggle = document.querySelector("#no-message-toggle");
const previewForm = document.querySelector(".preview-form");

if (noMessageToggle && previewForm) {
  noMessageToggle.addEventListener("change", () => {
    previewForm.hidden = noMessageToggle.checked;
  });
}
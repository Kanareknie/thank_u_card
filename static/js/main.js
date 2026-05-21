/* jshint esversion: 6 */

// Hidden message toggle

const noMessageToggle = document.querySelector("#no-message-toggle");
const previewForm = document.querySelector(".preview-form");

if (noMessageToggle && previewForm) {
  noMessageToggle.addEventListener("change", () => {
    previewForm.hidden = noMessageToggle.checked;
  });
}

// Live preview updates
document.addEventListener("DOMContentLoaded", function () {
  const recipientInput = document.getElementById("id_recipient_name");
  const messageInput = document.getElementById("id_message");
  const noMessageCheckbox = document.getElementById("id_no_message");

  const recipientPreview = document.getElementById("live-recipient-preview");
  const messagePreview = document.getElementById("live-message-preview");
  const messageFields = document.getElementById("message-fields");

  const recipientCounter = document.getElementById("recipient-counter");
  const messageCounter = document.getElementById("message-counter");


  // Function to update character counters for recipient name and message fields
  function updateCharacterCounters() {
    if (recipientInput && recipientCounter) {
      recipientCounter.textContent = `${recipientInput.value.length} / 50`;
    }

    if (messageInput && messageCounter) {
      messageCounter.textContent = `${messageInput.value.length} / 300`;
    }
  }

  // Function to update the live preview based on form inputs
  // This function checks the current values of the recipient name, message, and no message checkbox,
  // and updates the preview elements accordingly. If the "No Message" checkbox is selected, it hides the message fields and shows a default message.
  function updateLivePreview() {
    if (!recipientPreview || !messagePreview) {
      return;
    }

    const recipientValue = recipientInput ? recipientInput.value.trim() : "";
    const messageValue = messageInput ? messageInput.value.trim() : "";
    const noMessageSelected = noMessageCheckbox ? noMessageCheckbox.checked : false;

    recipientPreview.textContent = recipientValue ? `Dear ${recipientValue}` : "";

    // If "No Message" is selected, show a default message and hide the message fields. Otherwise, show the user's message and ensure the message fields are visible.
    if (noMessageSelected) {
      messagePreview.textContent = "This card has no message.";
      if (messageFields) {
        messageFields.classList.add("hidden");
      }
    } else {
      messagePreview.textContent = messageValue || "Your message will appear here";
      if (messageFields) {
        messageFields.classList.remove("hidden");
      }
    }

    updateCharacterCounters();
  }

  // Add event listeners to the recipient name input, message textarea, and "No Message" checkbox to update the live preview whenever any of these inputs change.
  if (recipientInput) {
    recipientInput.addEventListener("input", updateLivePreview);
  }

  if (messageInput) {
    messageInput.addEventListener("input", updateLivePreview);
  }

  if (noMessageCheckbox) {
    noMessageCheckbox.addEventListener("change", updateLivePreview);
  }

  updateLivePreview();
});

// Auto-refresh page when background generation is in progress
document.addEventListener("DOMContentLoaded", function () {
  const progressBox = document.querySelector("[data-refresh='true']");

  if (progressBox) {
    setTimeout(function () {
      window.location.reload();
    }, 12000);
  }
});

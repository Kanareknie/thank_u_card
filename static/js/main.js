/* jshint esversion: 6 */


// Live preview updates
document.addEventListener("DOMContentLoaded", function () {
  const recipientInput = document.getElementById("id_recipient_name");
  const messageInput = document.getElementById("id_message");
  const noMessageCheckbox = document.getElementById("id_no_message");
  const clearMessageButton = document.getElementById("clear-message-button");

  const recipientPreview = document.getElementById("live-recipient-preview");
  const messagePreview = document.getElementById("live-message-preview");
  const messageFields = document.getElementById("message-fields");
  const cardMessageBox = document.querySelector(".card-message-box");
  
  const recipientCounter = document.getElementById("recipient-counter");
  const messageCounter = document.getElementById("message-counter");

  // Function to update character counters for recipient name and message fields
  function updateCharacterCounters() {
    if (recipientInput && recipientCounter) {
      recipientCounter.textContent = `${recipientInput.value.length} / 50`;
    }

    if (messageInput && messageCounter) {
      messageCounter.textContent = `${messageInput.value.length} / 200`;
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

    // If "No Message" is selected, show a default message and hide the message fields. 
    // Otherwise, show the user's message and ensure the message fields are visible.

    if (noMessageSelected) {
      if (cardMessageBox) {
        cardMessageBox.classList.add("hidden");
      }

      if (messageFields) {
        messageFields.classList.add("hidden");
      }
    } else {
      if (cardMessageBox) {
        cardMessageBox.classList.remove("hidden");
      }

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

  // Clear message button functionality: When the "Clear Message" button is clicked, 
  // it clears the message textarea and updates the live preview to reflect the change.
  if (clearMessageButton && messageInput) {
    clearMessageButton.addEventListener("click", function () {
      messageInput.value = "";
      updateLivePreview();
    });
  }

  updateLivePreview();

});

// Auto-refresh page when background generation is in progress
document.addEventListener("DOMContentLoaded", function () {
  const progressBox = document.querySelector("[data-refresh='true']");

  if (progressBox) {

    // Scroll to the top of the page to ensure the user sees the progress box, 
    // then set a timeout to refresh the page after 12 seconds, 
    // allowing time for the background generation process to complete 
    // and update the progress status.
    
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });

    setTimeout(function () {
      window.location.reload();
    }, 12000);
  }
});

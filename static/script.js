function showMessage(formId, type, text) {
  const messageContainer = document.querySelector(`#${formId} .message-container`);
  messageContainer.innerHTML = `<div class="message ${type}">${text}</div>`;
}

// Change Behaviour form
document.getElementById("changeBehaviour").addEventListener('submit', async (event) => {
  event.preventDefault();
  const systemPrompt = document.getElementById("Behaviour").value;
  const content = document.getElementById("Content").value;
  const roadmapFile = document.getElementById("roadmapFile").files[0];
  const overrideBehaviour = document.getElementById("overrideBehaviour").checked;
  const defaultPrompt = document.getElementById("defaultPrompt").value;

  let finalPrompt;
  if (overrideBehaviour) {
    finalPrompt = systemPrompt;
  } else {
    finalPrompt = `${defaultPrompt}\n\nAdditional instructions:\n${systemPrompt}`;
  }
  console.log(`final prommpt is ${finalPrompt}`)
  const changeBehaviourURL = `https://${BASE_URL}/change_behaviour`;
  
  const formData = new FormData();
  formData.append('systemPrompt', finalPrompt);
  formData.append('content', content);
  if (roadmapFile) {
    formData.append('roadmapFile', roadmapFile);
  }
  formData.append('overrideBehaviour', overrideBehaviour);

  try {
    const response = await fetch(changeBehaviourURL, {
      method: "POST",
      body: formData
    });
    
    const result = await response.json();
    if (!result.status || result.status !== "success") {
      showMessage("changeBehaviour", "error", result.detail);
    } else {
      showMessage("changeBehaviour", "success", "Behaviour Changed successfully!");
      
      // Update the paragraph with the new behavior prompt
      const currentBehaviorPromptElement = document.getElementById("currentBehaviorPrompt");
      currentBehaviorPromptElement.textContent = finalPrompt;
      
      // Update the hidden input with the new prompt
      document.getElementById("defaultPrompt").value = finalPrompt;
      
      // Optionally, you can add a visual indication that the text has been updated
      currentBehaviorPromptElement.classList.add("updated");
      setTimeout(() => {
        currentBehaviorPromptElement.classList.remove("updated");
      }, 3000);  // Remove the 'updated' class after 3 seconds
    }
  } catch (error) {
    showMessage("changeBehaviour", "error", "An error occurred. Please try again.");
  }
});

document.getElementById("overrideBehaviour").addEventListener('change', function() {
  const behaviourTextarea = document.getElementById("Behaviour");
  if (this.checked) {
    behaviourTextarea.placeholder = "Enter new behavior prompt to override default";
  } else {
    behaviourTextarea.placeholder = "Enter additional instructions to append to default prompt";
  }
});

// Quick Outbound Call form
document.getElementById("outboundCallForm").addEventListener("submit", async (event) => {
event.preventDefault();
const recipient = document.getElementById("recipient").value;
const outboundCallURL = `https://${BASE_URL}/start_outbound_call`;              

try {
  const response = await fetch(outboundCallURL, {
    method: "POST",
    headers: {"Content-Type": "application/x-www-form-urlencoded"},
    body: `to_phone=${encodeURIComponent(recipient)}`
  });
  const result = await response.json();
  if (!result.status || result.status !== "success") {
    showMessage("outboundCallForm", "error", result.detail);
  } else {
    showMessage("outboundCallForm", "success", "Call started successfully!");
  }
} catch (error) {
  showMessage("outboundCallForm", "error", "An error occurred. Please try again.");
}
});

// Zoom Meeting Call form
document.getElementById("zoomCallForm").addEventListener("submit", async (event) => {
event.preventDefault();
const meetingId = document.getElementById("meetingId").value;
const meetingPassword = document.getElementById("meetingPassword").value;
const outboundCallURL = `https://${BASE_URL}/start_outbound_zoom`;              

try {
  const response = await fetch(outboundCallURL, {
    method: "POST",
    headers: {"Content-Type": "application/x-www-form-urlencoded"},
    body: `meeting_id=${encodeURIComponent(meetingId)}&meeting_password=${encodeURIComponent(meetingPassword)}`
  });
  const result = await response.json();
  if (!result.status || result.status !== "success") {
    showMessage("zoomCallForm", "error", result.detail);
  } else {
    showMessage("zoomCallForm", "success", "Call started successfully!");
  }
} catch (error) {
  showMessage("zoomCallForm", "error", "An error occurred. Please try again.");
}
});
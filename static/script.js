const outboundCallForm = document.getElementById("outboundCallForm");
const zoomCallForm = document.getElementById("zoomCallForm");
const messageContainer = document.getElementById("messageContainer");
const changeBehaviour = document.getElementById("changeBehaviour");
const voiceSettings=document.getElementById("audioSettings");

function showMessage(type, text) {
    messageContainer.innerHTML = `<div class="message ${type}">${text}</div>`;
}

voiceSettings.addEventListener('submit', async (event) => {
  console.log("Request submitted to update the audio settings");
  event.preventDefault();
  const userId=document.getElementById("playHTUserId").value;
  const apiKey=document.getElementById("playHTApiKey").value;  
  const avatar=document.getElementById("avatar").value;
  console.log(`avatar id is ${avatar}`)
  console.log(`Got id ${userId}`);
  console.log(`Got api key ${apiKey}`);
  const playHTconfigURL=`https://${BASE_URL}/update_play_ht_config`;

  const formData = new FormData();
  formData.append('userId',userId);
  formData.append('apiKey',apiKey);
  formData.append('avatar',avatar);

  const response = await fetch(playHTconfigURL, {
    method: "POST",
    body: formData  // Send as FormData
  });

  const result = await response.json();
  console.log(result);
  if (!result.status || result.status !== "success") {
    showMessage("error", result.detail);
  } else {
    showMessage("success", "Audio Settings updated successfully!");
  }
})





changeBehaviour.addEventListener('submit', async (event) => {
  console.log("Request submitted for changing behaviour");
  event.preventDefault();
  const systemPrompt = document.getElementById("Behaviour").value;
  const content = document.getElementById("Content").value;
  console.log(`value of system prompt ${systemPrompt}`);
  console.log(`value of content ${content}`);
  const changeBehaviourURL = `https://${BASE_URL}/change_behaviour`;
  
  const formData = new FormData();
  formData.append('systemPrompt', systemPrompt);
  formData.append('content', content);

  const response = await fetch(changeBehaviourURL, {
    method: "POST",
    body: formData  // Send as FormData
  });
  
  const result = await response.json();
  console.log(result);
  if (!result.status || result.status !== "success") {
    showMessage("error", result.detail);
  } else {
    showMessage("success", "Behaviour Changed successfully!");
  }
});

outboundCallForm.addEventListener("submit", async (event) => {
  console.log("TEST")
  event.preventDefault();
  const recipient = document.getElementById("recipient").value;
  const outboundCallURL = `https://${BASE_URL}/start_outbound_call`;              
    const response = await fetch(outboundCallURL, {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: `to_phone=${encodeURIComponent(recipient)}`
    });
    const result = await response.json();
    console.log(result);
    if (!result.status || result.status !== "success") {
        showMessage("error", result.detail);
    } else {
        showMessage("success", "Call started successfully!");
    }
});

zoomCallForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const meetingId = document.getElementById("meetingId").value;
      const meetingPassword = document.getElementById("meetingPassword").value;
    const outboundCallURL = `https://${BASE_URL}/start_outbound_zoom`;              
      const response = await fetch(outboundCallURL, {
          method: "POST",
          headers: {"Content-Type": "application/x-www-form-urlencoded"},
          body: `meeting_id=${encodeURIComponent(meetingId)}&meeting_password=${encodeURIComponent(meetingPassword)}`
      });
      const result = await response.json();
      console.log(result);
      if (!result.status || result.status !== "success") {
          showMessage("error", result.detail);
      } else {
          showMessage("success", "Call started successfully!");
      }
  });

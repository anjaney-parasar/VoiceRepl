const outboundCallForm = document.getElementById("outboundCallForm");
const zoomCallForm = document.getElementById("zoomCallForm");
const messageContainer = document.getElementById("messageContainer");
const changeBehaviour = document.getElementById("changeBehaviour");


function showMessage(type, text) {
    messageContainer.innerHTML = `<div class="message ${type}">${text}</div>`;
}

changeBehaviour.addEventListener('submit', async (event) => {
  console.log("Request submitted for changing behaviour");
  event.preventDefault();
  const systemPrompt=document.getElementById("Behaviour").value;
  const content=document.getElementById("Content").value;
    const changeBehaviourURL="https://{{env_vars.BASE_URL}}/change_behaviour";
    const response = await fetch(changeBehaviourURL , {
        method: "POST",
        headers:{"Content-Type":"application/x-www-form-urlencoded"},
        body: { "systemPrompt":systemPrompt,
                "content":content }  
    });
    const result = await response.json();
    console.log(result);
    if (!result.status || result.status !== "success") {
      showMessage("error", result.detail);
  } else {
      showMessage("success", "Behaviour Changed successfully!");
  }

}
)

outboundCallForm.addEventListener("submit", async (event) => {
  console.log("TEST")
  event.preventDefault();
  const recipient = document.getElementById("recipient").value;
  const outboundCallURL = "https://{{env_vars.BASE_URL}}/start_outbound_call";              
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
    const outboundCallURL = "https://{{env_vars.BASE_URL}}/start_outbound_zoom";              
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

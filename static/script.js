function showMessage(formId, type, text) {
  const messageContainer = document.querySelector(`#${formId} .message-container`);
  messageContainer.innerHTML = `<div class="message ${type}">${text}</div>`;
}

const BASE_URL= document.getElementById("BASE_URL").value

// Set client Email
document.getElementById("clientEmail").addEventListener("submit", async (event) => {
  event.preventDefault();
  const clientEmail=document.getElementById('email').value;
  const addEmailURL=`https://${BASE_URL}/update_email`
  const formData= new FormData();
  if (clientEmail) formData.append('clientEmail',clientEmail)
  try {
    const response=await fetch(addEmailURL,{
      method:"POST",
      body:formData
    });

    const result = await response.json();
    if (!result.status || result.status !=="success"){
      showMessage("clientEmail", "error", result.detail);
    } else {
      showMessage("clientEmail","success","Client Email Added successfully!");
    }
  }
  catch(error){
    showMessage("clientEmail","error","An error occured. Please try again.")
  }
});




// Change Behaviour form
document.getElementById("changeBehaviour").addEventListener('submit', async (event) => {
  event.preventDefault();
  const systemPrompt = document.getElementById("Behaviour").value;
  const content = document.getElementById("Content").value;
  const roadmapFile = document.getElementById("roadmapFile").files[0];
  const overrideBehaviour = document.getElementById("overrideBehaviour").checked;
  const defaultPrompt = document.getElementById("defaultPrompt").value;

  if (!systemPrompt && !content && !roadmapFile) {
    showMessage("changeBehaviour", "error", "Please provide either a Behaviour Prompt or a Roadmap.");
    return;
  }

  let finalPrompt;
  if (overrideBehaviour && systemPrompt) {
    finalPrompt = systemPrompt;
  } else if (systemPrompt) {
    finalPrompt = `${defaultPrompt}\n\nAdditional instructions:\n${systemPrompt}`;
  } else {
    finalPrompt = defaultPrompt;
  }

  const changeBehaviourURL = `https://${BASE_URL}/change_behaviour`;
  
  const formData = new FormData();
  if (systemPrompt) formData.append('systemPrompt', finalPrompt);
  if (content) formData.append('content', content);
  if (roadmapFile) {
    formData.append('roadmapFile', roadmapFile);
    showMessage("changeBehaviour", "info", `Uploading file: ${roadmapFile.name}`);
  }
  formData.append('overrideBehaviour', overrideBehaviour);

  try {
    const response = await fetch(changeBehaviourURL, {
      method: "POST",
      body: formData
    });
    
    const result = await response.json();
    if (!result.status || result.status !== "success") {
      showMessage("changeBehaviour", "error", result.detail || "An error occurred");
    } else {
      let successMessage = "Behaviour/Roadmap updated successfully!";
      if (roadmapFile) {
        successMessage += ` File "${roadmapFile.name}" uploaded and processed.`;
      }
      showMessage("changeBehaviour", "success", successMessage);
      
      if (systemPrompt) {
        const currentBehaviorPromptElement = document.getElementById("currentBehaviorPrompt");
        currentBehaviorPromptElement.textContent = finalPrompt;
        document.getElementById("defaultPrompt").value = finalPrompt;
        currentBehaviorPromptElement.classList.add("updated");
        setTimeout(() => {
          currentBehaviorPromptElement.classList.remove("updated");
        }, 3000);
      }

      // Clear the file input and selected file name display
      document.getElementById('roadmapFile').value = '';
      document.getElementById('selectedFileName').textContent = '';
    }
  } catch (error) {
    showMessage("changeBehaviour", "error", "An error occurred. Please try again.");
  }
});


document.getElementById('roadmapFile').addEventListener('change', function(event) {
  const fileName = event.target.files[0]?.name;
  document.getElementById('selectedFileName').textContent = fileName ? fileName : '';
});

document.getElementById("overrideBehaviour").addEventListener('change', function() {
  const behaviourTextarea = document.getElementById("Behaviour");
  if (this.checked) {
    behaviourTextarea.placeholder = "Enter new behavior prompt to override default";
  } else {
    behaviourTextarea.placeholder = "Enter additional instructions to append to default prompt";
  }
});


// Audio Settings form
document.getElementById("audioSettings").addEventListener('submit', async (event) => {
  event.preventDefault();
  console.log('Sending the avatar  ')
  const avatar = document.getElementById("avatar").value;
  console.log(`avatar is ${avatar}`)
  // const voice_name= avatar.voice_name
  // const language_code = avatar.language_code
  
  // if ((userId || apiKey) && (!userId || !apiKey)){
  //   showMessage("audioSettings","error","Please provide both UserID and API key")
  //   return;
  // }


  const playHTconfigURL = `https://${BASE_URL}/update_play_ht_config`;
  
  const formData = new FormData();

  // if ( userId && apiKey) {
  //   formData.append('userId', userId);
  //   formData.append('apiKey', apiKey);
  // }
  if (avatar) {
    formData.append('avatar', avatar);
    // formData.append('voice_name',voice_name);
    // formData.append('language_code',language_code);
  }  

  
  try {
    const response = await fetch(playHTconfigURL, {
      method: "POST",
      body: formData
    });
  
    const result = await response.json();
    if (!result.status || result.status !== "success") {
      showMessage("audioSettings", "error", result.detail);
    } else {
      showMessage("audioSettings", "success", "Audio Settings updated successfully!");
    }
  } catch (error) {
    showMessage("audioSettings", "error", "An error occurred. Please try again.");
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
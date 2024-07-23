import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
BASE_URL = os.getenv("BASE_URL")

st.title("AI Solution Advisor")

st.header("Environment Variables")
env_vars = {
    "BASE_URL": BASE_URL,
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
    "DEEPGRAM_API_KEY": os.environ.get("DEEPGRAM_API_KEY"),
    "TWILIO_ACCOUNT_SID": os.environ.get("TWILIO_ACCOUNT_SID"),
    "TWILIO_AUTH_TOKEN": os.environ.get("TWILIO_AUTH_TOKEN"),
    "OUTBOUND_CALLER_NUMBER": os.environ.get("OUTBOUND_CALLER_NUMBER")
}


st.write(F"Paste the following link on twilio : https://{BASE_URL}/inbound_call")

for key, value in env_vars.items():
    st.checkbox(key, value=bool(value), disabled=True)

st.header("Behaviour and Roadmap")
with st.form("prompt_form"):
    system_prompt=st.text_area("Behaviour prompt")
    roadmap=st.text_area("Roadmap")
    submit_button=st.form_submit_button("Submit")

    if  submit_button:
        st.session_state['roadmap']=roadmap
        st.session_state['system_prompt']=system_prompt


st.header("Quick Outbound Call")
with st.form("outbound_call_form"):
    recipient = st.text_input("Recipient Phone Number")
    # system_instruction = st.text_area("System Instruction")
    # content_prompt = st.text_area("Content Prompt")
    submit_button = st.form_submit_button("Start Call")

    if submit_button:
        response = requests.post(
            f"https://{BASE_URL}/start_outbound_call",
            data={
                "to_phone": recipient,
                # "system_instruction": system_instruction,
                # "content_prompt": content_prompt
            }
        )
        if response.status_code == 200 and response.json().get("status") == "success":
            st.success("Call started successfully!")
        else:
            st.error(f"Error starting call: {response.text}")

st.header("Zoom Meeting Call")
with st.form("zoom_call_form"):
    meeting_id = st.text_input("Meeting ID")
    meeting_password = st.text_input("Meeting Passcode")
    zoom_submit_button = st.form_submit_button("Start Zoom Call")

    if zoom_submit_button:
        response = requests.post(
            f"https://{BASE_URL}/start_outbound_zoom",
            data={
                "meeting_id": meeting_id,
                "meeting_password": meeting_password
            }
        )
        if response.status_code == 200 and response.json().get("status") == "success":
            st.success("Zoom call started successfully!")
        else:
            st.error(f"Error starting Zoom call: {response.text}")
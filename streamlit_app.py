import streamlit as st
import requests
import os
from dotenv import load_dotenv
from server_manager import ServerManager
from roadmap import prompt, roadmap
import multiprocessing
import subprocess
import time
load_dotenv()

# Start FastAPI server
def start_fastapi_server():
    subprocess.Popen(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

# Wait for FastAPI server to start
def wait_for_fastapi():
    max_retries = 30
    for _ in range(max_retries):
        try:
            requests.get("http://localhost:8000")
            return True
        except requests.ConnectionError:
            time.sleep(1)
    return False

# Start FastAPI server when Streamlit app starts
start_fastapi_server()

# Wait for FastAPI server to start
if not wait_for_fastapi():
    st.error("Failed to start FastAPI server")
    st.stop()



VOICE_AVATARS = {
    "Default": "s3://voice-cloning-zero-shot/daab7575-42c8-48f1-b01c-ee4e3281fba7/original/manifest.json",
    "Delilah": "s3://voice-cloning-zero-shot/1afba232-fae0-4b69-9675-7f1aac69349f/delilahsaad/manifest.json",
    "Benton": "s3://voice-cloning-zero-shot/b41d1a8c-2c99-4403-8262-5808bc67c3e0/bentonsaad/manifest.json",
    "Navya": "s3://voice-cloning-zero-shot/e5df2eb3-5153-40fa-9f6e-6e27bbb7a38e/original/manifest.json",
    "Adolfo": "s3://voice-cloning-zero-shot/d82d246c-148b-457f-9668-37b789520891/adolfosaad/manifest.json"
    # Add more voice avatars as needed
}

# Load environment variables
BASE_URL = os.getenv("BASE_URL")

@st.cache_resource(show_spinner="Setting up the telephony server")
def get_server_manager():
    return ServerManager()

def update_behaviour():
    st.session_state['system_prompt']=st.session_state['system_prompt_input']
    st.session_state['content']=st.session_state['content_input']


def main():
    st.title("Visa Solution Advisor")

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


    #Overiding behaviour and roadmap
    if 'system_prompt' not in st.session_state:
        st.session_state['system_prompt']=prompt
    if 'content' not in st.session_state:
        st.session_state['content']=roadmap
    
    st.header("Behaviour and Roadmap")
    with st.form("prompt_form"):
        system_prompt_input=st.text_area("Behaviour prompt", value=st.session_state['system_prompt'], key='system_prompt_input')
        content_input=st.text_area("Roadmap",value=st.session_state['content'],  key='content_input')
        submit_button=st.form_submit_button("Submit", on_click=update_behaviour)

        if submit_button:
                response = requests.post(
                    f"https://{BASE_URL}/change_behaviour",
                    data={
                        "system_prompt": system_prompt_input,
                        "content": content_input
                    }
                )
                if response.status_code == 200 and response.json().get("status") == "success":
                    st.success("Behaviour changed successfully!")
                    st.session_state['system_prompt'] = system_prompt_input
                    st.session_state['content'] = content_input
                else:
                    st.error(f"Error changing behaviour: {response.text}")    
    
    
    if "play_ht_api_key" not  in st.session_state:
        st.session_state['play_ht_api_key']=os.getenv("PLAY_HT_API_KEY")
    if "play_ht_user_id" not in st.session_state:
        st.session_state['play_ht_user_id']=os.getenv("PLAY_HT_USER_ID")    
    
    st.header("Audio Settings")
    with st.form("play_ht_credentials_form"):
        play_ht_api_key = st.text_input("Play.ht API Key", value=st.session_state.get('play_ht_api_key', ''), type="password")
        play_ht_user_id = st.text_input("Play.ht User ID", value=st.session_state.get('play_ht_user_id', ''))
        selected_avatar = st.selectbox("Select Voice Avatar", options=list(VOICE_AVATARS.keys()), index=0)
        submit_button = st.form_submit_button("Update Credentials and Voice")

        if submit_button:
            response = requests.post(
                f"https://{BASE_URL}/update_play_ht_config",
                data={
                    "api_key": play_ht_api_key,
                    "user_id": play_ht_user_id,
                    "voice_id": VOICE_AVATARS[selected_avatar]
                }
            )
            if response.status_code == 200 and response.json().get("status") == "success":
                st.success("Play.ht configuration updated successfully!")
                st.session_state['play_ht_api_key'] = play_ht_api_key
                st.session_state['play_ht_user_id'] = play_ht_user_id
                st.session_state['play_ht_voice_id'] = VOICE_AVATARS[selected_avatar]
            else:
                st.error(f"Error updating Play.ht configuration: {response.text}")

    # server_manager = get_server_manager()
    # server_manager.start_server()

    st.header("For Inbound calls")
    st.write("Give a call at +18159402559")

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

    # import atexit
    # atexit.register(lambda: fastapi_process.terminate())


if __name__ == "__main__":
    main()
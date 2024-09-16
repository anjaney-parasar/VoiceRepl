import logging
import json
from fastapi import FastAPI, Request, Form
from fastapi import UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pdf_reader import pdf_reader
import uvicorn
import sys 
import os
from dotenv import load_dotenv
load_dotenv()
from roadmap import prompt
print("Transcript URL is",os.getenv("TRANSCRIPT_CALLBACK_URL"))
print("Open AI env key is ", os.getenv("OPENAI_API_KEY"))


# print("OpenAIAPI key is ",os.getenv("OPENAI_API_KEY"))

# VOICE_AVATARS = {
#     "Navya Fast": "s3://voice-cloning-zero-shot/e5df2eb3-5153-40fa-9f6e-6e27bbb7a38e/original/manifest.json",
#     "Delilah Slow": "s3://voice-cloning-zero-shot/1afba232-fae0-4b69-9675-7f1aac69349f/delilahsaad/manifest.json",
#     "Benton Fast": "s3://voice-cloning-zero-shot/b41d1a8c-2c99-4403-8262-5808bc67c3e0/bentonsaad/manifest.json",
#     "Adolfo Medium": "s3://voice-cloning-zero-shot/d82d246c-148b-457f-9668-37b789520891/adolfosaad/manifest.json",
#     "AY Medium":"",
#     "Charlotte (Narrative)":"s3://voice-cloning-zero-shot/a59cb96d-bba8-4e24-81f2-e60b888a0275/charlottenarrativesaad/manifest.json",
#     "Dylan":"s3://voice-cloning-zero-shot/3a831d1f-2183-49de-b6d8-33f16b2e9867/dylansaad/manifest.json",
#     "Susan (Adversting)":"s3://voice-cloning-zero-shot/f6594c50-e59b-492c-bac2-047d57f8bdd8/susanadvertisingsaad/manifest.json",
#     "Olivia - Canadian (Advertising)":"s3://voice-cloning-zero-shot/9fc626dc-f6df-4f47-a112-39461e8066aa/oliviaadvertisingsaad/manifest.json",
#     "Micah (Smooth)":"s3://voice-cloning-zero-shot/a5cc7dd9-069c-4fe8-9ae7-0c4bae4779c5/micahsaad/manifest.json",
#     "Samuel (Slow Tempo)":"s3://voice-cloning-zero-shot/36e9c53d-ca4e-4815-b5ed-9732be3839b4/samuelsaad/manifest.json"
#     # Add more voice avatars as needed
# }


VOICE_AVATARS={
   "Ezinne":{"language_code":"en-NG","voice_name":"en-NG-EzinneNeural"},
   "Abeo":{"language_code":"en-NG","voice_name":"en-NG-AbeoNeural"},
   "Neerja":{"language_code":"en-IN","voice_name":"en-IN-NeerjaNeural"},
   "Prabhat":{"language_code":"en-IN","voice_name":"en-IN-PrabhatNeural"},
   "Ananya":{"language_code":"en-IN","voice_name":"en-IN-AnanyaNeural"},
   "Ava":{"language_code":"en-US","voice_name":"en-US-AvaNeural"},
   "Emma":{"language_code":"en-US","voice_name":"en-US-EmmaNeural"},
   "Jason":{"language_code":"en-US","voice_name":"en-US-JasonNeural"},
   "Sara":{"language_code":"en-US","voice_name":"en-US-SaraNeural"},
   "Tony":{"language_code":"en-US","voice_name":"en-US-TonyNeural"}
}

from vocode.logging import configure_pretty_logging
from events_manager import EventsManager

import asyncio

from transcriber import TRANS_CONFIG
from synthesizer import SYNTH_CONFIG
from agent import AGENT_CONFIG
from twilio import TWILIO_CONFIG, TWILIO_PHONE

from vocode.streaming.telephony.conversation.outbound_call import OutboundCall
from vocode.streaming.telephony.conversation.zoom_dial_in import ZoomDialIn
from vocode.streaming.telephony.server.base import TwilioInboundCallConfig, TelephonyServer
from vocode.streaming.synthesizer.play_ht_synthesizer_v2 import PlayHtSynthesizerConfig

from speller_agent import SpellerAgentFactory, SpellerAgentConfig

from config import BASE_URL


import os
from memory_config import config_manager
from dotenv import load_dotenv
load_dotenv()

configure_pretty_logging()

from typing import Optional

app = FastAPI(docs_url=None)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

CONFIG_MANAGER = config_manager  #RedisConfigManager()

events_manager=EventsManager(email="anjaneyparasar14@gmail.com")

# Let's create and expose that TelephonyServer.
telephony_server = TelephonyServer(
  base_url=BASE_URL,
  config_manager=CONFIG_MANAGER,
  inbound_call_configs=[
    TwilioInboundCallConfig(url="/inbound_call",
                      agent_config=AGENT_CONFIG,
                      twilio_config=TWILIO_CONFIG,
                      synthesizer_config=SYNTH_CONFIG,
                      transcriber_config=TRANS_CONFIG
                      )
  ],
  events_manager=events_manager
  # logger=logger,

)


@app.post("/update_email")
async def update_email(clientEmail:str=Form(...)):
   print("Entering  into update email endpoint")
   global events_manager
   events_manager.email=clientEmail
   print("Email changed successfully")
   return {"status":"success","message":f"Email updated to {clientEmail}"}


app.include_router(telephony_server.get_router())

# OutboundCall asks Twilio to call to_phone using our Twilio phone number
# and open an audio stream to our TelephonyServer.
async def start_outbound_call(to_phone: Optional[str]):
  if to_phone:
    outbound_call = OutboundCall(base_url=BASE_URL,
                                 to_phone=to_phone,
                                 from_phone=TWILIO_PHONE,
                                 config_manager=CONFIG_MANAGER,
                                 agent_config=AGENT_CONFIG,
                                 telephony_config=TWILIO_CONFIG,
                                 synthesizer_config=SYNTH_CONFIG,
                                 transcriber_config=TRANS_CONFIG
                                 )
    await outbound_call.start()


# Before we get started, you'll need a premium Zoom account that supports dial-in:
# https://zoom.us/zoomconference

ZOOM_NUMBER = "+15642172000"  # Zoom's San Jose number

async def start_outbound_zoom(meeting_id: Optional[str],
                        meeting_password: Optional[str]):
  if meeting_id and meeting_password:
    call = ZoomDialIn(zoom_meeting_id=meeting_id,
                      zoom_meeting_password=meeting_password,
                      base_url=BASE_URL,
                      config_manager=CONFIG_MANAGER,
                      zoom_number=ZOOM_NUMBER,
                      from_phone=TWILIO_PHONE,
                      agent_config=AGENT_CONFIG,
                      synthesizer_config=SYNTH_CONFIG,
                      twilio_config=TWILIO_CONFIG,
                      transcriber_config=TRANS_CONFIG
                      )
    await call.start()


# Expose the starter webpage
@app.get("/")
async def root(request: Request):
  env_vars = {
    "BASE_URL": BASE_URL,
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
    "DEEPGRAM_API_KEY": os.environ.get("DEEPGRAM_API_KEY"),
    "TWILIO_ACCOUNT_SID": os.environ.get("TWILIO_ACCOUNT_SID"),
    "TWILIO_AUTH_TOKEN": os.environ.get("TWILIO_AUTH_TOKEN"),
    "OUTBOUND_CALLER_NUMBER": os.environ.get("OUTBOUND_CALLER_NUMBER")
  }
  # print("Got env vairables")

  return templates.TemplateResponse("index.html", {
    "request": request,
    "env_vars": env_vars,
    "avatars":VOICE_AVATARS, 
    "prompt":prompt
  })


@app.post("/change_behaviour")
async def change_behaviour(
    request: Request,
    systemPrompt: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    roadmapFile: Optional[UploadFile] = File(None),
    overrideBehaviour: bool = Form(False)
):  
    global AGENT_CONFIG
    
    if not systemPrompt and not content and not roadmapFile:
        return {"status": "error", "detail": "Please provide either a Behaviour Prompt or a Roadmap."}

    full_prompt = ""
    if systemPrompt:
        full_prompt += systemPrompt

    if content:
        full_prompt += ("\n\n" + content) if full_prompt else content

    if roadmapFile:
        file_content = await roadmapFile.read()
        if roadmapFile.filename.lower().endswith('.pdf'):
           roadmap_text=pdf_reader(file_content)
        else:
           roadmap_text= file_content.decode('utf-8')   
        
        full_prompt += ("\n\n" + roadmap_text) if full_prompt else roadmap_text

    AGENT_CONFIG.prompt_preamble = full_prompt

    return {
        "status": "success",
        "message": "Behaviour/Roadmap updated successfully",
        "updated_prompt": full_prompt
    }    

@app.post("/update_play_ht_config")
async def update_play_ht_config(
    # systemPrompt: Optional[str] = Form(None),
    # content: Optional[str] = Form(None),
    apiKey: Optional[str] = Form(None),
    userId: Optional[str] = Form(None),
    avatar: Optional[str] = Form(None)
):
    global SYNTH_CONFIG
    print("avatar is ", avatar)
    
    print("type of avatar ", type(avatar))
    avatar_json_string = avatar.replace("'", '"')
    avatar=json.loads(avatar_json_string)
    
    print("language code is ", avatar['language_code'])
    print("user id is ", userId)
    print("apiKey is ", apiKey)
    SYNTH_CONFIG.voice_name=avatar['voice_name']
    SYNTH_CONFIG.language_code=avatar['language_code']
    # if userId and apiKey:
    #   SYNTH_CONFIG = PlayHtSynthesizerConfig.from_telephone_output_device(
    #       api_key=apiKey,
    #       user_id=userId,
    #       voice_id=avatar,
    #   )
    # else:
    #    apiKey=os.getenv("PLAY_HT_API_KEY")
    #    userId=os.getenv("PLAY_HT_USER_ID")
    #    print("sending avatar to synth config")
    #    SYNTH_CONFIG = PlayHtSynthesizerConfig.from_telephone_output_device(
    #       api_key=apiKey,
    #       user_id=userId,
    #       voice_id=avatar,
    #   )
    
    print("sending avatar to synth config")
    return {"status": "success"}

@app.post("/add_client_email")
async def client_email():
   return {"status":"success"}

@app.post("/add_transcript")
async def transcript():
    print("FULL TRANSCRIPT OF THE CALL: ")
    return {"status": "success"}


@app.post("/start_outbound_call")
async def api_start_outbound_call(to_phone: Optional[str] = Form(None)):
  await start_outbound_call(to_phone)
  return {"status": "success"}

@app.post("/start_outbound_zoom")
async def api_start_outbound_zoom(
    meeting_id: Optional[str] = Form(None),
    meeting_password: Optional[str] = Form(None)):
  await start_outbound_zoom(meeting_id, meeting_password)
  return {"status": "success"}



# def run_fastapi(port=8000):
#     uvicorn.run(app, host="127.0.0.1", port=port)

# uvicorn.run(app, host="0.0.0.0", port=3000)

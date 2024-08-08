import logging
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys 

# from vocode.logging import configure_pretty_logging
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

import os
from memory_config import config_manager
from dotenv import load_dotenv
load_dotenv()

# configure_pretty_logging()

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
# templates = Jinja2Templates(directory="templates")

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# First we will open up our TelephonyServer, which opens a path at
# our BASE_URL. Once we have a path, we can request a call from
# Twilio to Zoom's dial-in service or any phone number.

# We need a base URL for Twilio to talk to:
# If you're self-hosting and have an open IP/domain, set it here or in your env.
BASE_URL = os.getenv("BASE_URL")
print(BASE_URL)


# If neither of the above are true, we need a tunnel.
if not BASE_URL:
  from pyngrok import ngrok
  ngrok_auth = os.environ.get("NGROK_AUTH_TOKEN")
  if ngrok_auth is not None:
    ngrok.set_auth_token(ngrok_auth)
  port = sys.argv[sys.argv.index("--port") +
                  1] if "--port" in sys.argv else 3000

  # Open a ngrok tunnel to the dev server
  BASE_URL = ngrok.connect(port).public_url.replace("https://", "")
  logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(
    BASE_URL, port))

# We store the state of the call in memory, but you can also use Redis.
# https://docs.vocode.dev/telephony#accessing-call-information-in-your-agent
CONFIG_MANAGER = config_manager  #RedisConfigManager()


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
  events_manager=EventsManager()
  # logger=logger,

)
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

  # return templates.TemplateResponse("index.html", {
  #   "request": request,
  #   "env_vars": env_vars,
  # })


@app.post("/change_behaviour")
async def change_behaviour(
    system_prompt: str = Form(...),
    content: str = Form(...)
):
    global AGENT_CONFIG
    full_prompt = system_prompt + content
    AGENT_CONFIG.prompt_preamble = full_prompt
    return {"status": "success"}

@app.post("/update_play_ht_config")
async def update_play_ht_config(
    api_key: str = Form(...),
    user_id: str = Form(...),
    voice_id: str = Form(...)
):
    global SYNTH_CONFIG
    SYNTH_CONFIG = PlayHtSynthesizerConfig.from_telephone_output_device(
        api_key=api_key,
        user_id=user_id,
        voice_id=voice_id,
    )
    return {"status": "success"}

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

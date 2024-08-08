from vocode.streaming.models.agent import ChatGPTAgentConfig
from speller_agent import SpellerAgentFactory, SpellerAgentConfig
from vocode.streaming.models.message import BaseMessage
import streamlit as st
from roadmap import full_prompt

# system_prompt=st.session_state['system_prompt']
# content=st.session_state['content']
# full_prompt=system_prompt+content

def get_full_prompt():
    system_prompt = st.session_state.get('system_prompt', '')
    content = st.session_state.get('content', '')
    return system_prompt + content

AGENT_CONFIG = ChatGPTAgentConfig(
    initial_message=BaseMessage(text="Hey there! Am I audible?"),
    prompt_preamble=get_full_prompt(),
    allow_agent_to_be_cut_off=True,
    end_conversation_on_goodbye=True,
    send_filler_audio=True,
    goodbye_phrases=['bye','goodbye'],
    interrupt_sensitivity="high",
)

# AGENT_CONFIG=SpellerAgentConfig(
#                 initial_message=BaseMessage(
#                     text="im a speller agent, say something to me and ill spell it out for you"
#                 ),
#                 generate_responses=True
#                 )

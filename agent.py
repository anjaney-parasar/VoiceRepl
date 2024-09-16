from vocode.streaming.models.agent import ChatGPTAgentConfig
from speller_agent import SpellerAgentFactory, SpellerAgentConfig
from vocode.streaming.models.message import BaseMessage
from roadmap import full_prompt


from vocode.streaming.models.agent import CutOffResponse , FillerAudioConfig


filler_audio_config=FillerAudioConfig(silence_threshold_seconds=0.1,
                                      use_phrases=True,
                                      )

cutoff_response=CutOffResponse()

# system_prompt=st.session_state['system_prompt']
# content=st.session_state['content']
# full_prompt=system_prompt+content

AGENT_CONFIG = ChatGPTAgentConfig(
    initial_message=BaseMessage(text="Hey there! Am I audible?"),
    prompt_preamble=full_prompt,
    allow_agent_to_be_cut_off=True,
    end_conversation_on_goodbye=True,
    # send_filler_audio=filler_audio_config,
    goodbye_phrases=['bye','goodbye'],
    interrupt_sensitivity="high",
    # cut_off_response=cutoff_response ,

)

# AGENT_CONFIG=SpellerAgentConfig(
#                 initial_message=BaseMessage(
#                     text="im a speller agent, say something to me and ill spell it out for you"
#                 ),
#                 generate_responses=True
#                 )

import os

from vocode.streaming.models.synthesizer import ElevenLabsSynthesizerConfig, StreamElementsSynthesizerConfig
from vocode.streaming.synthesizer.play_ht_synthesizer_v2 import PlayHtSynthesizerV2
from vocode.streaming.synthesizer.play_ht_synthesizer_v2 import PlayHtSynthesizerConfig
import streamlit as st





def get_play_ht_config():
    return {
        "api_key": st.session_state.get('play_ht_api_key', os.getenv("PLAY_HT_API_KEY")),
        "user_id": st.session_state.get('play_ht_user_id', os.getenv("PLAY_HT_USER_ID")),
        "voice_id": st.session_state.get('play_ht_voice_id', 's3://voice-cloning-zero-shot/daab7575-42c8-48f1-b01c-ee4e3281fba7/original/manifest.json')
    }

def get_synth_config():
    config = get_play_ht_config()
    return PlayHtSynthesizerConfig.from_telephone_output_device(
        api_key=config['api_key'],
        user_id=config['user_id'],
        voice_id=config['voice_id'],
    )

SYNTH_CONFIG = get_synth_config()
# SYNTH_CONFIG = StreamElementsSynthesizerConfig.from_telephone_output_device()

# SYNTH_CONFIG = ElevenLabsSynthesizerConfig.from_telephone_output_device(
#   api_key=os.getenv("ELEVEN_LABS_API_KEY") or "<your EL token>")

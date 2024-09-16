import os

from vocode.streaming.models.synthesizer import ElevenLabsSynthesizerConfig, StreamElementsSynthesizerConfig
from vocode.streaming.synthesizer.play_ht_synthesizer_v2 import PlayHtSynthesizerV2
from vocode.streaming.synthesizer.play_ht_synthesizer_v2 import PlayHtSynthesizerConfig

# from vocode.streaming.synthesizer.google_synthesizer import GoogleSynthesizer, GoogleSynthesizerConfig
from vocode.streaming.synthesizer.azure_synthesizer import AzureSynthesizerConfig
# from vocode.streaming.synthesizer.gtts_synthesizer import GTTSSynthesizerConfig, GTTSSynthesizer


SYNTH_CONFIG=AzureSynthesizerConfig.from_telephone_output_device(
    voice_name="en-NG-EzinneNeural",
    language_code="en-NG",
)


# SYNTH_CONFIG=GoogleSynthesizerConfig.from_telephone_output_device(
#     language_code="en-US",
#     voice_name="n-US-Neural2-I",
#     pitch=0,
#     speaking_rate=1.2
# )
# SYNTH_CONFIG=GTTSSynthesizerConfig(sampling_rate=,
#                                    audio_encoding=)

def get_play_ht_config():
    return {
        "api_key": os.getenv("PLAY_HT_API_KEY"),
        "user_id":  os.getenv("PLAY_HT_USER_ID"),
        "voice_id": 's3://voice-cloning-zero-shot/daab7575-42c8-48f1-b01c-ee4e3281fba7/original/manifest.json'
    }

def get_synth_config():
    config = get_play_ht_config()
    return PlayHtSynthesizerConfig.from_telephone_output_device(
        api_key=config['api_key'],
        user_id=config['user_id'],
        voice_id=config['voice_id'],
    )

# SYNTH_CONFIG = get_synth_config()
# SYNTH_CONFIG = StreamElementsSynthesizerConfig.from_telephone_output_device()

# SYNTH_CONFIG = ElevenLabsSynthesizerConfig.from_telephone_output_device(
#   api_key=os.getenv("ELEVEN_LABS_API_KEY") or "<your EL token>")

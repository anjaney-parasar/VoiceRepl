from vocode.streaming.transcriber.deepgram_transcriber import DeepgramEndpointingConfig

from vocode.streaming.models.transcriber import (
    DeepgramTranscriberConfig,
    PunctuationEndpointingConfig,
)

from vocode.streaming.models.transcriber import (
          RevAITranscriberConfig, 
          WhisperCPPTranscriberConfig,
          EndpointingConfig,
          AssemblyAITranscriberConfig,
          GoogleTranscriberConfig,
          GladiaTranscriberConfig)

# TRANS_CONFIG=AssemblyAITranscriberConfig.from_telephone_input_device(
#                                     #  sampling_rate=8000,
#                                     #  audio_encoding='mulaw',
#                                     #  chunk_size=320,
#                                     # endpointing_config=EndpointingConfig(),
#                                     # libname = "whisper.dll",
#                                     # fname_model="ggml-base.bin"
#                                      )
#                 )

TRANS_CONFIG=GoogleTranscriberConfig.from_telephone_input_device(
             )


# TRANS_CONFIG=GoogleTranscriberConfig.from_telephone_input_device(endpointing_config=EndpointingConfig(),
#                                     #  sampling_rate=8000,
#                                     #  audio_encoding="linear16",
#                                     #  chunk_size=320
#                                      )

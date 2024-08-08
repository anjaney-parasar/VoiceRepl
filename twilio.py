import os
from vocode.streaming.telephony.server.base import TwilioInboundCallConfig, TelephonyServer
from vocode.streaming.models.telephony import TwilioConfig
# Now we need a Twilio account and number from which to make our call.
# You can make an account here: https://www.twilio.com/docs/iam/access-tokens#step-2-api-key
TWILIO_CONFIG = TwilioConfig(
  account_sid=os.getenv("TWILIO_ACCOUNT_SID") or "<your twilio account sid>",
  auth_token=os.getenv("TWILIO_AUTH_TOKEN") or "<your twilio auth token>",
)

# You can use your free number of buy a premium one here:
# https://www.twilio.com/console/phone-numbers/search
# Once you have one, set it here or in your env.
TWILIO_PHONE = os.getenv("OUTBOUND_CALLER_NUMBER")


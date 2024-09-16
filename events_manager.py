import os
import typing
from typing import Optional

# Import all required utils
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import TranscriptCompleteEvent
from vocode.streaming.utils import events_manager

import httpx

class EventsManager(events_manager.EventsManager):

    def __init__(self,email):
        super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])
        self.email=email

    async def handle_event(self, event: Event):
        if event.type == EventType.TRANSCRIPT_COMPLETE:
            transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
            
            # Prepare the data to be sent
            data = {
                "email":self.email,
                "conversation_id": transcript_complete_event.conversation_id,
                "user_id": 1,  # demo user id
                "transcript": transcript_complete_event.transcript.to_string()
            }

            # URL of the webhook endpoint you want to send the data to
            # webhook_url = os.environ.get("TRANSCRIPT_CALLBACK_URL")
            BASE_URL=os.getenv("BASE_URL")
            complete_url=os.getenv("TRANSCRIPT_CALLBACK_URL")
            make_url="https://hook.eu2.make.com/c1e8g64lgtwo2zqeija4xfnejyt6tmnt"
            # complete_url=f"https://{BASE_URL}/events"
            # Make the async HTTP POST request
            async with httpx.AsyncClient() as client:
                response = await client.post(complete_url, json=data)
                summary_res= await client.post(make_url, json=data)

                # Handle the response as needed (e.g., check for success or failure)
                if response.status_code == 201:
                    print("Transcript sent successfully.")
                else:
                    print("Failed to send transcript.")
                
                if summary_res.status_code==200:
                    print(f"Summary sent successfully over mail to {self.email}  ")
                else:
                    print("Failed to send meeting summary over mail")
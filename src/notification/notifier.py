# src/notification/notifier.py

from dotenv import load_dotenv
import os
from twilio.rest import Client

class Notifier:
    """
    Sends WhatsApp notifications via Twilio using credentials
    pulled securely from environment variables (.env file).
    """
    def __init__(self):
        # Load all entries from .env into os.environ
        load_dotenv()

        # Read Twilio credentials from environment
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token  = os.getenv("TWILIO_AUTH_TOKEN")
        if not account_sid or not auth_token:
            raise EnvironmentError(
                "Twilio ACCOUNT_SID or AUTH_TOKEN not found in environment variables."
            )

        # Initialize the Twilio REST client
        self.client = Client(account_sid, auth_token)

        # Read WhatsApp numbers from environment
        self.from_whatsapp = os.getenv("TWILIO_FROM_WHATSAPP")
        self.to_whatsapp   = os.getenv("TWILIO_TO_WHATSAPP")
        if not self.from_whatsapp or not self.to_whatsapp:
            raise EnvironmentError(
                "TWILIO_FROM_WHATSAPP or TWILIO_TO_WHATSAPP not set in environment variables."
            )

    def send_whatsapp(self, message: str):
        """
        Sends a WhatsApp message via Twilio.
        """
        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.from_whatsapp,
                to=self.to_whatsapp
            )
            print(f"WhatsApp message sent: {msg.sid}")
        except Exception as e:
            print(f"Notification error: {e}")


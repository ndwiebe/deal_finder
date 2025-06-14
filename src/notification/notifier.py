# WhatsApp notifier stub
from twilio.rest import Client

class Notifier:
    """
    Sends WhatsApp notifications via Twilio.
    """
    def __init__(self, config: dict):
        self.client = Client(config['account_sid'], config['auth_token'])
        self.from_whatsapp = config['from_whatsapp']
        self.to_whatsapp = config['to_whatsapp']

    def send_whatsapp(self, message: str):
        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.from_whatsapp,
                to=self.to_whatsapp
            )
            print(f"WhatsApp message sent: {msg.sid}")
        except Exception as e:
            print(f"Notification error: {e}")

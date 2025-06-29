from twilio.rest import Client
import os
import dotenv
dotenv.load_dotenv()

class Message:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, body='Ahoy 👋', to='+18777804236'):
        message = self.client.messages.create(
            messaging_service_sid=os.getenv("TWILIO_MESSAGING_SERVICE_SID"),
            body=body,
            to=to
        )
        print(message.status)
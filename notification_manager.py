from twilio.rest import Client
class NotificationManager:
    def __init__(self, account_sid, auth_token, from_whatsapp_number, to_whatsapp_number):
        self.client = Client(account_sid, auth_token)
        self.from_whatsapp_number = from_whatsapp_number
        self.to_whatsapp_number = to_whatsapp_number

    def send_price_alert(self, current_price , destination_city, departure_date):
        message_body = (
            f"Low price alert! ✈️\n"
            f"Only £{current_price} to fly to {destination_city}!\n"
            f"Departure: {departure_date}"
        )
        
        message = self.client.messages.create(
            body=message_body,
            from_=f'whatsapp:{self.from_whatsapp_number}',
            to=f'whatsapp:{self.to_whatsapp_number}'
        )
        print(f"Message sent! SID: {message.sid}")


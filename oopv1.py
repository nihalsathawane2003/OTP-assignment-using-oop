import random
import smtplib
from twilio.rest import Client

class OTPGenerator:
    def __init__(self, sender):
        self.sender = sender

    def generate_otp(self):
        """Generate a random OTP."""
        return ''.join([str(random.randint(0, 9)) for _ in range(4)])

    def send_otp(self, recipient, message):
        """Send OTP using the specified sender."""
        if self.sender.validate(recipient):
            self.sender.send_otp(recipient, self.generate_otp(), message)
        else:
            print(f"Invalid {self.sender.name.lower()} address.")

    @staticmethod
    def validate_email(email):
        """Validate the email format."""
        return "@gmail" in email and "." in email

    @staticmethod
    def validate_mobile(mobile):
        """Validate the mobile number format."""
        return len(mobile) == 10 and mobile.isdigit()


class CommunicationService:
    def validate(self, identifier):
        raise NotImplementedError("Subclasses must implement this method.")

    def send_otp(self, recipient, otp, message):
        raise NotImplementedError("Subclasses must implement this method.")


class SmtpServer(CommunicationService):
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.name = "Email"

    def validate(self, email):
        return OTPGenerator.validate_email(email)

    def send_otp(self, recipient, otp, message):
        """Send an email with the OTP using the SMTP server."""
        server = smtplib.SMTP(self.host, self.port)
        server.starttls()
        server.login(self.username, self.password)
        msg = f'Hello, your OTP is {otp}\n{message}'
        server.sendmail(self.username, recipient, msg)
        server.quit()


class TwilioClient(CommunicationService):
    def __init__(self, account_sid, auth_token, twilio_number):
        self.client = Client(account_sid, auth_token)
        self.twilio_number = twilio_number
        self.name = "SMS"

    def validate(self, mobile):
        return OTPGenerator.validate_mobile(mobile)

    def send_otp(self, recipient, otp, message):
        """Send an SMS with the OTP using the Twilio client."""
        message = self.client.messages.create(
            body=f'Hello, your OTP is {otp}\n{message}',
            from_=self.twilio_number,
            to=recipient
        )

if __name__ == "__main__":
    account_sid = 'AC32e472ca099fb7da6e850f8f9dd54e17'
    auth_token = 'e391f32bd79bd5b6e9094cc7f8db5f89'
    twilio_number = '+15132179720'
    target_number = '+917875808821'

    smtp_server = SmtpServer('smtp.gmail.com', 587, 'hanumanj2k3@gmail.com', 'iqvuzodoqtsvlfks')
    twilio_client = TwilioClient(account_sid, auth_token, twilio_number)

    otp_generator_smtp = OTPGenerator(smtp_server)
    otp_generator_twilio = OTPGenerator(twilio_client)

    email_address = "nihalsathawane2003@gmail.com"
    otp_generator_smtp.send_otp(email_address, 'Please do not share the OTP with anyone.\nThis is a system-generated mail, so do not reply.')

    mobile_number = "7875808821"
    otp_generator_twilio.send_otp(mobile_number, 'Please do not share the OTP with anyone.\nThis is a system-generated message, so do not reply.')

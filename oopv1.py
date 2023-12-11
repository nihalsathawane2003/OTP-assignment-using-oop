import random
import smtplib
from twilio.rest import Client
  # Assuming keys.py contains necessary Twilio credentials

class OTPGenerator:
    def __init__(self, account_sid, auth_token, twilio_number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_number=twilio_number

    def generate_otp(self):
        """Generate a random OTP."""
        return ''.join([str(random.randint(0, 9)) for _ in range(4)])

    def send_otp_over_email(self, email):
        """Send OTP over email to the specified email address."""
        if self.validate_email(email):
            # Creating a collaboration with SmtpServer class for email sending
            smtp_server = SmtpServer('smtp.gmail.com', 587, 'hanumanj2k3@gmail.com', 'iqvuzodoqtsvlfks')
            smtp_server.send_email(email, self.generate_otp())
            print(f"OTP is sent to {email} via email.")
        else:
            print("Invalid email address.")

    def send_otp_over_mobile(self, mobile):
        """Send OTP over mobile to the specified mobile number."""
        if self.validate_mobile(mobile):
            # Creating a collaboration with TwilioClient class for SMS sending
            twilio_client = TwilioClient(self.account_sid, self.auth_token,self.twilio_number)
            twilio_client.send_sms(mobile, self.generate_otp())
            print(f"OTP is sent to {mobile} via mobile.")
        else:
            print("Invalid mobile number.")

    @staticmethod
    def validate_email(email):
        """Validate the email format."""
        return "@gmail" in email and "." in email

    @staticmethod
    def validate_mobile(mobile):
        """Validate the mobile number format."""
        return len(mobile) == 10 and mobile.isdigit()


class SmtpServer:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def send_email(self, recipient, otp):
        """Send an email with the OTP using the SMTP server."""
        server = smtplib.SMTP(self.host, self.port)
        server.starttls()
        server.login(self.username, self.password)
        msg = f'Hello, your OTP is {otp}\nPlease do not share the OTP with anyone.\n' \
              'This is a system-generated mail, so do not reply.'
        server.sendmail(self.username, recipient, msg)
        server.quit()


class TwilioClient:
    def __init__(self, account_sid, auth_token, twilio_number):
        self.client = Client(account_sid, auth_token)
        self.twilio_number = twilio_number

    def send_sms(self, recipient, otp):
        """Send an SMS with the OTP using the Twilio client."""
        message = self.client.messages.create(
            body=f'Hello, your OTP is {otp}\nPlease do not share the OTP with anyone.\n'
                 'This is a system-generated message, so do not reply.',
            from_=self.twilio_number,
            to=recipient
        )



if __name__ == "__main__":
    account_sid = 'AC87d29f1bf3374f2067a057ddd8d8dd5e'
    auth_token = '50f3a51a3c806ed0a06f7fe95100efa4'

    twilio_number = '+14705163287'
    target_number = '+919552650041'
    otp_generator = OTPGenerator(account_sid,auth_token,twilio_number)

    email_address = "nihalsathawane2003@gmail.com"
    otp_generator.send_otp_over_email(email_address)

    mobile_number = "9552650041"
    otp_generator.send_otp_over_mobile(mobile_number)

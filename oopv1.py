import random
import smtplib
from twilio.rest import Client
  # Assuming keys.py contains necessary Twilio credentials

account_sid = 'AC87d29f1bf3374f2067a057ddd8d8dd5e'
auth_token = '50f3a51a3c806ed0a06f7fe95100efa4'

twilio_number = '+14705163287'
target_number = '+919552650041'
class OTPGenerator:
    def __init__(self):
        self.otp = self.generate_otp()

    def generate_otp(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(4)])

    def send_otp_over_email(self, email):
        if self.validate_email(email):
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('nihalsathawane2003@gmail.com', 'exgf spgh lmwn swie')
            msg = 'Hello, your OTP is ' + str(self.otp) + '\nPlease do not share the OTP with anyone.' \
                  '\nThis is a system-generated mail, so do not reply.'
            server.sendmail("nihalsathawane2003@gmail.com", email, msg)
            print(f"OTP is sent to {email} via email.")
            server.quit()
        else:
            print("Invalid email address.")

    def send_otp_over_mobile(self, mobile):
        if self.validate_mobile(mobile):
            client = Client(account_sid, auth_token)
            msg = client.messages.create(
                body='Hello, your OTP is ' + str(self.otp) + '\nPlease do not share the OTP with anyone.' \
                     '\nThis is a system-generated message, so do not reply.',
                from_=twilio_number,
                to=mobile
            )
            print(f"OTP is sent to {mobile} via mobile.")
        else:
            print("Invalid mobile number.")

    @staticmethod
    def validate_email(email):
        return "@gmail" in email and "." in email

    @staticmethod
    def validate_mobile(mobile):
        return len(mobile) == 10 and mobile.isdigit()


if __name__ == "__main__":
    otp_generator = OTPGenerator()

    email_address = "nihalsathvane@gmail.com"
    otp_generator.send_otp_over_email(email_address)

    mobile_number = "9552650041"
    otp_generator.send_otp_over_mobile(mobile_number)

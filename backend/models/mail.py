import smtplib
from email.mime.text import MIMEText
from models.settings import settings

class Mail:
    def __init__(self):
        pass

    # ==============================================================================
    # send email
    # if you send too many emails, then use contextmanager to close the connection
    # ==============================================================================
    @staticmethod
    def send_email(email, token, subject):
        msg = MIMEText("Verify your email with token " + token)
        msg['Subject'] = subject
        msg['From'] = "no-reply@local.dev"
        msg['To'] = email

        # send an email
        try:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.send_message(msg)
        except Exception as e:
            print('SMTP Error\n', e)
            return False;

        return True;

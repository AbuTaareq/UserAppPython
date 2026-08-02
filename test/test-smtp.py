"""

2/10/2026

A module for sending email messages using the SMTP protocol.

This module demonstrates sending a simple text email using the `smtplib`
library and the `email.mime.text.MIMEText` class to create an email message.
The email is sent to a local SMTP server for testing purposes.

You must install mail-hog to run this script successfully.

"""

import smtplib
from email.mime.text import MIMEText
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    smtp_host: str
    smtp_port: int

settings = Settings()

print(f'SMTP HOST   : {settings.smtp_host}')
print(f'SMTP PORT   : {settings.smtp_port}')

msg = MIMEText("Verify your email")
msg["Subject"] = "Signup Verification"
msg["From"] = "no-reply@local.dev"
msg["To"] = "test@example.com"

# send an email
try:
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.send_message(msg)
        print('Email sent')
except Exception as e:
    print('SMTP Error\n', e)
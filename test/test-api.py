"""
    Author: Shihab
    Created: 11/21/2024
    Modified: 03/22/2026
    ===========================================================
    The following python code will test the API call
    From now on we do not have to use POSTMAN anymore

    test using curl - command line url
    curl -X POST http://localhost:8001/user/create \
     -H "Content-Type: application/json" \
     -d '{"email":"sihaab@gmail.com","password":"boxi2008","token":""}'

    Another way to test the API is to use the requests library
    import requests

    # Send a POST request to create a user
    response = requests.post(
        "http://localhost:8001/user/create",  # Endpoint to hit
        headers={"Content-Type": "application/json"},  # Content type header
        json={"email": "sihaab@gmail.com", "password": "boxi2008", "token": ""}  # JSON data payload
    )

    # Print response
    print(response.text)

"""

import requests
import smtplib
from os import system
from email.mime.text import MIMEText

from models.color import Color as c
from models.settings import settings
from models.database import DB


system('clear')
print(f'{c.yellow}Test started {c.reset}\n')

print(f'{c.darkGrey}Database URL: {c.lightGreen}{settings.database_url} {c.reset}')
print(f'{c.darkGrey}API URL     : {c.lightGreen}{settings.api_url} {c.reset}')
print(f'{c.darkGrey}SMTP HOST   : {c.lightGreen}{settings.smtp_host} {c.reset}')
print(f'{c.darkGrey}SMTP PORT   : {c.lightGreen}{settings.smtp_port} {c.reset}')

msg = MIMEText("Verify your email")
msg["Subject"] = "Signup Verification"
msg["From"] = "no-reply@local.dev"
msg["To"] = "test@example.com"

try:
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.send_message(msg)
        print(f'{c.green}Test Email sent {c.reset}')
except Exception as e:
    print(f'{c.red}Error sending email: {e} {c.reset}')

# system('clear')
db_connection = DB.connect()
print(f'\n{c.yellow}Database connection established {c.reset}')
db_cursor = db_connection.cursor()

# Truncate tables
db_cursor.execute("Truncate Table app_user;")
db_cursor.execute("Truncate Table user_log;")
db_connection.commit()
print(f'{c.lightGrey}app_user truncated{c.reset}')
print(f'{c.lightGrey}user_log truncated{c.reset}\n')

def test_api(api_url, payload, code=200):
    api_response = requests.post(api_url, json=payload)
    if api_response.status_code != code:
        print(f'{c.red}Error({api_response.status_code}): '+
              f'{api_response.text} {c.reset}')
    else:
        print(f'{c.lightGreen}Success({api_response.status_code}){c.reset}')
        if api_response.text != 'null':
            print(f'{c.lightGrey}Response:{c.reset}{api_response.text}')
        else:
            print('')

user = {'email': 'sihaab@gmail.com', 'password': 'boxi2008', 'token': ''}

url = f"{settings.api_url}/user/create"

print(f"{c.cyan}1.0: {c.reset} Create user ", end='')
test_api(f"{settings.api_url}/user/create", user, 200)
db_cursor.execute("select user_email, user_password from app_user;")
for row in db_cursor.fetchall():
    print(row)

print(f"\n{c.cyan}1.1: {c.reset} Validate duplicate email " ,end='')
test_api(f"{settings.api_url}/user/create", user, 409)

print(f"\n{c.cyan}1.2: {c.reset} Add another email " ,end='')
user['email'] = 'sihaab.hassan@gmail.com'
test_api(f"{settings.api_url}/user/create", user)
db_cursor.execute("select user_email, user_password, user_id from app_user;")
for row in db_cursor.fetchall():
    user['user_id'] = row[2]
    print(row)

print(user['user_id'])

print(f"\n{c.cyan}1.3: {c.reset} Missing data points in the request " ,end='')
del user['email']
test_api(f"{settings.api_url}/user/create", user, 422)
user['email'] = 'sihaab@gmail.com'

print(f"\n{c.cyan}2.0: {c.reset} Login " ,end='')
test_api(f"{settings.api_url}/user/login", user, 200)
print(f'{c.lightGrey}App User ID: {c.reset}{user.get("user_id")}')

print(f"\n{c.cyan}2.0: {c.reset} Profile phone number " ,end='')
user['phone'] = '+14083961772'
test_api(f"{settings.api_url}/profile/phone", user, 200)

"""
print("\n2.1: user logout")
test_api(f"{settings.api_url}/user/logout, loginPayload)


print("\n2.3: user login with bad password")
loginPayload['login_password'] = "boxi2008"
print(loginPayload)
test_api(login_url, loginPayload)

print("\n2.4: user login with bad email")
print(loginPayload)
loginPayload['user_email'] = "sihaab.hassan@icloud.com"
test_api(login_url, loginPayload)
"""

print(f'\n{c.yellow}Test completed {c.reset}')
from main import app
import requests

session = requests.Session()

# Login (this sets the cookie)
login_res = session.post(
    "http://localhost:8001/user/login",
    json={
        "email": "sihaab@gmail.com",
        "password": "boxi2008"
    }
)

print("Login:", login_res.status_code)

# Call protected endpoint (cookie auto sent)
res = session.post(
    "http://localhost:8001/profile/phone",
    json={"phone":"1234567890"}
)

print("Status Code:", res.status_code)
print("Status Text:", res.text)

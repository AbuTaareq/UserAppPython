from datetime import datetime, UTC
import jwt

secret_key = "this is the secret key for the testing purpose"
token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaWhhYWJAZ21haWwuY29tIiwiZXhwIjoxNzc1ODcwMjUxLCJpYXQiOjE3NzU4Njg0NTF9.ibDVuOrGZPHbwrP-XJqkxOwm-tHUHHD9i8Q6lCtd7gw"

# Decode without verifying expiration
payload = jwt.decode(token, secret_key, algorithms=["HS256"], options={"verify_exp": False})

print(payload)

exp_ts = payload["exp"]
exp_dt = datetime.fromtimestamp(exp_ts, UTC)
now_ts = datetime.now(UTC)
duration = exp_dt - now_ts

print("Current Time    :", now_ts.strftime("%Y-%m-%d %H:%M:%S"))
print("Token expires at:", exp_dt.strftime("%Y-%m-%d %H:%M:%S"))
print("Token is valid  :", exp_dt > now_ts)
print("Duration Minutes:", round(duration.total_seconds()/60))
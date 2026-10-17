#
# FileName: webToken.py
# Author: Shihab Hassan
# Created:   11/01/2024
# Modified: 03/29/2026
#


from fastapi import Request, HTTPException
from datetime import datetime, timedelta, UTC
from pydantic import BaseModel
import jwt

class WebToken:

    # this User class is saved in the cookie.
    # if you want to carry more variables, then add them to the class.
    class User(BaseModel):
        id: int
        email: str

    secret_key = "this is the secret key for the testing purpose"
    algorithm = 'HS256'
    expires_in_minutes = 60


    # ===================================================================================
    def __init__(self):
        pass


    # ===================================================================================
    # build the token and return it, the token will be stored in the cookie
    @staticmethod
    def generate(user: User):
        now = datetime.now(UTC)
        payload = {
            # dump the user model to a dictionary
            **user.model_dump(),

            # JWT data iat = issued at, exp = expiration time
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=WebToken.expires_in_minutes)).timestamp()),
        }
        encoded_jwt = jwt.encode(payload, WebToken.secret_key, algorithm=WebToken.algorithm)
        return encoded_jwt


    # ===================================================================================
    # validate the token and return the payload
    # make sure the user is logged in, if not, then throw an exception
    # user cannot update the phone number without logging in
    # web token has user ID information, so NameModel must change
    @staticmethod
    def validate(request: Request):

        token = request.cookies.get("jwt")
        if not token:
            raise HTTPException(401, "Not authenticated")

        try:
            payload = jwt.decode(token, WebToken.secret_key, algorithms=WebToken.algorithm)
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")


    # ===================================================================================
    # this method can be used at every endpoint to check if the user is logged in or not
    @staticmethod
    def getuser(request: Request):
        payload = WebToken.validate(request)
        if payload is None:
            raise HTTPException(401, "User not logged in, cookie is missing")

        # manual deserialization of a dictionary to a typed object or pydantic model
        # build user model using the 'manual deserialization' process as below.
        # Now the payload dictionary is a pydantic model.
        # we do not use iat and exp, otherwise we can do user = User(**payload)
        # which will convert every column value to the correct type.
        user = WebToken.User(
            id=payload.get("id"),
            email=payload.get("email"),
        )

        # validation of the user in the database
        if user.id is None or user.email is None or user.id <= 0:
            raise HTTPException(401, "Cookie does not have user information, please login again")

        return user

"""
    Filename: user.py
     Author: Shihab Hassan
     Date: 2023-04-22
     Description: User API endpoints

This module provides API endpoints for user creation, login, logout, token management,
and token verification. It leverages FastAPI for building REST APIs and integrates
with PostgreSQL for data persistence. Utility libraries such as bcrypt are used for
password hashing, and JWT is implemented for session-based authentication.

Functions:
    user_create: Handles user creation and saves user details in the database.
    user_login: Performs user authentication
    user_logout: Deletes the session cookie and logs the user out.
    send_token: Generates a verification token and sends it to the user's email.
    user_token_verify: Validates the token entered by the user during signup verification.

Endpoints:
    POST /user/create: Creates a new user in the database.
    POST /user/login: Authenticates a user and returns a JWT token upon successful login.
    POST /user/logout: Logs out the user by deleting the session cookie.
    POST /user/tokenSend: Sends a verification token to the user's email.
    POST /user/tokenVerify: Verifies the token entered by the user during signup verification.
    POST /user/emailVerify: Verifies the user exists in the database.

"""

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from datetime import datetime, UTC
import bcrypt

# models
from models.baseModel import UserModel
from models.webToken import WebToken
from models.database import DB
from models.color import Color
from models.mail import Mail
from models.otp import OTP

router = APIRouter()

# ============================================
# database test cases
# Check entry at app_user and user_log tables
# it returns nothing if everything is ok
# ============================================
@router.post("/create")
async def user_create(user: UserModel):
	# login and password cannot be empty
	if not user.email or not user.password:
		raise HTTPException(status_code=400, detail="Login information not provided")
	
	# Encrypt the password using bcrypt and salt stored in the hashed password
	hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode("utf-8")
	
	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_user_create($1, $2)"
			await conn.execute(query, user.email, hashed_password)
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
			print(e)
	
	return {'success': True, 'message': 'Name updated successfully'}


# =========================================================
@router.post("/login")
async def user_login(user: UserModel, response: Response):
	
	is_agent: bool = False
	is_admin: bool = False
	first_name: str = ""
	last_name: str = ""
	
	# Perform basic validation (optional)
	if not user.email or not user.password:
		raise HTTPException(400, "Missing user information, try again")
	
	
	# validate user login in the database
	async with DB.pool.acquire() as conn:
		try:
			# stored procedure returns a table, so select * is ideal
			query = "select * from fn_auth_retrieve_user_password($1)"
			row = await conn.fetchrow(query, user.email)
			if not row:
				print(f'{Color.orange}User not found in the database{Color.reset}')
				raise HTTPException(400, "User not found, try again")
			
			db = UserModel(**dict(row))
			is_agent = True if row['role'].lower() == 'agent' else False
			is_admin = True if row['role'].lower() == 'admin' else False
			first_name = row['first_name']
			last_name = row['last_name']
			
			
			print(f'{Color.green}User found in the database{Color.reset}')
			# create hashed password from the database password stored in the database
			hashed_password = db.password.encode()
			
			# Compare the provided password with the hashed password
			if bcrypt.checkpw(user.password.encode(), hashed_password):
				print(f'{Color.lightGreen}Password verified, Login Successful{Color.reset}')
			else:
				print(f'{Color.red}Login failed, Incorrect Password, try again{Color.reset}')
				raise HTTPException(401, "Incorrect Password, try again")
		
		except HTTPException:
			raise
		
		except Exception as e:
			DB.exception(e)
		
		#
		# Once login is successful create jwt token with email and user_id
		# We will use this token to authenticate the user in the future
		# Also user user_id to add or update the user profile
		#
		print(f'{Color.yellow}Creating web token and cookie{Color.reset}')
		try:
			# here is the place where we can add more information to the jwt token
			# make sure to change UserModel if you add more fields
			token_user = WebToken.User(id=db.id, email=db.email)
			web_token = WebToken.generate(token_user)
		except Exception as e:
			print(f'{Color.red}Failed to create JWT token.{Color.reset}')
			print(f'{Color.red}{type(e).__name__}: {Color.orange}{e}{Color.reset}')
			raise HTTPException(500, "Failed to create JWT token, try again !!")
		
		print(f'{Color.lightGreen}JWT token created successfully{Color.reset}')
		
		# create the cookie with jwt token to send with FastAPI response
		# TODO: for production we should use https and secure must be True (production notes)
		response.set_cookie(
			key="jwt",
			value=web_token,
			httponly=True,
			secure=False,  # on http://localhost:8001, cookie will not be sent
			samesite="lax"
		)
		print(f'{Color.lightGreen}Cookie created successfully{Color.reset}')
	
	return {
		'success': True,
		'agent': is_agent,
		'admin': is_admin,
		'first_name': first_name,
		'last_name': last_name,
		'message': 'User login successfully'
	}


# ================================================================
@router.post("/logout")
async def user_logout(response: Response):
	# reset the cookie
	response.delete_cookie("jwt")
	print(f'{Color.lightGreen}(logout) Success, Cookie deleted{Color.reset}')
	
	return {'success' : True, 'message' : 'User logout successfully'}



# ================================================================
# 1. user sign up with email
# 2. create a hashed token, create expiry time for the token.
# 3. save the details at the database for later validation
# 4. if the user validates the email, then create the user
# ================================================================
@router.post("/sendOTP")
async def send_otp(user: UserModel):
	# login and password cannot be empty
	if not user.email:
		raise HTTPException(400, "User email is missing. Email required to send OTP")
	
	otp_generated, otp_hashed, otp_expires = OTP.generate()
	
	print(f'{Color.green}Email     : {Color.lightGreen}{user.email}')
	print(f'{Color.green}Actual OTP: {Color.lightCyan}{Color.bold}{otp_generated}{Color.reset}')
	
	# save the otp at the database, so we will be able to validate it later
	async with DB.pool.acquire() as conn:
		try:
			query = "select * from fn_user_signup($1, $2, $3)"
			await conn.execute(query, user.email, otp_hashed, otp_expires)
		
		except HTTPException:
			raise
		
		except Exception as e:
			DB.exception(e)
	
	# send the email with the otp
	print(f'{Color.yellow}Sending OTP to: {Color.lightGreen}{user.email}{Color.reset}')
	try:
		Mail.send_email(user.email, otp_generated, 'Signup verification')
	except Exception as e:
		print(f'{Color.red}Failed to send OTP.{Color.reset}')
		print(f'{Color.red}{type(e).__name__}: {Color.orange}{e}{Color.reset}')
		raise HTTPException(500, "Failed to send OTP, try again !!")
	
	print(f'{Color.lightGreen}OTP sent successfully.{Color.reset}')
	
	return {'success' : True, 'message' : 'OTP sent successfully'}


# =================================================================================
# After receiving a token from mail, the user will be entering the token at UI
# Calling the below API will validate the token
# =================================================================================
@router.post("/verifyOTP")
async def verify_otp(user: UserModel):
	if user.otp is None:
		raise HTTPException(401, "Verification Token not supplied")
	
	# save the otp at the database, so we will be able to validate it later
	async with DB.pool.acquire() as conn:
		try:
			query = "select * from fn_user_token_retrieve($1)"
			data = await conn.fetchrow(query, user.email)
			if data is None:
				raise HTTPException(400, "Something went wrong, try signup again")
			
			otp_in_db = data['otp']
			otp_expiry_date = data['expiry']
			
			if otp_in_db is None:
				raise HTTPException(401, "OTP not found or expired, signup again")
			
			if OTP.hashed(user.otp) != otp_in_db:
				raise HTTPException(403, "Token not matched, try again")
			
			if datetime.now(UTC) > otp_expiry_date:
				raise HTTPException(402, "Token expired, signup again")
		
		except HTTPException:
			raise
		
		except Exception as e:
			DB.exception(e)
			
	return {'success': True, 'message': 'OTP verified successfully'}


# ================================================================================
# Before updating a password,
# We must verify the user exists in the database
# We must also send and verify the OTP, the logic is build at the UI
# The following API will verify the user exists in the database
# ================================================================================
@router.post("/verifyEmail")
async def user_email_verify(user: UserModel):
	# login and password cannot be empty
	if not user.email:
		raise HTTPException(400, "User email parameter missing")
	
	# verify the user exists in the database
	async with DB.pool.acquire() as conn:
		try:
			query = "select * from fn_user_validation($1)"
			data = await conn.fetchval(query, user.email)
			if not data :
				raise HTTPException(400, "Something went wrong, contact admin")
		except HTTPException:
			raise
		
		except Exception as e:
			DB.exception(e)
	
	return {'success': True, 'message': 'Email verified successfully'}


@router.post("/password")
async def user_password(user: UserModel):
	
	# login and password cannot be empty
	if not user.email or not user.password:
		raise HTTPException(400, "Email and password required for password reset")
	
	# Encrypt the password using bcrypt and salt stored in the hashed password
	hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode("utf-8")
	
	# reset user password at the database
	async with DB.pool.acquire() as conn:
		try:
			query = "select * from fn_user_password_reset($1, $2)"
			await conn.execute(query, user.email, hashed_password)
		
		except HTTPException:
			raise
		
		except Exception as e:
			DB.exception(e)
	
	return {'success': True, 'message': 'Password updated successfully'}



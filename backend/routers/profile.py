#
# FileName: profile.py
# Author: Shihab Hassan
# Created:   11/01/2024
# Last Modified: 6/2/2026
#
#

from fastapi import APIRouter, HTTPException, Depends
from models.database import DB
from models.baseModel import UserInfoModel, AddressModel, EducationModel, RelativesModel, RolesModel
from models.baseModel import ReligionModel, LanguageModel, WorkHistoryModel, ConnectionModel
from models.webToken import WebToken
from models.color import Color

router = APIRouter()

# ===========================================================================================
# USER
# ===========================================================================================
@router.post("/load_user")
async def load_user(user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		row = await conn.fetchrow("select * from fn_get_user($1)", user.id)
		if not row:
			raise HTTPException(404, "User not found, login again")

		return UserInfoModel(**row)

# ===========================================================================================
@router.post("/update_user")
async def profile_update_user(
	data: UserInfoModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):

	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_update_user($1, $2::jsonb)"
			await conn.execute(query, token_user.id, data.model_dump_json())
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
			print(e)

	return {'success': True, 'message': 'Name updated successfully'}

# ===========================================================================================
# ADDRESS
# ===========================================================================================
@router.post("/load_address")
async def load_address(token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		rows = await conn.fetch("select * from fn_get_user_address($1)", token_user.id)
		return [AddressModel(**rows) for rows in rows]


# ===========================================================================================
@router.post("/update_address")
async def update_address(
	data: AddressModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	
	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_update_address($1, $2::jsonb)"
			await conn.execute(query, token_user.id, data.model_dump_json())

		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Address updated successfully'}


# ===========================================================================================
@router.post("/delete_address")
async def delete_address(
	data: AddressModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		try:
			await conn.execute(
				'select fn_delete_address($1, $2, $3)',
				token_user.id,      #1
				data.from_month, #2
				data.from_year,  #3
			)
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Address updated successfully'}


# ===========================================================================================
# LANGUAGE (No delete required as update drops and adds the languages)
# ===========================================================================================
@router.post("/lookup_languages")
async def lookup_languages():
	async with DB.pool.acquire() as conn:
		rows = await conn.fetch("select * from fn_lookup_languages()")
		if not rows:
			raise HTTPException(404, "Languages not found, please contact admin")

		# FastAPI will convert it to JSON
		return [dict(row) for row in rows]

# ===========================================================================================
@router.post("/load_language")
async def load_language(user: WebToken.User = Depends(WebToken.getuser)):
	async with (DB.pool.acquire() as conn):
		try:
			query = "select language_id, language_name from fn_get_user_language($1)"
			rows = await conn.fetch(query, user.id)
			return [dict(row) for row in rows]

		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': False, 'message': 'Language retrieve failed, please contact admin'}


# ===========================================================================================
@router.post("/update_language")
async def update_language(
	language: LanguageModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_update_language($1, $2::int[])"
			await conn.execute(query, token_user.id, language.id)
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Language updated successfully'}


# ===========================================================================================
# EDUCATION
# ===========================================================================================
@router.post("/load_education")
async def load_education(token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		rows = await conn.fetch("select * from fn_get_user_education($1)", token_user.id)
		return [EducationModel(**rows) for rows in rows]


# ===========================================================================================
@router.post("/update_education")
async def update_education(
	data: EducationModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	print(f'{Color.grey}data: {Color.yellow}{data.model_dump_json(indent=2)}')
	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_update_education($1, $2::jsonb)"
			await conn.execute(query, token_user.id, data.model_dump_json())
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Address updated successfully'}


# ===========================================================================================
@router.post("/delete_education")
async def delete_education(
	data: EducationModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		try:
			await conn.execute(
				'select fn_delete_education($1, $2)',
				token_user.id,      #1
				data.completed_year, #2
			)
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Data deleted successfully'}


# ===========================================================================================
# RELIGION
# ===========================================================================================
@router.post("/lookup_religions")
async def lookup_religions():
	async with DB.pool.acquire() as conn:
		rows = await conn.fetch("select * from fn_lookup_religions()")
		if not rows:
			raise HTTPException(404, "Religion not found, please contact admin")
		return [dict(row) for row in rows]


# ===========================================================================================
@router.post("/load_religion")
async def load_religion(token_user: WebToken.User = Depends(WebToken.getuser)):
	async with (DB.pool.acquire() as conn):
		try:
			query = "select religion_id, religion_name from fn_get_user_religion($1)"
			rows = await conn.fetch(query, token_user.id)
			return [dict(row) for row in rows]

		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': False, 'message': 'Religion retrieve failed, please contact admin'}


# ===========================================================================================
@router.post("/update_religion")
async def update_religion(
	data: ReligionModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_update_religion($1, $2::int[])"
			await conn.execute(query, token_user.id, data.id)
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Data updated successfully'}

# ===========================================================================================
# RELATIVES
# ===========================================================================================
@router.post("/lookup_relation")
async def lookup_relation():
	async with DB.pool.acquire() as conn:
		rows = await conn.fetch("select * from fn_lookup_relation()")
		if not rows:
			raise HTTPException(404, "Relatives not listed, please contact admin")
		return [dict(row) for row in rows]


# ===========================================================================================
@router.post("/load_relatives")
async def load_relatives(token_user: WebToken.User = Depends(WebToken.getuser)):
	async with (DB.pool.acquire() as conn):
		try:
			query = "select * from fn_get_user_relative($1)"
			rows = await conn.fetch(query, token_user.id)
			return [dict(row) for row in rows]
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': False, 'message': 'Data retrieved successfully'}


# ===========================================================================================
@router.post("/update_relative")
async def update_relative(
	data: RelativesModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	print(f'{Color.grey}data: {Color.yellow}{data.model_dump_json(indent=2)}')
	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_update_relative($1, $2::jsonb)"
			await conn.execute(query, token_user.id, data.model_dump_json())
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Data updated successfully'}


# ===========================================================================================
@router.post("/delete_relative")
async def delete_relative(
	data: RelativesModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	print(f'{Color.grey}data: {Color.yellow}{data.model_dump_json(indent=2)}')
	async with DB.pool.acquire() as conn:
		try:
			await conn.execute(
				'select fn_delete_relative($1, $2, $3)',
				token_user.id,      #1
				data.relation_id,   #2
				data.relative_name  #3
			)
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Data deleted successfully'}


# ===========================================================================================
# Work Experience
# ===========================================================================================
@router.post("/load_work_history")
async def load_work_work_history(token_user: WebToken.User = Depends(WebToken.getuser)):
	async with (DB.pool.acquire() as conn):
		try:
			query = "select * from fn_get_user_work_history($1)"
			rows = await conn.fetch(query, token_user.id)
			return [dict(row) for row in rows]
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': False, 'message': 'Data retrieved successfully'}

# ===========================================================================================
@router.post("/update_work_history")
async def update_work_history(
	data: WorkHistoryModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_update_work_history($1, $2::jsonb)"
			await conn.execute(query, token_user.id, data.model_dump_json(exclude_none=True))
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Data updated successfully'}

# ===========================================================================================
@router.post("/delete_work_history")
async def delete_work_history(
	data: WorkHistoryModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		try:
			await conn.execute(
				'select fn_delete_work_history($1, $2, $3)',
				token_user.id,    	#1
				data.work_year, 	#2
				data.designation,  	#3
			)
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Data deleted successfully'}

# ===========================================================================================
# Connections
# ===========================================================================================
@router.post("/load_connection")
async def load_connection(token_user: WebToken.User = Depends(WebToken.getuser)):
	async with (DB.pool.acquire() as conn):
		try:
			query = "select * from fn_get_user_connection($1)"
			rows = await conn.fetch(query, token_user.id)
			return [dict(row) for row in rows]
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': False, 'message': 'Data retrieved successfully'}

# ===========================================================================================
@router.post("/update_connection")
async def update_connection(
	data: ConnectionModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_update_connection($1, $2::jsonb)"
			await conn.execute(query, token_user.id, data.model_dump_json(exclude_none=True))
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Data updated successfully'}

# ===========================================================================================
@router.post("/verify_connection")
async def verify_connection(
	data: ConnectionModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	print(f'{Color.grey}data: {Color.yellow}{data.model_dump_json(indent=2)}')
	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_verify_connection($1, $2::jsonb)"
			await conn.execute(query, token_user.id, data.model_dump_json(exclude_none=True))
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Data updated successfully'}

# ===========================================================================================
@router.post("/delete_connection")
async def delete_connection(
	data: ConnectionModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		try:
			await conn.execute(
				'select fn_delete_connection($1, $2)',
				token_user.id,    	#1
				data.email, 		#2
			)
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Data deleted successfully'}

# ===========================================================================================
# Roles
# ===========================================================================================
@router.post("/lookup_roles")
async def lookup_roles():
	async with DB.pool.acquire() as conn:
		rows = await conn.fetch("select * from fn_lookup_roles()")
		if not rows:
			raise HTTPException(404, "Lookup data not found, please contact admin")

		# FastAPI will convert it to JSON
		return [dict(row) for row in rows]

# ===========================================================================================
@router.post("/load_roles")
async def load_roles(token_user: WebToken.User = Depends(WebToken.getuser)):
	async with (DB.pool.acquire() as conn):
		try:
			query = "select role_name from fn_get_user_roles($1)"
			rows = await conn.fetch(query, token_user.id)
			return [dict(row) for row in rows]

		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': False, 'message': 'Religion retrieve failed, please contact admin'}

# ===========================================================================================
@router.post("/update_roles")
async def update_roles(
	data: RolesModel,
	token_user: WebToken.User = Depends(WebToken.getuser)):
	async with DB.pool.acquire() as conn:
		try:
			query = "select fn_update_roles($1, $2::int[])"
			await conn.execute(query, token_user.id, data.id)
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
	return {'success': True, 'message': 'Data updated successfully'}


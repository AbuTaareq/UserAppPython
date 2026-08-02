# ===================================================
#  File: 	 data.py
#  Author:	 Shihab
#  Created:  6/10/26
#  Modified: 6/29/26
# ===================================================

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from models.database import DB
from models.baseModel import CandidatesDataPage

router = APIRouter()

@router.post("/candidates")
async def candidates(page: CandidatesDataPage):
	async with DB.pool.acquire() as conn:
		print(f"page: {page.limit} offset: {page.offset}")
		try:
			query = "select * from fn_get_candidates($1, $2)"
			rows = await conn.fetch(query, page.limit, page.offset)
			if not rows:
				raise HTTPException(404, "No candidates listed, please contact admin")
			return [dict(row) for row in rows]
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
			print(e)



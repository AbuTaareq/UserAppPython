# =================================================================================================
#  File: 	 data.py
#  Author:	 Shihab
#  Created:  6/10/26
#  Modified: 10/31/26
# =================================================================================================
#  Description:
#	1. Candidates must be active and not deleted
#	2. Candidates cannot be admin or agents, means they do not have a role
# =================================================================================================

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from models.database import DB
from models.baseModel import CandidatesDataPage
from typing import Any

router = APIRouter()

@router.post("/candidateList")
async def candidates(page: CandidatesDataPage):
	async with DB.pool.acquire() as conn:
		try:
			query = """
				select
					  p.first_name	as first_name
					 ,p.last_name	as last_name
					 ,p.screen_name	as screen_name
					 ,p.phone       as phone
					 ,p.birth_month as birth_month
					 ,p.birth_year  as birth_year
					 ,p.gender      as gender
					 ,round(p.height::numeric,1) as height
					 ,p.weight      as weight
					 ,a.city		as city
					 ,a.state		as state
					 ,a.country		as country
					 ,rm.role_name	as role
					 ,up.first_name	as agent_first_name
					 ,up.last_name	as agent_last_name
					 ,(count(*) over())::int  as total_count
				from user_profile p
				left join user_address a on a.user_id = p.user_id and a.is_current = true
				left join user_role r on r.user_id = p.user_id
				left join role_master rm on rm.role_id = r.role_id
					 and rm.role_name in ('Bride', 'Groom')
				left join user_agent ua on ua.user_id = p.user_id
				left join user_profile up on up.user_id = ua.agent_id
				where p.is_active = true
					and p.is_deleted = false
					and r.role_id is null
			"""
			
			# build the where clause
			params: list[Any] = []
			
			if page.gender != 'All':
				query += "and p.gender = $1"
				params.append(page.gender)
			
			query += f" order by p.first_name limit ${len(params) + 1} offset ${len(params) + 2}"
			params.extend([page.limit, page.offset])
			rows = await conn.fetch(query, *params)
			return [dict(row) for row in rows]
		except HTTPException:
			raise
		except Exception as e:
			DB.exception(e)
			print(e)


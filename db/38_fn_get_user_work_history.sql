/*

	File Name: 38_fn_get_user_work_history.sql
	Author: Shihab Hassan
	Created Date: 6/2/2026
	Last Modified: 6/2/2026

*/
drop function if exists fn_get_user_work_history(integer);

create or replace function fn_get_user_work_history(in_user_id integer)
returns table (
	work_year   	integer,
    designation 	varchar,
	company_name 	varchar,
    city        	varchar,
    state       	varchar,
    country     	varchar
)
as $$
begin
    return query
    select
         w.work_year    as work_year,
         w.designation  as designation,
    	 w.company_name as company_name,
         w.city         as city,
         w.state        as state,
         w.country      as country
    from user_work_history w
    join user_master u  on w.user_id = u.user_id
    where u.user_id = in_user_id
    order by w.work_year desc;
end;
$$ language plpgsql;




/*

	File Name: 37_fn_get_user_relative.sql
	Author: Shihab Hassan
	Created Date: 5/28/2026
	Last Modified: 5/28/2026

*/

drop function if exists fn_get_user_relative(int);

create function fn_get_user_relative(in_user_id int)
returns table (
	relation_id int,
    relation_name varchar,
    relative_name varchar,
    relative_email varchar,
    relative_phone varchar,
    relative_age integer,
    relative_location varchar,
    relative_occupation varchar
)
as $$
    select
    	m.relation_id 			as relation_id,
    	m.relation_name 		as relation_name,
    	u.relative_name 		as relative_name,
    	u.relative_email 		as relative_email,
    	u.relative_phone 		as relative_phone,
    	u.relative_age 			as relative_age,
    	u.relative_location 	as relative_location,
    	u.relative_occupation 	as relative_occupation
    from user_relative u
    join relation_master m on u.relation_id = m.relation_id
    where u.user_id = in_user_id;

$$ language sql;

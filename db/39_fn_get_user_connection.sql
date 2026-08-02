/*

	File Name: 39_fn_get_user_connection.sql
	Author: Shihab Hassan
	Created Date: 6/3/2026
	Last Modified: 6/3/2026

*/
drop function if exists fn_get_user_connection(integer);

create or replace function fn_get_user_connection(in_user_id integer)
returns table (
	name varchar,
	details varchar,
	email varchar,
	phone varchar,
	is_verified boolean
)
as $$
begin
    return query
    select
    	c.name as name,
    	c.details as details,
    	c.email as email,
    	c.phone as phone,
    	c.is_verified as is_verified
    from user_connection c
    join user_master u  on u.user_id = c.user_id
    where u.user_id = in_user_id;
end;
$$ language plpgsql;




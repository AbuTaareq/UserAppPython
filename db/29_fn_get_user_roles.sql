/*

	File Name: 30_fn_get_user_roles.sql
	Author: Shihab Hassan
	Created Date: 5/11/2026
	Last Modified: 6/7/2026

*/
drop function if exists fn_get_user_roles(integer);

create function fn_get_user_roles(in_user_id integer)
returns table (
	role_id integer,
	role_name varchar
)
as $$
begin
    return query
    select rm.role_id, rm.role_name
    from user_role r
    join role_master rm on r.role_id = rm.role_id
    where r.user_id = in_user_id;
end;
$$ language plpgsql;




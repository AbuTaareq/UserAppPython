/*

	File Name: 21_fn_lookup_roles.sql
	Author: Shihab Hassan
	Created Date: 4/30/2026
	Last Modified: 4/30/2026

*/
drop function if exists fn_lookup_roles();

create or replace function fn_lookup_roles()
returns table (
    role_id integer,
    role_name varchar
)
as $$
    select r.role_id, r.role_name
    from role_master r;
$$ language sql;




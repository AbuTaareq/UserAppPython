/*
	File Name: 04_fn_auth_retrieve_user_password.sql
	Author: Shihab Hassan
	Created Date: 2/27/2026
	Modified Date: 10/15/2026

	Description:
		The following procedure can be used to retrieve user login information
		from the database.

*/
drop function if exists fn_auth_retrieve_user_password(text);
create or replace function fn_auth_retrieve_user_password(in_email text)
returns table(
	id integer,
	email varchar,
	password varchar,
	first_name varchar,
	last_name varchar,
	role varchar
)
as $$
begin
	--
	-- limit 1 is not required, but it is a good practice.
	-- so that API uses proper fetch
	--
	return query
	select
		 u.user_id as id
		,u.user_email as email
		,u.user_password as password
		,coalesce(up.first_name, '') as first_name
		,coalesce(up.last_name, '') as last_name
		,coalesce(rm.role_name, '') as role
	from user_master u
	left join user_profile up on u.user_id = up.user_id
	left join user_role ur on u.user_id = ur.user_id
	left join role_master rm on ur.role_id = rm.role_id
	where u.user_email = in_email
	limit 1;
end;
$$ language plpgsql;




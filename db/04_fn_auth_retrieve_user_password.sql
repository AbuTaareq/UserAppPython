/*
	File Name: 04_fn_auth_retrieve_user_password.sql
	Author: Shihab Hassan
	Created Date: 2/27/2026
	Modified Date: 6/4/2026

	Description:
		The following procedure can be used to retrieve user login information
		from the database.

*/
drop function if exists fn_retrieve_user_password(text);
create or replace function fn_retrieve_user_password(in_email text)
returns table(
	id integer,
	email varchar,
	password varchar
)
as $$
begin
	--
	-- limit 1 is not required, but it is a good practice.
	-- so that API uses proper fetch
	--
	return query
	select
		user_id 		as id,
		user_email		as email,
		user_password	as password
	from user_master
	where user_email = in_email
	limit 1;
end;
$$ language plpgsql;




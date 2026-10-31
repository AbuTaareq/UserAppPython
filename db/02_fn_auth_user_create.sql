/*
	File Name: 02_fn_auth_user_create.sql
	Author: Shihab Hassan
	Created Date: 11/19/2024
	Modified Date: 6/4/2026

	Create new user profile

*/

drop function if exists fn_auth_user_create(text, text);
create or replace function fn_auth_user_create(
	in in_user_email text,
    in in_user_password text,
    in in_is_agent boolean default false
)
returns void
as $$
declare
    new_user_id integer;
begin

	-- create new user
    insert into user_master (user_email ,user_password)
    values (in_user_email ,in_user_password)
    returning user_id into new_user_id;

    -- create new user profile
    insert into user_profile (user_id)
    values (new_user_id);

    -- create new user agent
    if in_is_agent then
        insert into user_role (user_id, role_id )
		select new_user_id as user_id, role_id
		from role_master
		where role_name='Agent';
    end if;

end;
$$ language plpgsql;



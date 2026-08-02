/*
	File Name: 02_fn_auth_user_create.sql
	Author: Shihab Hassan
	Created Date: 11/19/2024
	Modified Date: 6/4/2026

	Create new user profile

*/

drop function if exists fn_user_create(text, text);
create or replace function fn_user_create(
	in in_user_email text,
    in in_user_password text
)
returns void
as $$
begin
    insert into user_master (user_email ,user_password)
    values (in_user_email ,in_user_password);
end;
$$ language plpgsql;



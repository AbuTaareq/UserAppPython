/*
	File Name: 06_fn_user_password_reset.sql
	Author: Shihab Hassan
	Created Date: 3/9/2026
	Modified Date: 6/5/2026
	Description:
		The following procedure can be used to reset the user password

*/
drop function if exists fn_user_password_reset(varchar, varchar);
create or replace function fn_user_password_reset(in_email varchar, in_password varchar)
returns void
language plpgsql
as $$
begin
    update user_master set user_password = in_password
    where user_email = in_email;
end;
$$;




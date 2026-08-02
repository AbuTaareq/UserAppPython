/*
	File Name: 07_fn_user_validation.sql
	Author: Shihab Hassan
	Created Date: 3/9/2026
	Modified Date: 6/5/2026

	The following procedure can be used to reset the user password

*/

drop function if exists fn_user_validation(varchar);
create or replace function fn_user_validation(in_email varchar)
returns boolean
as $$
begin
	return exists (
        select 1
        from   user_master
        where  user_email = in_email
    );
end;
$$ language plpgsql;







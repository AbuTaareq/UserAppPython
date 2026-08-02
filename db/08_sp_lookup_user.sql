/*
	File Name: 08_sp_lookup_user.sql
	Author: Shihab Hassan
	Created Date: 3/9/2026

	The following procedure can be used to reset the user password

*/
create or replace procedure sp_lookup_user(
	in in_email text,
    out out_user_id int
)
as $$
begin
    select user_master.user_id into out_user_id
    from user_master
    where user_email = in_email
    limit 1;
end;
$$ language plpgsql;




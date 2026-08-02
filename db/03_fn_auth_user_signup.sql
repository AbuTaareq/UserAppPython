/*
	File Name: 03_fn_auth_user_signup.sql
	Author: Shihab Hassan
	Created Date: 2/22/2026
	Modified Date: 6/5/2026
*/
drop function if exists fn_user_signup(varchar, varchar, timestamp with time zone);
create or replace function fn_user_signup(
	in in_email varchar,
    in in_otp varchar,
    in in_expiry timestamp with time zone
)
returns void
as $$
begin
    insert into user_signup (
        email,
        otp,
        expiry
    )
    values (
        in_email,
        in_otp,
        in_expiry
    );
end;
$$ language plpgsql;



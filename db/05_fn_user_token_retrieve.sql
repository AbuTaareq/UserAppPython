/*
	File Name: 05_fn_user_token_retrieve.sql
	Author: Shihab Hassan
	Created Date: 2/22/2026
*/

drop function if exists fn_user_token_retrieve(varchar);

create or replace function fn_user_token_retrieve(in_email varchar)
returns table(
	otp varchar,
	expiry timestamp with time zone
)
as $$
declare var_signup_id integer;
begin
    select	u.otp, u.expiry, u.signup_id
    into	otp, expiry, var_signup_id
    from    user_signup u
    where   u.email = in_email
            and u.is_verified is false
            and round(extract(epoch from now() - u.expiry)) <= 0
    limit 	1;

    if found then
        update  user_signup
        set     is_verified = true, modified_date = now()
        where   signup_id = var_signup_id;

		-- into assignment has all three columns in memory
		-- just return those three columns without the table name
		return query
    	select otp, expiry;

    end if;
end;
$$ language plpgsql;
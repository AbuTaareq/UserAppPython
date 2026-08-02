/*
	File Name: 54_fn_delete_connection.sql
	Author: Shihab Hassan
	Created Date: 6/3/2026
	Modified Date: 6/3/2026
*/
drop function if exists fn_delete_connection(int, varchar);
create or replace function fn_delete_connection(in_user_id int , in_email varchar)
returns void
as $$
begin

	-- delete row if found
    delete from user_connection
    where user_id = in_user_id
      and email = in_email;

end;
$$ language plpgsql;

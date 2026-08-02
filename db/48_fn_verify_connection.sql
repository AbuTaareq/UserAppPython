/*

	File Name: 48_fn_verify_connection.sql
	Author: Shihab Hassan
	Created Date: 6/3/2026
	Last Modified: 6/3/2026

*/

drop function if exists fn_verify_connection(int, jsonb);

create or replace function fn_verify_connection(in_user_id int, in_data jsonb)
returns void
as $$
begin
	update user_connection set
		is_verified = (in_data->>'is_verified')::boolean,
		modified_date = current_timestamp
	where user_id = in_user_id and email = in_data->>'email';

end;
$$ language plpgsql;




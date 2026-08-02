/*

	File Name: 47_fn_update_user_connection.sql
	Author: Shihab Hassan
	Created Date: 6/3/2026
	Last Modified: 6/3/2026

*/

drop function if exists fn_update_connection(int, jsonb);

create or replace function fn_update_connection(in_user_id int, in_data jsonb)
returns void
as $$
begin
	insert into user_connection (
		user_id,
		name,
		details,
		email,
		phone
	)
	values (
		in_user_id,
		nullif(in_data->>'name',''),
		nullif(in_data->>'details',''),
		nullif(in_data->>'email',''),
		nullif(in_data->>'phone','')
	)
	on conflict (user_id, email) do update set
		name = excluded.name,
		details = excluded.details,
        modified_date = current_timestamp
    where user_connection.user_id = in_user_id
      and user_connection.email = excluded.email;

end;
$$ language plpgsql;




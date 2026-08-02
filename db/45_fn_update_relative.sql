/*

	File Name: 45_fn_update_relative.sql
	Author: Shihab Hassan
	Created Date: 5/29/2026
	Last Modified: 5/29/2026

*/

drop function if exists fn_update_relative(int, jsonb);

create or replace function fn_update_relative(in_user_id int, in_data jsonb)
returns void
as $$
begin
	insert into user_relative (
		user_id,
		relation_id,
		relative_name,
		relative_age,
		relative_email,
		relative_phone,
		relative_location,
		relative_occupation,
		modified_date
	)
	values (
		in_user_id,
		nullif(in_data->>'relation_id', '')::int,
		nullif(in_data->>'relative_name',''),
		nullif(in_data->>'relative_age','')::int,
		nullif(in_data->>'relative_email',''),
		nullif(in_data->>'relative_phone',''),
		nullif(in_data->>'relative_location',''),
		nullif(in_data->>'relative_occupation',''),
		now()
	)
	on conflict (user_id, relation_id, relative_name) do update set
	 	relative_age = nullif(in_data->>'relative_age','') :: int,
	 	relative_email = nullif(in_data->>'relative_email',''),
	 	relative_phone = nullif(in_data->>'relative_phone',''),
	 	relative_location = nullif(in_data->>'relative_location',''),
	 	relative_occupation = nullif(in_data->>'relative_occupation',''),
	 	modified_date = current_timestamp
    where user_relative.user_id = in_user_id;
end;
$$ language plpgsql;




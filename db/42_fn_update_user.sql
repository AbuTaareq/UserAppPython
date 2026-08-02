/*
	File Name: 42_fn_update_user.sql
	Author: Shihab Hassan
	Created Date: 4/10/2026
	Modified Date: 5/26/2026
*/

drop function if exists fn_update_user(int, jsonb);

create or replace function fn_update_user(in_user_id int, in_data jsonb)
returns void
as $$
begin

	insert into user_profile (
		user_id,
		first_name,
		last_name,
		screen_name,
		phone,
		birth_month,
		birth_year,
		gender,
		height,
		weight
	)
	values (
		in_user_id,
		nullif(in_data->>'first_name'		, ''),
		nullif(in_data->>'last_name'		, ''),
		nullif(in_data->>'screen_name'		, ''),
		nullif(in_data->>'phone' 			, ''),
		nullif(in_data->>'birth_month'		, '')::integer,
		nullif(in_data->>'birth_year'		,'')::integer,
		nullif(in_data->>'gender'			, ''),
		nullif(in_data->>'height'			, '')::float4,
		nullif(in_data->>'weight'			, '')::integer
	)
	on conflict (user_id)
	do update set
    	first_name  = excluded.first_name,
        last_name   = excluded.last_name,
        screen_name = excluded.screen_name,
        phone       = excluded.phone,
        birth_month = excluded.birth_month,
        birth_year  = excluded.birth_year,
        gender      = excluded.gender,
        height      = excluded.height,
        weight      = excluded.weight,
        modified_date = CURRENT_TIMESTAMP
    where user_profile.user_id = in_user_id;

end;
$$ language plpgsql;




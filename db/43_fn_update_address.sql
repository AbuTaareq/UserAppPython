/*

	File Name: 43_fn_update_address.sql
	Author: Shihab Hassan
	Created Date: 4/27/2026
	Last Modified: 5/26/2026

*/

drop function if exists fn_update_address(int, jsonb);

create or replace function fn_update_address(in_user_id int, in_data jsonb)
returns void
as $$
begin
	insert into user_address (
		user_id,
		street,
		city,
		county,
		state,
		zip_code,
		country,
		from_month,
		from_year
	)
	values (
		in_user_id,
		nullif(in_data->>'street',''),
		nullif(in_data->>'city',''),
		nullif(in_data->>'county',''),
		nullif(in_data->>'state',''),
		nullif(in_data->>'zip_code',''),
		nullif(in_data->>'country',''),
		nullif(in_data->>'from_month','')::int,
		nullif(in_data->>'from_year','')::int
	)
	on conflict (user_id, from_month, from_year) do update set
        street = excluded.street,
        city = excluded.city,
        county = excluded.county,
        state = excluded.state,
        zip_code = excluded.zip_code,
        country = excluded.country,
        from_month = excluded.from_month,
        from_year = excluded.from_year,
        modified_date = current_timestamp
    where user_address.user_id = in_user_id;
end;
$$ language plpgsql;




/*
	File Name: 40_fn_update_eduction.sql
	Author: Shihab Hassan
	Created Date: 5/22/2026
	Modified Date: 5/26/2026
*/
drop function if exists fn_update_education(int, jsonb);

create or replace function fn_update_education(in_user_id int, in_data jsonb)
returns void
as $$
begin
	insert into user_education (
		user_id,
		completed_year,
		degree,
		major,
		institution,
		city,
		state,
		country
	)
	values (
		in_user_id,
		nullif(in_data ->> 'completed_year'	, '')::int,
		nullif(in_data ->> 'degree'       	, ''),
		nullif(in_data ->> 'major'        	, ''),
		nullif(in_data ->> 'institution'  	, ''),
		nullif(in_data ->> 'city'         	, ''),
		nullif(in_data ->> 'state'        	, ''),
		nullif(in_data ->> 'country'       	, '')
	)
	on conflict (user_id, completed_year) do update set
		degree 			= excluded.degree,
        major       	= excluded.major,
        institution 	= excluded.institution,
        city        	= excluded.city,
        state       	= excluded.state,
        country     	= excluded.country,
        modified_date 	= current_timestamp
    where user_education.user_id = in_user_id
      and user_education.completed_year = excluded.completed_year;
end;
$$ language plpgsql;

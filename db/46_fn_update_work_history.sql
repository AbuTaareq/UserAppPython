/*

	File Name: 46_fn_update_work_history.sql
	Author: Shihab Hassan
	Created Date: 6/22/2026
	Last Modified: 6/22/2026

*/

drop function if exists fn_update_work_history(int, jsonb);

create or replace function fn_update_work_history(in_user_id int, in_data jsonb)
returns void
as $$
begin
	insert into user_work_history (
		user_id,
		work_year,
		designation,
		company_name,
		city,
		state,
		country
	)
	values (
		in_user_id,
		nullif(in_data->>'work_year','')::int,
		nullif(in_data->>'designation',''),
		nullif(in_data->>'company_name',''),
		nullif(in_data->>'city',''),
		nullif(in_data->>'state',''),
		nullif(in_data->>'country','')
	)
	on conflict (user_id, work_year, designation) do update set
		company_name = excluded.company_name,
		city = excluded.city,
		state = excluded.state,
		country = excluded.country,
        modified_date = current_timestamp
    where user_work_history.user_id = in_user_id
      and user_work_history.work_year = excluded.work_year
      and user_work_history.designation = excluded.designation;

end;
$$ language plpgsql;




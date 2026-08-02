/*
	File Name: 15_fn_delete_eduction.sql
	Author: Shihab Hassan
	Created Date: 5/22/2026
	Modified Date: 5/22/2026
*/
drop function if exists fn_delete_education(int, int);

create or replace function fn_delete_education(
      in_user_id int
    , in_completed_year int
)
returns void
as $$
begin

	-- delete row if found
    delete from user_education
    where user_id = in_user_id
      and completed_year = in_completed_year;

end;
$$ language plpgsql;

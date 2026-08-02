/*
	File Name: 53_fn_delete_work_history.sql
	Author: Shihab Hassan
	Created Date: 5/26/2026
	Modified Date: 5/26/2026
*/
drop function if exists fn_delete_work_history(int, int, varchar);
create or replace function fn_delete_work_history(
      in_user_id int
	, in_work_year int
    , in_designation varchar
)
returns void
as $$
begin

	-- delete row if found
    delete from user_work_history
    where user_id = in_user_id
      and work_year = in_work_year
      and designation = in_designation;

end;
$$ language plpgsql;

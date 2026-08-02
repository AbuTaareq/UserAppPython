/*
	File Name: 51_fn_delete_education.sql
	Author: Shihab Hassan
	Created Date: 5/26/2026
	Modified Date: 5/26/2026
*/
drop function if exists fn_delete_address(int, int, int);
create or replace function fn_delete_address(
      in_user_id int
	, in_from_month int
    , in_from_year int
)
returns void
as $$
begin

	-- delete row if found
    delete from user_address
    where user_id = in_user_id
      and from_month = in_from_month
      and from_year = in_from_year;

end;
$$ language plpgsql;

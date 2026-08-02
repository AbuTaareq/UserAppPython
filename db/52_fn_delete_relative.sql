/*
	File Name: 52_fn_delete_relative.sql
	Author: Shihab Hassan
	Created Date: 5/29/2026
	Modified Date: 5/29/2026
*/
drop function if exists fn_delete_relative(int, int, varchar);

create function fn_delete_relative(
      in_user_id int
	, in_relation_id int
    , in_relative_name varchar
)
returns void
as $$
declare
    v_count int;
begin

	-- delete row if found
    delete from user_relative
    where user_id = in_user_id
      and relation_id = in_relation_id
      and relative_name = in_relative_name               ;

    get diagnostics v_count = row_count;

    if v_count = 0 then
        raise exception 'No row found for user_id: %, relation_id: %, relative_name: %', in_user_id, in_relation_id, in_relative_name;
    end if;

end;
$$ language plpgsql;

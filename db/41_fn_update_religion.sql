/*

	File Name: 41_fn_update_religion.sql
	Author: Shihab Hassan
	Created Date: 5/4/2026
	Last Modified: 5/4/2026

*/

drop function if exists fn_update_religion;

create function fn_update_religion(
    in_user_id int,
    in_religion_id int[]
)
returns void
as $$
begin

    -- delete existing religion for the user
    delete  from user_religion
    where   user_id = in_user_id;

    -- insert the new religion for the user
    insert into user_religion (user_id, religion_id)
    select in_user_id, unnest(in_religion_id)
    on conflict (user_id, religion_id) do nothing;

end;
$$ language plpgsql;




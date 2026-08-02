/*

	File Name: 49_fn_update_roles.sql
	Author: Shihab Hassan
	Created Date: 5/4/2026
	Last Modified: 6/6/2026

*/

drop function if exists fn_update_roles;

create function fn_update_roles(
    in_user_id int,
    in_religion_id int[]
)
returns void
as $$
begin

    -- delete existing religion for the user
    delete  from user_role
    where   user_id = in_user_id;

    -- insert the new religion for the user
    insert into user_role (user_id, role_id)
    select in_user_id, unnest(in_religion_id)
    on conflict (user_id, role_id) do nothing;

end;
$$ language plpgsql;




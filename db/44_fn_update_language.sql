/*

	File Name: 44_fn_update_language.sql
	Author: Shihab Hassan
	Created Date: 5/8/2026
	Last Modified: 5/8/2026

*/

drop function if exists fn_update_language;

create function fn_update_language(
	in_user_id int,
	in_language_id int[]
)
returns void
as $$
begin

    -- delete existing
    delete from user_language where user_id = in_user_id;

    -- insert the new
    insert into user_language (user_id, language_id)
    select in_user_id, unnest(in_language_id)
    on conflict (user_id, language_id)
    do nothing;

end;
$$ language plpgsql;




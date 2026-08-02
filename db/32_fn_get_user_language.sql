/*
    File: 32_fn_get_user_language.sql
    Author: Shihab Hassan
    Created on: 05/08/2026
    Last Modified: 05/08/2026
  */

drop function if exists fn_get_user_language(int);

create function fn_get_user_language(in_user_id int)
returns table (
    language_id integer,
    language_name varchar
)
as $$

	select ul.language_id, lm.language_name
	from user_language ul
	join language_master lm on lm.language_id = ul.language_id
	where ul.user_id = in_user_id;

$$ language sql;


/*

	File Name: 20_fn_lookup_languages.sql
	Author: Shihab Hassan
	Created Date: 5/6/2026
	Last Modified: 5/25/2026

*/
drop function if exists fn_lookup_languages();

create function fn_lookup_languages()
returns table (
    language_id integer,
    language_name varchar
)
as $$
    select language_id, language_name
    from language_master l;
$$ language sql;


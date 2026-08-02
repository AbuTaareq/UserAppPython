/*

	File Name: 22_fn_lookup_languages.sql
	Author: Shihab Hassan
	Created Date: 5/6/2026
	Last Modified: 5/25/2026

*/
drop function if exists fn_lookup_religions();

create function fn_lookup_religions()
returns table (
	religion_id integer,
	religion_name varchar
)
as $$
	select religion_id, religion_name
	from religion_master
$$ language sql;


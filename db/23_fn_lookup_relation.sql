/*

	File Name: 23_fn_lookup_relation.sql
	Author: Shihab Hassan
	Created Date: 5/28/2026
	Last Modified: 5/28/2026

*/
drop function if exists fn_lookup_relation();

create function fn_lookup_relation()
returns table (
	relation_id integer,
	relation_name varchar
)
as $$
	select relation_id, relation_name
	from relation_master
	order by relation_id
$$ language sql;


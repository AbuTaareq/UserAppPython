/*

	File Name: 35_fn_get_user_religion.sql
	Author: Shihab Hassan
	Created Date: 5/4/2026
	Last Modified: 5/25/2026

*/

drop function if exists fn_get_user_religion(int);

create function fn_get_user_religion(in_user_id int)
returns table (
    religion_id integer,
    religion_name varchar
)
as $$
    select u.religion_id, m.religion_name
    from user_religion u
    join religion_master m on u.religion_id = m.religion_id
    where u.user_id = in_user_id;
$$ language sql;

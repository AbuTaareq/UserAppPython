/*

	File Name: 33_fn_get_user_education.sql
	Author: Shihab Hassan
	Created Date: 5/21/2026
	Last Modified: 5/21/2026

*/
drop function if exists fn_get_user_education(integer);

create function fn_get_user_education(in_user_id integer)
returns table (
     completed_year integer
    ,degree         varchar
    ,major          varchar
    ,institution    varchar
    ,city          varchar
    ,state         varchar
    ,country       varchar
)
as $$
begin
    return query
    select
         e.completed_year
        ,e.degree
        ,e.major
        ,e.institution
        ,e.city
        ,e.state
        ,e.country
    from user_education e
    where e.user_id = in_user_id
    order by e.completed_year desc;
end;
$$ language plpgsql;




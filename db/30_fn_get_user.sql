/*

	File Name: 30_fn_get_user.sql
	Author: Shihab Hassan
	Created Date: 5/11/2026
	Last Modified: 5/11/2026

*/
drop function if exists fn_get_user(integer);

create function fn_get_user(in_user_id integer)
returns table (
     first_name  varchar
    ,last_name   varchar
    ,screen_name varchar
    ,phone       varchar
    ,birth_month integer
    ,birth_year  integer
    ,gender      varchar
    ,height      numeric(3,1)
    ,weight      integer
)
as $$
begin
    return query
    select
         p.first_name    as first_name
        ,p.last_name     as last_name
        ,p.screen_name   as screen_name
        ,p.phone         as phone
        ,p.birth_month   as birth_month
        ,p.birth_year    as birth_year
        ,p.gender        as gender
        ,round(p.height::numeric,1) as height
        ,p.weight         as weight
    from user_master u
    left join user_profile p on p.user_id = u.user_id
    where u.user_id = in_user_id;
end;
$$ language plpgsql;




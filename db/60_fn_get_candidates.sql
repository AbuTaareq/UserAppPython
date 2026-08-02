/*

	File Name: 60_fn_get_candidates.sql
	Author: Shihab Hassan
	Created Date: 6/26/2026

	Calculating offset: (page - 1) * limit

*/
drop function if exists fn_get_candidates(in_limit integer, in_offset integer);

create function fn_get_candidates(
	in_limit integer default 10,
	in_offset integer default 0
)
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
    ,total_count integer
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
        ,(count(*) over())::int  as total_count
    from user_profile p
    order by p.first_name
    limit in_limit
    offset in_offset;
end;
$$ language plpgsql;




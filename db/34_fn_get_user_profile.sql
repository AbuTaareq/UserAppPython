/*

	File Name: 34_fn_get_user_profile.sql
	Author: Shihab Hassan
	Created Date: 4/17/2026
	Last Modified: 5/4/2026

*/
drop function public.fn_get_user_profile(integer);

create or replace function fn_get_user_profile(in_user_id integer)
returns table (
    user_id     integer,
    user_email  varchar,
    phone       varchar,
    first_name  varchar,
    last_name   varchar,
    screen_name varchar,
    birth_month integer,
    birth_year  integer,
    gender      varchar,
    height      float4,
    weight      integer,
    role_id     integer,
    role_name   varchar
)
as $$
begin
    return query
    select
         u.user_id
        ,u.user_email
        ,p.phone
        ,p.first_name
        ,p.last_name
        ,p.screen_name
        ,p.birth_month
        ,p.birth_year
        ,p.gender
        ,p.height
        ,p.weight
        ,p.user_role_id
        ,r.role_name
    from user_master u
    left join user_profile p on p.user_id = u.user_id
    left join role_master r on r.role_id = p.user_role_id
    where u.user_id = in_user_id;
end;
$$ language plpgsql;




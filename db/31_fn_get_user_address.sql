/*

	File Name: 31_fn_get_user_address.sql
	Author: Shihab Hassan
	Created Date: 4/30/2026
	Last Modified: 10/28/2026

*/
drop function if exists fn_get_user_address(integer);

create or replace function fn_get_user_address(in_user_id integer)
returns table (
    street      varchar,
    city        varchar,
    county      varchar,
    state       varchar,
    zip_code    varchar,
    country     varchar,
    from_month  integer,
    from_year   integer,
    is_current  boolean
)
as $$
begin
    return query
    select
         a.street       as street,
         a.city         as city,
         a.county       as county,
         a.state        as state,
         a.zip_code     as zip_code,
         a.country      as country,
         a.from_month   as from_month,
         a.from_year    as from_year,
         a.is_current   as is_primary
    from user_master u
    left join user_address a on a.user_id = u.user_id
    where u.user_id = in_user_id
    order by a.from_year desc, a.from_month desc;
end;
$$ language plpgsql;




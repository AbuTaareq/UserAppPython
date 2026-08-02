# Postgres
If you are working with Postgres at localhost,
    Login with Shihab with no password
    If you want to change admin or password, go to pgadmin GUI
    Stop the server and change the user or password restart.

### Cannot drop database
    # The below command fails becauase there are active connections.
    drop database user_project;

    # force drop, will kill all connections and drop the database
    drop database user_project (FORCE);

### Kill connections
    # query postgres stat activities
    select pid, username, application_name from pg_stat_activity;

    # kill query
    select pg_cancel_backend(<PID>);

    # terminate connection
    select pg_terminate_backend(<PID>);


### Create admin user
    create user app_user with superuser password 'pass123';

### Change existing user as a admin user
    alter user app_user with superuser;

### create user with password grant all privileges on database
    create user app_user with password 'pass123';
    grant all privileges on database user_project to app_user;
    grant all on schema public to app_user;
    grant all privileges on all tables in schema public to app_user;

    Now app_user can login with password and access the database and tables.

# Initialize

    -- must be db admin other than app_user
    -- switch to postgres database other than user_project
    drop database user_project (FORCE);
    reassign owned by app_user to postgres;
    drop owned by app_user;
    drop user app_user; 


    drop database user_project (FORCE);
    reassign owned by app_user to postgres;
    drop owned by app_user;
    drop user app_user;
    
    create role app_user with login password 'pass123';
    create database user_project owner app_user;
    grant all on schema public to app_user;
    alter schema public owner to app_user;

    -- after the above create your database objects
    
    -- validate current user and database
    -- select current_database(), current_user;

    -- use the role before creating objects
    -- set role app_user;

    -- alter table to set the owner to the role
    -- alter table table_name owner to app_user;

    -- set the search path to the database schema before creating objects
    -- set search_path to app_user, public;

    -- validate the schema by the following query
    -- select table_name from pg_tables where table_schema = 'app_user';
    -- select table_name from pg_tables where table_schema = 'public';
    --

    
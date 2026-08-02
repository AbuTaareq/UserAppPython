import asyncpg
import sys
import json
from fastapi import HTTPException

from models.settings import settings
from models.color import Color

# noinspection PyUnresolvedReferences
class DB:

    # asyncpg pool to store database connections
    pool: asyncpg.Pool = None

    def __init__(self):
        pass

    @classmethod
    async def create_pool(cls):
        
        print(f'{Color.yellow}Attempting database connection pool')
        # Create a database connection pool
        try:
            cls.pool = await asyncpg.create_pool(
                settings.database_url,
                min_size=1,
                max_size=10
            )
            print(f'{Color.lightGreen}Database connection pool created{Color.reset}')
            return cls.pool
        except OSError as e:
            print(f'{Color.red}OSError: {Color.orange}Connection refused{Color.reset}')
            print(f'{Color.red}Details: {Color.orange}{e}{Color.reset}')
            print(f'{Color.red}Program Abort !!{Color.reset}')
            raise SystemExit(1)
        except Exception as e:
            print(f'\n{Color.red}(CreatePool) DB ERROR: {e} {Color.reset}')
            print(f"{Color.green}The exact exception raised is: {type(e).__name__}")
            print(f'{Color.red}Program Abort !!{Color.reset}')
            raise SystemExit(1)
        

    @classmethod
    async def close_pool(cls):
        if cls.pool:
            # Close the database connection pool
            await cls.pool.close()

    @staticmethod
    def connect():
        try:
            connection = psycopg.connect(settings.database_url)
        except Exception as e:
            print(f'\n{Color.red}(ConnectDB) DB ERROR: {e}\nProgram Abort !!{Color.reset}')
            sys.exit(1)
        return connection


    # Generic reusable database handler
    @staticmethod
    def exception(e: Exception):

        if isinstance(e, asyncpg.exceptions.NotNullViolationError):
            print(f'\n{Color.red}Not Null Violation Error:\n {e}\n{Color.reset}')
            raise HTTPException(400, "Missing required fields")

        if isinstance(e, asyncpg.exceptions.UniqueViolationError):
            print(f'\n{Color.red}Unique Violation Error:\n {e}\n{Color.reset}')
            raise HTTPException(409, "Unique Constraint Violation")

        if isinstance(e, asyncpg.exceptions.UndefinedFunctionError):
            print(f'\n{Color.red}Undefined Function Error:\n {e}\n{Color.reset}')
            raise HTTPException(500, f"Undefined Function Error")

        if isinstance(e, asyncpg.PostgresError):
            print(f'\n{Color.red}Database Error:\n {e}\n{Color.reset}')
            raise HTTPException(501, f"Database Error, contact support")

        print(f'{Color.red}Uncaptured Database Error.')
        print(f'{Color.orange}{e}{Color.reset}')
        print(f"{Color.green}Exception: {type(e).__name__}")
        raise HTTPException(502, f"Unexpected error")


    # database log entries
    @staticmethod
    def log(message: dict):
        with DB.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute('CALL sp_user_log (%s)', (json.dumps(message),))
                except Exception as e:
                    DB.exception(e)

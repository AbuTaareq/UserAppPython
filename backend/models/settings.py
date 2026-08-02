from pydantic_settings import BaseSettings

# Environment variables
class Settings(BaseSettings):

    # CORS
    origins: list[str] = [
        "http://localhost",
        "http://127.0.0.1",

        "http://127.0.0.1:3000",
        "http://localhost:3000",

        "http://129.121.78.197",
        "http://129.121.78.197:3000",
        "http://129.121.78.197:80"
    ]

    # Environment variables
    database_url: str = 'postgresql://app_user:pass123@localhost:5432/user_project'
    api_url: str = 'http://localhost:8001'
    smtp_host: str = 'localhost'
    smtp_port: int = 1025

# instantiate the settings is must here, because environment variables are not set
settings = Settings()




#
#   Author: Shihab Hassan
#   Created:  11/01/2024
#   Modified: 03/29/2026
import asyncio

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# import models
from models.color import Color
from models.settings import settings
from models.database import DB

# import routers
from routers import user
from routers import profile
from routers import data

# Create the asyncpg connection pool at startup and reuse it for the entire application
@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    fast_api.state.pool = await DB.create_pool()
    yield
    await DB.close_pool()

# Create a fast API instance
print(f'{Color.yellow}Starting the main application...{Color.reset}')
app = FastAPI(lifespan=lifespan)
print(f'{Color.lightGreen}Created app instance{Color.reset}')
print(f'{Color.yellow}Attempting lifespan{Color.reset}')

# Include routers from the routers folder
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(data.router, prefix="/data", tags=["Data"])

# enable cors to allow request from every origin
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log all requests and responses
@app.middleware("http")
async def log_request(request: Request, call_next):
    print(f'{Color.purple}Request: {Color.reset}{request.url}')
    response = await call_next(request)
    # print(f'{Color.green}Response: {Color.reset}{response.status_code}')
    return response


# Catch and customize validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    print("🔥 Path:", request.url.path)
    print("🔥 Method:", request.method)
    print("🔥 Validation errors:", exc.errors())
    print("🔥 Incoming body:", exc.body)

    return JSONResponse(
        status_code=422,
        content={
            "message": "Invalid request body",
            "errors": [
                {
                    "field": err["loc"][-1],
                    "error": err["msg"]
                }
                for err in exc.errors()
            ],
            "body": exc.body
        }
    )


# Define homepage endpoint or path
@app.get("/")
async def root():
    return {"message": "Hello World"}


async def check_database():
    await DB.create_pool()
    await DB.close_pool()


if __name__ == "__main__":
    
    print(f'{Color.yellow}Validate database connections...{Color.reset}')
    try:
        asyncio.run(check_database())
    except OSError as e:
        print(f'{Color.red}OSError: {Color.orange}Connection refused{Color.reset}')
        print(f'{Color.red}Details: {Color.orange}{e}{Color.reset}')
        raise
    except Exception as e:
        print(f'{Color.red}DB ERROR: {Color.orange}{e}{Color.reset}')
        print(f"{Color.red}Exception: {Color.orange}{type(e).__name__}{Color.reset}")
        print(f'{Color.yellow}Program Abort !!{Color.reset}')
        raise
    
    # Use this for debugging purposes only
    print(f'{Color.lightGreen}Database Connection validated...{Color.reset}')
    print(f'{Color.yellow}Starting uvicorn...{Color.reset}')
    import uvicorn
    uvicorn.run(app, port=8001, log_level="debug")



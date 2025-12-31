from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from users.routes import router as users_routes
from expenses.routers import router as expense_routes
from expenses.exceptions import ExpenseNotFoundError
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from core.config import settings


tags_metadata = [
    {
        "name": "authenticates",
        "description": "Operations with authes, including creating, updating, and deleting authes.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup.")
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(
        RedisBackend(redis),
        prefix="fastapi-cache"
    )
    yield
    await redis.close()
    print("Application shutdown.")


app = FastAPI(
    title="Management Cost",
    description="This is descriptation.",
    version="0.0.1",
    contact={
        "name": "Arash Mousavi",
        "email": "arashzmousavi@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.include_router(users_routes)
app.include_router(expense_routes)


@app.exception_handler(ExpenseNotFoundError)
async def expense_not_found_handler(
    request: Request, exc: ExpenseNotFoundError
):
    error_response = {
        "error": True,
        "message": str(exc.message),
        "path": request.url.path,
        "method": request.method,
    }

    return JSONResponse(status_code=exc.status_code, content=error_response)

from fastapi import FastAPI
from contextlib import asynccontextmanager
from users.routes import router as users_routes
from expenses.routers import router as expense_routes


tags_metadata = [
    {
        "name": "authenticates",
        "description": "Operations with authes, including creating, updating, and deleting authes.",
    },
]


@asynccontextmanager
async def lifspan(app: FastAPI):
    print("Application startup.")
    yield
    print("Application shutdown.")


app = FastAPI(
    title="Auth Application",
    description="This is descriptation.",
    version="0.0.1",
    contact={
        "name": "Arash Mousavi",
        "email": "arashzmousavi@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifspan,
    openapi_tags=tags_metadata,
)

app.include_router(users_routes)
app.include_router(expense_routes)

from fastapi import FastAPI
from app.core.db import Base, engine

from app.api.routers import main_router
from app.api.endpoints.charity_project import router as charity_project_router
from app.api.endpoints.donation import router as donation_router
from app.api.endpoints.user import router as user_router
from app.core.user import fastapi_users, auth_backend
from app.schemas.user import UserCreate, UserRead

app = FastAPI(
    title='Благотворительный фонд QRKot',
    description='Приложение для управления благотворительными проектами',
    version='1.0.0',
)

app.include_router(main_router)

app.include_router(fastapi_users.get_auth_router(auth_backend))


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)


app.include_router(
    fastapi_users.get_users_router(UserRead, UserCreate),
    prefix='/users',
    tags=['users'],
)


app.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['charity_projects'],
)

app.include_router(
    donation_router,
    prefix='/donation',
    tags=['donations'],
)


app.include_router(
    user_router,
    prefix='/users_custom',
    tags=['users_custom'],
)


@app.get('/')
async def root():
    return {'message': 'Добро пожаловать в API Благотворительного фонда QRKot'}


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

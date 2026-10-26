import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.user import User


TEST_DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv("TEST_DATABASE_USER", "postgres"),
    password=os.getenv("TEST_DATABASE_PASSWORD"),
    host=os.getenv("TEST_DATABASE_HOST", "localhost"),
    port=int(os.getenv("TEST_DATABASE_PORT", "5432")),
    database="tixstern_test",
)

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(
    scope="session",
    loop_scope="session",
    autouse=True,
)
async def prepare_database():
    """Ensure the test database has the application tables."""
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(prepare_database):
    """Provide a clean database session for each test."""
    async with TestSessionLocal() as session:
        await session.execute(delete(User))
        await session.commit()

        yield session

        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session):
    """Create an HTTP client using the test database."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
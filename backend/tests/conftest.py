import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import settings
from app.core.database import db, connect_to_mongo

settings.DATABASE_NAME = "contentiq_test"

@pytest.fixture(autouse=True)
async def setup_test_db():
    await connect_to_mongo()
    yield
    if db.client:
        await db.client.drop_database("contentiq_test")

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

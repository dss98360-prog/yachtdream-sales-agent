import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
os.environ["DATABASE_URL"] = "sqlite:///./data/test_yachtdream.db"
os.environ["ADMIN_API_KEY"] = "test-admin-key"
os.environ["ALLOWED_HOSTS"] = "testserver,localhost,127.0.0.1"

from app.config import get_settings  # noqa: E402

get_settings.cache_clear()
from app.db import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def valid_lead():
    return {
        "name": "Алексей",
        "email": "alex@example.com",
        "phone": "+7 900 123-45-67",
        "experience": "none",
        "goal": "captain",
        "destination": "turkey",
        "season": "autumn",
        "group_type": "solo",
        "comment": "Хочу научиться управлять яхтой",
    }


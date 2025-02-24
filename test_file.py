from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from app.api.dbhelper import models,schemas
import pytest
from app.api.dbhelper.database import get_db

client = TestClient(app)

DB_URL_LITE = "sqlite:///:memory:"

Engine = create_engine(DB_URL_LITE, connect_args={"check_same_thread": False}, poolclass = StaticPool)

TestingSessionLocal = sessionmaker(bind=Engine, autoflush=False)

@pytest.fixture(scope="module",autouse= True)
def setup_and_teardown():
    models.Base.metadata.create_all(bind=Engine)  
    yield  
    models.Base.metadata.drop_all(bind=Engine)  

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


#/////////////////////////////////#

@pytest.fixture
def mock_user():
    user_data = schemas.User(
        username="testuser",
        password="password123",
        email="testuser@example.com", 
        base_role="Student",  
        auth_role="SomeRole" 
    )
    return user_data

def test_login_token(mock_user):
    db = TestingSessionLocal()
    db_user = models.User(username=mock_user.username, password="hashedpassword", base_role=mock_user.base_role)
    db.add(db_user)
    db.commit()

    login_data = {"username": mock_user.username, "password": mock_user.password}
    response = client.post("/login_token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert "SESSION_COOKIE_NAME" in response.cookies



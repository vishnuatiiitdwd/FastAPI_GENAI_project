from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import pytest
from app.api.dbhelper import models
from app.api.dbhelper.database import get_db
from app.api.helpers import hashing
import os
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module", autouse=True)
def override_get_db(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

@pytest.fixture
def mock_user(db_session):
    db = db_session 
    hashed_password = hashing.get_hash_password("password123")

    existing_user = db.query(models.User).filter(models.User.username == "testuser").first()
    if existing_user:
        db.delete(existing_user)
        db.commit()

    db_user = models.User(
        username="myuser",
        email="testuser@example.com",
        password=hashed_password, 
        base_role="Student",
        auth_role="SomeRole"
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)  

    yield db_user 
    db.delete(db_user)
    db.commit()


def test_login_token(mock_user):

    login_data = {"username": mock_user.username, "password": "password123"}
    response = client.post("/login_token", data=login_data)

    assert response.status_code == 200, response.text
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert "session_token" in response.cookies

    return response.json()["access_token"]  

# def test_create_user():
#     response = client.post("/user_create",json={
#         "username":"dhilipkarthikk",
#         "email": "harish@gmail.com",
#         "password":"karthik",
#         "base_role":"Banker",
#         "auth_role":"user"
#     })
#     assert response.status_code == 200,response.text
#     data = response.json()
#     assert data["username"] == "dhilipkarthikk"
#     assert data["base_role"] == "Banker"


def test_read_users_me(mock_user):
    login_data = {"username": "myuser", "password": "password123"}
    res = client.post("/login_token", data=login_data)

    assert res.status_code == 200, res.text
    access_token = res.json()["access_token"] 
    print(access_token)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/me", cookies={"session_token": access_token})  

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["username"] == "myuser"

def test_delete_item():
    login_data = {"username": "dhilip", "password": "dhilip"}
    res = client.post("/login_token", data=login_data)

    assert res.status_code == 200, res.text
    access_token = res.json()["access_token"] 
    response = client.get("/users/me", cookies={"session_token": access_token})
    user_id = 7
    response = client.delete(f"/delete/user/{user_id}",cookies={"session_token": access_token})
    assert response.status_code == 200,response.text
    

def test_update_item():
    login_data = {"username": "dhilip", "password": "dhilip"}
    res = client.post("/login_token", data=login_data)

    assert res.status_code == 200, res.text
    access_token = res.json()["access_token"]
    response = client.put(
        f"/update_user/{4}",
        json={"username":"vishnu","email":"vishnu@gmail.com","password":"False","base_role": "Banker","auth_role":"user"},
        cookies={"session_token": access_token}
    )
    assert response.status_code == 200,response.text
    data = response.json()
    assert data["username"] == "vishnu"
    assert data["email"] == "vishnu@gmail.com"

def test_logout():
    login_data = {"username": "dhilip", "password": "dhilip"}
    res = client.post("/login_token", data=login_data)

    assert res.status_code == 200, res.text
    access_token = res.json()["access_token"]
    response = client.post("/user/logout",cookies={"session_token": access_token})
    assert response.status_code == 200,response.text

def test_genai_response():
    login_data = {"username": "dhilip", "password": "dhilip"}
    res = client.post("/login_token", data=login_data)
    assert res.status_code == 200, res.text
    access_token = res.json()["access_token"]
    file_content = b"Fake audio file content"
    files = {"file": ("test_audio.wav", file_content, "audio/wav")}
    data = {"question": "What is the summary of this audio?"}
    response = client.post("/upload", files=files, data=data, cookies={"session_token": access_token})
    assert response.status_code == 200, response.text
    assert response.json()["message"] == "File uploaded successfully"
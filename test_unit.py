# from fastapi.testclient import TestClient
# from main import app
# from fastapi import Depends
# from sqlalchemy import create_engine
# from sqlalchemy.pool import StaticPool
# from sqlalchemy.orm import sessionmaker
# from app.api.dbhelper import models,schemas
# from sqlalchemy.orm import Session
# import pytest
# from app.api.dbhelper.database import get_db
# from app.api.helpers import hashing
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# client = TestClient(app)

# DB_URL = "postgresql://postgres:Dhilip04@localhost:5432/GenAI"
# engine = create_engine(DB_URL)

# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# Base = declarative_base()

# @pytest.fixture
# def mock_user():
#     """Create a user in the actual PostgreSQL database"""
#     db = SessionLocal()
#     hashed_password = hashing.get_hash_password("password123")

#     db_user = models.User(
#         username="testuser",
#         email="testuser@example.com",
#         password=hashed_password,
#         base_role="Student",
#         auth_role="SomeRole"
#     )

#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)  # Ensure instance is attached to session

#     return db_user



# def test_login_token(mock_user):
#     login_data = {"username": mock_user.username, "password": "password123"}
#     response = client.post("/login_token", data=login_data)

#     assert response.status_code == 200
#     assert "access_token" in response.json()
#     assert response.json()["token_type"] == "bearer"
#     assert "session_token" in response.cookies

# # def test_create_user():
# #     response = client.post("/user_create",json={
# #         "username":"dhilipp",
# #         "email": "harish@gmail.com",
# #         "password":"karthik",
# #         "base_role":"Banker",
# #         "auth_role":"user"
# #     })
# #     assert response.status_code == 200,response.text
# #     data = response.json()
# #     assert data["username"] == "dhilipp"
# #     assert data["base_role"] == "Banker"


# def test_read_item():
#     login_data = {"username": "dhilipp", "password": "karthik"}  
#     res = client.post("/login_token", data=login_data)
#     access_token = res.json()["access_token"]
#     print(access_token)
#     headers = {"Authorization": f"Bearer {access_token}"}
#     response = client.get("/users/me",headers=headers)
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["username"] == "testuser"
#     assert data["base_role"] == "Student"
    


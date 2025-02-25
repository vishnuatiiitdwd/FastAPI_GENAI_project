from fastapi import FastAPI
from app.api.dbhelper.database import engine
from app.api.dbhelper import models
from app.api import routes
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(engine)


app.include_router(routes.router)

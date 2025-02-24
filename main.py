from fastapi import FastAPI
from app.api.dbhelper.database import engine
from app.api.dbhelper import models
from app.api import routes


app=FastAPI()


models.Base.metadata.create_all(engine)


app.include_router(routes.router)

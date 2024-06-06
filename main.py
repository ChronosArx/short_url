from fastapi import FastAPI
from core import shorten_router
from database.data_base_conf import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(shorten_router.router)

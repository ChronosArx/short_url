from fastapi import FastAPI
from free_shorten import free_router
from database.data_base_conf import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(free_router.router)

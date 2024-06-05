from fastapi import FastAPI
from core import shorten_router

app = FastAPI()

app.include_router(shorten_router.router)
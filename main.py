from fastapi import FastAPI
from free_shorten import free_router

app = FastAPI()

app.include_router(free_router.router)
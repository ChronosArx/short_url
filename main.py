from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .free_shorten import free_routes
from .auth import auth_routes
from .premium_shorten import premium_routes

app = FastAPI()


app.include_router(router=free_routes.router)
app.include_router(router=auth_routes.router)
app.include_router(router=premium_routes.router)

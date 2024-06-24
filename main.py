from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .shorten import shorten_routes
from .auth import auth_routes
from. redirects import redirects_routes

app = FastAPI()

VERSION_API = '/apiv1'

app.include_router(router=redirects_routes.router)
app.include_router(prefix=VERSION_API, router=shorten_routes.router)
app.include_router(prefix=VERSION_API,router=auth_routes.router)
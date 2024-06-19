from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .free_shorten import free_routes
from .auth import auth_routes
from .premium_shorten import premium_routes
from. redirects import redirects_routes

app = FastAPI()

VERSION_API = '/apiv1'

app.include_router(router=redirects_routes.router)
app.include_router(prefix=VERSION_API, router=free_routes.router)
app.include_router(prefix=VERSION_API,router=auth_routes.router)
app.include_router(prefix=VERSION_API,router=premium_routes.router)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import shorten_router
from .routers import auth_router
from .routers import user_router
from .routers import redirects_router

app = FastAPI()

VERSION_API = "/apiv1"

app.include_router(router=redirects_router.router)
app.include_router(prefix=VERSION_API, router=shorten_router.router)
app.include_router(prefix=VERSION_API, router=auth_router.router)
app.include_router(prefix=VERSION_API, router=user_router.router)

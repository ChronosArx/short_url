from fastapi import FastAPI
from free_shorten import free_router
from auth import auth_routes
from database.data_base_conf import Base, engine

app = FastAPI()

#Base.metadata.create_all(bind=engine)

app.include_router(free_router.router)
app.include_router(auth_routes.router)

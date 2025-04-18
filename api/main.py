from utils.lifespan import lifespan
from fastapi import FastAPI
from router.endpoints import router
app = FastAPI(lifespan=lifespan)
app.include_router(router)

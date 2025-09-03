from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="Algorand Hackathon API",
    description="FastAPI backend for Algorand hackathon project",
    version="0.1.0",
)

app.include_router(router)
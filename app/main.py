from fastapi import FastAPI
from app.routers import auth
from app.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI()

# Register routes
app.include_router(auth.router)
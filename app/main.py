
from fastapi import FastAPI
from app.routers import auth
from app.database import Base, engine

# Initialize db
def init_db():
    Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(title="ModuMart API", version="1.0")

# Call DB setup at startup
init_db()

# Register routers
app.include_router(auth.router)
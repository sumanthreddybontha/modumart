
from fastapi import FastAPI
from app.routers import auth
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Initialize db
def init_db():
    Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(title="ModuMart API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Call DB setup at startup
init_db()

# Register routers
app.include_router(auth.router)
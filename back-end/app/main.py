from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from core.config import settings
from api.v1 import providers, chatbot

# Initialize the FastAPI application
app = FastAPI(
    title="Provider Management API",
    version="1.0.0",
    docs_url="/docs"
)

# Configure Security & CORS using environment settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect your feature-specific routers
app.include_router(
    providers.router, 
    prefix="/api/v1/providers", 
    tags=["Providers"]
)

@app.get("/health", tags=["Health"])
async def health_check():
    """Verify service is live."""
    return {"status": "healthy"}

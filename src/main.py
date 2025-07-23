import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.firebase import initialize_firebase
import os
from src.config.config import get_settings
from src.api.v1.routers import api_router
from dotenv import load_dotenv
import json
from src.core.cache import init_cache
load_dotenv()
raw_origins = os.environ.get("BACKEND_CORS_ORIGINS", "[]")
try:
    origins = json.loads(raw_origins)
except json.JSONDecodeError:
    origins = []
    print("⚠️ BACKEND_CORS_ORIGINS could not be parsed. Falling back to empty list.")
app = FastAPI(
    title=get_settings().PROJECT_NAME,
    description=get_settings().PROJECT_DESCRIPTION,
    version=get_settings().VERSION,
    openapi_url=f"{get_settings().API_V1_STR}/openapi.json",
    docs_url=f"{get_settings().API_V1_STR}/docs",
    redoc_url=f"{get_settings().API_V1_STR}/redoc",
)
# Get CORS origins from environment variable
origins = os.environ.get("BACKEND_CORS_ORIGINS", "")
print("url test===",origins)
@app.on_event("startup")
async def startup():
    await init_cache()  # Initialize Redis connection
    initialize_firebase()

@app.get("/public")
async def public_endpoint():
    return {"message": "Testing"}


# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)


# Include API routers
app.include_router(api_router, prefix=get_settings().API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=get_settings().HOST,
        port=get_settings().PORT,
        reload=get_settings().RELOAD,
        workers=get_settings().WORKERS,
    )
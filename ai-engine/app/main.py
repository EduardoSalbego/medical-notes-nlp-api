from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from app.config import settings
from app.routers import medical_notes, health
from app.database import engine, Base

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Engine...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down AI Engine...")

app = FastAPI(
    title="Medical Notes NLP API - AI Engine",
    description="AI Engine for processing medical notes using NLP (NER and Risk Classification)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(medical_notes.router, prefix="/api/v1", tags=["Medical Notes"])


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status": "error"}
    )


@app.get("/")
async def root():
    return {
        "service": "Medical Notes NLP API - AI Engine",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }
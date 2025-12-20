"""
My Local AI Hub - FastAPI Main Entry

Auto-scan apps directory and register routes
"""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import torch
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from common.limiter import limiter

# Project directories
BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent

# Create FastAPI app
app = FastAPI(
    title="My Local AI Hub",
    description="Local AI inference service",
    version="1.0.0",
)



# Rate limiter config
app.state.limiter = limiter

from fastapi.responses import JSONResponse

async def custom_rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "code": 429,
            "message": "请求次数过多，请1分钟后再试",
            "data": None
        }
    )

app.add_exception_handler(RateLimitExceeded, custom_rate_limit_exceeded_handler)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files - dataset directory
dataset_dir = BASE_DIR / "storage" / "image-processing" / "dataset"
if dataset_dir.exists():
    app.mount("/dataset", StaticFiles(directory=str(dataset_dir)), name="dataset")
else:
    print(f"Warning: dataset directory not found - {dataset_dir}")

# Device detection
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Model paths
STORAGE_DIR = BASE_DIR / "storage" / "image-processing" / "checkpoint"


def init_models():
    """Initialize all models"""
    # Denoising model
    from apps.image_processing.denoising import init_model as init_denoising

    denoiser_path = STORAGE_DIR / "denoiser.pt"
    if denoiser_path.exists():
        init_denoising(str(denoiser_path), device)
    else:
        print(f"Warning: denoiser model not found - {denoiser_path}")

    # Classification model
    from apps.image_processing.classification import init_model as init_classification

    classifier_path = STORAGE_DIR / "classifier.pt"
    if classifier_path.exists():
        init_classification(str(classifier_path), device)
    else:
        print(f"Warning: classifier model not found - {classifier_path}")

    # Similarity model
    from apps.image_processing.similarity import init_model as init_similarity

    encoder_path = STORAGE_DIR / "encoder.pt"
    embeddings_path = STORAGE_DIR / "embeddings.npy"
    if encoder_path.exists() and embeddings_path.exists():
        init_similarity(str(encoder_path), str(embeddings_path), device)
    else:
        print(f"Warning: similarity model not found")


def register_routes():
    """Register all routes"""
    from apps.image_processing.routes import router as image_processing_router

    app.include_router(image_processing_router, prefix="/api")


from common.schemas import Result, ApiCode


@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    """System info"""
    return Result(
        code=ApiCode.SUCCESS,
        data={
            "name": "My Local AI Hub",
            "status": "running",
            "device": str(device),
            "endpoints": ["/api/denoising", "/api/classification", "/api/simimages"],
        },
        message="Service running"
    )


@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    """Health check"""
    return Result(
        code=ApiCode.SUCCESS,
        data={"status": "healthy"},
        message="Service healthy"
    )


# Startup initialization
@app.on_event("startup")
async def startup():
    print("Initializing models...")
    init_models()
    register_routes()
    print("Service started!")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)

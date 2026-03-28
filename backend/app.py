"""
My Local AI Hub - FastAPI Main Entry

Auto-scan apps directory and register routes
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded

from apps.image_processing import device
from common.limiter import limiter
from common.schemas import ApiCode, Result

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


async def custom_rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"code": 429, "message": "请求次数过多，请1分钟后再试", "data": None},
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
    app.mount(
        "/storage/image-processing/dataset",
        StaticFiles(directory=str(dataset_dir)),
        name="dataset",
    )
else:
    print(f"Warning: dataset directory not found - {dataset_dir}")


def register_routes():
    """Register all routes"""
    from apps.address_alignment import router as address_alignment_router
    from apps.ai_news import router as ai_news_router
    from apps.chat import router as chat_router
    from apps.image_processing import router as image_processing_router
    from apps.product_classification import router as product_classification_router

    app.include_router(image_processing_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")
    app.include_router(
        product_classification_router, prefix="/api/product-classification"
    )
    app.include_router(ai_news_router, prefix="/api/ai-news")
    app.include_router(address_alignment_router, prefix="/api/address-alignment")


@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    """System info"""
    return Result(
        code=ApiCode.SUCCESS,
        data={
            "name": "My Local AI Hub",
            "status": "running",
            "device": str(device),
            "endpoints": [
                "/api/denoising",
                "/api/classification",
                "/api/simimages",
                "/api/product-classification/predict",
                "/api/ai-news/classify",
                "/api/ai-news/summarize",
                "/api/ai-news/analyze",
                "/api/address-alignment/align",
                "/api/address-alignment/extract",
            ],
        },
        message="Service running",
    )


# Startup initialization
@app.on_event("startup")
async def startup():
    from apps.address_alignment import init_model as init_address_alignment
    from apps.ai_news import init_model as init_ai_news
    from apps.image_processing import init_all_models
    from apps.product_classification import init_model as init_product_classification

    # print("Initializing models...")
    init_all_models()
    init_product_classification()
    init_ai_news()
    init_address_alignment()
    register_routes()
    print("Service started!")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)

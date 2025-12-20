from io import BytesIO
from PIL import Image
from fastapi import APIRouter, UploadFile, File, Form, Request
from common.limiter import limiter
from common.schemas import Result, ApiCode

# Schemas
from .schemas import ClassificationResponse, DenoisingResponse, SimilarityResponse

# Services
from .classification.service import classify_image
from .denoising.service import denoise_image
from .similarity.service import find_similar_images

router = APIRouter()

# --- Classification ---
@router.post("/classification", response_model=Result[ClassificationResponse], tags=["Classification"])
@limiter.limit("10/minute")
async def classify(request: Request, image: UploadFile = File(..., description="Image to classify")):
    """
    Image classification endpoint
    
    Upload an image and get classification result
    """
    try:
        contents = await image.read()
        pil_image = Image.open(BytesIO(contents))
        result = classify_image(pil_image)
        return Result(
            code=ApiCode.SUCCESS,
            data=ClassificationResponse(result=result),
            message="Classification successful"
        )
    except Exception as e:
        return Result(
            code=ApiCode.SERVER_ERROR,
            message=f"Classification failed: {str(e)}"
        )


# --- Denoising ---
@router.post("/denoising", response_model=Result[DenoisingResponse], tags=["Denoising"])
@limiter.limit("10/minute")
async def denoise(request: Request, image: UploadFile = File(..., description="Image to denoise")):
    """
    Image denoising endpoint
    
    Upload an image and get noisy + denoised versions
    """
    try:
        contents = await image.read()
        pil_image = Image.open(BytesIO(contents))
        noisy_base64, denoised_base64 = denoise_image(pil_image)

        return Result(
            code=ApiCode.SUCCESS,
            data=DenoisingResponse(
                noisy_img=noisy_base64, denoised_image=denoised_base64
            ),
            message="Denoising successful"
        )
    except Exception as e:
        return Result(
            code=ApiCode.SERVER_ERROR,
            message=f"Denoising failed: {str(e)}"
        )


# --- Similarity ---
@router.post("/simimages", response_model=Result[SimilarityResponse], tags=["Similarity"])
@limiter.limit("10/minute")
async def find_similar(
    request: Request,
    image: UploadFile = File(..., description="Image to search"),
    num_images: int = Form(default=10, description="Number of similar images"),
):
    """
    Similar image search endpoint
    
    Upload an image and get N most similar images
    """
    try:
        contents = await image.read()
        pil_image = Image.open(BytesIO(contents))
        _, image_urls = find_similar_images(pil_image, num_images)
        return Result(
            code=ApiCode.SUCCESS,
            data=SimilarityResponse(image_urls=image_urls),
            message="Search successful"
        )
    except Exception as e:
        return Result(
            code=ApiCode.SERVER_ERROR,
            message=f"Search failed: {str(e)}"
        )

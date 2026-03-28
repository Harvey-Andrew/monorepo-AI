"""
商品标题分类 - API 路由
"""

from fastapi import APIRouter, Request

from common.limiter import limiter
from common.schemas import ApiCode, Result

from .schemas import (
    BatchClassificationResponse,
    BatchTextInput,
    ClassificationResponse,
    TextInput,
)
from .service import classify_text, classify_texts

router = APIRouter()


@router.post(
    "/predict",
    response_model=Result[ClassificationResponse],
    tags=["Product Classification"],
)
@limiter.limit("30/minute")
async def predict(request: Request, body: TextInput):
    """
    商品标题分类接口

    输入商品标题文本，返回分类结果
    """
    try:
        category = classify_text(body.text)
        return Result(
            code=ApiCode.SUCCESS,
            data=ClassificationResponse(category=category),
            message="分类成功",
        )
    except Exception as e:
        return Result(code=ApiCode.SERVER_ERROR, message=f"分类失败: {str(e)}")


@router.post(
    "/predict/batch",
    response_model=Result[BatchClassificationResponse],
    tags=["Product Classification"],
)
@limiter.limit("10/minute")
async def predict_batch(request: Request, body: BatchTextInput):
    """
    批量商品标题分类接口

    输入多个商品标题文本，返回分类结果列表
    """
    try:
        categories = classify_texts(body.texts)
        return Result(
            code=ApiCode.SUCCESS,
            data=BatchClassificationResponse(categories=categories),
            message="批量分类成功",
        )
    except Exception as e:
        return Result(code=ApiCode.SERVER_ERROR, message=f"批量分类失败: {str(e)}")

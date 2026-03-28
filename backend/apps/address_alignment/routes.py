"""
地址对齐 - API 路由
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from common.limiter import limiter
from common.schemas import ApiCode, Result

from .schemas import AddressInput, AddressResponse, TaggingResponse
from .service import align_address, extract_address, is_ready, predict_tags

router = APIRouter()


@router.post(
    "/align",
    response_model=Result[AddressResponse],
    tags=["Address Alignment"],
)
@limiter.limit("30/minute")
async def align(request: Request, body: AddressInput):
    """
    地址对齐接口

    输入地址文本，返回结构化地址（包含数据库校验）
    """
    if not is_ready():
        return JSONResponse(
            status_code=503,
            content={"code": 503, "message": "模型未加载，请先训练模型", "data": None},
        )

    try:
        address = align_address(body.text, use_db_check=True)
        return Result(
            code=ApiCode.SUCCESS,
            data=AddressResponse(**address),
            message="地址对齐成功",
        )
    except Exception as e:
        return Result(code=ApiCode.SERVER_ERROR, message=f"地址对齐失败: {str(e)}")


@router.post(
    "/extract",
    response_model=Result[AddressResponse],
    tags=["Address Alignment"],
)
@limiter.limit("30/minute")
async def extract(request: Request, body: AddressInput):
    """
    地址提取接口

    输入地址文本，返回结构化地址（不使用数据库校验）
    """
    if not is_ready():
        return JSONResponse(
            status_code=503,
            content={"code": 503, "message": "模型未加载，请先训练模型", "data": None},
        )

    try:
        address = extract_address(body.text)
        return Result(
            code=ApiCode.SUCCESS,
            data=AddressResponse(**address),
            message="地址提取成功",
        )
    except Exception as e:
        return Result(code=ApiCode.SERVER_ERROR, message=f"地址提取失败: {str(e)}")


@router.post(
    "/tagging",
    response_model=Result[TaggingResponse],
    tags=["Address Alignment"],
)
@limiter.limit("30/minute")
async def tagging(request: Request, body: AddressInput):
    """
    序列标注接口

    输入地址文本，返回每个字符的标签
    """
    if not is_ready():
        return JSONResponse(
            status_code=503,
            content={"code": 503, "message": "模型未加载，请先训练模型", "data": None},
        )

    try:
        tags = predict_tags(body.text)
        return Result(
            code=ApiCode.SUCCESS,
            data=TaggingResponse(text=body.text, tags=tags),
            message="序列标注成功",
        )
    except Exception as e:
        return Result(code=ApiCode.SERVER_ERROR, message=f"序列标注失败: {str(e)}")


@router.get(
    "/status",
    tags=["Address Alignment"],
)
async def status():
    """
    服务状态接口
    """
    return Result(
        code=ApiCode.SUCCESS,
        data={"ready": is_ready()},
        message="状态查询成功",
    )

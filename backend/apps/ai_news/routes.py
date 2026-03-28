"""
AI 新闻分类与摘要 - API 路由
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from common.limiter import limiter
from common.schemas import ApiCode, Result

from .schemas import (
    AnalyzeResponse,
    ClassifyResponse,
    NewsInput,
    SummarizeResponse,
)
from .service import (
    analyze_news,
    classify_news,
    is_classify_ready,
    is_summarize_ready,
    summarize_news,
)

router = APIRouter()


@router.post(
    "/classify",
    response_model=Result[ClassifyResponse],
    tags=["AI News"],
)
@limiter.limit("30/minute")
async def classify(request: Request, body: NewsInput):
    """
    新闻分类接口

    输入新闻文本，返回分类结果（7类：财经、社会、教育、科技、时政、体育、游戏）
    """
    if not is_classify_ready():
        return JSONResponse(
            status_code=503,
            content={
                "code": 503,
                "message": "分类模型未加载，请先训练模型",
                "data": None,
            },
        )

    try:
        category = classify_news(body.text)
        return Result(
            code=ApiCode.SUCCESS,
            data=ClassifyResponse(category=category),
            message="分类成功",
        )
    except Exception as e:
        return Result(code=ApiCode.SERVER_ERROR, message=f"分类失败: {str(e)}")


@router.post(
    "/summarize",
    response_model=Result[SummarizeResponse],
    tags=["AI News"],
)
@limiter.limit("20/minute")
async def summarize(request: Request, body: NewsInput):
    """
    新闻摘要接口

    输入新闻文本，返回自动生成的摘要
    """
    if not is_summarize_ready():
        return JSONResponse(
            status_code=503,
            content={
                "code": 503,
                "message": "摘要模型未加载，请先训练模型",
                "data": None,
            },
        )

    try:
        summary = summarize_news(body.text)
        return Result(
            code=ApiCode.SUCCESS,
            data=SummarizeResponse(summary=summary),
            message="摘要生成成功",
        )
    except Exception as e:
        return Result(code=ApiCode.SERVER_ERROR, message=f"摘要生成失败: {str(e)}")


@router.post(
    "/analyze",
    response_model=Result[AnalyzeResponse],
    tags=["AI News"],
)
@limiter.limit("15/minute")
async def analyze(request: Request, body: NewsInput):
    """
    新闻综合分析接口

    输入新闻文本，返回分类结果和摘要
    """
    classify_ready = is_classify_ready()
    summarize_ready = is_summarize_ready()
    print(
        f"DEBUG: analyze called. classify_ready={classify_ready}, summarize_ready={summarize_ready}"
    )

    if not classify_ready or not summarize_ready:
        print("DEBUG: Returning 503")
        return JSONResponse(
            status_code=503,
            content={"code": 503, "message": "模型未加载，请先训练模型", "data": None},
        )

    try:
        result = analyze_news(body.text)
        return Result(
            code=ApiCode.SUCCESS,
            data=AnalyzeResponse(**result),
            message="分析成功",
        )
    except Exception as e:
        return Result(code=ApiCode.SERVER_ERROR, message=f"分析失败: {str(e)}")


@router.get(
    "/status",
    tags=["AI News"],
)
async def status():
    """
    服务状态接口

    返回模型加载状态
    """
    return Result(
        code=ApiCode.SUCCESS,
        data={
            "classify_ready": is_classify_ready(),
            "summarize_ready": is_summarize_ready(),
        },
        message="状态查询成功",
    )

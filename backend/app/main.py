"""
EKG Learning System - FastAPI 主应用
心电图学习系统后端服务
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
from typing import Dict
import logging

from app.api import ekg, review
from app.core.config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 Starting EKG Learning System...")
    logger.info(f"📋 Version: {settings.VERSION}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")
    
    yield
    
    # 关闭时执行
    logger.info("👋 Shutting down EKG Learning System...")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="心电图学习系统 - 基于 AI 的心电图分析与学习平台",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求处理时间中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """添加请求处理时间到响应头"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred",
            "path": str(request.url)
        }
    )


# 根路由
@app.get("/")
async def root() -> Dict[str, str]:
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
        "medical_disclaimer": "⚠️ 本系统仅供教育目的使用，不得用于临床诊断"
    }


# 健康检查
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """健康检查端点"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }


# API 信息
@app.get("/api/info")
async def api_info() -> Dict:
    """API 信息"""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "endpoints": {
            "ekg_analysis": "/api/ekg/analyze",
            "ekg_history": "/api/ekg/history",
            "review_next": "/api/review/next",
            "review_submit": "/api/review/submit"
        },
        "features": [
            "心电图信号分析",
            "多种心律失常检测（AFIB, VT, AVB, LBBB, RBBB）",
            "ST段分析（STEMI, NSTEMI）",
            "智能复习系统",
            "3D心脏可视化数据",
            "PDF文档解析"
        ],
        "supported_formats": ["CSV", "PDF"],
        "medical_disclaimer": settings.SHOW_MEDICAL_DISCLAIMER
    }


# 注册路由
app.include_router(ekg.router, prefix="/api/ekg", tags=["EKG Analysis"])
app.include_router(review.router, prefix="/api/review", tags=["Review System"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

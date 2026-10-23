"""
应用配置模块
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用信息
    APP_NAME: str = "EKG Learning System"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # 数据库配置
    DATABASE_URL: str = "postgresql://ekg_user:changeme@localhost:5432/ekg_learning"
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS 配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    # 文件上传配置
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # EKG 分析配置
    DEFAULT_SAMPLING_RATE: int = 500  # Hz
    MIN_HEART_RATE: int = 40
    MAX_HEART_RATE: int = 200
    
    # 医疗免责声明
    SHOW_MEDICAL_DISCLAIMER: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()

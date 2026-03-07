"""
Pydantic 数据模型
定义 API 请求和响应的数据结构
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


# ========== EKG 分析相关模型 ==========

class EKGAnalysisResult(BaseModel):
    """EKG 分析结果"""
    signal_quality: Dict[str, Any] = Field(..., description="信号质量评估")
    heart_rate: float = Field(..., description="心率 (bpm)")
    r_peak_count: int = Field(..., description="R波数量")
    intervals: Dict[str, float] = Field(..., description="各种间期测量值")
    hrv: Dict[str, float] = Field(..., description="心率变异性指标")
    peaks: Dict[str, List[int]] = Field(..., description="检测到的波峰位置")
    processed_signal: List[float] = Field(..., description="处理后的信号数据")
    sampling_rate: int = Field(..., description="采样率 (Hz)")
    diagnosis: Optional[Dict] = Field(None, description="诊断结果")
    filename: Optional[str] = Field(None, description="文件名")
    analysis_time: Optional[str] = Field(None, description="分析时间")
    medical_disclaimer: Optional[str] = Field(None, description="医疗免责声明")


class EKGHistoryItem(BaseModel):
    """EKG 分析历史记录项"""
    id: str = Field(..., description="记录ID")
    filename: str = Field(..., description="文件名")
    analysis_time: str = Field(..., description="分析时间")
    heart_rate: float = Field(..., description="心率 (bpm)")
    diagnosis_summary: str = Field(..., description="诊断摘要")
    has_anomaly: bool = Field(False, description="是否有异常")


# ========== 诊断相关模型 ==========

class DiagnosisCondition(BaseModel):
    """诊断条件"""
    condition_id: str = Field(..., description="条件ID")
    name: str = Field(..., description="诊断名称（中文）")
    name_en: str = Field("", description="诊断名称（英文）")
    severity: str = Field(..., description="严重程度")
    recommendations: List[str] = Field([], description="建议")
    confidence: float = Field(..., description="置信度 (0-1)")


class DiagnosisAlert(BaseModel):
    """诊断警报"""
    type: str = Field(..., description="警报类型")
    severity: str = Field(..., description="严重程度")
    message: str = Field(..., description="警报消息")
    recommendation: str = Field("", description="建议")


class DiagnosisResult(BaseModel):
    """诊断结果"""
    primary_diagnosis: DiagnosisCondition = Field(..., description="主要诊断")
    secondary_diagnoses: List[DiagnosisCondition] = Field([], description="次要诊断")
    alerts: List[DiagnosisAlert] = Field([], description="警报列表")
    summary: str = Field(..., description="诊断总结")
    clinical_notes: List[str] = Field([], description="临床备注")


# ========== 复习系统相关模型 ==========

class ReviewOption(BaseModel):
    """复习选项"""
    id: str = Field(..., description="选项ID")
    text: str = Field(..., description="选项文本")


class ReviewItem(BaseModel):
    """复习项目"""
    id: str = Field(..., description="项目ID")
    category: str = Field(..., description="类别")
    question: str = Field(..., description="问题")
    ekg_data: Dict[str, Any] = Field(..., description="心电图数据")
    options: List[ReviewOption] = Field(..., description="选项列表")
    correct_answer: str = Field(..., description="正确答案ID")
    difficulty: str = Field("medium", description="难度")
    last_reviewed: Optional[str] = Field(None, description="上次复习时间")
    review_count: int = Field(0, description="复习次数")
    mastery_level: int = Field(0, description="掌握程度 (0-5)")


class ReviewSubmission(BaseModel):
    """复习提交"""
    item_id: str = Field(..., description="项目ID")
    selected_answer: str = Field(..., description="选择的答案ID")
    time_spent: Optional[int] = Field(None, description="用时（秒）")
    review_count: int = Field(0, description="当前复习次数")


class ReviewResult(BaseModel):
    """复习结果"""
    is_correct: bool = Field(..., description="是否正确")
    correct_answer: str = Field(..., description="正确答案")
    selected_answer: str = Field(..., description="选择的答案")
    explanation: str = Field(..., description="详细解析")
    key_points: List[str] = Field([], description="关键点")
    related_topics: List[str] = Field([], description="相关主题")
    next_review_date: str = Field(..., description="下次复习时间")
    mastery_level_change: int = Field(0, description="掌握程度变化")
    total_review_count: int = Field(0, description="总复习次数")


class CategoryProgress(BaseModel):
    """类别进度"""
    total: int = Field(..., description="总项目数")
    mastered: int = Field(..., description="已掌握数")
    accuracy: float = Field(..., description="正确率")


class ReviewStatistics(BaseModel):
    """复习统计"""
    total_items: int = Field(..., description="总项目数")
    reviewed_items: int = Field(..., description="已复习数")
    mastered_items: int = Field(..., description="已掌握数")
    learning_items: int = Field(..., description="学习中")
    new_items: int = Field(..., description="新项目数")
    review_streak_days: int = Field(0, description="连续复习天数")
    total_review_count: int = Field(0, description="总复习次数")
    accuracy_rate: float = Field(0.0, description="总体正确率")
    category_progress: Dict[str, CategoryProgress] = Field({}, description="各类别进度")
    recent_activity: List[Dict[str, Any]] = Field([], description="最近活动")
    upcoming_reviews: int = Field(0, description="待复习数")
    next_review_date: Optional[str] = Field(None, description="下次复习时间")


# ========== 用户相关模型 ==========

class User(BaseModel):
    """用户模型"""
    id: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")
    full_name: Optional[str] = Field(None, description="全名")
    role: str = Field("student", description="角色")
    is_active: bool = Field(True, description="是否激活")
    created_at: Optional[datetime] = Field(None, description="创建时间")


class UserCreate(BaseModel):
    """创建用户请求"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: str = Field(..., description="邮箱")
    password: str = Field(..., min_length=8, description="密码")
    full_name: Optional[str] = Field(None, description="全名")


class Token(BaseModel):
    """认证令牌"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("bearer", description="令牌类型")


class TokenData(BaseModel):
    """令牌数据"""
    username: Optional[str] = None


# ========== 通用响应模型 ==========

class SuccessResponse(BaseModel):
    """成功响应"""
    success: bool = Field(True, description="是否成功")
    message: str = Field(..., description="消息")
    data: Optional[Any] = Field(None, description="数据")


class ErrorResponse(BaseModel):
    """错误响应"""
    error: str = Field(..., description="错误类型")
    message: str = Field(..., description="错误消息")
    details: Optional[Dict[str, Any]] = Field(None, description="详细信息")


# ========== 配置模型 ==========

class AppConfig(BaseModel):
    """应用配置"""
    app_name: str
    version: str
    debug: bool
    cors_origins: List[str]
    max_upload_size: int
    default_sampling_rate: int

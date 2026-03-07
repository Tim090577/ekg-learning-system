"""
EKG API 路由
心电图分析相关的 API 端点
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging
from datetime import datetime

from app.core.ekg_analyzer import EKGAnalyzer
from app.core.pdf_parser import PDFParser
from app.core.diagnosis import DiagnosisEngine
from app.models.schemas import EKGAnalysisResult, EKGHistoryItem

logger = logging.getLogger(__name__)
router = APIRouter()

# 初始化分析引擎
ekg_analyzer = EKGAnalyzer()
pdf_parser = PDFParser()
diagnosis_engine = DiagnosisEngine()


@router.post("/analyze", response_model=EKGAnalysisResult)
async def analyze_ekg(
    file: UploadFile = File(...),
    sampling_rate: Optional[int] = Query(500, description="采样率 (Hz)")
):
    """
    分析上传的心电图数据
    
    支持格式：
    - CSV: 包含心电图信号数据
    - PDF: 包含心电图图像或数据
    
    Args:
        file: 上传的文件
        sampling_rate: 采样率（Hz），默认 500
    
    Returns:
        EKGAnalysisResult: 分析结果
    """
    try:
        logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        # 读取文件内容
        content = await file.read()
        
        # 根据文件类型处理
        if file.filename.endswith('.csv'):
            # CSV 文件处理
            signal_data = await ekg_analyzer.parse_csv(content)
        elif file.filename.endswith('.pdf'):
            # PDF 文件处理
            signal_data = await pdf_parser.extract_ekg_from_pdf(content)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式。支持的格式：CSV, PDF"
            )
        
        # 分析心电图信号
        analysis_result = await ekg_analyzer.analyze(signal_data, sampling_rate)
        
        # 诊断分析
        diagnosis_result = await diagnosis_engine.diagnose(analysis_result)
        
        # 合并结果
        result = {
            **analysis_result,
            "diagnosis": diagnosis_result,
            "filename": file.filename,
            "analysis_time": datetime.now().isoformat(),
            "medical_disclaimer": "⚠️ 本分析结果仅供教育参考，不得用于临床诊断"
        }
        
        logger.info(f"Analysis completed for {file.filename}")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")
    finally:
        await file.close()


@router.get("/history", response_model=List[EKGHistoryItem])
async def get_analysis_history(
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    offset: int = Query(0, ge=0, description="偏移量")
):
    """
    获取分析历史记录
    
    Args:
        limit: 返回记录数（1-100）
        offset: 偏移量
    
    Returns:
        List[EKGHistoryItem]: 历史记录列表
    """
    try:
        # TODO: 从数据库获取历史记录
        # 这里返回模拟数据
        history = [
            {
                "id": f"hist_{i}",
                "filename": f"ekg_sample_{i}.csv",
                "analysis_time": "2026-03-07T10:00:00",
                "heart_rate": 75 + i,
                "diagnosis_summary": "正常窦性心律",
                "has_anomaly": False
            }
            for i in range(offset, min(offset + limit, 20))
        ]
        
        return history
        
    except Exception as e:
        logger.error(f"Failed to fetch history: {str(e)}")
        raise HTTPException(status_code=500, detail="获取历史记录失败")


@router.get("/{analysis_id}")
async def get_analysis_detail(analysis_id: str):
    """
    获取特定分析结果的详细信息
    
    Args:
        analysis_id: 分析记录 ID
    
    Returns:
        分析详情
    """
    try:
        # TODO: 从数据库获取详细记录
        # 这里返回模拟数据
        detail = {
            "id": analysis_id,
            "filename": "ekg_sample.csv",
            "analysis_time": "2026-03-07T10:00:00",
            "signal_quality": "good",
            "heart_rate": 75,
            "pr_interval": 160,
            "qrs_duration": 90,
            "qt_interval": 400,
            "qtc_interval": 420,
            "diagnosis": {
                "primary": "正常窦性心律",
                "secondary": [],
                "confidence": 0.95,
                "alerts": []
            },
            "peaks": {
                "r_peaks": [100, 200, 300, 400, 500],
                "p_peaks": [80, 180, 280, 380, 480],
                "t_peaks": [150, 250, 350, 450, 550]
            },
            "medical_disclaimer": "⚠️ 本分析结果仅供教育参考，不得用于临床诊断"
        }
        
        return detail
        
    except Exception as e:
        logger.error(f"Failed to fetch detail: {str(e)}")
        raise HTTPException(status_code=500, detail="获取分析详情失败")


@router.delete("/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """
    删除分析记录
    
    Args:
        analysis_id: 分析记录 ID
    
    Returns:
        删除结果
    """
    try:
        # TODO: 从数据库删除记录
        logger.info(f"Deleted analysis: {analysis_id}")
        
        return {
            "success": True,
            "message": f"分析记录 {analysis_id} 已删除",
            "deleted_id": analysis_id
        }
        
    except Exception as e:
        logger.error(f"Failed to delete: {str(e)}")
        raise HTTPException(status_code=500, detail="删除失败")


@router.get("/stats/overview")
async def get_statistics():
    """
    获取统计概览
    
    Returns:
        统计数据
    """
    try:
        stats = {
            "total_analyses": 150,
            "total_patients": 45,
            "anomaly_rate": 0.23,
            "most_common_diagnosis": [
                {"name": "正常窦性心律", "count": 100},
                {"name": "房颤", "count": 15},
                {"name": "室性早搏", "count": 12},
                {"name": "ST段异常", "count": 10},
                {"name": "房室传导阻滞", "count": 8}
            ],
            "analysis_by_date": [
                {"date": "2026-03-01", "count": 12},
                {"date": "2026-03-02", "count": 15},
                {"date": "2026-03-03", "count": 18},
                {"date": "2026-03-04", "count": 14},
                {"date": "2026-03-05", "count": 16},
                {"date": "2026-03-06", "count": 20},
                {"date": "2026-03-07", "count": 25}
            ]
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Failed to fetch statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="获取统计数据失败")

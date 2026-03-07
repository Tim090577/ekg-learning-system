"""
Review API 路由
复习系统相关的 API 端点
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging
from datetime import datetime, timedelta
import random

from app.models.schemas import ReviewItem, ReviewSubmission, ReviewStatistics

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/next", response_model=ReviewItem)
async def get_next_review_item(
    category: Optional[str] = Query(None, description="复习类别（可选）")
):
    """
    获取下一个复习项目（基于间隔重复算法）
    
    Args:
        category: 可选的复习类别筛选
    
    Returns:
        ReviewItem: 复习项目
    """
    try:
        # 模拟复习题目数据库
        review_items = [
            {
                "id": "review_001",
                "category": "rhythm",
                "question": "以下心电图显示什么心律？",
                "ekg_data": {
                    "image_url": "/static/ekg/afib_sample.png",
                    "signal_preview": [1, 2, 3, 4, 5],
                },
                "options": [
                    {"id": "a", "text": "正常窦性心律"},
                    {"id": "b", "text": "房颤"},
                    {"id": "c", "text": "室性心动过速"},
                    {"id": "d", "text": "房室传导阻滞"}
                ],
                "correct_answer": "b",
                "difficulty": "medium",
                "last_reviewed": None,
                "review_count": 0,
                "mastery_level": 0
            },
            {
                "id": "review_002",
                "category": "st_segment",
                "question": "这个心电图的ST段有什么特征？",
                "ekg_data": {
                    "image_url": "/static/ekg/stemi_sample.png",
                    "signal_preview": [1, 2, 3, 4, 5],
                },
                "options": [
                    {"id": "a", "text": "ST段正常"},
                    {"id": "b", "text": "ST段压低"},
                    {"id": "c", "text": "ST段抬高（STEMI）"},
                    {"id": "d", "text": "倒置T波"}
                ],
                "correct_answer": "c",
                "difficulty": "hard",
                "last_reviewed": None,
                "review_count": 0,
                "mastery_level": 0
            },
            {
                "id": "review_003",
                "category": "conduction",
                "question": "这个心电图显示什么类型的传导阻滞？",
                "ekg_data": {
                    "image_url": "/static/ekg/lbbb_sample.png",
                    "signal_preview": [1, 2, 3, 4, 5],
                },
                "options": [
                    {"id": "a", "text": "左束支传导阻滞（LBBB）"},
                    {"id": "b", "text": "右束支传导阻滞（RBBB）"},
                    {"id": "c", "text": "一度房室传导阻滞"},
                    {"id": "d", "text": "完全性房室传导阻滞"}
                ],
                "correct_answer": "a",
                "difficulty": "hard",
                "last_reviewed": None,
                "review_count": 0,
                "mastery_level": 0
            }
        ]
        
        # 根据类别筛选（如果提供）
        if category:
            filtered_items = [item for item in review_items if item["category"] == category]
            if not filtered_items:
                raise HTTPException(status_code=404, detail=f"未找到类别为 {category} 的复习项目")
            review_items = filtered_items
        
        # 使用间隔重复算法选择项目（这里简化为随机选择）
        # 实际应用中应该实现 SM-2 或类似算法
        selected_item = random.choice(review_items)
        
        logger.info(f"Selected review item: {selected_item['id']}")
        return selected_item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get next review item: {str(e)}")
        raise HTTPException(status_code=500, detail="获取复习项目失败")


@router.post("/submit")
async def submit_review(submission: ReviewSubmission):
    """
    提交复习答案
    
    Args:
        submission: 复习提交数据
    
    Returns:
        提交结果，包括正确性和解析
    """
    try:
        # 这里应该验证答案并更新用户的学习记录
        # 简化示例：假设我们有正确答案
        correct_answers = {
            "review_001": "b",
            "review_002": "c",
            "review_003": "a"
        }
        
        correct_answer = correct_answers.get(submission.item_id)
        is_correct = submission.selected_answer == correct_answer
        
        # 根据正确性调整下次复习时间（SM-2 算法简化版）
        if is_correct:
            # 正确，延长复习间隔
            next_review_days = 1 if submission.review_count == 0 else submission.review_count * 2
        else:
            # 错误，重置为明天复习
            next_review_days = 1
        
        next_review_date = datetime.now() + timedelta(days=next_review_days)
        
        # 生成详细解析
        explanations = {
            "review_001": {
                "correct": "b",
                "explanation": "这是典型的房颤（Atrial Fibrillation）表现。房颤的特征包括：\n1. 不规则的R-R间期\n2. 缺乏明显的P波\n3. 基线呈现f波（颤动波）\n4. 心室率通常较快且不规则",
                "key_points": [
                    "房颤是最常见的持续性心律失常",
                    "增加卒中风险，需要抗凝治疗",
                    "可以是阵发性、持续性或永久性"
                ],
                "related_topics": ["心律失常", "抗凝治疗", "卒中预防"]
            },
            "review_002": {
                "correct": "c",
                "explanation": "这显示ST段抬高型心肌梗死（STEMI）。STEMI的特征：\n1. ST段明显抬高（≥2mm在胸导联，≥1mm在肢导联）\n2. 可能伴有病理性Q波\n3. T波可能倒置\n4. 需要紧急冠脉介入治疗",
                "key_points": [
                    "STEMI需要在90分钟内进行PCI",
                    "时间就是心肌",
                    "早期识别和治疗至关重要"
                ],
                "related_topics": ["急性冠脉综合征", "冠脉介入", "心肌梗死"]
            },
            "review_003": {
                "correct": "a",
                "explanation": "这是左束支传导阻滞（LBBB）。LBBB的特征：\n1. QRS波群增宽（≥120ms）\n2. V1导联呈rS或QS波\n3. V5/V6导联呈宽大的R波，无Q波\n4. ST-T改变继发于QRS波群改变",
                "key_points": [
                    "LBBB可能提示潜在的心脏结构性疾病",
                    "影响ST段和T波的判读",
                    "在STEMI诊断中需要特殊考虑（Sgarbossa准则）"
                ],
                "related_topics": ["传导系统", "束支阻滞", "Sgarbossa准则"]
            }
        }
        
        explanation = explanations.get(submission.item_id, {
            "correct": correct_answer,
            "explanation": "暂无详细解析",
            "key_points": [],
            "related_topics": []
        })
        
        result = {
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "selected_answer": submission.selected_answer,
            "explanation": explanation["explanation"],
            "key_points": explanation["key_points"],
            "related_topics": explanation["related_topics"],
            "next_review_date": next_review_date.isoformat(),
            "mastery_level_change": 1 if is_correct else -1,
            "total_review_count": submission.review_count + 1
        }
        
        logger.info(f"Review submitted: {submission.item_id}, correct: {is_correct}")
        return result
        
    except Exception as e:
        logger.error(f"Failed to submit review: {str(e)}")
        raise HTTPException(status_code=500, detail="提交复习失败")


@router.get("/statistics", response_model=ReviewStatistics)
async def get_review_statistics(
    user_id: Optional[str] = Query(None, description="用户ID（可选）")
):
    """
    获取复习统计数据
    
    Args:
        user_id: 用户ID（可选）
    
    Returns:
        ReviewStatistics: 统计数据
    """
    try:
        # 模拟统计数据
        stats = {
            "total_items": 150,
            "reviewed_items": 45,
            "mastered_items": 20,
            "learning_items": 15,
            "new_items": 105,
            "review_streak_days": 7,
            "total_review_count": 230,
            "accuracy_rate": 0.78,
            "category_progress": {
                "rhythm": {"total": 50, "mastered": 10, "accuracy": 0.82},
                "st_segment": {"total": 40, "mastered": 5, "accuracy": 0.70},
                "conduction": {"total": 30, "mastered": 3, "accuracy": 0.75},
                "intervals": {"total": 30, "mastered": 2, "accuracy": 0.80}
            },
            "recent_activity": [
                {"date": "2026-03-07", "reviews": 12, "accuracy": 0.83},
                {"date": "2026-03-06", "reviews": 10, "accuracy": 0.80},
                {"date": "2026-03-05", "reviews": 8, "accuracy": 0.75},
                {"date": "2026-03-04", "reviews": 15, "accuracy": 0.73},
                {"date": "2026-03-03", "reviews": 11, "accuracy": 0.82}
            ],
            "upcoming_reviews": 8,
            "next_review_date": (datetime.now() + timedelta(hours=2)).isoformat()
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Failed to fetch statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="获取统计数据失败")


@router.get("/categories")
async def get_review_categories():
    """
    获取所有复习类别
    
    Returns:
        类别列表
    """
    categories = [
        {
            "id": "rhythm",
            "name": "心律识别",
            "description": "学习识别各种心律失常，包括房颤、室速等",
            "item_count": 50,
            "icon": "heartbeat"
        },
        {
            "id": "st_segment",
            "name": "ST段分析",
            "description": "学习识别ST段抬高、压低及其临床意义",
            "item_count": 40,
            "icon": "chart-line"
        },
        {
            "id": "conduction",
            "name": "传导异常",
            "description": "学习识别各种传导阻滞和束支阻滞",
            "item_count": 30,
            "icon": "route"
        },
        {
            "id": "intervals",
            "name": "间期测量",
            "description": "学习测量和解读PR、QRS、QT间期",
            "item_count": 30,
            "icon": "ruler"
        }
    ]
    
    return {"categories": categories}


@router.post("/reset-progress")
async def reset_progress(
    user_id: str = Query(..., description="用户ID"),
    category: Optional[str] = Query(None, description="类别（可选，为空则重置全部）")
):
    """
    重置学习进度
    
    Args:
        user_id: 用户ID
        category: 类别（可选）
    
    Returns:
        重置结果
    """
    try:
        # TODO: 实现进度重置逻辑
        message = f"已重置"
        if category:
            message += f"类别 {category} 的"
        message += "学习进度"
        
        logger.info(f"Reset progress for user {user_id}, category: {category}")
        
        return {
            "success": True,
            "message": message,
            "user_id": user_id,
            "category": category
        }
        
    except Exception as e:
        logger.error(f"Failed to reset progress: {str(e)}")
        raise HTTPException(status_code=500, detail="重置进度失败")

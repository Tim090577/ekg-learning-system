"""
诊断引擎
基于规则和知识库的心电图诊断系统
"""

import json
import os
from typing import Dict, List, Optional
import logging
import numpy as np

logger = logging.getLogger(__name__)


class DiagnosisEngine:
    """心电图诊断引擎"""
    
    def __init__(self, rules_path: str = "data/diagnosis_rules.json"):
        """
        初始化诊断引擎
        
        Args:
            rules_path: 诊断规则文件路径
        """
        self.rules_path = rules_path
        self.rules = self._load_rules()
        logger.info(f"DiagnosisEngine initialized with {len(self.rules)} rules")
    
    def _load_rules(self) -> Dict:
        """加载诊断规则"""
        try:
            if os.path.exists(self.rules_path):
                with open(self.rules_path, 'r', encoding='utf-8') as f:
                    rules = json.load(f)
                logger.info(f"Loaded {len(rules.get('conditions', []))} diagnosis rules")
                return rules
        except Exception as e:
            logger.warning(f"Failed to load rules from {self.rules_path}: {str(e)}")
        
        # 返回默认规则
        return self._get_default_rules()
    
    def _get_default_rules(self) -> Dict:
        """获取默认诊断规则"""
        return {
            "conditions": [
                {
                    "id": "normal_sinus_rhythm",
                    "name": "正常窦性心律",
                    "name_en": "Normal Sinus Rhythm",
                    "criteria": {
                        "heart_rate_min": 60,
                        "heart_rate_max": 100,
                        "pr_interval_min": 120,
                        "pr_interval_max": 200,
                        "qrs_duration_max": 120,
                        "rhythm_regular": True
                    },
                    "severity": "normal",
                    "recommendations": ["继续监测", "保持健康生活方式"]
                },
                {
                    "id": "sinus_tachycardia",
                    "name": "窦性心动过速",
                    "name_en": "Sinus Tachycardia",
                    "criteria": {
                        "heart_rate_min": 100,
                        "heart_rate_max": 200
                    },
                    "severity": "mild",
                    "recommendations": ["评估病因", "排除甲亢、贫血等"]
                },
                {
                    "id": "sinus_bradycardia",
                    "name": "窦性心动过缓",
                    "name_en": "Sinus Bradycardia",
                    "criteria": {
                        "heart_rate_min": 40,
                        "heart_rate_max": 60
                    },
                    "severity": "mild",
                    "recommendations": ["评估是否需要起搏器", "排除药物影响"]
                },
                {
                    "id": "afib",
                    "name": "心房颤动",
                    "name_en": "Atrial Fibrillation",
                    "criteria": {
                        "rhythm_irregular": True,
                        "p_wave_absent": True,
                        "rr_variability_high": True
                    },
                    "severity": "moderate",
                    "recommendations": [
                        "评估卒中风险（CHA2DS2-VASc评分）",
                        "考虑抗凝治疗",
                        "控制心室率"
                    ]
                }
            ]
        }
    
    async def diagnose(self, analysis_result: Dict) -> Dict:
        """
        基于分析结果进行诊断
        
        Args:
            analysis_result: EKG分析结果
        
        Returns:
            Dict: 诊断结果
        """
        try:
            heart_rate = analysis_result.get('heart_rate', 0)
            intervals = analysis_result.get('intervals', {})
            hrv = analysis_result.get('hrv', {})
            
            # 评估心律规整性
            rhythm_regular = self._assess_rhythm_regularity(hrv)
            
            # 匹配诊断规则
            diagnoses = []
            
            for condition in self.rules.get('conditions', []):
                if self._match_criteria(condition['criteria'], {
                    'heart_rate': heart_rate,
                    'pr_interval': intervals.get('pr_interval', 0),
                    'qrs_duration': intervals.get('qrs_duration', 0),
                    'qt_interval': intervals.get('qt_interval', 0),
                    'qtc_interval': intervals.get('qtc_interval', 0),
                    'rhythm_regular': rhythm_regular,
                    'rhythm_irregular': not rhythm_regular,
                    'rr_variability_high': hrv.get('sdnn', 0) > 50
                }):
                    diagnoses.append({
                        'condition_id': condition['id'],
                        'name': condition['name'],
                        'name_en': condition.get('name_en', ''),
                        'severity': condition.get('severity', 'unknown'),
                        'recommendations': condition.get('recommendations', []),
                        'confidence': 0.85  # 简化：固定置信度
                    })
            
            # 如果没有匹配的诊断，返回正常
            if not diagnoses:
                diagnoses.append({
                    'condition_id': 'normal_sinus_rhythm',
                    'name': '正常窦性心律',
                    'name_en': 'Normal Sinus Rhythm',
                    'severity': 'normal',
                    'recommendations': ['继续监测'],
                    'confidence': 0.90
                })
            
            # 检测异常
            alerts = self._detect_anomalies(analysis_result)
            
            # 生成总结
            primary_diagnosis = diagnoses[0]
            secondary_diagnoses = diagnoses[1:] if len(diagnoses) > 1 else []
            
            result = {
                'primary_diagnosis': primary_diagnosis,
                'secondary_diagnoses': secondary_diagnoses,
                'alerts': alerts,
                'summary': self._generate_summary(primary_diagnosis, alerts),
                'clinical_notes': self._generate_clinical_notes(analysis_result, diagnoses)
            }
            
            logger.info(f"Diagnosis completed: {primary_diagnosis['name']}")
            return result
            
        except Exception as e:
            logger.error(f"Diagnosis failed: {str(e)}", exc_info=True)
            return {
                'primary_diagnosis': {
                    'condition_id': 'error',
                    'name': '诊断失败',
                    'severity': 'unknown',
                    'recommendations': ['请咨询医疗专业人员'],
                    'confidence': 0.0
                },
                'secondary_diagnoses': [],
                'alerts': [],
                'summary': '诊断过程出错，请检查数据质量',
                'clinical_notes': []
            }
    
    def _match_criteria(self, criteria: Dict, measurements: Dict) -> bool:
        """
        检查测量值是否符合诊断标准
        
        Args:
            criteria: 诊断标准
            measurements: 测量值
        
        Returns:
            bool: 是否匹配
        """
        for key, value in criteria.items():
            if key.endswith('_min'):
                measure_key = key.replace('_min', '')
                if measurements.get(measure_key, 0) < value:
                    return False
            elif key.endswith('_max'):
                measure_key = key.replace('_max', '')
                if measurements.get(measure_key, 0) > value:
                    return False
            elif isinstance(value, bool):
                if measurements.get(key, False) != value:
                    return False
        
        return True
    
    def _assess_rhythm_regularity(self, hrv: Dict) -> bool:
        """
        评估心律是否规整
        
        Args:
            hrv: 心率变异性数据
        
        Returns:
            bool: 心律是否规整
        """
        # 如果 SDNN < 50ms，认为心律规整
        sdnn = hrv.get('sdnn', 0)
        return sdnn < 50
    
    def _detect_anomalies(self, analysis_result: Dict) -> List[Dict]:
        """
        检测异常情况
        
        Args:
            analysis_result: 分析结果
        
        Returns:
            List[Dict]: 异常列表
        """
        alerts = []
        
        heart_rate = analysis_result.get('heart_rate', 0)
        intervals = analysis_result.get('intervals', {})
        
        # 心率异常
        if heart_rate > 100:
            alerts.append({
                'type': 'tachycardia',
                'severity': 'moderate' if heart_rate < 150 else 'high',
                'message': f'心率过快: {heart_rate} bpm',
                'recommendation': '评估病因，考虑药物治疗'
            })
        elif heart_rate < 60 and heart_rate > 0:
            alerts.append({
                'type': 'bradycardia',
                'severity': 'moderate' if heart_rate > 40 else 'high',
                'message': f'心率过缓: {heart_rate} bpm',
                'recommendation': '评估是否需要起搏器'
            })
        
        # PR 间期异常
        pr_interval = intervals.get('pr_interval', 0)
        if pr_interval > 200:
            alerts.append({
                'type': 'prolonged_pr',
                'severity': 'moderate',
                'message': f'PR间期延长: {pr_interval} ms',
                'recommendation': '考虑一度房室传导阻滞'
            })
        
        # QRS 时限异常
        qrs_duration = intervals.get('qrs_duration', 0)
        if qrs_duration > 120:
            alerts.append({
                'type': 'wide_qrs',
                'severity': 'moderate',
                'message': f'QRS波群增宽: {qrs_duration} ms',
                'recommendation': '考虑束支传导阻滞或室性心律'
            })
        
        # QTc 异常
        qtc = intervals.get('qtc_interval', 0)
        if qtc > 450:
            alerts.append({
                'type': 'prolonged_qt',
                'severity': 'high',
                'message': f'QTc间期延长: {qtc} ms',
                'recommendation': '警惕尖端扭转型室速风险，检查电解质和药物'
            })
        
        return alerts
    
    def _generate_summary(self, primary_diagnosis: Dict, alerts: List[Dict]) -> str:
        """生成诊断总结"""
        summary = f"诊断：{primary_diagnosis['name']}"
        
        if alerts:
            summary += f"\n发现 {len(alerts)} 个异常需要关注"
        
        return summary
    
    def _generate_clinical_notes(
        self, 
        analysis_result: Dict, 
        diagnoses: List[Dict]
    ) -> List[str]:
        """生成临床备注"""
        notes = []
        
        heart_rate = analysis_result.get('heart_rate', 0)
        intervals = analysis_result.get('intervals', {})
        
        notes.append(f"心率: {heart_rate} bpm")
        notes.append(f"PR间期: {intervals.get('pr_interval', 0)} ms")
        notes.append(f"QRS时限: {intervals.get('qrs_duration', 0)} ms")
        notes.append(f"QTc: {intervals.get('qtc_interval', 0)} ms")
        
        # 信号质量备注
        quality = analysis_result.get('signal_quality', {})
        if quality.get('quality_level') in ['poor', 'fair']:
            notes.append(f"注意：信号质量为 {quality.get('quality_level')}，可能影响诊断准确性")
        
        return notes

"""
知识库模块
存储心电图诊断规则、疾病知识等
"""

import json
import os
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """心电图知识库"""
    
    def __init__(self, data_dir: str = "data"):
        """
        初始化知识库
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = data_dir
        self.diagnosis_rules = {}
        self.disease_symptoms = {}
        self.educational_content = {}
        
        self._load_all_data()
    
    def _load_all_data(self):
        """加载所有知识库数据"""
        self.diagnosis_rules = self._load_json('diagnosis_rules.json')
        self.disease_symptoms = self._load_json('disease_symptoms.json')
        logger.info("Knowledge base loaded successfully")
    
    def _load_json(self, filename: str) -> Dict:
        """
        加载 JSON 文件
        
        Args:
            filename: 文件名
        
        Returns:
            Dict: JSON 数据
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Loaded {filename}")
                return data
        except Exception as e:
            logger.warning(f"Failed to load {filename}: {str(e)}")
        
        return {}
    
    def get_diagnosis_rule(self, condition_id: str) -> Optional[Dict]:
        """
        获取特定条件的诊断规则
        
        Args:
            condition_id: 条件ID
        
        Returns:
            Optional[Dict]: 诊断规则
        """
        for condition in self.diagnosis_rules.get('conditions', []):
            if condition['id'] == condition_id:
                return condition
        return None
    
    def get_disease_info(self, disease_id: str) -> Optional[Dict]:
        """
        获取疾病信息
        
        Args:
            disease_id: 疾病ID
        
        Returns:
            Optional[Dict]: 疾病信息
        """
        return self.disease_symptoms.get('diseases', {}).get(disease_id)
    
    def search_by_symptoms(self, symptoms: List[str]) -> List[Dict]:
        """
        根据症状搜索可能的疾病
        
        Args:
            symptoms: 症状列表
        
        Returns:
            List[Dict]: 可能的疾病列表
        """
        matches = []
        
        for disease_id, disease in self.disease_symptoms.get('diseases', {}).items():
            disease_symptoms = set(disease.get('symptoms', []))
            symptom_match = len(set(symptoms) & disease_symptoms)
            
            if symptom_match > 0:
                matches.append({
                    'disease_id': disease_id,
                    'name': disease.get('name', ''),
                    'match_count': symptom_match,
                    'confidence': symptom_match / len(disease_symptoms) if disease_symptoms else 0
                })
        
        # 按匹配度排序
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        
        return matches
    
    def get_all_conditions(self) -> List[Dict]:
        """获取所有诊断条件"""
        return self.diagnosis_rules.get('conditions', [])
    
    def get_all_diseases(self) -> Dict:
        """获取所有疾病"""
        return self.disease_symptoms.get('diseases', {})
    
    def get_educational_content(self, topic: str) -> Optional[str]:
        """
        获取教育内容
        
        Args:
            topic: 主题
        
        Returns:
            Optional[str]: 教育内容
        """
        return self.educational_content.get(topic)
    
    def add_diagnosis_rule(self, rule: Dict):
        """
        添加诊断规则
        
        Args:
            rule: 诊断规则
        """
        if 'conditions' not in self.diagnosis_rules:
            self.diagnosis_rules['conditions'] = []
        
        self.diagnosis_rules['conditions'].append(rule)
        logger.info(f"Added diagnosis rule: {rule.get('id')}")
    
    def update_diagnosis_rule(self, condition_id: str, updates: Dict):
        """
        更新诊断规则
        
        Args:
            condition_id: 条件ID
            updates: 更新内容
        """
        for condition in self.diagnosis_rules.get('conditions', []):
            if condition['id'] == condition_id:
                condition.update(updates)
                logger.info(f"Updated diagnosis rule: {condition_id}")
                return True
        
        return False
    
    def save_all_data(self):
        """保存所有数据到文件"""
        self._save_json('diagnosis_rules.json', self.diagnosis_rules)
        self._save_json('disease_symptoms.json', self.disease_symptoms)
        logger.info("Knowledge base saved successfully")
    
    def _save_json(self, filename: str, data: Dict):
        """
        保存数据到 JSON 文件
        
        Args:
            filename: 文件名
            data: 要保存的数据
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {filename}")
        except Exception as e:
            logger.error(f"Failed to save {filename}: {str(e)}")


# 全局知识库实例
knowledge_base = KnowledgeBase()

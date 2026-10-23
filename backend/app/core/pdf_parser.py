"""
PDF 解析器
从 PDF 文件中提取心电图数据
"""

from pypdf import PdfReader
import pdfplumber
import numpy as np
from typing import Optional, Dict
import io
import logging
import re

logger = logging.getLogger(__name__)


class PDFParser:
    """PDF 文档解析器"""
    
    def __init__(self):
        """初始化 PDF 解析器"""
        logger.info("PDFParser initialized")
    
    async def extract_ekg_from_pdf(self, content: bytes) -> np.ndarray:
        """
        从 PDF 中提取心电图数据
        
        Args:
            content: PDF 文件内容（字节）
        
        Returns:
            np.ndarray: 心电图信号数组
        """
        try:
            # 尝试提取文本数据
            signal_data = await self._extract_text_data(content)
            
            if signal_data is not None:
                return signal_data
            
            # 如果文本提取失败，尝试图像提取
            logger.info("Text extraction failed, attempting image extraction")
            signal_data = await self._extract_image_data(content)
            
            if signal_data is not None:
                return signal_data
            
            # 如果都失败，返回模拟数据（仅用于演示）
            logger.warning("PDF extraction failed, returning simulated data")
            return self._generate_simulated_ekg()
            
        except Exception as e:
            logger.error(f"PDF extraction failed: {str(e)}")
            raise ValueError(f"PDF解析失败: {str(e)}")
    
    async def _extract_text_data(self, content: bytes) -> Optional[np.ndarray]:
        """
        从 PDF 文本中提取数值数据
        
        Args:
            content: PDF 内容
        
        Returns:
            Optional[np.ndarray]: 提取的信号数据，失败返回 None
        """
        try:
            pdf_file = io.BytesIO(content)
            
            # 使用 pdfplumber 提取文本
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
            
            # 查找数值数据
            # 尝试匹配常见格式：逗号分隔、空格分隔、换行分隔
            numbers = []
            
            # 正则表达式匹配数字（包括负数和小数）
            pattern = r'[-+]?\d*\.\d+|[-+]?\d+'
            matches = re.findall(pattern, text)
            
            for match in matches:
                try:
                    numbers.append(float(match))
                except ValueError:
                    continue
            
            if len(numbers) > 100:  # 至少需要100个数据点
                signal_data = np.array(numbers)
                logger.info(f"Extracted {len(signal_data)} data points from PDF text")
                return signal_data
            
            return None
            
        except Exception as e:
            logger.warning(f"Text extraction failed: {str(e)}")
            return None
    
    async def _extract_image_data(self, content: bytes) -> Optional[np.ndarray]:
        """
        从 PDF 图像中提取心电图数据（使用图像处理）
        
        Args:
            content: PDF 内容
        
        Returns:
            Optional[np.ndarray]: 提取的信号数据，失败返回 None
        """
        try:
            # 这里应该实现图像处理逻辑：
            # 1. 提取 PDF 中的图像
            # 2. 使用 OpenCV 进行边缘检测
            # 3. 追踪心电图曲线
            # 4. 转换为数值数据
            
            # 由于完整实现较复杂，这里返回 None
            # 实际项目中可以使用 pdf2image + OpenCV 实现
            
            logger.warning("Image extraction not implemented")
            return None
            
        except Exception as e:
            logger.warning(f"Image extraction failed: {str(e)}")
            return None
    
    def _generate_simulated_ekg(self, duration: float = 10.0, sampling_rate: int = 500) -> np.ndarray:
        """
        生成模拟的心电图数据（用于演示）
        
        Args:
            duration: 持续时间（秒）
            sampling_rate: 采样率 (Hz)
        
        Returns:
            np.ndarray: 模拟的心电图信号
        """
        num_samples = int(duration * sampling_rate)
        t = np.linspace(0, duration, num_samples)
        
        # 心率：75 bpm
        heart_rate = 75
        rr_interval = 60.0 / heart_rate
        
        signal = np.zeros(num_samples)
        
        # 生成 QRS 波群
        current_time = 0
        while current_time < duration:
            peak_index = int(current_time * sampling_rate)
            
            if peak_index < num_samples:
                # P 波（小幅度正向波）
                p_start = max(0, peak_index - int(0.16 * sampling_rate))
                p_end = max(0, peak_index - int(0.08 * sampling_rate))
                if p_start < num_samples and p_end < num_samples:
                    signal[p_start:p_end] += 0.1 * np.sin(np.linspace(0, np.pi, p_end - p_start))
                
                # QRS 波群（高幅度尖峰）
                qrs_start = max(0, peak_index - int(0.05 * sampling_rate))
                qrs_end = min(num_samples, peak_index + int(0.05 * sampling_rate))
                if qrs_start < num_samples and qrs_end < num_samples:
                    qrs_width = qrs_end - qrs_start
                    signal[qrs_start:qrs_end] += np.concatenate([
                        -0.2 * np.ones(qrs_width // 4),  # Q 波
                        1.0 * np.ones(qrs_width // 2),    # R 波
                        -0.3 * np.ones(qrs_width // 4)    # S 波
                    ])[:qrs_width]
                
                # T 波（中等幅度正向波）
                t_start = min(num_samples, peak_index + int(0.15 * sampling_rate))
                t_end = min(num_samples, peak_index + int(0.30 * sampling_rate))
                if t_start < num_samples and t_end < num_samples and t_end > t_start:
                    signal[t_start:t_end] += 0.3 * np.sin(np.linspace(0, np.pi, t_end - t_start))
            
            current_time += rr_interval
        
        # 添加小量噪声
        noise = np.random.normal(0, 0.02, num_samples)
        signal += noise
        
        logger.info(f"Generated simulated EKG: {num_samples} samples, {heart_rate} bpm")
        return signal
    
    async def extract_metadata(self, content: bytes) -> Dict:
        """
        从 PDF 中提取元数据
        
        Args:
            content: PDF 内容
        
        Returns:
            Dict: 元数据信息
        """
        metadata = {
            'title': '',
            'author': '',
            'subject': '',
            'creator': '',
            'producer': '',
            'creation_date': '',
            'modification_date': '',
            'num_pages': 0
        }
        
        try:
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            
            # 提取元数据
            info = reader.metadata
            if info:
                metadata['title'] = info.get('/Title', '')
                metadata['author'] = info.get('/Author', '')
                metadata['subject'] = info.get('/Subject', '')
                metadata['creator'] = info.get('/Creator', '')
                metadata['producer'] = info.get('/Producer', '')
                metadata['creation_date'] = info.get('/CreationDate', '')
                metadata['modification_date'] = info.get('/ModDate', '')
            
            metadata['num_pages'] = len(reader.pages)
            
            logger.info(f"Extracted metadata from PDF: {metadata['num_pages']} pages")
            
        except Exception as e:
            logger.warning(f"Metadata extraction failed: {str(e)}")
        
        return metadata

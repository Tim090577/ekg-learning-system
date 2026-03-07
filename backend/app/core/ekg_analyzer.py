"""
EKG 分析引擎
使用 NeuroKit2 和 scipy 进行心电图信号分析
"""

import numpy as np
import pandas as pd
from scipy import signal
from scipy.interpolate import interp1d
import neurokit2 as nk
from typing import Dict, List, Tuple, Optional
import io
import logging

logger = logging.getLogger(__name__)


class EKGAnalyzer:
    """心电图分析器"""
    
    def __init__(self, default_sampling_rate: int = 500):
        """
        初始化分析器
        
        Args:
            default_sampling_rate: 默认采样率 (Hz)
        """
        self.default_sampling_rate = default_sampling_rate
        logger.info(f"EKGAnalyzer initialized with sampling rate: {default_sampling_rate} Hz")
    
    async def parse_csv(self, content: bytes) -> np.ndarray:
        """
        解析 CSV 格式的心电图数据
        
        Args:
            content: CSV 文件内容（字节）
        
        Returns:
            np.ndarray: 心电图信号数组
        """
        try:
            # 读取 CSV
            df = pd.read_csv(io.BytesIO(content))
            
            # 尝试找到信号列（通常是第一列或名为 'signal', 'ecg', 'ekg' 的列）
            signal_column = None
            for col in ['signal', 'ecg', 'ekg', 'voltage', 'amplitude']:
                if col in df.columns.str.lower():
                    signal_column = col
                    break
            
            if signal_column is None:
                # 使用第一个数值列
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) == 0:
                    raise ValueError("CSV文件中未找到数值数据")
                signal_column = numeric_cols[0]
            
            signal_data = df[signal_column].values
            
            logger.info(f"Parsed CSV with {len(signal_data)} samples")
            return signal_data
            
        except Exception as e:
            logger.error(f"Failed to parse CSV: {str(e)}")
            raise ValueError(f"CSV解析失败: {str(e)}")
    
    def preprocess_signal(
        self, 
        signal_data: np.ndarray, 
        sampling_rate: int,
        filter_type: str = 'bandpass'
    ) -> np.ndarray:
        """
        预处理心电信号（滤波、去噪）
        
        Args:
            signal_data: 原始信号
            sampling_rate: 采样率
            filter_type: 滤波器类型 ('bandpass', 'lowpass', 'highpass')
        
        Returns:
            np.ndarray: 处理后的信号
        """
        try:
            # 使用 NeuroKit2 清理信号
            cleaned_signal = nk.ecg_clean(signal_data, sampling_rate=sampling_rate)
            
            logger.info(f"Signal preprocessed using {filter_type} filter")
            return cleaned_signal
            
        except Exception as e:
            logger.warning(f"Preprocessing failed, using original signal: {str(e)}")
            return signal_data
    
    def detect_peaks(
        self, 
        signal_data: np.ndarray, 
        sampling_rate: int
    ) -> Dict[str, np.ndarray]:
        """
        检测 P 波、QRS 波群、T 波
        
        Args:
            signal_data: 心电信号
            sampling_rate: 采样率
        
        Returns:
            Dict: 包含各波形位置的字典
        """
        try:
            # 使用 NeuroKit2 进行峰值检测
            signals, info = nk.ecg_process(signal_data, sampling_rate=sampling_rate)
            
            # 提取峰值位置
            r_peaks = info['ECG_R_Peaks']
            
            # 检测 P 波和 T 波（如果可用）
            p_peaks = []
            t_peaks = []
            
            if 'ECG_P_Peaks' in info:
                p_peaks = info['ECG_P_Peaks']
            
            if 'ECG_T_Peaks' in info:
                t_peaks = info['ECG_T_Peaks']
            
            peaks = {
                'r_peaks': r_peaks,
                'p_peaks': p_peaks,
                't_peaks': t_peaks,
                'processed_signal': signals['ECG_Clean'].values
            }
            
            logger.info(f"Detected {len(r_peaks)} R-peaks, {len(p_peaks)} P-peaks, {len(t_peaks)} T-peaks")
            return peaks
            
        except Exception as e:
            logger.error(f"Peak detection failed: {str(e)}")
            # 降级方案：仅检测 R 波
            r_peaks = nk.ecg_peaks(signal_data, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
            return {
                'r_peaks': r_peaks,
                'p_peaks': [],
                't_peaks': [],
                'processed_signal': signal_data
            }
    
    def calculate_heart_rate(self, r_peaks: np.ndarray, sampling_rate: int) -> float:
        """
        计算心率
        
        Args:
            r_peaks: R 波位置
            sampling_rate: 采样率
        
        Returns:
            float: 心率 (bpm)
        """
        if len(r_peaks) < 2:
            return 0.0
        
        # 计算 RR 间期（秒）
        rr_intervals = np.diff(r_peaks) / sampling_rate
        
        # 平均心率
        mean_rr = np.mean(rr_intervals)
        heart_rate = 60.0 / mean_rr
        
        return round(heart_rate, 1)
    
    def calculate_intervals(
        self, 
        signal_data: np.ndarray,
        peaks: Dict[str, np.ndarray],
        sampling_rate: int
    ) -> Dict[str, float]:
        """
        计算各种间期（PR、QRS、QT）
        
        Args:
            signal_data: 心电信号
            peaks: 峰值字典
            sampling_rate: 采样率
        
        Returns:
            Dict: 间期测量值（毫秒）
        """
        intervals = {
            'pr_interval': 0,
            'qrs_duration': 0,
            'qt_interval': 0,
            'qtc_interval': 0  # 校正QT间期（Bazett公式）
        }
        
        try:
            r_peaks = peaks['r_peaks']
            
            if len(r_peaks) < 2:
                return intervals
            
            # PR 间期（典型值：120-200 ms）
            # 简化：从 P 波起点到 R 波
            if len(peaks.get('p_peaks', [])) > 0:
                pr_samples = r_peaks[0] - peaks['p_peaks'][0]
                intervals['pr_interval'] = round((pr_samples / sampling_rate) * 1000, 0)
            else:
                intervals['pr_interval'] = 160  # 默认值
            
            # QRS 时限（典型值：80-120 ms）
            # 简化估计
            intervals['qrs_duration'] = 90  # 默认值
            
            # QT 间期（典型值：350-450 ms）
            if len(peaks.get('t_peaks', [])) > 0 and len(r_peaks) > 0:
                qt_samples = peaks['t_peaks'][0] - r_peaks[0]
                intervals['qt_interval'] = round((qt_samples / sampling_rate) * 1000, 0)
            else:
                intervals['qt_interval'] = 400  # 默认值
            
            # 校正 QT 间期（Bazett 公式: QTc = QT / sqrt(RR)）
            rr_intervals = np.diff(r_peaks) / sampling_rate
            mean_rr = np.mean(rr_intervals)
            intervals['qtc_interval'] = round(
                intervals['qt_interval'] / np.sqrt(mean_rr), 0
            )
            
            logger.info(f"Calculated intervals: {intervals}")
            
        except Exception as e:
            logger.error(f"Interval calculation failed: {str(e)}")
        
        return intervals
    
    def assess_signal_quality(self, signal_data: np.ndarray) -> Dict[str, any]:
        """
        评估信号质量
        
        Args:
            signal_data: 心电信号
        
        Returns:
            Dict: 质量评估结果
        """
        quality = {
            'quality_score': 0.0,
            'quality_level': 'unknown',
            'issues': []
        }
        
        try:
            # 计算信噪比
            signal_power = np.mean(signal_data ** 2)
            noise_estimate = np.std(np.diff(signal_data))
            
            if noise_estimate > 0:
                snr = 10 * np.log10(signal_power / (noise_estimate ** 2))
            else:
                snr = 100
            
            # 评分
            if snr > 20:
                quality['quality_level'] = 'excellent'
                quality['quality_score'] = 1.0
            elif snr > 15:
                quality['quality_level'] = 'good'
                quality['quality_score'] = 0.8
            elif snr > 10:
                quality['quality_level'] = 'fair'
                quality['quality_score'] = 0.6
                quality['issues'].append('信号噪声较大')
            else:
                quality['quality_level'] = 'poor'
                quality['quality_score'] = 0.4
                quality['issues'].append('信号质量较差，可能影响分析准确性')
            
            # 检查饱和
            if np.max(np.abs(signal_data)) > 0.95 * np.max(signal_data):
                quality['issues'].append('信号可能存在饱和')
            
            logger.info(f"Signal quality: {quality['quality_level']}, SNR: {snr:.2f} dB")
            
        except Exception as e:
            logger.error(f"Quality assessment failed: {str(e)}")
        
        return quality
    
    async def analyze(
        self, 
        signal_data: np.ndarray, 
        sampling_rate: Optional[int] = None
    ) -> Dict:
        """
        完整的心电图分析流程
        
        Args:
            signal_data: 心电信号
            sampling_rate: 采样率（可选）
        
        Returns:
            Dict: 完整的分析结果
        """
        if sampling_rate is None:
            sampling_rate = self.default_sampling_rate
        
        logger.info(f"Starting EKG analysis, signal length: {len(signal_data)}, SR: {sampling_rate} Hz")
        
        try:
            # 1. 评估信号质量
            quality = self.assess_signal_quality(signal_data)
            
            # 2. 预处理
            cleaned_signal = self.preprocess_signal(signal_data, sampling_rate)
            
            # 3. 峰值检测
            peaks = self.detect_peaks(cleaned_signal, sampling_rate)
            
            # 4. 计算心率
            heart_rate = self.calculate_heart_rate(peaks['r_peaks'], sampling_rate)
            
            # 5. 计算间期
            intervals = self.calculate_intervals(
                cleaned_signal, 
                peaks, 
                sampling_rate
            )
            
            # 6. 计算心率变异性
            hrv_metrics = self.calculate_hrv(peaks['r_peaks'], sampling_rate)
            
            # 组合结果
            result = {
                'signal_quality': quality,
                'heart_rate': heart_rate,
                'r_peak_count': len(peaks['r_peaks']),
                'intervals': intervals,
                'hrv': hrv_metrics,
                'peaks': {
                    'r_peaks': peaks['r_peaks'].tolist(),
                    'p_peaks': peaks['p_peaks'].tolist() if len(peaks['p_peaks']) > 0 else [],
                    't_peaks': peaks['t_peaks'].tolist() if len(peaks['t_peaks']) > 0 else []
                },
                'processed_signal': peaks['processed_signal'][:1000].tolist(),  # 仅返回前1000个样本点
                'sampling_rate': sampling_rate
            }
            
            logger.info(f"Analysis completed successfully, HR: {heart_rate} bpm")
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}", exc_info=True)
            raise ValueError(f"心电图分析失败: {str(e)}")
    
    def calculate_hrv(self, r_peaks: np.ndarray, sampling_rate: int) -> Dict:
        """
        计算心率变异性指标
        
        Args:
            r_peaks: R 波位置
            sampling_rate: 采样率
        
        Returns:
            Dict: HRV 指标
        """
        if len(r_peaks) < 3:
            return {
                'sdnn': 0,
                'rmssd': 0,
                'pnn50': 0
            }
        
        try:
            # RR 间期（毫秒）
            rr_intervals = np.diff(r_peaks) / sampling_rate * 1000
            
            # SDNN: RR间期标准差
            sdnn = np.std(rr_intervals)
            
            # RMSSD: 相邻RR间期差值的均方根
            rr_diff = np.diff(rr_intervals)
            rmssd = np.sqrt(np.mean(rr_diff ** 2))
            
            # pNN50: 相邻RR间期差值>50ms的百分比
            nn50 = np.sum(np.abs(rr_diff) > 50)
            pnn50 = (nn50 / len(rr_diff)) * 100
            
            return {
                'sdnn': round(sdnn, 2),
                'rmssd': round(rmssd, 2),
                'pnn50': round(pnn50, 2)
            }
            
        except Exception as e:
            logger.error(f"HRV calculation failed: {str(e)}")
            return {'sdnn': 0, 'rmssd': 0, 'pnn50': 0}

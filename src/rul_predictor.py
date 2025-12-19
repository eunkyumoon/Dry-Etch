"""
잔존 수명 예측 (RUL) 모듈
간단한 선형 회귀 모델 기반 RUL 예측
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class RULPredictor:
    """잔존 수명 예측 클래스"""
    
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def train(self, X: np.ndarray, y: np.ndarray):
        """
        모델 학습
        
        Args:
            X: 입력 특성 (n_samples, n_features)
               [vpp, vdc, phase, yttrium_peak, fo_ratio, cumulative_rf_time]
            y: 타겟 값 (잔여 두께, μm)
        """
        if X.shape[0] != y.shape[0]:
            raise ValueError("입력과 타겟의 샘플 수가 일치하지 않습니다.")
        
        # 데이터 정규화
        X_scaled = self.scaler.fit_transform(X)
        
        # 모델 학습
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def predict(self, vpp: float, vdc: float, phase: float, 
               yttrium_peak: float, fo_ratio: float, 
               cumulative_rf_time: float) -> Tuple[float, float, float]:
        """
        잔존 수명 예측
        
        Args:
            vpp: Peak-to-Peak Voltage
            vdc: Self-Bias Voltage
            phase: Phase Angle
            yttrium_peak: OES Yttrium Peak
            fo_ratio: F/O Ratio
            cumulative_rf_time: 누적 RF On-time
            
        Returns:
            (예상 잔여 두께, RUL 시간, 신뢰 구간 하한)
        """
        if not self.is_trained:
            # 학습 데이터가 없는 경우 간단한 휴리스틱 사용
            return self._heuristic_predict(vpp, yttrium_peak, cumulative_rf_time)
        
        # 입력 데이터 준비
        X = np.array([[vpp, vdc, phase, yttrium_peak, fo_ratio, cumulative_rf_time]])
        X_scaled = self.scaler.transform(X)
        
        # 예측
        predicted_thickness = self.model.predict(X_scaled)[0]
        
        # RUL 계산 (간단한 선형 가정: 시간당 마모율)
        if predicted_thickness > 0:
            # 평균 마모율 가정 (시간당 0.1 μm)
            wear_rate = 0.1  # μm/hour
            rul_hours = predicted_thickness / wear_rate
        else:
            rul_hours = 0
        
        # 신뢰 구간 (간단한 고정값, 실제로는 모델 불확실성 계산 필요)
        confidence_lower = predicted_thickness * 0.9
        
        return predicted_thickness, rul_hours, confidence_lower
    
    def _heuristic_predict(self, vpp: float, yttrium_peak: float, 
                         cumulative_rf_time: float) -> Tuple[float, float, float]:
        """학습 데이터가 없을 때 사용하는 휴리스틱 예측"""
        initial_thickness = 1000.0  # 초기 두께 가정
        
        # 간단한 휴리스틱: Vpp 증가와 Yttrium Peak 감소 기반
        vpp_factor = (vpp - 400) / 200  # 400~600V 정규화
        yttrium_factor = 1 - yttrium_peak
        
        # 마모 진행도 추정
        wear_progress = min((vpp_factor * 0.4 + yttrium_factor * 0.4 + 
                           cumulative_rf_time / 2000 * 0.2), 1.0)
        
        predicted_thickness = initial_thickness * (1 - wear_progress)
        wear_rate = 0.1  # μm/hour
        rul_hours = predicted_thickness / wear_rate if predicted_thickness > 0 else 0
        confidence_lower = predicted_thickness * 0.9
        
        return predicted_thickness, rul_hours, confidence_lower


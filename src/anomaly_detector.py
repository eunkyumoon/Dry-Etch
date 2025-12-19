"""
이상 탐지 모듈
Arcing 위험 및 급격한 마모 탐지
"""

from typing import Dict, Tuple, Optional
from datetime import datetime


class AnomalyDetector:
    """이상 탐지 클래스"""
    
    def __init__(self):
        self.vpp_history = []
        self.wear_rate_history = []
        
    def detect_arcing_risk(self, vpp: float, vdc: float, phase: float,
                          yttrium_peak: float, degradation_index: float) -> Tuple[float, str]:
        """
        Arcing 위험도 계산
        
        Args:
            vpp: Peak-to-Peak Voltage
            vdc: Self-Bias Voltage
            phase: Phase Angle
            yttrium_peak: OES Yttrium Peak
            degradation_index: 마모 진행도
            
        Returns:
            (위험도 %, 위험 등급)
        """
        risk_score = 0.0
        
        # Vpp 급증 위험 (30%)
        if vpp > 550:
            risk_score += 30
        elif vpp > 520:
            risk_score += 15
        
        # Vdc 불안정 위험 (20%)
        if abs(vdc) > 250:
            risk_score += 20
        elif abs(vdc) > 220:
            risk_score += 10
        
        # Phase 불안정 위험 (20%)
        if phase < 30 or phase > 70:
            risk_score += 20
        elif phase < 40 or phase > 60:
            risk_score += 10
        
        # Yttrium Peak 급감 위험 (20%)
        if yttrium_peak < 0.3:
            risk_score += 20
        elif yttrium_peak < 0.5:
            risk_score += 10
        
        # 마모 진행도 위험 (10%)
        if degradation_index > 80:
            risk_score += 10
        elif degradation_index > 60:
            risk_score += 5
        
        # 위험 등급 분류
        if risk_score >= 70:
            risk_level = "매우높음"
        elif risk_score >= 50:
            risk_level = "높음"
        elif risk_score >= 30:
            risk_level = "보통"
        else:
            risk_level = "낮음"
        
        return min(risk_score, 100), risk_level
    
    def detect_rapid_wear(self, current_degradation: float, 
                         previous_degradation: Optional[float] = None,
                         time_interval_hours: float = 1.0) -> Tuple[bool, float]:
        """
        급격한 마모 탐지
        
        Args:
            current_degradation: 현재 마모 진행도
            previous_degradation: 이전 마모 진행도
            time_interval_hours: 시간 간격 (시간)
            
        Returns:
            (급격한 마모 여부, 마모율 %/시간)
        """
        if previous_degradation is None:
            return False, 0.0
        
        wear_rate = (current_degradation - previous_degradation) / time_interval_hours
        
        # 임계값: 시간당 5% 이상 증가 시 급격한 마모로 판단
        threshold = 5.0  # %/hour
        
        is_rapid_wear = wear_rate > threshold
        
        return is_rapid_wear, wear_rate
    
    def check_replacement_threshold(self, degradation_index: float, 
                                  remaining_thickness: float,
                                  vpp: float, yttrium_peak: float) -> Tuple[bool, str]:
        """
        교체 임계값 확인
        
        Args:
            degradation_index: 마모 진행도
            remaining_thickness: 예상 잔여 두께
            vpp: 현재 Vpp
            yttrium_peak: 현재 Yttrium Peak
            
        Returns:
            (교체 권장 여부, 알람 레벨)
        """
        # 교체 임계값
        degradation_threshold = 80  # 80% 이상
        thickness_threshold = 200  # 200 μm 이하
        vpp_increase_threshold = 1.15  # 초기 대비 15% 증가
        yttrium_decrease_threshold = 0.3  # 0.3 이하
        
        # 긴급 조건
        if degradation_index >= 90 or remaining_thickness <= 100:
            return True, "긴급"
        
        # 경고 조건
        if (degradation_index >= degradation_threshold or 
            remaining_thickness <= thickness_threshold or
            yttrium_peak <= yttrium_decrease_threshold):
            return True, "경고"
        
        # 주의 조건
        if degradation_index >= 60 or remaining_thickness <= 400:
            return True, "주의"
        
        return False, "정상"


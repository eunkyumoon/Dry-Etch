"""
이상 탐지 모듈
Arcing 위험 및 급격한 마모 탐지
"""

from typing import Tuple

from .config import Config
from .models import ProcessData, WearState


class AnomalyDetector:
    """이상 탐지 클래스"""

    def __init__(self):
        # 향후 히스토리 기반 분석을 위한 변수 (현재 미사용)
        # self.vpp_history: list[float] = []
        # self.wear_rate_history: list[float] = []
        pass

    def detect_arcing_risk(
        self, process_data: ProcessData, wear_state: WearState
    ) -> Tuple[float, str]:
        """
        Arcing 위험도 계산

        Args:
            process_data: 공정 데이터
            wear_state: 마모 상태

        Returns:
            (위험도 %, 위험 등급)
        """
        rf = process_data.rf_params
        oes = process_data.oes_data

        risk_score = 0.0

        # Vpp 급증 위험
        risk_score += self._calculate_vpp_risk(rf.vpp)

        # Vdc 불안정 위험
        risk_score += self._calculate_vdc_risk(rf.vdc)

        # Phase 불안정 위험
        risk_score += self._calculate_phase_risk(rf.phase)

        # Yttrium Peak 급감 위험
        risk_score += self._calculate_yttrium_risk(oes.yttrium_peak)

        # 마모 진행도 위험
        risk_score += self._calculate_degradation_risk(
            wear_state.degradation_index
        )

        # 위험 등급 분류
        risk_level = self._classify_risk_level(risk_score)

        return min(risk_score, 100), risk_level

    def _calculate_vpp_risk(self, vpp: float) -> float:
        """Vpp 위험도 계산"""
        if vpp > Config.VPP_HIGH_RISK:
            return Config.VPP_RISK_WEIGHT
        if vpp > Config.VPP_MEDIUM_RISK:
            return Config.VPP_RISK_WEIGHT / 2
        return 0.0

    def _calculate_vdc_risk(self, vdc: float) -> float:
        """Vdc 위험도 계산"""
        abs_vdc = abs(vdc)
        if abs_vdc > Config.VDC_HIGH_RISK:
            return Config.VDC_RISK_WEIGHT
        if abs_vdc > Config.VDC_MEDIUM_RISK:
            return Config.VDC_RISK_WEIGHT / 2
        return 0.0

    def _calculate_phase_risk(self, phase: float) -> float:
        """Phase 위험도 계산"""
        if phase < Config.PHASE_LOW or phase > Config.PHASE_HIGH:
            return Config.PHASE_RISK_WEIGHT
        if (
            phase < Config.PHASE_CAUTION_LOW
            or phase > Config.PHASE_CAUTION_HIGH
        ):
            return Config.PHASE_RISK_WEIGHT / 2
        return 0.0

    def _calculate_yttrium_risk(self, yttrium_peak: float) -> float:
        """Yttrium Peak 위험도 계산"""
        if yttrium_peak < Config.YTTRIUM_HIGH_RISK:
            return Config.YTTRIUM_RISK_WEIGHT
        if yttrium_peak < Config.YTTRIUM_MEDIUM_RISK:
            return Config.YTTRIUM_RISK_WEIGHT / 2
        return 0.0

    def _calculate_degradation_risk(self, degradation_index: float) -> float:
        """마모 진행도 위험도 계산"""
        if degradation_index > Config.DEGRADATION_WARNING:
            return Config.DEGRADATION_RISK_WEIGHT
        if degradation_index > Config.DEGRADATION_CAUTION_THRESHOLD:
            return Config.DEGRADATION_RISK_WEIGHT / 2
        return 0.0

    def _classify_risk_level(self, risk_score: float) -> str:
        """위험 등급 분류"""
        if risk_score >= Config.RISK_VERY_HIGH:
            return "매우높음"
        if risk_score >= Config.RISK_HIGH:
            return "높음"
        if risk_score >= Config.RISK_MEDIUM:
            return "보통"
        return "낮음"

    def detect_rapid_wear(
        self,
        current_degradation: float,
        previous_degradation: float | None = None,
        time_interval_hours: float = 1.0,
    ) -> Tuple[bool, float]:
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

        wear_rate = (
            current_degradation - previous_degradation
        ) / time_interval_hours

        is_rapid_wear = wear_rate > Config.RAPID_WEAR_THRESHOLD

        return is_rapid_wear, wear_rate

    def check_replacement_threshold(
        self, wear_state: WearState, oes_yttrium_peak: float
    ) -> Tuple[bool, str]:
        """
        교체 임계값 확인

        Args:
            wear_state: 마모 상태
            oes_yttrium_peak: 현재 Yttrium Peak

        Returns:
            (교체 권장 여부, 알람 레벨)
        """
        # 긴급 조건
        if (
            wear_state.degradation_index >= Config.DEGRADATION_URGENT
            or wear_state.remaining_thickness <= Config.THICKNESS_URGENT
        ):
            return True, "긴급"

        # 경고 조건
        if (
            wear_state.degradation_index >= Config.DEGRADATION_THRESHOLD
            or wear_state.remaining_thickness <= Config.THICKNESS_THRESHOLD
            or oes_yttrium_peak <= Config.YTTRIUM_DECREASE_THRESHOLD
        ):
            return True, "경고"

        # 주의 조건
        if (
            wear_state.degradation_index >= Config.DEGRADATION_CAUTION_THRESHOLD
            or wear_state.remaining_thickness <= Config.THICKNESS_CAUTION
        ):
            return True, "주의"

        return False, "정상"


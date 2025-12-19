"""
마모 상태 추정 모듈
Degradation Index 계산 및 마모 진행도 추정
"""

from .config import Config
from .models import WearState


class WearEstimator:
    """마모 상태 추정 클래스"""

    def __init__(self, initial_thickness: float = Config.INITIAL_THICKNESS):
        """
        초기화

        Args:
            initial_thickness: 초기 코팅 두께 (μm)
        """
        self.initial_thickness = initial_thickness
        self.initial_vpp: float | None = None
        self.initial_yttrium_peak: float | None = None

    def set_initial_state(self, vpp: float, yttrium_peak: float):
        """
        초기 상태 설정

        Args:
            vpp: 초기 Vpp 값
            yttrium_peak: 초기 OES Yttrium Peak 값
        """
        self.initial_vpp = vpp
        self.initial_yttrium_peak = yttrium_peak

    def calculate_degradation_index(
        self, vpp: float, yttrium_peak: float, cumulative_rf_time: float
    ) -> float:
        """
        마모 진행도 (Degradation Index) 계산

        Args:
            vpp: 현재 Vpp 값
            yttrium_peak: 현재 OES Yttrium Peak 값
            cumulative_rf_time: 누적 RF On-time (시간)

        Returns:
            Degradation Index (0~100%)

        Raises:
            ValueError: 초기 상태가 설정되지 않은 경우
        """
        if self.initial_vpp is None or self.initial_yttrium_peak is None:
            raise ValueError("초기 상태가 설정되지 않았습니다.")

        # Vpp 기반 마모 진행도 (0~50%)
        vpp_increase = ((vpp - self.initial_vpp) / self.initial_vpp) * 100
        vpp_degradation = min(max(vpp_increase * 2, 0), 50)

        # OES Yttrium Peak 기반 마모 진행도 (0~50%)
        yttrium_decrease = (
            (self.initial_yttrium_peak - yttrium_peak)
            / self.initial_yttrium_peak
            * 100
        )
        yttrium_degradation = min(max(yttrium_decrease * 2, 0), 50)

        # 누적 손상 모델 (시간 기반, 0~20%)
        time_degradation = min(
            cumulative_rf_time
            / Config.TIME_DEGRADATION_FACTOR
            * Config.TIME_DEGRADATION_MAX,
            Config.TIME_DEGRADATION_MAX,
        )

        # 종합 마모 진행도
        degradation_index = min(
            vpp_degradation + yttrium_degradation + time_degradation, 100
        )

        return degradation_index

    def estimate_remaining_thickness(self, degradation_index: float) -> float:
        """
        예상 잔여 두께 계산

        Args:
            degradation_index: 마모 진행도 (0~100%)

        Returns:
            예상 잔여 두께 (μm)
        """
        remaining_thickness = self.initial_thickness * (
            1 - degradation_index / 100
        )
        return max(remaining_thickness, 0)

    def get_wear_status(self, degradation_index: float) -> str:
        """
        마모 상태 분류

        Args:
            degradation_index: 마모 진행도 (0~100%)

        Returns:
            상태 (정상 / 주의 / 위험 / 긴급)
        """
        if degradation_index < Config.DEGRADATION_NORMAL:
            return "정상"
        if degradation_index < Config.DEGRADATION_CAUTION:
            return "주의"
        if degradation_index < Config.DEGRADATION_WARNING:
            return "위험"
        return "긴급"

    def calculate_wear_state(
        self, vpp: float, yttrium_peak: float, cumulative_rf_time: float
    ) -> WearState:
        """
        마모 상태 전체 계산

        Args:
            vpp: 현재 Vpp 값
            yttrium_peak: 현재 OES Yttrium Peak 값
            cumulative_rf_time: 누적 RF On-time (시간)

        Returns:
            WearState 객체
        """
        degradation_index = self.calculate_degradation_index(
            vpp, yttrium_peak, cumulative_rf_time
        )
        remaining_thickness = self.estimate_remaining_thickness(
            degradation_index
        )
        status = self.get_wear_status(degradation_index)

        return WearState(
            degradation_index=degradation_index,
            remaining_thickness=remaining_thickness,
            status=status,
        )


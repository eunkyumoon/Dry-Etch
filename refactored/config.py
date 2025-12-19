"""
설정 파일
시스템 전반에 사용되는 상수 및 설정값 정의
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Config:
    """시스템 설정 클래스"""

    # 초기값
    INITIAL_THICKNESS: float = 1000.0  # 초기 코팅 두께 (μm)
    INITIAL_VPP: float = 450.0  # 초기 Vpp (V)
    INITIAL_YTTRIUM_PEAK: float = 0.85  # 초기 Yttrium Peak

    # RF 파라미터 범위
    VPP_MIN: float = 400.0
    VPP_MAX: float = 600.0
    VDC_MIN: float = -300.0
    VDC_MAX: float = -100.0
    PHASE_MIN: float = 0.0
    PHASE_MAX: float = 90.0

    # OES 데이터 범위
    YTTRIUM_PEAK_MIN: float = 0.0
    YTTRIUM_PEAK_MAX: float = 1.0
    FO_RATIO_MIN: float = 0.5
    FO_RATIO_MAX: float = 2.0

    # 마모 진행도 임계값
    DEGRADATION_NORMAL: float = 30.0
    DEGRADATION_CAUTION: float = 50.0
    DEGRADATION_WARNING: float = 80.0
    DEGRADATION_URGENT: float = 90.0

    # 교체 임계값
    DEGRADATION_THRESHOLD: float = 80.0
    THICKNESS_THRESHOLD: float = 200.0
    THICKNESS_URGENT: float = 100.0
    THICKNESS_CAUTION: float = 400.0
    VPP_INCREASE_THRESHOLD: float = 1.15  # 초기 대비 15% 증가
    YTTRIUM_DECREASE_THRESHOLD: float = 0.3

    # Arcing 위험 임계값
    VPP_HIGH_RISK: float = 550.0
    VPP_MEDIUM_RISK: float = 520.0
    VDC_HIGH_RISK: float = 250.0
    VDC_MEDIUM_RISK: float = 220.0
    PHASE_LOW: float = 30.0
    PHASE_HIGH: float = 70.0
    PHASE_CAUTION_LOW: float = 40.0
    PHASE_CAUTION_HIGH: float = 60.0
    YTTRIUM_HIGH_RISK: float = 0.3
    YTTRIUM_MEDIUM_RISK: float = 0.5

    # 마모율
    WEAR_RATE: float = 0.1  # μm/hour
    RAPID_WEAR_THRESHOLD: float = 5.0  # %/hour

    # 시간 기반 마모 계산
    TIME_DEGRADATION_FACTOR: float = 1000.0  # 시간당 마모율 계산 기준
    TIME_DEGRADATION_MAX: float = 20.0  # 최대 시간 기반 마모 진행도 (%)

    # Arcing 위험도 가중치
    VPP_RISK_WEIGHT: float = 30.0
    VDC_RISK_WEIGHT: float = 20.0
    PHASE_RISK_WEIGHT: float = 20.0
    YTTRIUM_RISK_WEIGHT: float = 20.0
    DEGRADATION_RISK_WEIGHT: float = 10.0

    # Arcing 위험 등급 임계값
    RISK_VERY_HIGH: float = 70.0
    RISK_HIGH: float = 50.0
    RISK_MEDIUM: float = 30.0

    # 시뮬레이션 파라미터
    WEAR_PROGRESS_BASE_HOURS: float = 2000.0  # 마모 진행도 계산 기준 시간
    VPP_INCREASE_RATE: float = 0.2  # Vpp 증가율
    INITIAL_VDC: float = -200.0  # 초기 Vdc 값
    VDC_INCREASE_RATE: float = 0.1  # Vdc 증가율
    INITIAL_PHASE: float = 45.0  # 초기 Phase 값
    PHASE_INCREASE_RATE: float = 10.0  # Phase 증가량
    YTTRIUM_DECREASE_RATE: float = 0.5  # Yttrium Peak 감소율
    DEFAULT_FO_RATIO: float = 1.2  # 기본 F/O Ratio 값
    DEFAULT_MATCHER_POS: float = 0.5  # 기본 Matcher Position 값

    # 신뢰 구간 계산
    CONFIDENCE_LOWER_FACTOR: float = 0.9  # 신뢰 구간 하한 계수
    CONFIDENCE_UPPER_FACTOR: float = 1.1  # 신뢰 구간 상한 계수

    # 휴리스틱 예측 가중치
    HEURISTIC_VPP_WEIGHT: float = 0.4  # Vpp 가중치
    HEURISTIC_YTTRIUM_WEIGHT: float = 0.4  # Yttrium Peak 가중치
    HEURISTIC_TIME_WEIGHT: float = 0.2  # 시간 가중치
    HEURISTIC_TIME_BASE: float = 2000.0  # 시간 기반 마모 계산 기준

    # 마모 진행도 주의 임계값
    DEGRADATION_CAUTION_THRESHOLD: float = 60.0  # 마모 진행도 주의 임계값

    @classmethod
    def get_vpp_range(cls) -> Tuple[float, float]:
        """Vpp 유효 범위 반환"""
        return cls.VPP_MIN, cls.VPP_MAX

    @classmethod
    def get_vdc_range(cls) -> Tuple[float, float]:
        """Vdc 유효 범위 반환"""
        return cls.VDC_MIN, cls.VDC_MAX

    @classmethod
    def get_phase_range(cls) -> Tuple[float, float]:
        """Phase 유효 범위 반환"""
        return cls.PHASE_MIN, cls.PHASE_MAX


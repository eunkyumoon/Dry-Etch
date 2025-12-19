"""
데이터 모델
데이터 클래스를 통한 타입 안전성 향상
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RFParameters:
    """RF 파라미터 데이터 클래스"""

    vpp: float
    vdc: float
    phase: float
    matcher_pos: float
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """초기화 후 검증"""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class OESData:
    """OES 데이터 클래스"""

    yttrium_peak: float
    fo_ratio: float
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """초기화 후 검증"""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class ProcessData:
    """공정 데이터 클래스"""

    rf_params: RFParameters
    oes_data: OESData
    cumulative_rf_time: float
    cumulative_energy: float = 0.0
    recipe_name: str = ""


@dataclass
class WearState:
    """마모 상태 클래스"""

    degradation_index: float
    remaining_thickness: float
    status: str
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """초기화 후 검증"""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class RULPrediction:
    """RUL 예측 결과 클래스"""

    predicted_thickness: float
    rul_hours: float
    confidence_lower: float
    confidence_upper: Optional[float] = None


@dataclass
class SystemStatus:
    """시스템 상태 정보 클래스"""

    hour: int
    vpp: float
    yttrium_peak: float
    wear_state: WearState
    rul_prediction: RULPrediction
    arcing_risk: float
    risk_level: str
    replacement_needed: bool
    alarm_level: str
    is_rapid_wear: bool
    wear_rate: float


@dataclass
class SimulationParameters:
    """시뮬레이션 파라미터 클래스"""

    wear_progress: float
    vpp: float
    vdc: float
    phase: float
    yttrium_peak: float
    fo_ratio: float


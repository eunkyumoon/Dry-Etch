"""
데이터 수집 모듈
RF 파라미터 및 OES 데이터 수집 기능
"""

from datetime import datetime
from typing import Optional

import pandas as pd

from .config import Config
from .models import OESData, RFParameters


class DataCollector:
    """데이터 수집 클래스"""

    def __init__(self):
        self.rf_data: list[RFParameters] = []
        self.oes_data: list[OESData] = []

    def collect_rf_parameters(
        self, rf_params: RFParameters
    ) -> RFParameters:
        """
        RF 파라미터 데이터 수집

        Args:
            rf_params: RF 파라미터 데이터 클래스

        Returns:
            수집된 RF 파라미터

        Raises:
            ValueError: RF 파라미터가 유효 범위를 벗어난 경우
        """
        if not self._validate_rf_data(rf_params):
            raise ValueError("RF 파라미터가 유효 범위를 벗어났습니다.")

        self.rf_data.append(rf_params)
        return rf_params

    def collect_oes_data(self, oes_data: OESData) -> OESData:
        """
        OES 데이터 수집

        Args:
            oes_data: OES 데이터 클래스

        Returns:
            수집된 OES 데이터

        Raises:
            ValueError: OES 데이터가 유효 범위를 벗어난 경우
        """
        if not self._validate_oes_data(oes_data):
            raise ValueError("OES 데이터가 유효 범위를 벗어났습니다.")

        self.oes_data.append(oes_data)
        return oes_data

    def _validate_rf_data(self, rf_params: RFParameters) -> bool:
        """RF 데이터 유효성 검증"""
        vpp_min, vpp_max = Config.get_vpp_range()
        vdc_min, vdc_max = Config.get_vdc_range()
        phase_min, phase_max = Config.get_phase_range()

        return (
            vpp_min <= rf_params.vpp <= vpp_max
            and vdc_min <= rf_params.vdc <= vdc_max
            and phase_min <= rf_params.phase <= phase_max
        )

    def _validate_oes_data(self, oes_data: OESData) -> bool:
        """OES 데이터 유효성 검증"""
        return (
            Config.YTTRIUM_PEAK_MIN
            <= oes_data.yttrium_peak
            <= Config.YTTRIUM_PEAK_MAX
            and Config.FO_RATIO_MIN <= oes_data.fo_ratio <= Config.FO_RATIO_MAX
        )

    def get_rf_dataframe(self) -> pd.DataFrame:
        """RF 데이터를 DataFrame으로 반환"""
        if not self.rf_data:
            return pd.DataFrame()

        data = [
            {
                "timestamp": rf.timestamp,
                "vpp": rf.vpp,
                "vdc": rf.vdc,
                "phase": rf.phase,
                "matcher_pos": rf.matcher_pos,
            }
            for rf in self.rf_data
        ]
        return pd.DataFrame(data)

    def get_oes_dataframe(self) -> pd.DataFrame:
        """OES 데이터를 DataFrame으로 반환"""
        if not self.oes_data:
            return pd.DataFrame()

        data = [
            {
                "timestamp": oes.timestamp,
                "yttrium_peak": oes.yttrium_peak,
                "fo_ratio": oes.fo_ratio,
            }
            for oes in self.oes_data
        ]
        return pd.DataFrame(data)

    def clear_data(self):
        """수집된 데이터 초기화"""
        self.rf_data = []
        self.oes_data = []


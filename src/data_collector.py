"""
데이터 수집 모듈
RF 파라미터 및 OES 데이터 수집 기능
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime


class DataCollector:
    """데이터 수집 클래스"""
    
    def __init__(self):
        self.rf_data = []
        self.oes_data = []
        
    def collect_rf_parameters(self, vpp: float, vdc: float, phase: float, 
                              matcher_pos: float, timestamp: Optional[datetime] = None) -> Dict:
        """
        RF 파라미터 데이터 수집
        
        Args:
            vpp: Peak-to-Peak Voltage (V)
            vdc: Self-Bias Voltage (V)
            phase: Phase Angle (degrees)
            matcher_pos: Matcher Position
            timestamp: 데이터 수집 시간
            
        Returns:
            수집된 RF 파라미터 딕셔너리
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        # 데이터 검증
        if not self._validate_rf_data(vpp, vdc, phase):
            raise ValueError("RF 파라미터가 유효 범위를 벗어났습니다.")
        
        data = {
            'timestamp': timestamp,
            'vpp': vpp,
            'vdc': vdc,
            'phase': phase,
            'matcher_pos': matcher_pos
        }
        
        self.rf_data.append(data)
        return data
    
    def collect_oes_data(self, yttrium_peak: float, fo_ratio: float,
                         timestamp: Optional[datetime] = None) -> Dict:
        """
        OES 데이터 수집
        
        Args:
            yttrium_peak: Yttrium Emission Peak (0~1.0)
            fo_ratio: F/O/Ar Intensity Ratio
            timestamp: 데이터 수집 시간
            
        Returns:
            수집된 OES 데이터 딕셔너리
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        # 데이터 검증
        if not self._validate_oes_data(yttrium_peak, fo_ratio):
            raise ValueError("OES 데이터가 유효 범위를 벗어났습니다.")
        
        data = {
            'timestamp': timestamp,
            'yttrium_peak': yttrium_peak,
            'fo_ratio': fo_ratio
        }
        
        self.oes_data.append(data)
        return data
    
    def _validate_rf_data(self, vpp: float, vdc: float, phase: float) -> bool:
        """RF 데이터 유효성 검증"""
        return (400 <= vpp <= 600 and 
                -300 <= vdc <= -100 and 
                0 <= phase <= 90)
    
    def _validate_oes_data(self, yttrium_peak: float, fo_ratio: float) -> bool:
        """OES 데이터 유효성 검증"""
        return (0 <= yttrium_peak <= 1.0 and 
                0.5 <= fo_ratio <= 2.0)
    
    def get_rf_dataframe(self) -> pd.DataFrame:
        """RF 데이터를 DataFrame으로 반환"""
        if not self.rf_data:
            return pd.DataFrame()
        return pd.DataFrame(self.rf_data)
    
    def get_oes_dataframe(self) -> pd.DataFrame:
        """OES 데이터를 DataFrame으로 반환"""
        if not self.oes_data:
            return pd.DataFrame()
        return pd.DataFrame(self.oes_data)
    
    def clear_data(self):
        """수집된 데이터 초기화"""
        self.rf_data = []
        self.oes_data = []


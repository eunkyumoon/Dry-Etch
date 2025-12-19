"""
잔존 수명 예측 (RUL) 모듈
간단한 선형 회귀 모델 기반 RUL 예측
"""

import warnings
from typing import Tuple

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from .config import Config
from .models import ProcessData, RULPrediction

warnings.filterwarnings("ignore")


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

        Raises:
            ValueError: 입력과 타겟의 샘플 수가 일치하지 않는 경우
        """
        if X.shape[0] != y.shape[0]:
            raise ValueError("입력과 타겟의 샘플 수가 일치하지 않습니다.")

        # 데이터 정규화
        X_scaled = self.scaler.fit_transform(X)

        # 모델 학습
        self.model.fit(X_scaled, y)
        self.is_trained = True

    def predict(self, process_data: ProcessData) -> RULPrediction:
        """
        잔존 수명 예측

        Args:
            process_data: 공정 데이터

        Returns:
            RULPrediction 객체
        """
        if not self.is_trained:
            return self._heuristic_predict(process_data)

        # 입력 데이터 준비
        rf = process_data.rf_params
        oes = process_data.oes_data
        X = np.array(
            [
                [
                    rf.vpp,
                    rf.vdc,
                    rf.phase,
                    oes.yttrium_peak,
                    oes.fo_ratio,
                    process_data.cumulative_rf_time,
                ]
            ]
        )
        X_scaled = self.scaler.transform(X)

        # 예측
        predicted_thickness = self.model.predict(X_scaled)[0]

        # RUL 계산
        rul_hours = self._calculate_rul(predicted_thickness)

        # 신뢰 구간
        confidence_lower, confidence_upper = self._calculate_confidence_interval(
            predicted_thickness
        )

        return RULPrediction(
            predicted_thickness=predicted_thickness,
            rul_hours=rul_hours,
            confidence_lower=confidence_lower,
            confidence_upper=confidence_upper,
        )

    def _calculate_rul(self, predicted_thickness: float) -> float:
        """
        RUL 계산

        Args:
            predicted_thickness: 예상 잔여 두께

        Returns:
            RUL 시간 (시간)
        """
        if predicted_thickness > 0:
            return predicted_thickness / Config.WEAR_RATE
        return 0.0

    def _calculate_confidence_interval(
        self, predicted_thickness: float
    ) -> Tuple[float, float]:
        """
        신뢰 구간 계산

        Args:
            predicted_thickness: 예상 잔여 두께

        Returns:
            (신뢰 구간 하한, 신뢰 구간 상한)
        """
        return (
            predicted_thickness * Config.CONFIDENCE_LOWER_FACTOR,
            predicted_thickness * Config.CONFIDENCE_UPPER_FACTOR,
        )

    def _heuristic_predict(self, process_data: ProcessData) -> RULPrediction:
        """
        학습 데이터가 없을 때 사용하는 휴리스틱 예측

        Args:
            process_data: 공정 데이터

        Returns:
            RULPrediction 객체
        """
        initial_thickness = Config.INITIAL_THICKNESS
        rf = process_data.rf_params
        oes = process_data.oes_data

        # 간단한 휴리스틱: Vpp 증가와 Yttrium Peak 감소 기반
        vpp_min, vpp_max = Config.get_vpp_range()
        vpp_factor = (rf.vpp - vpp_min) / (vpp_max - vpp_min)
        yttrium_factor = 1 - oes.yttrium_peak

        # 마모 진행도 추정
        wear_progress = min(
            (
                vpp_factor * Config.HEURISTIC_VPP_WEIGHT
                + yttrium_factor * Config.HEURISTIC_YTTRIUM_WEIGHT
                + process_data.cumulative_rf_time
                / Config.HEURISTIC_TIME_BASE
                * Config.HEURISTIC_TIME_WEIGHT
            ),
            1.0,
        )

        predicted_thickness = initial_thickness * (1 - wear_progress)
        rul_hours = self._calculate_rul(predicted_thickness)
        confidence_lower, confidence_upper = self._calculate_confidence_interval(
            predicted_thickness
        )

        return RULPrediction(
            predicted_thickness=predicted_thickness,
            rul_hours=rul_hours,
            confidence_lower=confidence_lower,
            confidence_upper=confidence_upper,
        )


"""
메인 실행 파일
Y2O3 Focus Ring 마모도 예측 시스템 실행
"""

from datetime import datetime, timedelta

from .anomaly_detector import AnomalyDetector
from .config import Config
from .data_collector import DataCollector
from .models import (
    OESData,
    ProcessData,
    RFParameters,
    SimulationParameters,
    SystemStatus,
)
from .rul_predictor import RULPredictor
from .wear_estimator import WearEstimator


def simulate_wear_progress(
    collector: DataCollector,
    wear_estimator: WearEstimator,
    rul_predictor: RULPredictor,
    anomaly_detector: AnomalyDetector,
    max_hours: int = 1200,
    interval: int = 100,
):
    """
    마모 진행 시뮬레이션

    Args:
        collector: 데이터 수집기
        wear_estimator: 마모 추정기
        rul_predictor: RUL 예측기
        anomaly_detector: 이상 탐지기
        max_hours: 최대 시뮬레이션 시간
        interval: 시간 간격
    """
    cumulative_rf_time = 0.0
    previous_degradation = 0.0

    for hour in range(0, max_hours, interval):
        cumulative_rf_time = float(hour)

        # 마모 진행에 따른 파라미터 변화 시뮬레이션
        sim_params = calculate_simulation_parameters(hour)

        # 데이터 수집
        rf_params = RFParameters(
            vpp=sim_params.vpp,
            vdc=sim_params.vdc,
            phase=sim_params.phase,
            matcher_pos=Config.DEFAULT_MATCHER_POS,
            timestamp=datetime.now() + timedelta(hours=hour),
        )
        oes_data = OESData(
            yttrium_peak=sim_params.yttrium_peak,
            fo_ratio=sim_params.fo_ratio,
            timestamp=datetime.now() + timedelta(hours=hour),
        )

        collector.collect_rf_parameters(rf_params)
        collector.collect_oes_data(oes_data)

        # 마모 상태 계산
        wear_state = wear_estimator.calculate_wear_state(
            sim_params.vpp, sim_params.yttrium_peak, cumulative_rf_time
        )

        # RUL 예측
        process_data = ProcessData(
            rf_params=rf_params,
            oes_data=oes_data,
            cumulative_rf_time=cumulative_rf_time,
        )
        rul_prediction = rul_predictor.predict(process_data)

        # 이상 탐지
        arcing_risk, risk_level = anomaly_detector.detect_arcing_risk(
            process_data, wear_state
        )

        is_rapid_wear, wear_rate = anomaly_detector.detect_rapid_wear(
            wear_state.degradation_index, previous_degradation, float(interval)
        )

        replacement_needed, alarm_level = (
            anomaly_detector.check_replacement_threshold(
                wear_state, sim_params.yttrium_peak
            )
        )

        # 상태 정보 생성
        status = SystemStatus(
            hour=hour,
            vpp=sim_params.vpp,
            yttrium_peak=sim_params.yttrium_peak,
            wear_state=wear_state,
            rul_prediction=rul_prediction,
            arcing_risk=arcing_risk,
            risk_level=risk_level,
            replacement_needed=replacement_needed,
            alarm_level=alarm_level,
            is_rapid_wear=is_rapid_wear,
            wear_rate=wear_rate,
        )

        # 상태 출력
        print_status(status)

        previous_degradation = wear_state.degradation_index

        # 교체 필요 시 시뮬레이션 종료
        if replacement_needed and alarm_level == "긴급":
            print("\n긴급 교체 필요! 시뮬레이션 종료.")
            break


def calculate_simulation_parameters(hour: int) -> SimulationParameters:
    """
    시뮬레이션 파라미터 계산

    Args:
        hour: 누적 시간

    Returns:
        SimulationParameters 객체
    """
    wear_progress = hour / Config.WEAR_PROGRESS_BASE_HOURS
    return SimulationParameters(
        wear_progress=wear_progress,
        vpp=Config.INITIAL_VPP * (1 + wear_progress * Config.VPP_INCREASE_RATE),
        vdc=Config.INITIAL_VDC * (1 + wear_progress * Config.VDC_INCREASE_RATE),
        phase=Config.INITIAL_PHASE + wear_progress * Config.PHASE_INCREASE_RATE,
        yttrium_peak=Config.INITIAL_YTTRIUM_PEAK
        * (1 - wear_progress * Config.YTTRIUM_DECREASE_RATE),
        fo_ratio=Config.DEFAULT_FO_RATIO,
    )


def print_status(status: SystemStatus):
    """
    상태 출력

    Args:
        status: 시스템 상태 정보
    """
    print(f"\n[누적 시간: {status.hour:.0f}시간]")
    print(f"  Vpp: {status.vpp:.1f}V | Yttrium Peak: {status.yttrium_peak:.3f}")
    print(
        f"  마모 진행도: {status.wear_state.degradation_index:.1f}% "
        f"({status.wear_state.status})"
    )
    print(f"  예상 잔여 두께: {status.wear_state.remaining_thickness:.1f}μm")
    print(f"  예상 RUL: {status.rul_prediction.rul_hours:.0f}시간")
    print(f"  Arcing 위험도: {status.arcing_risk:.1f}% ({status.risk_level})")

    if status.replacement_needed:
        print(f"  [경고] 교체 권장! 알람 레벨: {status.alarm_level}")

    if status.is_rapid_wear:
        print(f"  [경고] 급격한 마모 감지! 마모율: {status.wear_rate:.2f}%/시간")


def main():
    """메인 함수"""
    print("=" * 60)
    print("Y2O3 Focus Ring 마모도 예측 시스템")
    print("=" * 60)

    # 컴포넌트 초기화
    collector = DataCollector()
    wear_estimator = WearEstimator(initial_thickness=Config.INITIAL_THICKNESS)
    rul_predictor = RULPredictor()
    anomaly_detector = AnomalyDetector()

    # 초기 상태 설정
    wear_estimator.set_initial_state(
        Config.INITIAL_VPP, Config.INITIAL_YTTRIUM_PEAK
    )

    print("\n초기 상태 설정 완료")
    print(f"초기 Vpp: {Config.INITIAL_VPP}V")
    print(f"초기 Yttrium Peak: {Config.INITIAL_YTTRIUM_PEAK}")
    print(f"초기 두께: {Config.INITIAL_THICKNESS}μm")

    # 시뮬레이션 실행
    print("\n" + "=" * 60)
    print("시뮬레이션 데이터 분석")
    print("=" * 60)

    simulate_wear_progress(
        collector, wear_estimator, rul_predictor, anomaly_detector
    )

    print("\n" + "=" * 60)
    print("시뮬레이션 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()


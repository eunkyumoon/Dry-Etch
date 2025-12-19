"""
메인 실행 파일
Y2O3 Focus Ring 마모도 예측 시스템 실행
"""

import sys
from datetime import datetime, timedelta
from data_collector import DataCollector
from wear_estimator import WearEstimator
from rul_predictor import RULPredictor
from anomaly_detector import AnomalyDetector


def main():
    """메인 함수"""
    print("=" * 60)
    print("Y2O3 Focus Ring 마모도 예측 시스템")
    print("=" * 60)
    
    # 컴포넌트 초기화
    collector = DataCollector()
    wear_estimator = WearEstimator(initial_thickness=1000.0)
    rul_predictor = RULPredictor()
    anomaly_detector = AnomalyDetector()
    
    # 초기 상태 설정 (예시)
    initial_vpp = 450.0
    initial_yttrium_peak = 0.85
    wear_estimator.set_initial_state(initial_vpp, initial_yttrium_peak)
    
    print("\n초기 상태 설정 완료")
    print(f"초기 Vpp: {initial_vpp}V")
    print(f"초기 Yttrium Peak: {initial_yttrium_peak}")
    print(f"초기 두께: {wear_estimator.initial_thickness}μm")
    
    # 시뮬레이션 데이터 수집 및 분석
    print("\n" + "=" * 60)
    print("시뮬레이션 데이터 분석")
    print("=" * 60)
    
    # 시간에 따른 마모 진행 시뮬레이션
    cumulative_rf_time = 0.0
    previous_degradation = 0.0
    
    for hour in range(0, 1200, 100):  # 0~1200시간, 100시간 간격
        cumulative_rf_time = hour
        
        # 마모 진행에 따른 파라미터 변화 시뮬레이션
        wear_progress = hour / 2000  # 간단한 선형 가정
        current_vpp = initial_vpp * (1 + wear_progress * 0.2)  # 20% 증가
        current_vdc = -200 * (1 + wear_progress * 0.1)
        current_phase = 45 + wear_progress * 10
        current_yttrium_peak = initial_yttrium_peak * (1 - wear_progress * 0.5)
        current_fo_ratio = 1.2
        
        # 데이터 수집
        collector.collect_rf_parameters(
            current_vpp, current_vdc, current_phase, 0.5,
            datetime.now() + timedelta(hours=hour)
        )
        collector.collect_oes_data(
            current_yttrium_peak, current_fo_ratio,
            datetime.now() + timedelta(hours=hour)
        )
        
        # 마모 진행도 계산
        degradation_index = wear_estimator.calculate_degradation_index(
            current_vpp, current_yttrium_peak, cumulative_rf_time
        )
        
        # 잔여 두께 예측
        remaining_thickness = wear_estimator.estimate_remaining_thickness(degradation_index)
        
        # RUL 예측
        predicted_thickness, rul_hours, confidence_lower = rul_predictor.predict(
            current_vpp, current_vdc, current_phase,
            current_yttrium_peak, current_fo_ratio, cumulative_rf_time
        )
        
        # 이상 탐지
        arcing_risk, risk_level = anomaly_detector.detect_arcing_risk(
            current_vpp, current_vdc, current_phase,
            current_yttrium_peak, degradation_index
        )
        
        is_rapid_wear, wear_rate = anomaly_detector.detect_rapid_wear(
            degradation_index, previous_degradation, 100.0
        )
        
        replacement_needed, alarm_level = anomaly_detector.check_replacement_threshold(
            degradation_index, remaining_thickness, current_vpp, current_yttrium_peak
        )
        
        # 상태 출력
        status = wear_estimator.get_wear_status(degradation_index)
        
        print(f"\n[누적 시간: {cumulative_rf_time:.0f}시간]")
        print(f"  Vpp: {current_vpp:.1f}V | Yttrium Peak: {current_yttrium_peak:.3f}")
        print(f"  마모 진행도: {degradation_index:.1f}% ({status})")
        print(f"  예상 잔여 두께: {remaining_thickness:.1f}μm")
        print(f"  예상 RUL: {rul_hours:.0f}시간")
        print(f"  Arcing 위험도: {arcing_risk:.1f}% ({risk_level})")
        
        if replacement_needed:
            print(f"  ⚠️  교체 권장! 알람 레벨: {alarm_level}")
        
        if is_rapid_wear:
            print(f"  ⚠️  급격한 마모 감지! 마모율: {wear_rate:.2f}%/시간")
        
        previous_degradation = degradation_index
        
        # 교체 필요 시 시뮬레이션 종료
        if replacement_needed and alarm_level == "긴급":
            print("\n긴급 교체 필요! 시뮬레이션 종료.")
            break
    
    print("\n" + "=" * 60)
    print("시뮬레이션 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()


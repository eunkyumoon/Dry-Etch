# Y2O3 Focus Ring 마모도 예측 시스템 - 코드 가이드

## 📁 프로젝트 구조

```
Dry Etch/
├── src/
│   ├── __init__.py
│   ├── data_collector.py      # 데이터 수집 모듈
│   ├── wear_estimator.py       # 마모 상태 추정 모듈
│   ├── rul_predictor.py        # 잔존 수명 예측 모듈
│   ├── anomaly_detector.py     # 이상 탐지 모듈
│   └── main.py                 # 메인 실행 파일
├── requirements.txt            # 패키지 의존성
└── README_CODE.md             # 코드 가이드 (현재 파일)
```

## 🚀 설치 및 실행

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 실행

```bash
cd src
python main.py
```

## 📦 모듈 설명

### 1. DataCollector (`data_collector.py`)

RF 파라미터 및 OES 데이터 수집 기능

**주요 기능:**
- `collect_rf_parameters()`: RF 파라미터 수집
- `collect_oes_data()`: OES 데이터 수집
- 데이터 유효성 검증
- DataFrame 변환

**사용 예시:**
```python
from data_collector import DataCollector

collector = DataCollector()
collector.collect_rf_parameters(vpp=450.0, vdc=-200.0, phase=45.0, matcher_pos=0.5)
collector.collect_oes_data(yttrium_peak=0.85, fo_ratio=1.2)
```

### 2. WearEstimator (`wear_estimator.py`)

마모 진행도 계산 및 상태 분류

**주요 기능:**
- `calculate_degradation_index()`: 마모 진행도 (0~100%) 계산
- `estimate_remaining_thickness()`: 예상 잔여 두께 계산
- `get_wear_status()`: 마모 상태 분류 (정상/주의/위험/긴급)

**사용 예시:**
```python
from wear_estimator import WearEstimator

estimator = WearEstimator(initial_thickness=1000.0)
estimator.set_initial_state(vpp=450.0, yttrium_peak=0.85)
degradation = estimator.calculate_degradation_index(
    vpp=500.0, yttrium_peak=0.70, cumulative_rf_time=500.0
)
```

### 3. RULPredictor (`rul_predictor.py`)

잔존 수명 예측 (간단한 선형 회귀 모델)

**주요 기능:**
- `train()`: 모델 학습
- `predict()`: RUL 예측 (잔여 두께, RUL 시간, 신뢰 구간)

**사용 예시:**
```python
from rul_predictor import RULPredictor
import numpy as np

predictor = RULPredictor()
# 학습 데이터가 있으면 학습
# X = np.array([[vpp, vdc, phase, yttrium_peak, fo_ratio, cumulative_rf_time]])
# y = np.array([remaining_thickness])
# predictor.train(X, y)

# 예측
thickness, rul_hours, confidence_lower = predictor.predict(
    vpp=500.0, vdc=-210.0, phase=50.0,
    yttrium_peak=0.70, fo_ratio=1.2, cumulative_rf_time=500.0
)
```

### 4. AnomalyDetector (`anomaly_detector.py`)

이상 탐지 및 알람 기능

**주요 기능:**
- `detect_arcing_risk()`: Arcing 위험도 계산
- `detect_rapid_wear()`: 급격한 마모 탐지
- `check_replacement_threshold()`: 교체 임계값 확인

**사용 예시:**
```python
from anomaly_detector import AnomalyDetector

detector = AnomalyDetector()
arcing_risk, risk_level = detector.detect_arcing_risk(
    vpp=550.0, vdc=-250.0, phase=60.0,
    yttrium_peak=0.30, degradation_index=75.0
)

replacement_needed, alarm_level = detector.check_replacement_threshold(
    degradation_index=75.0, remaining_thickness=250.0,
    vpp=550.0, yttrium_peak=0.30
)
```

## 🔧 주요 기능

### 최소 기능 구현 목록

1. ✅ **데이터 수집** (F-001 ~ F-013)
   - RF 파라미터 수집 및 검증
   - OES 데이터 수집 및 검증

2. ✅ **마모 상태 추정** (F-026 ~ F-033)
   - Degradation Index 계산
   - 마모 상태 분류
   - 잔여 두께 예측

3. ✅ **RUL 예측** (F-034 ~ F-042)
   - 잔존 수명 예측
   - 신뢰 구간 계산

4. ✅ **이상 탐지** (F-043 ~ F-057)
   - Arcing 위험 탐지
   - 급격한 마모 탐지
   - 교체 임계값 확인

## 📊 시뮬레이션 실행

`main.py`를 실행하면 시간에 따른 마모 진행 시뮬레이션이 실행됩니다.

**출력 예시:**
```
[누적 시간: 500시간]
  Vpp: 495.0V | Yttrium Peak: 0.638
  마모 진행도: 25.0% (정상)
  예상 잔여 두께: 750.0μm
  예상 RUL: 7500시간
  Arcing 위험도: 15.0% (낮음)
```

## 🔄 확장 가능성

현재 구현은 최소 기능만 포함되어 있습니다. 다음 기능들을 추가할 수 있습니다:

1. **데이터베이스 연동**: 실제 장비 데이터 수집
2. **고급 모델**: 딥러닝 모델 적용
3. **대시보드**: 웹 기반 시각화
4. **알람 시스템**: 이메일/SMS 알람
5. **리포트 생성**: 자동 리포트 생성

## ⚠️ 주의사항

- 현재 구현은 시뮬레이션 데이터 기반입니다.
- 실제 운영 환경에서는 데이터베이스 연동 및 보안 고려 필요
- 모델 성능 향상을 위해 실제 데이터로 재학습 필요

## 📝 라이선스

본 프로젝트는 내부 사용 목적으로 제한됩니다.


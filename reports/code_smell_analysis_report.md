# Code Smell 분석 리포트

**프로젝트:** Y2O3 Focus Ring 마모도 예측 및 공정 로그 상관관계 분석  
**분석일:** 2024-12-19  
**분석 대상:** refactored/ 폴더의 모든 Python 파일

---

## 📊 분석 요약

리팩토링된 코드를 대상으로 Code Smell 분석을 수행했습니다. 총 **12개의 Code Smell**을 발견했습니다.

### 발견된 Code Smell 분류

| Code Smell 유형 | 발견 수 | 심각도 | 우선순위 |
|----------------|---------|--------|---------|
| Magic Numbers | 8 | 중간 | 높음 |
| Long Parameter List | 1 | 중간 | 높음 |
| Duplicate Code | 2 | 낮음 | 중간 |
| Dead Code | 1 | 낮음 | 낮음 |
| Primitive Obsession | 1 | 낮음 | 중간 |
| Feature Envy | 1 | 낮음 | 낮음 |

---

## 🔍 발견된 Code Smell 상세 분석

### 1. Magic Numbers (매직 넘버)

**심각도:** 중간  
**우선순위:** 높음  
**발견 위치:** 여러 파일

#### 문제점
하드코딩된 숫자 값들이 코드 전반에 산재되어 있어 의미를 파악하기 어렵고 유지보수가 어렵습니다.

#### 발견된 매직 넘버

| 파일 | 라인 | 매직 넘버 | 의미 추정 | 개선 방안 |
|------|------|----------|----------|----------|
| `main.py` | 42 | `2000` | 마모 진행도 계산 기준 시간 | Config로 이동 |
| `main.py` | 43 | `0.2` | Vpp 증가율 | Config로 이동 |
| `main.py` | 44 | `-200` | 초기 Vdc 값 | Config로 이동 |
| `main.py` | 44 | `0.1` | Vdc 증가율 | Config로 이동 |
| `main.py` | 45 | `45` | 초기 Phase 값 | Config로 이동 |
| `main.py` | 45 | `10` | Phase 증가량 | Config로 이동 |
| `main.py` | 46 | `0.5` | Yttrium Peak 감소율 | Config로 이동 |
| `main.py` | 49 | `1.2` | F/O Ratio 값 | Config로 이동 |
| `main.py` | 56 | `0.5` | Matcher Position 값 | Config로 이동 |
| `rul_predictor.py` | 86 | `0.9` | 신뢰 구간 하한 계수 | Config로 이동 |
| `rul_predictor.py` | 87 | `1.1` | 신뢰 구간 상한 계수 | Config로 이동 |
| `rul_predictor.py` | 132 | `0.4` | Vpp 가중치 | Config로 이동 |
| `rul_predictor.py` | 133 | `0.4` | Yttrium 가중치 | Config로 이동 |
| `rul_predictor.py` | 134 | `2000` | 시간 기반 마모 계산 기준 | Config로 이동 |
| `rul_predictor.py` | 134 | `0.2` | 시간 가중치 | Config로 이동 |
| `rul_predictor.py` | 141 | `0.9` | 신뢰 구간 하한 계수 | Config로 이동 |
| `rul_predictor.py` | 142 | `1.1` | 신뢰 구간 상한 계수 | Config로 이동 |
| `anomaly_detector.py` | 99 | `60` | 마모 진행도 주의 임계값 | Config로 이동 |
| `anomaly_detector.py` | 171 | `60` | 마모 진행도 주의 임계값 | Config로 이동 |

#### 개선 예시

```python
# 문제 코드 (main.py)
wear_progress = hour / 2000
current_vpp = Config.INITIAL_VPP * (1 + wear_progress * 0.2)
current_vdc = -200 * (1 + wear_progress * 0.1)

# 개선 후
wear_progress = hour / Config.WEAR_PROGRESS_BASE_HOURS
current_vpp = Config.INITIAL_VPP * (1 + wear_progress * Config.VPP_INCREASE_RATE)
current_vdc = Config.INITIAL_VDC * (1 + wear_progress * Config.VDC_INCREASE_RATE)
```

---

### 2. Long Parameter List (긴 매개변수 목록)

**심각도:** 중간  
**우선순위:** 높음  
**발견 위치:** `main.py` - `print_status()` 함수

#### 문제점
`print_status()` 함수가 11개의 매개변수를 받고 있어 가독성이 떨어지고 유지보수가 어렵습니다.

#### 현재 코드
```python
def print_status(
    hour: int,
    vpp: float,
    yttrium_peak: float,
    wear_state,
    rul_prediction,
    arcing_risk: float,
    risk_level: str,
    replacement_needed: bool,
    alarm_level: str,
    is_rapid_wear: bool,
    wear_rate: float,
):
```

#### 개선 방안
상태 정보를 담은 데이터 클래스를 생성하여 매개변수 수를 줄입니다.

```python
# 개선 후
@dataclass
class SystemStatus:
    """시스템 상태 정보"""
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

def print_status(status: SystemStatus):
    ...
```

---

### 3. Duplicate Code (중복 코드)

**심각도:** 낮음  
**우선순위:** 중간  
**발견 위치:** 여러 파일

#### 문제점 1: 신뢰 구간 계산 중복

**위치:** `rul_predictor.py`
- 라인 86-87: `predict()` 메서드
- 라인 141-142: `_heuristic_predict()` 메서드

```python
# 중복 코드
confidence_lower = predicted_thickness * 0.9
confidence_upper = predicted_thickness * 1.1
```

**개선 방안:**
```python
def _calculate_confidence_interval(self, predicted_thickness: float) -> Tuple[float, float]:
    """신뢰 구간 계산"""
    return (
        predicted_thickness * Config.CONFIDENCE_LOWER_FACTOR,
        predicted_thickness * Config.CONFIDENCE_UPPER_FACTOR
    )
```

#### 문제점 2: 위험도 계산 패턴 중복

**위치:** `anomaly_detector.py`
- `_calculate_vpp_risk()`, `_calculate_vdc_risk()`, `_calculate_yttrium_risk()` 등

**개선 방안:**
```python
def _calculate_threshold_risk(
    self, value: float, high_threshold: float, medium_threshold: float, weight: float
) -> float:
    """임계값 기반 위험도 계산 (템플릿 메서드)"""
    if value > high_threshold:
        return weight
    if value > medium_threshold:
        return weight / 2
    return 0.0
```

---

### 4. Dead Code (죽은 코드)

**심각도:** 낮음  
**우선순위:** 낮음  
**발견 위치:** `anomaly_detector.py`

#### 문제점
`AnomalyDetector` 클래스의 `__init__()` 메서드에서 초기화한 변수들이 사용되지 않습니다.

```python
def __init__(self):
    self.vpp_history: list[float] = []  # 사용되지 않음
    self.wear_rate_history: list[float] = []  # 사용되지 않음
```

**개선 방안:**
- 사용 계획이 있다면 주석 추가
- 사용 계획이 없다면 제거

---

### 5. Primitive Obsession (원시 타입 집착)

**심각도:** 낮음  
**우선순위:** 중간  
**발견 위치:** `main.py` - 시뮬레이션 로직

#### 문제점
시뮬레이션 파라미터들이 개별 변수로 관리되어 관련 데이터가 분산되어 있습니다.

```python
# 문제 코드
wear_progress = hour / 2000
current_vpp = Config.INITIAL_VPP * (1 + wear_progress * 0.2)
current_vdc = -200 * (1 + wear_progress * 0.1)
current_phase = 45 + wear_progress * 10
current_yttrium_peak = Config.INITIAL_YTTRIUM_PEAK * (1 - wear_progress * 0.5)
current_fo_ratio = 1.2
```

**개선 방안:**
```python
@dataclass
class SimulationParameters:
    """시뮬레이션 파라미터"""
    wear_progress: float
    vpp: float
    vdc: float
    phase: float
    yttrium_peak: float
    fo_ratio: float

def calculate_simulation_parameters(hour: int) -> SimulationParameters:
    """시뮬레이션 파라미터 계산"""
    wear_progress = hour / Config.WEAR_PROGRESS_BASE_HOURS
    return SimulationParameters(
        wear_progress=wear_progress,
        vpp=Config.INITIAL_VPP * (1 + wear_progress * Config.VPP_INCREASE_RATE),
        vdc=Config.INITIAL_VDC * (1 + wear_progress * Config.VDC_INCREASE_RATE),
        phase=Config.INITIAL_PHASE + wear_progress * Config.PHASE_INCREASE_RATE,
        yttrium_peak=Config.INITIAL_YTTRIUM_PEAK * (1 - wear_progress * Config.YTTRIUM_DECREASE_RATE),
        fo_ratio=Config.DEFAULT_FO_RATIO
    )
```

---

### 6. Feature Envy (기능 질투)

**심각도:** 낮음  
**우선순위:** 낮음  
**발견 위치:** `main.py` - `simulate_wear_progress()`

#### 문제점
`simulate_wear_progress()` 함수가 여러 객체의 메서드를 호출하여 복잡도가 높습니다.

**개선 방안:**
시뮬레이션 로직을 별도의 클래스로 분리:

```python
class WearSimulator:
    """마모 시뮬레이터 클래스"""
    
    def __init__(self, collector, wear_estimator, rul_predictor, anomaly_detector):
        self.collector = collector
        self.wear_estimator = wear_estimator
        self.rul_predictor = rul_predictor
        self.anomaly_detector = anomaly_detector
    
    def simulate(self, max_hours: int = 1200, interval: int = 100):
        """시뮬레이션 실행"""
        ...
```

---

## 📋 우선순위별 개선 계획

### 높은 우선순위 (즉시 수정)

#### 1. Magic Numbers 제거
- **예상 소요 시간:** 2시간
- **작업 내용:**
  - `config.py`에 매직 넘버 상수 추가
  - 모든 매직 넘버를 Config 상수로 교체
  - 주석 추가로 의미 명확화

#### 2. Long Parameter List 개선
- **예상 소요 시간:** 1시간
- **작업 내용:**
  - `SystemStatus` 데이터 클래스 생성
  - `print_status()` 함수 리팩토링

### 중간 우선순위 (단기 개선)

#### 3. Duplicate Code 제거
- **예상 소요 시간:** 1시간
- **작업 내용:**
  - 신뢰 구간 계산 메서드 추출
  - 위험도 계산 템플릿 메서드 생성

#### 4. Primitive Obsession 개선
- **예상 소요 시간:** 1시간
- **작업 내용:**
  - `SimulationParameters` 데이터 클래스 생성
  - 시뮬레이션 파라미터 계산 함수 생성

### 낮은 우선순위 (장기 개선)

#### 5. Dead Code 제거
- **예상 소요 시간:** 30분
- **작업 내용:**
  - 사용하지 않는 변수 제거 또는 주석 추가

#### 6. Feature Envy 개선
- **예상 소요 시간:** 2시간
- **작업 내용:**
  - `WearSimulator` 클래스 생성
  - 시뮬레이션 로직 캡슐화

---

## 🛠️ 개선 예시 코드

### 개선된 config.py (추가 필요)

```python
# config.py에 추가할 상수들

# 시뮬레이션 파라미터
WEAR_PROGRESS_BASE_HOURS: float = 2000.0
VPP_INCREASE_RATE: float = 0.2
INITIAL_VDC: float = -200.0
VDC_INCREASE_RATE: float = 0.1
INITIAL_PHASE: float = 45.0
PHASE_INCREASE_RATE: float = 10.0
YTTRIUM_DECREASE_RATE: float = 0.5
DEFAULT_FO_RATIO: float = 1.2
DEFAULT_MATCHER_POS: float = 0.5

# 신뢰 구간
CONFIDENCE_LOWER_FACTOR: float = 0.9
CONFIDENCE_UPPER_FACTOR: float = 1.1

# 휴리스틱 가중치
HEURISTIC_VPP_WEIGHT: float = 0.4
HEURISTIC_YTTRIUM_WEIGHT: float = 0.4
HEURISTIC_TIME_WEIGHT: float = 0.2
HEURISTIC_TIME_BASE: float = 2000.0

# 마모 진행도 임계값
DEGRADATION_CAUTION_THRESHOLD: float = 60.0
```

### 개선된 models.py (추가 필요)

```python
@dataclass
class SystemStatus:
    """시스템 상태 정보"""
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
    """시뮬레이션 파라미터"""
    wear_progress: float
    vpp: float
    vdc: float
    phase: float
    yttrium_peak: float
    fo_ratio: float
```

---

## 📊 개선 효과 예상

### 코드 품질
- **가독성**: 향상 (매직 넘버 제거, 명확한 상수명)
- **유지보수성**: 향상 (중복 코드 제거)
- **확장성**: 향상 (데이터 클래스 도입)

### 개발 생산성
- **버그 발견 용이성**: 향상
- **코드 재사용성**: 향상
- **테스트 용이성**: 향상

---

## ✅ 개선 체크리스트

### 높은 우선순위
- [ ] Magic Numbers 제거 (Config로 이동)
- [ ] Long Parameter List 개선 (SystemStatus 클래스)

### 중간 우선순위
- [ ] Duplicate Code 제거 (공통 메서드 추출)
- [ ] Primitive Obsession 개선 (SimulationParameters 클래스)

### 낮은 우선순위
- [ ] Dead Code 제거
- [ ] Feature Envy 개선 (WearSimulator 클래스)

---

## 🎯 결론

리팩토링된 코드에서도 일부 Code Smell이 발견되었습니다. 주요 개선 사항:

1. **Magic Numbers 제거**: 하드코딩된 값들을 Config로 이동
2. **Long Parameter List 개선**: 데이터 클래스 도입
3. **Duplicate Code 제거**: 공통 메서드 추출
4. **Primitive Obsession 개선**: 관련 데이터를 클래스로 그룹화

이러한 개선을 통해 코드의 가독성과 유지보수성을 더욱 향상시킬 수 있습니다.

---

**리포트 버전:** v1.0  
**작성일:** 2024-12-19  
**다음 분석 예정일:** Code Smell 개선 후


# Dry Etch 소모품(Y2O3 Ring) 예지보전 및 원가 절감 솔루션

## 📋 프로젝트 개요

### Role
- **설비 기술팀** 및 **AI 데이터 분석 파트**

### Goal
- Y2O3 Focus Ring의 교체 주기를 데이터 기반으로 **15% 이상 연장**
- 부품 마모로 인한 불량(Arcing, CD Uniformity 저하) 발생 전 교체 알람 적중률 **95% 달성**
- 연간 소모품 구매 비용 및 장비 다운타임(PM 횟수) 감축을 통한 **OPEX 최적화**

---

## 📥 입력 데이터 정의 (Input)

정확한 RUL 예측을 위해 실시간 공정 로그와 계측 데이터를 통합합니다.

### 분류 항목 (Feature)

| 항목 | 데이터 소스 |
|------|------------|
| **전기적 특성** | |
| - Vpp (Peak-to-Peak) | 장비 PLC 로그 |
| - Vdc (Bias) | 장비 PLC 로그 |
| - Impedance Phase | 장비 PLC 로그 |
| - Matcher Position | 장비 PLC 로그 |
| **화학적 특성** | |
| - OES Yttrium Peak | OES 센서 데이터 |
| - F/O Ratio | OES 센서 데이터 |
| **공정 부하** | |
| - 누적 RF On-time | 설비 이력 DB |
| - 누적 에너지 (Joule) | 설비 이력 DB |
| - Recipe Severity | 설비 이력 DB |

### 측정값 (Label)

- 부품 교체 시 잔여 코팅 두께 (μm)
- 소모품 중량 변화
- 데이터 소스: PM 계측 리포트

---

## 🎯 핵심 요구 기능 (Requirements)

### 3.1 마모 상태 실시간 추정 (State Estimation)

- 입력된 RF 파라미터와 OES 데이터를 분석하여 현재 Y2O3 코팅의 **마모 진행도(Degradation Index)**를 0~100% 사이의 지수로 산출
- 레시피별로 마모 속도가 다르므로, 가중치를 적용한 **누적 손상 모델(Cumulative Damage Model)** 적용

### 3.2 잔존 수명 예측 (RUL Prediction)

- 현재 마모 상태에서 해당 장비의 가동 스케줄을 고려하여, **교체 임계치까지 남은 시간(Remaining Hours)** 예측
- 예측값의 **신뢰 구간(Confidence Interval)**을 함께 제시하여 엔지니어의 판단 지원

### 3.3 이상 징후 조기 경보 (Anomaly Detection)

- RUL과 별개로, 부품 파손이나 급격한 마모로 인한 Vpp 급증 또는 아킹(Arcing) 징후 포착 시 즉시 Interlock 또는 알람 발생

---

## 📤 최종 출력 및 활용 (Output)

### 엔지니어 대시보드
- 챔버별 소모품 실시간 잔여 수명 시각화
- 교체 예정 리스트 제공

### 알람 시스템
- 교체 임계점 **24시간 전** 사전 알림 송출

### 비용 절감 레포트
- 기존 대비 연장된 수명 시간과 그에 따른 연간 절감 예상 비용 자동 산출

---

## ✅ 성공 지표 (Success Metrics)

| 지표 | 목표 |
|------|------|
| **Life Extension** | 기존 정기 교체 주기 대비 평균 사용 시간 **15% 증가** |
| **Accuracy** | 실제 측정된 잔여 두께와 AI 예측치 사이의 오차 **±5μm 이내** |
| **Stability** | 모델 도입 후 부품 마모로 인한 공정 사고(품질 불량) **0건 유지** |

---

## ⚠️ 제약 사항 및 리스크 (Constraints & Risk)

### 데이터 정합성
- 챔버별 센서 보정(Calibration) 상태에 따른 데이터 편차 존재 가능

### 레시피 가변성
- 신규 레시피 도입 시 학습 데이터 부족으로 초기 예측력이 떨어질 수 있음
- **해결 방안**: 전이 학습(Transfer Learning) 기법 필요

---

---

## 📄 PRD (Product Requirements Document)

이 문서는 엔지니어링 팀, 데이터 사이언스 팀, 그리고 경영진이 프로젝트의 방향성을 합의하는 기초 자료로 활용될 수 있습니다.

### [PRD] Dry Etch 소모품(Y2O3 Ring) 예지보전 및 원가 절감 솔루션

#### 1. 프로젝트 개요 (Role & Goal)

**Role:** 설비 기술팀 및 AI 데이터 분석 파트

**Goal:**
- Y2O3 Focus Ring의 교체 주기를 데이터 기반으로 15% 이상 연장.
- 부품 마모로 인한 불량(Arcing, CD Uniformity 저하) 발생 전 교체 알람 적중률 95% 달성.
- 연간 소모품 구매 비용 및 장비 다운타임(PM 횟수) 감축을 통한 OPEX 최적화.

#### 2. 입력 데이터 정의 (Input)

정확한 RUL 예측을 위해 실시간 공정 로그와 계측 데이터를 통합합니다.

**분류 항목 (Feature)**

| 항목 | 데이터 소스 |
|------|------------|
| **전기적 특성** | |
| Vpp(Peak-to-Peak), Vdc(Bias), Impedance Phase, Matcher Position | 장비 PLC 로그 |
| **화학적 특성** | |
| OES(Optical Emission Spectroscopy) Yttrium Peak, F/O Ratio | OES 센서 데이터 |
| **공정 부하** | |
| 누적 RF On-time, 누적 에너지(Joule), Recipe Severity | 설비 이력 DB |

**측정값 (Label)**
- 부품 교체 시 잔여 코팅 두께 ($\mu m$)
- 소모품 중량 변화
- 데이터 소스: PM 계측 리포트

#### 3. 핵심 요구 기능 (Requirements)

##### 3.1 마모 상태 실시간 추정 (State Estimation)

입력된 RF 파라미터와 OES 데이터를 분석하여 현재 Y2O3 코팅의 **마모 진행도(Degradation Index)**를 0~100% 사이의 지수로 산출해야 함.

레시피별로 마모 속도가 다르므로, 가중치를 적용한 **누적 손상 모델(Cumulative Damage Model)**을 적용함.

##### 3.2 잔존 수명 예측 (RUL Prediction)

현재 마모 상태에서 해당 장비의 가동 스케줄을 고려하여, **교체 임계치까지 남은 시간(Remaining Hours)**을 예측함.

예측값의 신뢰 구간(Confidence Interval)을 함께 제시하여 엔지니어의 판단을 도움.

##### 3.3 이상 징후 조기 경보 (Anomaly Detection)

RUL과 별개로, 부품 파손이나 급격한 마모로 인한 Vpp 급증 또는 아킹(Arcing) 징후 포착 시 즉시 Interlock 또는 알람을 발생시켜야 함.

#### 4. 최종 출력 및 활용 (Output)

**엔지니어 대시보드:** 챔버별 소모품 실시간 잔여 수명 시각화 및 교체 예정 리스트 제공.

**알람 시스템:** 교체 임계점 24시간 전 사전 알림 송출.

**비용 절감 레포트:** 기존 대비 연장된 수명 시간과 그에 따른 연간 절감 예상 비용 자동 산출.

#### 5. 성공 지표 (Success Metrics)

- **Life Extension:** 기존 정기 교체 주기 대비 평균 사용 시간 15% 증가.
- **Accuracy:** 실제 측정된 잔여 두께와 AI 예측치 사이의 오차 $\pm 5\mu m$ 이내.
- **Stability:** 모델 도입 후 부품 마모로 인한 공정 사고(품질 불량) 0건 유지.

#### 6. 제약 사항 및 리스크 (Constraints & Risk)

**데이터 정합성:** 챔버별 센서 보정(Calibration) 상태에 따른 데이터 편차 존재 가능.

**레시피 가변성:** 신규 레시피 도입 시 학습 데이터 부족으로 초기 예측력이 떨어질 수 있음 (전이 학습 기법 필요).

---

## 🔧 리팩토링 TODO 목록

코드 품질 개선 및 유지보수를 위한 리팩토링 작업 목록입니다.

### 코드 구조 개선
- [ ] 모듈 간 의존성 최소화 및 인터페이스 정의
- [ ] 설정 파일 분리 (config.py 또는 YAML 파일)
- [ ] 로깅 시스템 통합 (Python logging 모듈)
- [ ] 예외 처리 강화 및 커스텀 예외 클래스 정의
- [ ] 타입 힌팅 추가 (Type Hints)

### 데이터 처리 개선
- [ ] 데이터베이스 연동 모듈 추가 (실제 장비 데이터 수집)
- [ ] 데이터 검증 로직 강화
- [ ] 데이터 캐싱 메커니즘 구현
- [ ] 배치 처리 기능 추가
- [ ] 데이터 품질 모니터링 기능 추가

### 모델 개선
- [ ] 실제 데이터 기반 모델 학습 파이프라인 구축
- [ ] 모델 버전 관리 시스템 구현
- [ ] 모델 성능 모니터링 및 자동 재학습 기능
- [ ] 신뢰 구간 계산 개선 (불확실성 정량화)
- [ ] 앙상블 모델 적용 검토
- [ ] 딥러닝 모델 (LSTM, Transformer) 적용 검토

### 성능 최적화
- [ ] 대용량 데이터 처리 최적화
- [ ] 병렬 처리 구현 (멀티프로세싱/멀티스레딩)
- [ ] 메모리 사용량 최적화
- [ ] API 응답 시간 개선
- [ ] 데이터베이스 쿼리 최적화

### 테스트 및 품질 관리
- [ ] 단위 테스트 작성 (pytest)
- [ ] 통합 테스트 작성
- [ ] 성능 테스트 작성
- [ ] 코드 커버리지 80% 이상 달성
- [ ] 정적 코드 분석 도구 적용 (pylint, mypy)

### 문서화 개선
- [ ] API 문서 자동 생성 (Sphinx 또는 docstring)
- [ ] 사용자 가이드 작성
- [ ] 개발자 가이드 작성
- [ ] 코드 주석 보완
- [ ] 아키텍처 다이어그램 작성

### 보안 및 안정성
- [ ] 입력 데이터 검증 및 Sanitization
- [ ] SQL Injection 방지 (파라미터화된 쿼리)
- [ ] 인증 및 권한 관리 시스템 구현
- [ ] 로그 보안 강화 (민감 정보 마스킹)
- [ ] 에러 메시지 보안 강화

### 사용자 경험 개선
- [ ] 웹 대시보드 개발 (Flask/FastAPI + React)
- [ ] 실시간 알람 시스템 구현 (WebSocket)
- [ ] 리포트 자동 생성 및 이메일 전송
- [ ] 모바일 알림 기능 추가
- [ ] 다국어 지원 (한국어/영어)

### 운영 환경 대응
- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인 구축 (GitHub Actions)
- [ ] 환경 변수 관리 (.env 파일)
- [ ] 모니터링 및 알람 시스템 통합 (Prometheus, Grafana)
- [ ] 로그 집계 시스템 구축 (ELK Stack)

### 코드 품질 개선
- [ ] 코드 스타일 통일 (Black, isort)
- [ ] 중복 코드 제거 (DRY 원칙)
- [ ] 매직 넘버 상수화
- [ ] 긴 함수 분리 및 리팩토링
- [ ] 클래스 책임 분리 (SRP)

### 확장성 개선
- [ ] 플러그인 아키텍처 도입
- [ ] 다른 소모품 타입 지원 확장
- [ ] 다른 공정 타입 지원 확장
- [ ] 마이크로서비스 아키텍처 검토
- [ ] API 버전 관리

---

## 🚀 프로젝트 실행 방법

### 사전 요구사항

- Python 3.8 이상
- pip 패키지 관리자

### 1. 저장소 클론

```bash
git clone https://github.com/eunkyumoon/Dry-Etch.git
cd Dry-Etch
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

필요한 패키지:
- `numpy>=1.21.0`
- `pandas>=1.3.0`
- `scikit-learn>=1.0.0`
- `matplotlib>=3.4.0`
- `seaborn>=0.11.0`
- `streamlit>=1.28.0`
- `plotly>=5.17.0`

### 3. 실행 방법

#### 방법 1: 웹 대시보드 실행 (권장)

실시간 모니터링 대시보드를 실행합니다:

```bash
streamlit run dashboard.py
```

브라우저에서 자동으로 열리며, `http://localhost:8501`에서 접속 가능합니다.

**대시보드 기능:**
- 중앙 네트워크 시각화 (챔버 상태)
- 좌측 패널: RF 파라미터 모니터링, 마모 상태 분석, RUL 예측
- 우측 패널: 설비 운영 모니터링, 위험 모니터링, 교체 알람
- 하단 패널: 시간 시리즈 차트

**사이드바 설정:**
- 챔버 선택 (Chamber1-4)
- 누적 시간 슬라이더 (0-2000시간)
- 자동 새로고침 옵션

자세한 내용은 [DASHBOARD_README.md](DASHBOARD_README.md)를 참조하세요.

#### 방법 2: 콘솔 기반 실행

시뮬레이션을 콘솔에서 실행합니다:

```bash
python -m refactored.main
```

또는

```bash
cd refactored
python main.py
```

**실행 결과:**
- 시간별 마모 진행도 시뮬레이션
- RF 파라미터 변화 추이
- 마모 상태 및 RUL 예측 결과
- 이상 탐지 결과

자세한 내용은 [refactored/README.md](refactored/README.md)를 참조하세요.

### 4. 프로젝트 구조

```
Dry-Etch/
├── dashboard.py              # 웹 대시보드 메인 파일
├── requirements.txt          # 패키지 의존성
├── README.md                 # 프로젝트 개요 및 실행 방법
├── DASHBOARD_README.md       # 대시보드 사용 가이드
├── refactored/               # 리팩토링된 코드
│   ├── __init__.py
│   ├── config.py             # 설정 파일
│   ├── models.py             # 데이터 모델
│   ├── data_collector.py    # 데이터 수집
│   ├── wear_estimator.py     # 마모 상태 추정
│   ├── rul_predictor.py      # RUL 예측
│   ├── anomaly_detector.py  # 이상 탐지
│   └── main.py              # 메인 실행 파일
├── src/                      # 초기 구현 코드
├── reports/                  # 프로젝트 리포트
├── prompting/                # AI 프롬프트 템플릿
└── test_cases/              # 테스트 케이스
```

### 5. 문제 해결

#### 대시보드가 열리지 않는 경우

1. **포트 충돌**: 다른 포트 사용
   ```bash
   streamlit run dashboard.py --server.port 8502
   ```

2. **모듈을 찾을 수 없는 경우**: 
   - `refactored/` 폴더가 같은 디렉토리에 있는지 확인
   - Python 경로 확인

3. **패키지 설치 오류**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

#### 콘솔 실행 오류

1. **모듈 import 오류**: 프로젝트 루트에서 실행 확인
2. **데이터 오류**: `refactored/config.py`의 설정값 확인

### 6. 추가 리소스

- **대시보드 가이드**: [DASHBOARD_README.md](DASHBOARD_README.md)
- **코드 가이드**: [refactored/README.md](refactored/README.md)
- **테스트 케이스**: [test_cases/README.md](test_cases/README.md)
- **프로젝트 리포트**: [reports/README.md](reports/README.md)

---

## 👥 담당 팀

- **설비 기술팀**
- **AI 데이터 분석 파트**

---

## 📝 라이선스

본 프로젝트는 내부 사용 목적으로 제한됩니다.


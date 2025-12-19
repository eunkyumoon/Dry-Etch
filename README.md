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

## 👥 담당 팀

- **설비 기술팀**
- **AI 데이터 분석 파트**

---

## 📝 라이선스

본 프로젝트는 내부 사용 목적으로 제한됩니다.


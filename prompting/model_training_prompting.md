# 모델 학습 프롬프트

## 목적
Y2O3 Focus Ring의 RUL 예측 모델 학습을 위한 프롬프트 템플릿입니다.

---

## 프롬프트 템플릿

### 모델 학습 가이드 프롬프트

```
당신은 시계열 예측 모델 개발 전문가입니다.

Y2O3 Focus Ring의 잔존 수명(RUL) 예측 모델을 개발하기 위한 학습 가이드를 제공해주세요.

**프로젝트 목표:**
- 목표: Y2O3 Focus Ring의 교체 주기를 데이터 기반으로 15% 이상 연장
- 정확도 목표: 실제 측정된 잔여 두께와 AI 예측치 사이의 오차 ±5μm 이내
- 알람 적중률 목표: 95% 이상

**입력 특성:**
1. 전기적 특성: Vpp, Vdc, Impedance Phase, Matcher Position
2. 화학적 특성: OES Yttrium Peak, F/O Ratio
3. 공정 부하: 누적 RF On-time, 누적 에너지(Joule), Recipe Severity

**출력:**
- 잔존 수명 (RUL): 시간 단위
- 마모 진행도 (Degradation Index): 0~100%
- 신뢰 구간: 95% Confidence Interval

**제약사항:**
- 챔버별 센서 보정 상태에 따른 데이터 편차 존재
- 신규 레시피 도입 시 학습 데이터 부족 가능성

**요청사항:**
1. 적합한 모델 아키텍처 제안 (LSTM, GRU, Transformer 등)
2. 데이터 전처리 방법 제안
3. 특성 엔지니어링 방안
4. 하이퍼파라미터 튜닝 가이드
5. 교차 검증 전략
6. 전이 학습 전략 (신규 레시피 대응)
```

---

### 데이터 전처리 프롬프트

```
당신은 머신러닝 데이터 전처리 전문가입니다.

Y2O3 Focus Ring RUL 예측을 위한 데이터 전처리 방법을 제안해주세요.

**데이터 특성:**
- 데이터 타입: 시계열 데이터 (시간별 측정값)
- 특성 수: 9개 (Vpp, Vdc, Impedance Phase, Matcher Position, OES Yttrium Peak, F/O Ratio, 누적 RF On-time, 누적 에너지, Recipe Severity)
- 레이블: 잔여 코팅 두께 (μm), 소모품 중량 변화
- 데이터 소스: 장비 PLC 로그, OES 센서 데이터, 설비 이력 DB, PM 계측 리포트

**데이터 이슈:**
- 챔버별 센서 보정 상태 차이로 인한 데이터 편차
- 결측값 존재 가능성
- 노이즈 포함 가능성
- 레시피별 마모 속도 차이

**요청사항:**
1. 결측값 처리 방법
2. 이상치 탐지 및 처리 방법
3. 정규화/표준화 방법 (챔버별 보정 고려)
4. 시계열 데이터 윈도우링 방법
5. 레시피 인코딩 방법
6. 데이터 증강 방법
```

---

### 특성 엔지니어링 프롬프트

```
당신은 특성 엔지니어링 전문가입니다.

Y2O3 Focus Ring 마모 예측을 위한 효과적인 특성을 생성해주세요.

**기존 특성:**
- Vpp (Peak-to-Peak Voltage)
- Vdc (Bias Voltage)
- Impedance Phase
- Matcher Position
- OES Yttrium Peak
- F/O Ratio
- 누적 RF On-time
- 누적 에너지 (Joule)
- Recipe Severity

**도메인 지식:**
- Vpp 증가는 마모 진행을 나타낼 수 있음
- OES Yttrium Peak 감소는 코팅 두께 감소를 의미
- 레시피별로 마모 속도가 다름 (누적 손상 모델 필요)
- RF On-time과 에너지가 누적되면서 마모 진행

**요청사항:**
1. 파생 특성 생성 방안 (예: Vpp 변화율, 마모율 등)
2. 상호작용 특성 생성 방안
3. 시간 기반 특성 생성 방안
4. 레시피별 가중치 적용 방법
5. 특성 중요도 분석 방법
```

---

### 모델 아키텍처 설계 프롬프트

```
당신은 딥러닝 모델 아키텍처 설계 전문가입니다.

Y2O3 Focus Ring RUL 예측을 위한 최적의 모델 아키텍처를 설계해주세요.

**요구사항:**
- 입력: 시계열 데이터 (시간별 9개 특성)
- 출력: RUL (시간), Degradation Index (0~100%), 신뢰 구간
- 정확도 목표: ±5μm 이내
- 실시간 추론 필요

**제약사항:**
- 학습 데이터: 제한적 (XX,XXX건)
- 레시피 가변성: 신규 레시피 대응 필요
- 챔버별 차이: 일반화 필요

**요청사항:**
1. 모델 타입 제안 (LSTM, GRU, Transformer, CNN-LSTM 등)
2. 레이어 구조 설계
3. Attention 메커니즘 적용 여부
4. Multi-task Learning 적용 여부 (RUL + Degradation Index 동시 예측)
5. 불확실성 정량화 방법 (신뢰 구간 계산)
6. 모델 경량화 방안
```

---

### 하이퍼파라미터 튜닝 프롬프트

```
당신은 하이퍼파라미터 최적화 전문가입니다.

Y2O3 Focus Ring RUL 예측 모델의 하이퍼파라미터를 최적화해주세요.

**모델 타입:** [LSTM / GRU / Transformer]

**튜닝 대상 하이퍼파라미터:**
- Learning Rate
- Batch Size
- Hidden Units
- Number of Layers
- Dropout Rate
- Sequence Length
- Optimizer (Adam, RMSprop 등)
- Learning Rate Schedule

**검증 방법:**
- 교차 검증: K-Fold (K=5)
- 평가 지표: MAE, RMSE, MAPE, R²

**요청사항:**
1. 하이퍼파라미터 탐색 범위 제안
2. 탐색 방법 제안 (Grid Search, Random Search, Bayesian Optimization)
3. 조기 종료(Early Stopping) 전략
4. 학습 곡선 모니터링 방법
5. 최적 하이퍼파라미터 조합 제안
```

---

### 전이 학습 프롬프트

```
당신은 전이 학습(Transfer Learning) 전문가입니다.

신규 레시피 도입 시 학습 데이터 부족 문제를 해결하기 위한 전이 학습 전략을 제안해주세요.

**상황:**
- 기존 레시피: Recipe A, B, C (충분한 학습 데이터 보유)
- 신규 레시피: Recipe D (학습 데이터 부족, XX건만 보유)
- 목표: 신규 레시피에서도 정확한 RUL 예측

**기존 모델:**
- 학습 완료된 모델 존재
- 기존 레시피에서 ±5μm 정확도 달성

**요청사항:**
1. 전이 학습 전략 제안 (Fine-tuning, Feature Extraction 등)
2. 레시피 간 유사도 측정 방법
3. 소량 데이터로 학습하는 방법 (Few-shot Learning)
4. 도메인 적응(Domain Adaptation) 방법
5. 앙상블 방법 (기존 모델 + 신규 모델)
```

---

### 모델 평가 프롬프트

```
당신은 머신러닝 모델 평가 전문가입니다.

Y2O3 Focus Ring RUL 예측 모델의 성능을 종합적으로 평가해주세요.

**평가 데이터:**
- 테스트 데이터: X,XXX건
- 챔버별 분포: Chamber 1~4
- 레시피별 분포: Recipe A, B, C

**평가 지표:**
- MAE (Mean Absolute Error)
- RMSE (Root Mean Square Error)
- MAPE (Mean Absolute Percentage Error)
- R² Score
- 신뢰 구간 정확도

**요청사항:**
1. 전체 성능 평가
2. 챔버별 성능 분석
3. 레시피별 성능 분석
4. 오류 케이스 분석 (과대 예측, 과소 예측)
5. 모델 한계점 식별
6. 개선 방안 제안
```

---

## 사용 가이드

### 단계별 활용 방법

1. **데이터 수집 단계**: 데이터 전처리 프롬프트 사용
2. **특성 설계 단계**: 특성 엔지니어링 프롬프트 사용
3. **모델 설계 단계**: 모델 아키텍처 설계 프롬프트 사용
4. **모델 학습 단계**: 하이퍼파라미터 튜닝 프롬프트 사용
5. **모델 평가 단계**: 모델 평가 프롬프트 사용
6. **신규 레시피 대응**: 전이 학습 프롬프트 사용

---

## 주의사항

1. **도메인 지식 반영**: Dry Etch 공정의 특성을 반영한 프롬프트 작성
2. **실용성 고려**: 실제 운영 환경에서 사용 가능한 모델 설계
3. **확장성 고려**: 신규 레시피, 챔버 추가 시 대응 가능한 구조
4. **해석 가능성**: 모델의 예측 결과를 엔지니어가 이해할 수 있어야 함


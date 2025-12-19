# 이상 탐지 프롬프트

## 목적
Y2O3 Focus Ring의 이상 징후를 조기 탐지하고 분석하기 위한 프롬프트 템플릿입니다.

---

## 프롬프트 템플릿

### 실시간 이상 탐지 프롬프트

```
당신은 설비 이상 탐지 전문가입니다.

다음 실시간 데이터를 분석하여 Y2O3 Focus Ring의 이상 징후를 탐지해주세요.

**입력 데이터:**
- 챔버: {chamber_id}
- 시간: {timestamp}
- RF 파라미터:
  - Vpp: {vpp}V (이전 평균: {vpp_avg}V)
  - Vdc: {vdc}V (이전 평균: {vdc_avg}V)
  - Impedance Phase: {phase}° (이전 평균: {phase_avg}°)
- OES 데이터:
  - Yttrium Peak: {yttrium_peak} (이전 평균: {yttrium_avg})
  - F/O Ratio: {fo_ratio} (이전 평균: {fo_avg})
- 마모 진행도: {degradation}% (1시간 전: {degradation_prev}%)

**임계값:**
- Vpp 급증 임계값: {vpp_threshold}% 증가
- 마모율 급증 임계값: {wear_rate_threshold}%/시간
- Arcing 위험 임계값: {arcing_threshold}

**요청사항:**
1. 이상 징후 여부 판단 (정상 / 주의 / 위험 / 긴급)
2. 이상 유형 분류 (Arcing 위험, 급격한 마모, 센서 오류 등)
3. 이상 심각도 평가 (1~5점)
4. 즉시 조치 필요 여부
5. 권장 조치 사항
6. 알람 발생 여부 결정

**출력 형식:**
- 이상 여부: [정상/주의/위험/긴급]
- 이상 유형: [유형명]
- 심각도: [1~5점]
- 이상 지표:
  - Vpp 변화율: {vpp_change}%
  - 마모율: {wear_rate}%/시간
  - Arcing 위험도: {arcing_risk}%
- 조치 필요: [예/아니오]
- 권장 조치: [조치 내용]
- 알람 발생: [예/아니오] - [알람 레벨]
```

---

### Arcing 위험 탐지 프롬프트

```
당신은 Dry Etch 공정의 Arcing 현상 전문가입니다.

다음 데이터를 분석하여 Arcing 발생 위험을 평가해주세요.

**입력 데이터:**
- Vpp: {vpp}V (정상 범위: {vpp_normal_min}~{vpp_normal_max}V)
- Vdc: {vdc}V
- Impedance Phase: {phase}°
- Matcher Position: {matcher_pos}
- OES Yttrium Peak: {yttrium_peak} (정상 범위: {yttrium_normal_min}~{yttrium_normal_max})
- 현재 마모 진행도: {degradation}%
- 최근 Vpp 변동성: {vpp_volatility}

**Arcing 발생 이력:**
- 과거 Arcing 발생 시 Vpp: {historical_arcing_vpp}V
- 과거 Arcing 발생 시 마모 진행도: {historical_arcing_degradation}%

**요청사항:**
1. Arcing 발생 위험도 평가 (0~100%)
2. 위험 요인 식별 (Vpp 급증, 마모 진행도, Impedance 불안정 등)
3. Arcing 발생 가능 시간 예측
4. 예방 조치 제안
5. Interlock 작동 필요 여부

**출력 형식:**
- Arcing 위험도: {risk_score}% (0~100%)
- 위험 등급: [낮음/보통/높음/매우높음]
- 주요 위험 요인:
  1. {risk_factor_1}: {contribution}%
  2. {risk_factor_2}: {contribution}%
  3. {risk_factor_3}: {contribution}%
- 예상 발생 시간: {estimated_time}시간 후 (신뢰도: {confidence}%)
- 예방 조치: [조치 1], [조치 2]
- Interlock 필요: [예/아니오]
```

---

### 급격한 마모 탐지 프롬프트

```
당신은 부품 마모 분석 전문가입니다.

다음 데이터를 분석하여 Y2O3 Focus Ring의 급격한 마모를 탐지해주세요.

**입력 데이터:**
- 시간 범위: {start_time} ~ {end_time} (기간: {duration}시간)
- 마모 진행도 변화: {degradation_start}% → {degradation_end}%
- 평균 마모율: {wear_rate}%/시간 (정상 범위: {normal_wear_rate_min}~{normal_wear_rate_max}%/시간)
- 레시피: {recipe_name}
- 누적 RF On-time: {cumulative_rf_time}시간
- 누적 에너지: {cumulative_energy}J

**이전 마모 패턴:**
- 이전 기간 평균 마모율: {previous_wear_rate}%/시간
- 레시피별 평균 마모율: {recipe_wear_rate}%/시간

**요청사항:**
1. 급격한 마모 여부 판단
2. 마모 가속화 원인 분석 (레시피 변경, 공정 조건 변화, 부품 결함 등)
3. 예상 교체 시점 재계산
4. 긴급 교체 필요 여부
5. 원인별 대응 방안

**출력 형식:**
- 급격한 마모 여부: [예/아니오]
- 마모율 증가율: {increase_rate}% (정상 대비)
- 원인 분석:
  - 레시피 영향: {recipe_contribution}%
  - 공정 조건 영향: {process_contribution}%
  - 부품 결함 가능성: {defect_probability}%
- 예상 교체 시점: {estimated_replacement_time} (기존 예측: {previous_estimate})
- 긴급 교체 필요: [예/아니오]
- 대응 방안: [방안 1], [방안 2]
```

---

### 센서 이상 탐지 프롬프트

```
당신은 센서 데이터 검증 전문가입니다.

다음 센서 데이터를 분석하여 센서 이상을 탐지해주세요.

**입력 데이터:**
- 챔버: {chamber_id}
- 센서 타입: {sensor_type} (RF / OES)
- 현재 측정값: {current_value}
- 이전 측정값: {previous_value}
- 평균값 (최근 24시간): {avg_24h}
- 표준편차 (최근 24시간): {std_24h}
- 측정 시간: {timestamp}

**정상 범위:**
- 최소값: {min_normal}
- 최대값: {max_normal}
- 평균값: {mean_normal}
- 표준편차: {std_normal}

**요청사항:**
1. 센서 이상 여부 판단 (정상 / 노이즈 / 드리프트 / 고장)
2. 이상 유형 분류
3. 데이터 신뢰도 평가 (0~100%)
4. 데이터 보정 필요 여부
5. 대체 데이터 소스 제안

**출력 형식:**
- 센서 상태: [정상/노이즈/드리프트/고장]
- 이상 유형: [유형명]
- 데이터 신뢰도: {reliability}%
- 이상 지표:
  - 정상 범위 이탈: {deviation}%
  - 노이즈 레벨: {noise_level}
  - 드리프트 정도: {drift_amount}
- 보정 필요: [예/아니오]
- 보정값: {calibrated_value}
- 대체 데이터 소스: [소스명]
```

---

### 패턴 이상 탐지 프롬프트

```
당신은 시계열 패턴 분석 전문가입니다.

다음 시계열 데이터를 분석하여 이상 패턴을 탐지해주세요.

**입력 데이터:**
- 시간 범위: {start_date} ~ {end_date}
- 데이터 포인트 수: {data_points}개
- 측정 간격: {interval}시간
- 분석 대상 특성: {feature_name}

**시계열 데이터:**
{time_series_data}

**정상 패턴:**
- 정상 추세: {normal_trend} (선형 증가/감소, 지수 증가/감소 등)
- 정상 변동성: {normal_volatility}
- 계절성 패턴: {seasonal_pattern}

**요청사항:**
1. 이상 패턴 탐지 (급격한 변화, 주기 이상, 추세 변화 등)
2. 이상 구간 식별
3. 이상 패턴 유형 분류
4. 원인 추정
5. 영향도 평가

**출력 형식:**
- 이상 패턴 여부: [예/아니오]
- 이상 패턴 유형: [유형명]
- 이상 구간:
  - 시작: {anomaly_start}
  - 종료: {anomaly_end}
  - 지속 시간: {duration}시간
- 이상 정도: {severity} (1~5점)
- 원인 추정: [원인 1], [원인 2]
- 영향도: [높음/중간/낮음]
- 권장 조치: [조치 내용]
```

---

### 종합 이상 분석 프롬프트

```
당신은 설비 진단 전문가입니다.

다음 종합 데이터를 분석하여 Y2O3 Focus Ring의 전반적인 상태를 평가하고 이상을 탐지해주세요.

**입력 데이터:**
- 챔버: {chamber_id}
- 분석 시간: {timestamp}
- RF 파라미터: Vpp={vpp}V, Vdc={vdc}V, Phase={phase}°
- OES 데이터: Yttrium={yttrium}, F/O={fo_ratio}
- 마모 진행도: {degradation}%
- 최근 마모율: {wear_rate}%/시간
- 레시피: {recipe_name}
- 누적 사용 시간: {cumulative_time}시간

**이전 상태 (1주일 전):**
- 마모 진행도: {degradation_week_ago}%
- 평균 Vpp: {vpp_week_ago}V
- 평균 마모율: {wear_rate_week_ago}%/시간

**요청사항:**
1. 전반적인 상태 평가 (양호 / 주의 / 위험)
2. 이상 징후 종합 분석
3. 각 이상 징후의 심각도 및 우선순위
4. 종합 위험도 평가
5. 즉시 조치 필요 항목
6. 예방 조치 제안

**출력 형식:**
- 종합 상태: [양호/주의/위험/긴급]
- 종합 위험도: {overall_risk}% (0~100%)
- 이상 징후 목록:
  1. {anomaly_1}: 심각도 {severity_1}/5, 우선순위 {priority_1}
  2. {anomaly_2}: 심각도 {severity_2}/5, 우선순위 {priority_2}
- 즉시 조치 필요: [항목 1], [항목 2]
- 예방 조치: [조치 1], [조치 2]
- 다음 점검 시점: {next_check_time}
```

---

## 사용 예시

### 예시 1: 실시간 이상 탐지

```python
prompt = f"""
당신은 설비 이상 탐지 전문가입니다.

다음 실시간 데이터를 분석하여 Y2O3 Focus Ring의 이상 징후를 탐지해주세요.

**입력 데이터:**
- 챔버: Chamber 1
- 시간: 2024-12-19 10:30:00
- RF 파라미터:
  - Vpp: 520V (이전 평균: 450V)
  - Vdc: -210V (이전 평균: -200V)
  - Impedance Phase: 50° (이전 평균: 45°)
- OES 데이터:
  - Yttrium Peak: 0.72 (이전 평균: 0.85)
  - F/O Ratio: 1.3 (이전 평균: 1.2)
- 마모 진행도: 72% (1시간 전: 65%)

**임계값:**
- Vpp 급증 임계값: 10% 증가
- 마모율 급증 임계값: 5%/시간
- Arcing 위험 임계값: 70%

[나머지 프롬프트...]
"""
```

---

## 이상 탐지 체크리스트

### 실시간 모니터링 항목
- [ ] Vpp 급증 (10% 이상 증가)
- [ ] 마모율 급증 (5%/시간 이상)
- [ ] OES Yttrium Peak 급감 (20% 이상 감소)
- [ ] Impedance Phase 불안정 (±10° 이상 변동)
- [ ] Arcing 위험도 증가 (70% 이상)

### 주기적 점검 항목
- [ ] 마모 패턴 이상 (예상과 다른 추세)
- [ ] 레시피별 마모율 이상 (평균 대비 2σ 이상)
- [ ] 센서 데이터 이상 (드리프트, 노이즈)
- [ ] 챔버별 편차 이상 (다른 챔버 대비 20% 이상 차이)

---

## 주의사항

1. **False Positive 최소화**: 알람 피로도를 줄이기 위해 임계값 조정 필요
2. **컨텍스트 고려**: 레시피 변경, PM 후 등 정상적인 변화와 구분
3. **다중 신호 확인**: 단일 지표가 아닌 여러 지표 종합 분석
4. **역사적 패턴 비교**: 과거 데이터와 비교하여 이상 여부 판단
5. **도메인 지식 반영**: Dry Etch 공정의 특성을 고려한 판단


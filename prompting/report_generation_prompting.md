# 리포트 생성 프롬프트

## 목적
Y2O3 Focus Ring 예지보전 프로젝트의 다양한 리포트를 자동 생성하기 위한 프롬프트 템플릿입니다.

---

## 프롬프트 템플릿

### 프로젝트 진행 리포트 생성 프롬프트

```
당신은 프로젝트 관리 전문가입니다.

다음 정보를 바탕으로 프로젝트 진행 리포트를 작성해주세요.

**프로젝트 정보:**
- 프로젝트명: Dry Etch 소모품(Y2O3 Ring) 예지보전 및 원가 절감 솔루션
- 보고 기간: {start_date} ~ {end_date}
- 작성자: {author_name}

**프로젝트 현황:**
- 진행 단계: {current_stage}
- 진행률: {progress}%
- 목표 달성도: {goal_achievement}%

**주요 성과:**
{achievements_list}

**세부 진행 상황:**
- 데이터 수집: {data_collection_status}
- 모델 개발: {model_development_status}
- 시스템 통합: {system_integration_status}

**성공 지표 달성 현황:**
- Life Extension: 목표 15%, 현재 {current_life_extension}%
- Accuracy: 목표 ±5μm, 현재 ±{current_accuracy}μm
- Stability: 목표 0건, 현재 {current_stability}건

**비용 절감 현황:**
- 소모품 구매 비용 절감: {cost_savings_amount}원
- 장비 다운타임 감소: {downtime_reduction}시간

**요청사항:**
1. 명확하고 구조화된 리포트 작성
2. 데이터 기반 인사이트 제공
3. 시각화가 필요한 부분 명시
4. 다음 단계 계획 수립
5. 리스크 및 이슈 명확히 기술
```

---

### 비용 절감 리포트 생성 프롬프트

```
당신은 재무 분석 전문가입니다.

다음 데이터를 바탕으로 비용 절감 리포트를 작성해주세요.

**보고 기간:** {start_date} ~ {end_date}

**소모품 구매 비용:**
- 기존 연간 구매 비용: {original_cost}원
- 현재 연간 구매 비용: {current_cost}원
- 절감액: {savings_amount}원
- 절감률: {savings_rate}%

**교체 주기:**
- 기존 평균 교체 주기: {original_cycle}시간
- 현재 평균 교체 주기: {current_cycle}시간
- 연장률: {extension_rate}%

**장비 다운타임:**
- 기존 PM 횟수: {original_pm_count}회/년
- 현재 PM 횟수: {current_pm_count}회/년
- 감소율: {reduction_rate}%
- 시간당 생산 손실 비용: {cost_per_hour}원/시간
- 다운타임 절감 비용: {downtime_savings}원

**품질 불량 비용:**
- 기존 Arcing 발생: {original_arcing}건
- 현재 Arcing 발생: {current_arcing}건
- 기존 CD Uniformity 불량: {original_cd}건
- 현재 CD Uniformity 불량: {current_cd}건
- 불량 비용 절감: {quality_savings}원

**요청사항:**
1. 총 절감액 계산 및 ROI 산출
2. 월별/분기별 추이 분석
3. 챔버별 절감 현황 분석
4. 목표 대비 달성률 평가
5. 추가 개선 기회 제시
6. 시각화가 필요한 차트 및 그래프 명시
```

---

### 모델 성능 평가 리포트 생성 프롬프트

```
당신은 머신러닝 모델 평가 전문가입니다.

다음 모델 성능 데이터를 바탕으로 평가 리포트를 작성해주세요.

**모델 정보:**
- 모델명: {model_name}
- 모델 버전: {model_version}
- 평가 기간: {start_date} ~ {end_date}
- 평가 데이터량: {test_data_count}건

**성능 지표:**
- MAE: {mae}μm (목표: ±5μm)
- RMSE: {rmse}μm
- MAPE: {mape}%
- R² Score: {r2_score}

**챔버별 성능:**
{chamber_performance_table}

**레시피별 성능:**
{recipe_performance_table}

**이상 탐지 성능:**
- Precision: {precision}%
- Recall: {recall}%
- F1-Score: {f1_score}%
- False Positive Rate: {fpr}%

**요청사항:**
1. 목표 대비 성능 평가
2. 챔버별/레시피별 성능 차이 분석
3. 오류 케이스 분석 및 원인 추정
4. 모델 개선 방안 제시
5. 특성 중요도 분석 결과 포함
6. 시각화 자료 제안 (혼동 행렬, 예측 vs 실제 그래프 등)
```

---

### 월간 리포트 생성 프롬프트

```
당신은 프로젝트 관리 및 데이터 분석 전문가입니다.

다음 데이터를 바탕으로 월간 리포트를 작성해주세요.

**보고 기간:** {year}년 {month}월 ({start_date} ~ {end_date})

**핵심 지표:**
- RUL 예측 정확도: ±{accuracy}μm
- 교체 주기 연장률: {extension_rate}%
- 알람 적중률: {alarm_accuracy}%
- 비용 절감액: {cost_savings}원

**운영 현황:**
- 모델 예측 횟수: {prediction_count}회
- 알람 발생 횟수: {alarm_count}회
- False Positive: {false_positive}회
- False Negative: {false_negative}회
- 시스템 가동률: {uptime}%

**챔버별 현황:**
{chamber_status_table}

**레시피별 현황:**
{recipe_status_table}

**이슈 및 대응:**
{issues_list}

**요청사항:**
1. 간결하고 명확한 요약 제공
2. 전월 대비 변화율 분석
3. 주요 성과 하이라이트
4. 이슈 및 대응 내역 정리
5. 다음 달 계획 수립
6. 시각화가 필요한 부분 명시
```

---

### 알람 리포트 생성 프롬프트

```
당신은 설비 모니터링 시스템 전문가입니다.

다음 알람 발생 내역을 바탕으로 알람 리포트를 작성해주세요.

**보고 기간:** {start_date} ~ {end_date}

**알람 통계:**
- 총 알람 발생 횟수: {total_alarms}회
- True Positive: {true_positive}회
- False Positive: {false_positive}회
- False Negative: {false_negative}회
- 알람 적중률: {accuracy}%

**알람 유형별 분류:**
- 교체 임계점 알람: {replacement_alarm}회
- 이상 징후 알람 (Arcing): {arcing_alarm}회
- 급격한 마모 알람: {rapid_wear_alarm}회
- 기타 알람: {other_alarm}회

**주요 알람 사례:**
{alarm_cases_list}

**요청사항:**
1. 알람 발생 패턴 분석
2. False Positive/Negative 원인 분석
3. 알람 시스템 개선 방안 제시
4. 챔버별/레시피별 알람 발생 빈도 분석
5. 알람 응답 시간 분석
6. 시각화 자료 제안 (알람 발생 시간대 분포, 알람 유형별 분포 등)
```

---

### 데이터 품질 리포트 생성 프롬프트

```
당신은 데이터 품질 관리 전문가입니다.

다음 데이터 품질 정보를 바탕으로 리포트를 작성해주세요.

**평가 기간:** {start_date} ~ {end_date}

**데이터 수집 현황:**
- 총 데이터 포인트: {total_data_points}개
- 예상 데이터 포인트: {expected_data_points}개
- 데이터 수집률: {collection_rate}%

**데이터 품질 지표:**
- 결측값 비율: {missing_rate}%
- 이상치 비율: {outlier_rate}%
- 중복 데이터 비율: {duplicate_rate}%
- 데이터 일관성 점수: {consistency_score}/100

**특성별 품질:**
{feature_quality_table}

**챔버별 데이터 품질:**
{chamber_quality_table}

**이슈 및 개선사항:**
{data_quality_issues}

**요청사항:**
1. 데이터 품질 종합 평가
2. 챔버별/특성별 품질 차이 분석
3. 데이터 품질이 모델 성능에 미치는 영향 분석
4. 데이터 품질 개선 방안 제시
5. 데이터 수집 프로세스 개선 제안
6. 시각화 자료 제안 (품질 지표 트렌드, 결측값 패턴 등)
```

---

## 사용 예시

### 예시 1: 월간 리포트 자동 생성

```python
prompt = f"""
당신은 프로젝트 관리 및 데이터 분석 전문가입니다.

다음 데이터를 바탕으로 월간 리포트를 작성해주세요.

**보고 기간:** 2024년 12월 (2024-12-01 ~ 2024-12-31)

**핵심 지표:**
- RUL 예측 정확도: ±4.2μm
- 교체 주기 연장률: 18%
- 알람 적중률: 96%
- 비용 절감액: 15,000,000원

**운영 현황:**
- 모델 예측 횟수: 1,250회
- 알람 발생 횟수: 8회
- False Positive: 1회
- False Negative: 0회
- 시스템 가동률: 99.5%

[추가 데이터...]
"""
```

---

## 리포트 작성 가이드라인

### 공통 원칙
1. **명확성**: 기술 용어를 사용하되, 이해하기 쉽게 설명
2. **구조화**: 일관된 구조와 형식 유지
3. **데이터 기반**: 모든 주장은 데이터로 뒷받침
4. **시각화**: 복잡한 데이터는 차트/그래프로 표현
5. **액션 아이템**: 구체적인 다음 단계 제시

### 리포트 구조
1. **요약 (Executive Summary)**: 핵심 내용 한눈에 파악
2. **상세 분석**: 데이터 기반 상세 분석
3. **성과 지표**: 목표 대비 달성 현황
4. **이슈 및 대응**: 발생한 이슈와 대응 내역
5. **다음 단계**: 구체적인 계획 수립

---

## 주의사항

1. **데이터 검증**: 리포트 생성 전 데이터의 정확성 확인
2. **컨텍스트 제공**: 충분한 배경 정보 포함
3. **비교 기준**: 전월/전년 대비 비교 기준 명확히 제시
4. **시각화**: 적절한 차트/그래프 타입 선택
5. **액션 가능**: 구체적이고 실행 가능한 권고사항 제시


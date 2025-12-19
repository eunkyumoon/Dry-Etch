# 🚀 프로젝트 실행 가이드

Y2O3 Focus Ring 모니터링 시스템 실행 방법을 단계별로 안내합니다.

## 📋 목차

1. [사전 요구사항](#사전-요구사항)
2. [설치 방법](#설치-방법)
3. [실행 방법](#실행-방법)
4. [실행 화면 예시](#실행-화면-예시)
5. [문제 해결](#문제-해결)

---

## 사전 요구사항

### 필수 요구사항

- **Python 3.8 이상** (권장: Python 3.9+)
- **pip** 패키지 관리자
- **인터넷 연결** (패키지 다운로드용)

### 시스템 확인

```bash
# Python 버전 확인
python --version
# 또는
python3 --version

# pip 버전 확인
pip --version
```

---

## 설치 방법

### 1단계: 저장소 클론 (또는 다운로드)

```bash
git clone https://github.com/eunkyumoon/Dry-Etch.git
cd Dry-Etch
```

### 2단계: 가상 환경 생성 (권장)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3단계: 패키지 설치

```bash
# pip 업그레이드
pip install --upgrade pip

# 필수 패키지 설치
pip install -r requirements.txt
```

**설치되는 패키지:**
- `numpy>=1.21.0` - 수치 계산
- `pandas>=1.3.0` - 데이터 처리
- `scikit-learn>=1.0.0` - 머신러닝
- `matplotlib>=3.4.0` - 그래프 시각화
- `seaborn>=0.11.0` - 통계 시각화
- `streamlit>=1.28.0` - 웹 대시보드
- `plotly>=5.17.0` - 인터랙티브 차트

### 4단계: 설치 확인

```bash
# Python에서 import 테스트
python -c "import streamlit, plotly, pandas, numpy, sklearn; print('All packages installed successfully!')"
```

---

## 실행 방법

### 방법 1: 웹 대시보드 실행 (권장) ⭐

**가장 추천하는 방법입니다.** 실시간 모니터링 대시보드를 웹 브라우저에서 실행합니다.

#### 실행 명령어

```bash
streamlit run dashboard.py
```

#### 실행 과정

1. 명령어 실행 후 자동으로 브라우저가 열립니다
2. 브라우저가 열리지 않으면 수동으로 접속:
   - 주소: `http://localhost:8501`
   - 또는: `http://127.0.0.1:8501`

#### 대시보드 기능

- ✅ 중앙 네트워크 시각화 (챔버 상태)
- ✅ 좌측 패널: RF 파라미터, 마모 상태, RUL 예측
- ✅ 우측 패널: 설비 운영, 위험 모니터링, 교체 알람
- ✅ 하단 패널: 시간 시리즈 차트
- ✅ 사이드바: 챔버 선택, 시간 조정, 자동 새로고침

#### 종료 방법

- 터미널에서 `Ctrl + C` 누르기
- 브라우저 창 닫기 (서버는 계속 실행됨)

---

### 방법 2: 콘솔 기반 실행

시뮬레이션을 콘솔에서 실행하여 텍스트 기반 결과를 확인합니다.

#### 실행 명령어

```bash
# 방법 A: 모듈로 실행 (권장)
python -m refactored.main

# 방법 B: 직접 실행
cd refactored
python main.py
```

#### 실행 결과 예시

```
=== Y2O3 Focus Ring 마모 진행도 시뮬레이션 ===

시간: 0시간
Vpp: 450.0V, Yttrium Peak: 0.85
마모 진행도: 0.0%
잔여 두께: 1000.0μm
상태: 정상
RUL 예측: 8000.0시간
Arcing 위험도: 10.0% (낮음)
교체 필요: 아니오

시간: 500시간
Vpp: 495.0V, Yttrium Peak: 0.64
마모 진행도: 25.0%
잔여 두께: 750.0μm
상태: 정상
RUL 예측: 6000.0시간
Arcing 위험도: 25.0% (낮음)
교체 필요: 아니오

...
```

---

### 방법 3: 다른 포트로 실행

포트 8501이 사용 중일 때 다른 포트를 사용합니다.

```bash
streamlit run dashboard.py --server.port 8502
```

접속 주소: `http://localhost:8502`

---

## 실행 화면 예시

### 웹 대시보드 화면 구성

```
┌─────────────────────────────────────────────────────────┐
│  Y2O3 Focus Ring 실시간 모니터링 시스템                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│         [중앙 네트워크 그래프]                          │
│         (챔버 상태 시각화)                               │
│                                                          │
├──────────────────┬───────────────────────────────────────┤
│  좌측 패널       │  우측 패널                            │
│                  │                                       │
│  RF 파라미터     │  설비 운영 모니터링                   │
│  - Vpp: 495V    │  - 자산 마모도: 25%                   │
│  - Vdc: -220V   │                                       │
│  - Phase: 50°   │  위험 모니터링                        │
│                  │  - Arcing 위험도: 25%                │
│  마모 상태       │  - 위험 등급: 낮음                   │
│  [게이지 차트]   │                                       │
│  - 진행도: 25%   │  교체 알람                            │
│  - 잔여: 750μm  │  ✅ 정상 상태                         │
│                  │                                       │
│  RUL 예측        │                                       │
│  - 예상: 6000h   │                                       │
│  - 두께: 750μm  │                                       │
├──────────────────┴───────────────────────────────────────┤
│  하단 패널: 시간 시리즈 차트                             │
│  [Vpp 차트]  [Yttrium Peak 차트]  [마모 진행도 차트]    │
└─────────────────────────────────────────────────────────┘
```

### 사이드바 설정

```
⚙️ 설정
├─ 챔버 선택: [Chamber1 ▼]
├─ 누적 시간: [━━━━━━━━━━━━━━━━━━━━] 500시간
├─ 자동 새로고침: [✓]
└─ 새로고침 간격: [━━━━━━━━━━━━━━━━━━━━] 5초
```

---

## 문제 해결

### ❌ 문제 1: "streamlit: command not found"

**원인**: Streamlit이 설치되지 않았거나 PATH에 없음

**해결 방법**:
```bash
# Streamlit 재설치
pip install streamlit

# 또는 전체 패키지 재설치
pip install -r requirements.txt --force-reinstall
```

---

### ❌ 문제 2: "포트 8501이 이미 사용 중입니다"

**원인**: 다른 프로세스가 포트를 사용 중

**해결 방법**:
```bash
# 방법 1: 다른 포트 사용
streamlit run dashboard.py --server.port 8502

# 방법 2: 포트 사용 프로세스 종료 (Windows)
netstat -ano | findstr :8501
taskkill /PID <PID번호> /F
```

---

### ❌ 문제 3: "ModuleNotFoundError: No module named 'refactored'"

**원인**: 프로젝트 루트 디렉토리에서 실행하지 않음

**해결 방법**:
```bash
# 프로젝트 루트로 이동
cd "C:\DEV\Dry Etch"

# 다시 실행
streamlit run dashboard.py
```

---

### ❌ 문제 4: "ERR_CONNECTION_REFUSED"

**원인**: Streamlit 서버가 실행되지 않음

**해결 방법**:
1. 터미널에서 Streamlit이 실행 중인지 확인
2. 오류 메시지 확인
3. Python 버전 확인 (3.8 이상 필요)
4. 패키지 재설치:
   ```bash
   pip install --upgrade streamlit plotly pandas numpy scikit-learn
   ```

---

### ❌ 문제 5: 차트가 표시되지 않음

**원인**: Plotly가 제대로 설치되지 않음

**해결 방법**:
```bash
# Plotly 재설치
pip install --upgrade plotly

# 브라우저 콘솔 확인 (F12)
# JavaScript 오류 확인
```

---

### ❌ 문제 6: 한글 폰트 깨짐

**원인**: 시스템에 한글 폰트가 없음

**해결 방법**:
- Windows: 기본적으로 한글 지원
- Linux: 한글 폰트 설치 필요
  ```bash
  sudo apt-get install fonts-nanum
  ```

---

## 빠른 시작 체크리스트

- [ ] Python 3.8+ 설치 확인
- [ ] 프로젝트 디렉토리로 이동
- [ ] 가상 환경 생성 및 활성화 (선택사항)
- [ ] `pip install -r requirements.txt` 실행
- [ ] `streamlit run dashboard.py` 실행
- [ ] 브라우저에서 `http://localhost:8501` 접속 확인

---

## 추가 리소스

- **대시보드 상세 가이드**: [DASHBOARD_README.md](DASHBOARD_README.md)
- **프로젝트 개요**: [README.md](README.md)
- **코드 가이드**: [refactored/README.md](refactored/README.md)
- **Streamlit 문서**: https://docs.streamlit.io/
- **Plotly 문서**: https://plotly.com/python/

---

## 지원

문제가 해결되지 않으면 다음을 확인하세요:

1. Python 버전: `python --version`
2. 설치된 패키지: `pip list`
3. 프로젝트 구조: `ls` 또는 `dir`
4. 오류 로그: 터미널 출력 확인

---

**마지막 업데이트**: 2024년


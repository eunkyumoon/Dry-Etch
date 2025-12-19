# 🚀 빠른 시작 가이드

## 대시보드 실행 방법

### ⚠️ 중요: 올바른 디렉토리에서 실행하세요!

배치 파일은 **프로젝트 루트 디렉토리** (`C:\DEV\Dry Etch`)에서 실행해야 합니다.

### 방법 1: 배치 파일 더블클릭 (가장 간단)

1. **파일 탐색기**에서 `C:\DEV\Dry Etch` 폴더를 엽니다
2. `run_dashboard.bat` 파일을 **더블클릭**합니다
3. 명령 프롬프트 창이 열리고 대시보드가 시작됩니다
4. 브라우저가 자동으로 열리거나, 수동으로 `http://localhost:8501` 접속

### 방법 2: PowerShell에서 실행

1. **PowerShell**을 엽니다
2. 다음 명령어를 실행합니다:

```powershell
cd "C:\DEV\Dry Etch"
.\run_dashboard.bat
```

또는:

```powershell
cd "C:\DEV\Dry Etch"
streamlit run dashboard.py --server.port 8501
```

### 방법 3: 명령 프롬프트에서 실행

1. **명령 프롬프트 (cmd)**를 엽니다
2. 다음 명령어를 실행합니다:

```cmd
cd "C:\DEV\Dry Etch"
run_dashboard.bat
```

또는:

```cmd
cd "C:\DEV\Dry Etch"
streamlit run dashboard.py --server.port 8501
```

## ❌ 문제 해결

### "파일을 찾을 수 없습니다" 오류

**원인**: 잘못된 디렉토리에서 실행했습니다.

**해결**:
1. 프로젝트 루트 디렉토리로 이동:
   ```powershell
   cd "C:\DEV\Dry Etch"
   ```
2. 현재 디렉토리 확인:
   ```powershell
   Get-Location
   # 또는
   pwd
   ```
3. `run_dashboard.bat` 파일이 있는지 확인:
   ```powershell
   Test-Path "run_dashboard.bat"
   ```

### 포트 8501이 이미 사용 중입니다

**해결**: 다른 포트 사용
```powershell
streamlit run dashboard.py --server.port 8502
```

### 모듈을 찾을 수 없습니다

**해결**: 패키지 재설치
```powershell
pip install -r requirements.txt
```

## 📝 실행 확인

대시보드가 정상적으로 실행되면:

1. 터미널에 다음과 같은 메시지가 표시됩니다:
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```

2. 브라우저가 자동으로 열리거나, 수동으로 `http://localhost:8501` 접속

3. 대시보드 화면이 표시됩니다:
   - 중앙 네트워크 그래프
   - 좌측/우측 패널
   - 하단 시간 시리즈 차트

## 🛑 종료 방법

- 터미널 창에서 `Ctrl + C` 누르기
- 또는 터미널 창 닫기

---

**팁**: 파일 탐색기에서 `run_dashboard.bat`를 더블클릭하는 것이 가장 간단합니다!


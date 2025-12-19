# 🔧 문제 해결 가이드

## Streamlit 대시보드 연결 문제 해결

### ✅ 서버가 실행 중인지 확인

PowerShell에서 다음 명령어로 확인:

```powershell
netstat -ano | findstr :8501
```

**정상적인 경우:**
```
TCP    0.0.0.0:8501           0.0.0.0:0              LISTENING       4636
TCP    [::]:8501              [::]:0                 LISTENING       4636
```

### 🔍 문제 해결 단계

#### 1. 서버가 실행되지 않는 경우

**해결 방법:**

```powershell
cd "C:\DEV\Dry Etch"
python -m streamlit run dashboard.py --server.port 8501
```

#### 2. 포트가 이미 사용 중인 경우

**확인:**
```powershell
netstat -ano | findstr :8501
```

**해결:** 다른 포트 사용
```powershell
streamlit run dashboard.py --server.port 8502
```

#### 3. 방화벽 문제

Windows 방화벽이 localhost 연결을 차단할 수 있습니다.

**해결:**
1. Windows 보안 설정 열기
2. 방화벽 및 네트워크 보호
3. 앱이 방화벽을 통과하도록 허용
4. Python 또는 Streamlit 추가

#### 4. 브라우저 캐시 문제

**해결:**
- 브라우저 캐시 삭제
- 시크릿 모드에서 접속 시도
- 다른 브라우저로 시도

#### 5. 127.0.0.1로 접속 시도

`localhost` 대신 `127.0.0.1` 사용:

```
http://127.0.0.1:8501
```

### 🚀 올바른 실행 방법

#### 방법 1: PowerShell에서 직접 실행

```powershell
cd "C:\DEV\Dry Etch"
python -m streamlit run dashboard.py --server.port 8501
```

#### 방법 2: 배치 파일 사용

1. 파일 탐색기에서 `C:\DEV\Dry Etch` 폴더 열기
2. `run_dashboard.bat` 더블클릭

#### 방법 3: 새 PowerShell 창에서 실행

```powershell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\DEV\Dry Etch'; streamlit run dashboard.py --server.port 8501"
```

### 📋 실행 확인 체크리스트

- [ ] Python이 설치되어 있음 (`python --version`)
- [ ] Streamlit이 설치되어 있음 (`pip list | findstr streamlit`)
- [ ] 프로젝트 루트 디렉토리에서 실행 (`C:\DEV\Dry Etch`)
- [ ] 포트 8501이 사용 가능함
- [ ] 방화벽이 차단하지 않음
- [ ] 브라우저가 localhost 접속 가능함

### 🆘 여전히 문제가 있는 경우

1. **터미널 출력 확인**: 오류 메시지가 있는지 확인
2. **로그 확인**: Streamlit 로그 파일 확인
3. **재설치**: 패키지 재설치
   ```powershell
   pip install --upgrade streamlit plotly pandas numpy scikit-learn
   ```

### 📞 접속 주소

서버가 정상 실행되면 다음 주소로 접속:

- **로컬**: http://localhost:8501
- **로컬 (IP)**: http://127.0.0.1:8501
- **네트워크**: http://[내부IP]:8501

---

**마지막 업데이트**: 2024년


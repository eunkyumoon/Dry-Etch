@echo off
chcp 65001 >nul
echo ========================================
echo Y2O3 Focus Ring 대시보드 실행
echo ========================================
echo.

REM 스크립트가 있는 디렉토리로 이동
cd /d "%~dp0"

REM 현재 디렉토리 확인
echo 현재 디렉토리: %CD%
echo.

REM dashboard.py 파일 존재 확인
if not exist "dashboard.py" (
    echo [오류] dashboard.py 파일을 찾을 수 없습니다!
    echo 현재 디렉토리: %CD%
    echo.
    echo 프로젝트 루트 디렉토리(C:\DEV\Dry Etch)에서 실행하세요.
    pause
    exit /b 1
)

echo Streamlit 대시보드를 시작합니다...
echo 브라우저가 자동으로 열립니다.
echo.
echo 접속 주소: http://localhost:8501
echo.
echo 종료하려면 이 창을 닫거나 Ctrl+C를 누르세요.
echo.
echo ========================================
echo.

streamlit run dashboard.py --server.port 8501

if errorlevel 1 (
    echo.
    echo [오류] 대시보드를 시작하는 중 오류가 발생했습니다.
    echo.
    echo 확인 사항:
    echo 1. Python이 설치되어 있는지 확인: python --version
    echo 2. 패키지가 설치되어 있는지 확인: pip list ^| findstr streamlit
    echo 3. 포트 8501이 사용 중인지 확인: netstat -ano ^| findstr :8501
    echo.
)

pause

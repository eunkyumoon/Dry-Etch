# Y2O3 Focus Ring 대시보드 실행 스크립트
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Y2O3 Focus Ring 대시보드 실행" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 현재 스크립트 디렉토리로 이동
Set-Location $PSScriptRoot
Write-Host "현재 디렉토리: $PWD" -ForegroundColor Yellow
Write-Host ""

# Streamlit 실행
Write-Host "Streamlit 대시보드를 시작합니다..." -ForegroundColor Green
Write-Host "브라우저가 자동으로 열립니다." -ForegroundColor Green
Write-Host ""
Write-Host "종료하려면 Ctrl+C를 누르세요." -ForegroundColor Yellow
Write-Host ""

streamlit run dashboard.py --server.port 8501


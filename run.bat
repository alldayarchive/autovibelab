@echo off
title AutoVibeLab - Full AI Video Studio
echo ===================================================
echo 🚀 AutoVibeLab 풀 버전 스튜디오를 가동합니다.
echo 필요한 의존성 패키지를 설치 중입니다...
echo ===================================================
pip install -r requirements.txt
echo.
echo 🌐 브라우저를 열어 AutoVibeLab 스튜디오를 실행합니다...
streamlit run app.py
pause

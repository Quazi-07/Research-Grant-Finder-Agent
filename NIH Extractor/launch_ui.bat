@echo off
cd /d "%~dp0"
python -m streamlit run streamlit_app.py --server.port 8501
pause

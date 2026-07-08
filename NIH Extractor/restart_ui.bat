@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*streamlit_app.py*' -and $_.CommandLine -like '*NIH_info*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
python -m streamlit run streamlit_app.py --server.port 8501
pause

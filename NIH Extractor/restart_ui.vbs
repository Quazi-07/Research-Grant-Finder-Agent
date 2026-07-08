Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
appDir = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = appDir
shell.Run "powershell -NoProfile -ExecutionPolicy Bypass -Command ""Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*streamlit_app.py*' -and $_.CommandLine -like '*NIH_info*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }""", 0, True
shell.Run "cmd /c python -m streamlit run streamlit_app.py --server.port 8501", 0, False
WScript.Sleep 3000
shell.Run "http://localhost:8501", 1, False

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
appDir = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = appDir
shell.Run "cmd /c python -m streamlit run streamlit_app.py --server.port 8501", 0, False
WScript.Sleep 3000
shell.Run "http://localhost:8501", 1, False

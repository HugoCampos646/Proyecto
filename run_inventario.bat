@echo off

set SCRIPT_STREAMLIT=inventario.py

pushd "%~dp0"
streamlit run %SCRIPT_STREAMLIT% --server.port=8010

deactivate
pause

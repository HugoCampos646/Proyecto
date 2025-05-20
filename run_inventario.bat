@echo off

set NOMBRE_ENTORNO=env_desarrollo
set RUTA_PROYECTO=inventario
set SCRIPT_STREAMLIT=inventario.py

call %NOMBRE_ENTORNO%\Scripts\activate

pushd "%~dp0"
streamlit run %SCRIPT_STREAMLIT% --server.port=8010

deactivate
pause

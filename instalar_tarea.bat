@echo off
:: Ruta al ejecutable de Python (ajústalo si es necesario)
set "PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"

:: Ruta al script de backup (usa el mismo directorio del .bat)
set "SCRIPT_PATH=%~dp0backup_diario.py"

:: Nombre que le daremos a la tarea programada
set "TASK_NAME=BackupInventario"

:: Crear la tarea programada: al iniciar el equipo
schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
  /sc onstart ^
  /rl highest ^
  /f

echo.
echo ✅ Tarea programada creada con éxito.
pause

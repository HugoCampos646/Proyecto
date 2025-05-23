@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo    INSTALADOR DE COPIA DE SEGURIDAD AUTOMATICA
echo ===============================================
echo.

REM Verificar que se ejecuta como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Este script debe ejecutarse como ADMINISTRADOR
    echo Haz clic derecho en el archivo .bat y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

echo [1/4] Verificando permisos de administrador... OK
echo.

REM Obtener la ruta del directorio donde esta este .bat
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Definir rutas (MODIFICA ESTAS RUTAS SEGUN TUS ARCHIVOS)
set "PYTHON_SCRIPT=%SCRIPT_DIR%\backup_diario.py"
set "PYTHON_EXE=python"

echo [2/4] Verificando archivos...
if not exist "%PYTHON_SCRIPT%" (
    echo ERROR: No se encuentra el script de Python en: %PYTHON_SCRIPT%
    echo Modifica la variable PYTHON_SCRIPT en este .bat con la ruta correcta
    pause
    exit /b 1
)
echo      Script encontrado: %PYTHON_SCRIPT%

REM Verificar que Python esta disponible
%PYTHON_EXE% --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python no encontrado en el PATH del sistema
    echo Instala Python o agrega python.exe al PATH
    pause
    exit /b 1
)
echo      Python encontrado: OK
echo.

echo [3/4] Creando tarea programada...

REM Eliminar tarea existente si existe
schtasks /delete /tn "CopiaSeguridad_Inventario" /f >nul 2>&1

REM Crear nueva tarea programada
schtasks /create /tn "CopiaSeguridad_Inventario" /tr "\"%PYTHON_EXE%\" \"%PYTHON_SCRIPT%\"" /sc onstart /ru "SYSTEM" /rl highest /f

if %errorLevel% neq 0 (
    echo ERROR: No se pudo crear la tarea programada
    pause
    exit /b 1
)

echo      Tarea programada creada exitosamente
echo.

echo [4/4] Verificando instalacion...
schtasks /query /tn "CopiaSeguridad_Inventario" >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: La tarea no se creo correctamente
    pause
    exit /b 1
)

echo ===============================================
echo           INSTALACION COMPLETADA
echo ===============================================
echo.
echo ✅ La copia de seguridad automatica ha sido instalada
echo ✅ Se ejecutara automaticamente cada vez que inicies el ordenador
echo ✅ Se ejecuta con permisos de sistema para evitar problemas
echo.
echo COMANDOS UTILES:
echo.
echo Para DESINSTALAR:
echo   schtasks /delete /tn "CopiaSeguridad_Inventario" /f
echo.
echo Para ver el ESTADO:
echo   schtasks /query /tn "CopiaSeguridad_Inventario"
echo.
echo Para EJECUTAR AHORA (prueba):
echo   schtasks /run /tn "CopiaSeguridad_Inventario"
echo.
echo ¿Quieres ejecutar una prueba ahora? (S/N)
set /p respuesta=
if /i "%respuesta%"=="S" (
    echo.
    echo Ejecutando prueba...
    schtasks /run /tn "CopiaSeguridad_Inventario"
    echo Prueba lanzada. Revisa si se crean las copias de seguridad.
)

echo.
echo Presiona cualquier tecla para salir...
pause >nul
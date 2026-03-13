@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: Directorio donde esta este .bat (raiz del proyecto)
set "DIR=%~dp0"
cd /d "%DIR%"

title Calculadora de Costos - Excel-ente

echo.
echo  =====================================================
echo    CALCULADORA DE COSTOS DE RECETAS
echo    by Excel-ente -- youtube.com/@excel-ente
echo  =====================================================
echo.

:: ─────────────────────────────────────────────────────────────
:: 1. VERIFICAR PYTHON
:: ─────────────────────────────────────────────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 goto :NO_PYTHON

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set "PYVER=%%v"
echo  [OK] Python !PYVER! detectado.

:: ─────────────────────────────────────────────────────────────
:: 2. DETECTAR SI FALTA PREPARAR EL ENTORNO
:: ─────────────────────────────────────────────────────────────
set "FIRST_RUN=0"
if not exist "%DIR%venv\Scripts\activate.bat" set "FIRST_RUN=1"

if "!FIRST_RUN!"=="1" goto :SETUP

:: ─────────────────────────────────────────────────────────────
:: EJECUCION NORMAL (entorno ya instalado)
:: ─────────────────────────────────────────────────────────────
call "%DIR%venv\Scripts\activate.bat"
echo  [OK] Entorno virtual activado.

pip install -r "%DIR%requirements.txt" -q --no-warn-script-location >nul 2>&1
echo  [OK] Dependencias verificadas.

goto :MIGRATE

:: ─────────────────────────────────────────────────────────────
:SETUP
:: CONFIGURACION INICIAL (primera vez)
:: ─────────────────────────────────────────────────────────────
echo.
echo  Primera ejecucion detectada. Configurando el proyecto...
echo.

echo  [1/4] Creando entorno virtual de Python...
python -m venv "%DIR%venv"
if %errorlevel% neq 0 goto :ERROR_VENV

call "%DIR%venv\Scripts\activate.bat"
echo  [OK] Entorno virtual creado y activado.

echo.
echo  [2/4] Instalando dependencias del proyecto...
echo  (Esto puede tardar unos minutos la primera vez)
echo.
pip install -r "%DIR%requirements.txt"
if %errorlevel% neq 0 goto :ERROR_DEPS
echo.
echo  [OK] Dependencias instaladas correctamente.

:: ─────────────────────────────────────────────────────────────
:MIGRATE
:: BASE DE DATOS Y CONFIGURACION
:: ─────────────────────────────────────────────────────────────

:: Crear .env si no existe
if not exist "%DIR%.env" (
    echo  [INFO] Creando archivo de configuracion .env...
    (
        echo MODO_DESARROLLO=True
        echo SECRET_KEY=calculadora-costos-excel-ente-local-dev-clave-secreta-1234
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
    ) > "%DIR%.env"
    echo  [OK] Archivo .env creado.
)

:: Aplicar migraciones
if "!FIRST_RUN!"=="1" (
    echo.
    echo  [3/4] Aplicando migraciones de base de datos...
) else (
    echo  [INFO] Verificando base de datos...
)

python "%DIR%manage.py" migrate
if %errorlevel% neq 0 goto :ERROR_MIGRATE
echo  [OK] Base de datos lista.

:: Detectar si falta el superusuario inicial
set "NEED_ROOT_USER=0"
python "%DIR%manage.py" shell -c "from django.contrib.auth import get_user_model; import sys; sys.exit(0 if get_user_model().objects.filter(is_superuser=True).exists() else 1)" >nul 2>&1
if %errorlevel% neq 0 set "NEED_ROOT_USER=1"

:: Crear superusuario inicial si no existe ninguno
if "!NEED_ROOT_USER!"=="1" (
    echo.
    echo  [4/4] Crear usuario administrador inicial
    echo  -------------------------------------------------------
    echo  Ingresa el nombre de usuario, email ^(opcional^) y contrasena.
    echo  El email es opcional, podes dejarlo en blanco.
    echo  -------------------------------------------------------
    echo.
    python "%DIR%manage.py" createsuperuser
    python "%DIR%manage.py" shell -c "from django.contrib.auth import get_user_model; import sys; sys.exit(0 if get_user_model().objects.filter(is_superuser=True).exists() else 1)" >nul 2>&1
    if errorlevel 1 (
        echo.
        echo  [AVISO] No se creo el usuario administrador. Podes crearlo luego con:
        echo  python manage.py createsuperuser
    ) else (
        echo.
        set /p "CARGAR_DEMO=  Queres cargar 1 receta de ejemplo con datos demo? (s/N): "
        if /i "!CARGAR_DEMO!"=="s" (
            echo.
            echo  [INFO] Cargando configuracion demo inicial...
            python "%DIR%manage.py" adema
            if errorlevel 1 (
                echo  [AVISO] No se pudieron cargar los datos demo.
                echo  Podes intentarlo luego con:
                echo  python manage.py adema
            ) else (
                echo  [OK] Datos demo cargados.
            )
        ) else (
            echo.
            echo  [INFO] Se omitio la carga de la receta de ejemplo.
        )
    )
)

if "!NEED_ROOT_USER!"=="0" if "!FIRST_RUN!"=="1" (
    echo.
    echo  Setup completado. La proxima vez este script arranca directo.
    echo.
    set /p "CREAR_ACCESO=  Crear acceso directo en el escritorio? (s/N): "
    if /i "!CREAR_ACCESO!"=="s" goto :CREAR_ACCESO
)

if "!NEED_ROOT_USER!"=="1" (
    echo.
    echo  Setup completado. La proxima vez este script arranca directo.
    echo.
    set /p "CREAR_ACCESO=  Crear acceso directo en el escritorio? (s/N): "
    if /i "!CREAR_ACCESO!"=="s" goto :CREAR_ACCESO
)

goto :INICIAR_SERVIDOR

:: ─────────────────────────────────────────────────────────────
:CREAR_ACCESO
:: CREAR ACCESO DIRECTO EN EL ESCRITORIO via PowerShell
:: ─────────────────────────────────────────────────────────────
echo  [INFO] Creando acceso directo en el escritorio...

echo $bat = '%DIR%iniciar_windows.bat' > "%TEMP%\crear_acceso.ps1"
echo $desk = [Environment]::GetFolderPath('Desktop') >> "%TEMP%\crear_acceso.ps1"
echo $ws = New-Object -ComObject WScript.Shell >> "%TEMP%\crear_acceso.ps1"
echo $s = $ws.CreateShortcut($desk + '\Calculadora de Costos.lnk') >> "%TEMP%\crear_acceso.ps1"
echo $s.TargetPath = $bat >> "%TEMP%\crear_acceso.ps1"
echo $s.WorkingDirectory = '%DIR%' >> "%TEMP%\crear_acceso.ps1"
echo $s.Description = 'Calculadora de Costos - Excel-ente' >> "%TEMP%\crear_acceso.ps1"
echo $s.Save() >> "%TEMP%\crear_acceso.ps1"

powershell -NoProfile -ExecutionPolicy Bypass -File "%TEMP%\crear_acceso.ps1"
del "%TEMP%\crear_acceso.ps1" >nul 2>&1
echo  [OK] Acceso directo creado en el escritorio.

goto :INICIAR_SERVIDOR

:: ─────────────────────────────────────────────────────────────
:INICIAR_SERVIDOR
:: ─────────────────────────────────────────────────────────────
echo.
echo  =====================================================
echo    Aplicacion lista en: http://127.0.0.1:8000/admin/
echo    Acceso desde la red local habilitado en: 0.0.0.0:8000
echo    Presiona CTRL+C en esta ventana para detener
echo  =====================================================
echo.

start "" "http://127.0.0.1:8000/admin/"
python "%DIR%manage.py" runserver 0.0.0.0:8000

goto :FIN

:: ─────────────────────────────────────────────────────────────
:: MENSAJES DE ERROR
:: ─────────────────────────────────────────────────────────────

:NO_PYTHON
echo.
echo  [ERROR] Python no encontrado en el sistema.
echo.
echo  Para instalar Python:
echo   1. Ve a: https://www.python.org/downloads/
echo   2. Descarga Python 3.12 o superior
echo   3. Durante la instalacion MARCA "Add Python to PATH"
echo   4. Cierra esta ventana y vuelve a ejecutar el script
echo.
goto :FIN

:ERROR_VENV
echo.
echo  [ERROR] No se pudo crear el entorno virtual.
echo  Asegurate de tener Python 3.12+ instalado correctamente.
echo.
goto :FIN

:ERROR_DEPS
echo.
echo  [ERROR] No se pudieron instalar las dependencias.
echo  Verifica tu conexion a internet e intentalo de nuevo.
echo.
goto :FIN

:ERROR_MIGRATE
echo.
echo  [ERROR] Fallo al aplicar las migraciones de base de datos.
echo  Revisa los mensajes de error mostrados arriba.
echo.
goto :FIN

:FIN
endlocal
pause

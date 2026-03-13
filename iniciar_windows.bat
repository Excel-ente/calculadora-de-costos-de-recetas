@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "LAUNCHER_BAT=%~f0"
set "REPO_URL=https://github.com/Excel-ente/calculadora-de-costos-de-recetas.git"
set "PROJECT_SUBDIR=calculadora-de-costos-de-recetas"
set "BOOTSTRAP_MODE=0"
set "PYTHON_CMD="

if exist "%SCRIPT_DIR%manage.py" (
    set "PROJECT_DIR=%SCRIPT_DIR%"
) else (
    set "BOOTSTRAP_MODE=1"
    set "PROJECT_DIR=%SCRIPT_DIR%%PROJECT_SUBDIR%\"
)

cd /d "%SCRIPT_DIR%"
title Calculadora de Costos - Excel-ente

echo.
echo  =====================================================
echo    CALCULADORA DE COSTOS DE RECETAS
echo    by Excel-ente -- youtube.com/@excel-ente
echo  =====================================================
echo.

if "%BOOTSTRAP_MODE%"=="1" (
    echo  [INFO] Modo instalador detectado.
    echo  [INFO] La app se instalara o actualizara en:
    echo         %PROJECT_DIR%
    echo.
) else (
    echo  [INFO] Modo proyecto detectado en:
    echo         %PROJECT_DIR%
    echo.
)

call :ENSURE_PYTHON
if errorlevel 1 goto :FIN

if "%BOOTSTRAP_MODE%"=="1" (
    call :ENSURE_GIT
    if errorlevel 1 goto :FIN
    call :SYNC_REPOSITORY
    if errorlevel 1 goto :FIN
) else (
    if exist "%PROJECT_DIR%.git" (
        call :ENSURE_GIT
        if not errorlevel 1 call :SYNC_REPOSITORY
    )
)

if not exist "%PROJECT_DIR%manage.py" goto :ERROR_PROJECT

set "FIRST_RUN=0"
if not exist "%PROJECT_DIR%venv\Scripts\activate.bat" set "FIRST_RUN=1"

if "!FIRST_RUN!"=="1" goto :SETUP

call "%PROJECT_DIR%venv\Scripts\activate.bat"
echo  [OK] Entorno virtual activado.

pip install -r "%PROJECT_DIR%requirements.txt" -q --no-warn-script-location >nul 2>&1
echo  [OK] Dependencias verificadas.

goto :MIGRATE

:SETUP
echo.
echo  Primera ejecucion detectada. Configurando el proyecto...
echo.

echo  [1/4] Creando entorno virtual de Python...
call %PYTHON_CMD% -m venv "%PROJECT_DIR%venv"
if errorlevel 1 goto :ERROR_VENV

call "%PROJECT_DIR%venv\Scripts\activate.bat"
echo  [OK] Entorno virtual creado y activado.

echo.
echo  [2/4] Instalando dependencias del proyecto...
echo  (Esto puede tardar unos minutos la primera vez)
echo.
pip install -r "%PROJECT_DIR%requirements.txt"
if errorlevel 1 goto :ERROR_DEPS
echo.
echo  [OK] Dependencias instaladas correctamente.

:MIGRATE
if not exist "%PROJECT_DIR%.env" (
    if exist "%PROJECT_DIR%.env.example" (
        copy /y "%PROJECT_DIR%.env.example" "%PROJECT_DIR%.env" >nul
        echo  [OK] Archivo .env creado desde .env.example.
    ) else (
        echo  [INFO] Creando archivo de configuracion .env...
        (
            echo MODO_DESARROLLO=True
            echo SECRET_KEY=calculadora-costos-excel-ente-local-dev-clave-secreta-1234
            echo DEBUG=True
            echo ALLOWED_HOSTS=localhost,127.0.0.1
        ) > "%PROJECT_DIR%.env"
        echo  [OK] Archivo .env creado.
    )
)

if "!FIRST_RUN!"=="1" (
    echo.
    echo  [3/4] Aplicando migraciones de base de datos...
) else (
    echo  [INFO] Verificando base de datos...
)

python "%PROJECT_DIR%manage.py" migrate
if errorlevel 1 goto :ERROR_MIGRATE
echo  [OK] Base de datos lista.

set "NEED_ROOT_USER=0"
python "%PROJECT_DIR%manage.py" shell -c "from django.contrib.auth import get_user_model; import sys; sys.exit(0 if get_user_model().objects.filter(is_superuser=True).exists() else 1)" >nul 2>&1
if errorlevel 1 set "NEED_ROOT_USER=1"

if "!NEED_ROOT_USER!"=="1" (
    echo.
    echo  [4/4] Crear usuario administrador inicial
    echo  -------------------------------------------------------
    echo  Ingresa el nombre de usuario, email ^(opcional^) y contrasena.
    echo  El email es opcional, podes dejarlo en blanco.
    echo  -------------------------------------------------------
    echo.
    python "%PROJECT_DIR%manage.py" createsuperuser
    python "%PROJECT_DIR%manage.py" shell -c "from django.contrib.auth import get_user_model; import sys; sys.exit(0 if get_user_model().objects.filter(is_superuser=True).exists() else 1)" >nul 2>&1
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
            python "%PROJECT_DIR%manage.py" adema
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

if "!FIRST_RUN!"=="1" (
    echo.
    echo  Setup completado. La proxima vez este script arranca directo.
    echo.
    set /p "CREAR_ACCESO=  Crear acceso directo en el escritorio? (s/N): "
    if /i "!CREAR_ACCESO!"=="s" goto :CREAR_ACCESO
)

goto :INICIAR_SERVIDOR

:CREAR_ACCESO
echo  [INFO] Creando acceso directo en el escritorio...

echo $bat = '%LAUNCHER_BAT%' > "%TEMP%\crear_acceso.ps1"
echo $desk = [Environment]::GetFolderPath('Desktop') >> "%TEMP%\crear_acceso.ps1"
echo $ws = New-Object -ComObject WScript.Shell >> "%TEMP%\crear_acceso.ps1"
echo $s = $ws.CreateShortcut($desk + '\Calculadora de Costos.lnk') >> "%TEMP%\crear_acceso.ps1"
echo $s.TargetPath = $bat >> "%TEMP%\crear_acceso.ps1"
echo $s.WorkingDirectory = '%SCRIPT_DIR%' >> "%TEMP%\crear_acceso.ps1"
echo $s.Description = 'Calculadora de Costos - Excel-ente' >> "%TEMP%\crear_acceso.ps1"
echo $s.Save() >> "%TEMP%\crear_acceso.ps1"

powershell -NoProfile -ExecutionPolicy Bypass -File "%TEMP%\crear_acceso.ps1"
del "%TEMP%\crear_acceso.ps1" >nul 2>&1
echo  [OK] Acceso directo creado en el escritorio.

goto :INICIAR_SERVIDOR

:INICIAR_SERVIDOR
echo.
echo  =====================================================
echo    Aplicacion lista en: http://127.0.0.1:8000/admin/
echo    Carpeta del proyecto: %PROJECT_DIR%
echo    Acceso desde la red local habilitado en: 0.0.0.0:8000
echo    Presiona CTRL+C en esta ventana para detener
echo  =====================================================
echo.

start "" "http://127.0.0.1:8000/admin/"
python "%PROJECT_DIR%manage.py" runserver 0.0.0.0:8000

goto :FIN

:ENSURE_PYTHON
call :DETECT_PYTHON
if not errorlevel 1 exit /b 0

echo  [INFO] Python 3.12+ no encontrado. Intentando instalarlo con winget...
call :INSTALL_WITH_WINGET Python.Python.3.12 "Python 3.12"
if errorlevel 1 goto :ERROR_NO_PYTHON

call :REFRESH_PATH
call :DETECT_PYTHON
if not errorlevel 1 exit /b 0

goto :ERROR_NO_PYTHON

:DETECT_PYTHON
set "PYTHON_CMD="
set "PYVER="

where py.exe >nul 2>&1
if not errorlevel 1 (
    py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON_CMD=py -3"
        for /f "tokens=2 delims= " %%v in ('py -3 --version 2^>^&1') do set "PYVER=%%v"
        echo  [OK] Python !PYVER! detectado.
        exit /b 0
    )
)

where python.exe >nul 2>&1
if not errorlevel 1 (
    python -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON_CMD=python"
        for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set "PYVER=%%v"
        echo  [OK] Python !PYVER! detectado.
        exit /b 0
    )
)

exit /b 1

:ENSURE_GIT
git --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=3 delims= " %%v in ('git --version 2^>^&1') do set "GITVER=%%v"
    echo  [OK] Git !GITVER! detectado.
    exit /b 0
)

echo  [INFO] Git no encontrado. Intentando instalarlo con winget...
call :INSTALL_WITH_WINGET Git.Git Git
if errorlevel 1 goto :ERROR_NO_GIT

call :REFRESH_PATH
git --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=3 delims= " %%v in ('git --version 2^>^&1') do set "GITVER=%%v"
    echo  [OK] Git !GITVER! detectado.
    exit /b 0
)

goto :ERROR_NO_GIT

:INSTALL_WITH_WINGET
where winget.exe >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [ERROR] winget no esta disponible en esta PC.
    echo  Instala la app "App Installer" desde Microsoft Store y volve a ejecutar este script.
    echo.
    exit /b 1
)

echo  [INFO] Instalando %~2...
winget install --id %~1 --exact --accept-package-agreements --accept-source-agreements --scope machine
if not errorlevel 1 exit /b 0

echo  [AVISO] No se pudo instalar %~2 para todo el equipo. Reintentando para el usuario actual...
winget install --id %~1 --exact --accept-package-agreements --accept-source-agreements --scope user
if not errorlevel 1 exit /b 0

echo.
echo  [ERROR] Fallo la instalacion automatica de %~2.
echo.
exit /b 1

:REFRESH_PATH
for /f "skip=2 tokens=2,*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SYS_PATH=%%b"
for /f "skip=2 tokens=2,*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USR_PATH=%%b"
set "PATH=%SYS_PATH%;%USR_PATH%;%PATH%"
exit /b 0

:SYNC_REPOSITORY
if exist "%PROJECT_DIR%.git" (
    echo  [INFO] Buscando actualizaciones del proyecto...
    pushd "%PROJECT_DIR%"
    git pull --ff-only
    if errorlevel 1 (
        echo  [AVISO] No se pudo actualizar con git pull. Se continuara con la version local.
    ) else (
        echo  [OK] Proyecto actualizado.
    )
    popd
    exit /b 0
)

if exist "%PROJECT_DIR%manage.py" (
    echo  [INFO] Se detecto una copia local del proyecto sin carpeta .git.
    echo  [AVISO] La app se usara igual, pero las actualizaciones automaticas requieren Git.
    exit /b 0
)

if exist "%PROJECT_DIR%" (
    dir /b "%PROJECT_DIR%" | findstr . >nul 2>&1
    if not errorlevel 1 goto :ERROR_DEST_DIR
)

echo  [INFO] Descargando el proyecto oficial...
git clone "%REPO_URL%" "%PROJECT_DIR%"
if errorlevel 1 goto :ERROR_CLONE
echo  [OK] Proyecto descargado.
exit /b 0

:ERROR_NO_PYTHON
echo.
echo  [ERROR] Python 3.12+ no pudo instalarse automaticamente.
echo  Instalala manualmente desde https://www.python.org/downloads/ y volve a ejecutar este script.
echo.
exit /b 1

:ERROR_NO_GIT
echo.
echo  [ERROR] Git no pudo instalarse automaticamente.
echo  Instalala manualmente desde https://git-scm.com/download/win y volve a ejecutar este script.
echo.
exit /b 1

:ERROR_DEST_DIR
echo.
echo  [ERROR] La carpeta destino ya existe pero no contiene una copia valida del proyecto:
echo          %PROJECT_DIR%
echo  Renombrala, vaciala o move el .bat a otra ubicacion y volve a probar.
echo.
exit /b 1

:ERROR_CLONE
echo.
echo  [ERROR] No se pudo descargar el proyecto desde GitHub.
echo  Verifica tu conexion a internet e intentalo de nuevo.
echo.
exit /b 1

:ERROR_PROJECT
echo.
echo  [ERROR] No se encontro manage.py en la carpeta del proyecto.
echo  Revisa que la descarga o actualizacion del repo haya terminado correctamente.
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

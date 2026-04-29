@echo off
REM Script para executar a aplicação de Informações de Hardware
REM Este script ativa o ambiente virtual e executa o programa

setlocal enabledelayedexpansion

REM Verificar se o ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo ============================================================
    echo PRIMEIRO USO - Criando ambiente virtual...
    echo ============================================================
    echo.
    python -m venv venv
    if errorlevel 1 (
        echo Erro ao criar ambiente virtual!
        echo Certifique-se de que Python 3.7+ está instalado
        pause
        exit /b 1
    )
)

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Instalar dependências (silenciosamente se já estiverem instaladas)
echo.
echo Verificando dependências...
pip install -r requirements.txt -q

REM Executar a aplicação
echo.
echo Iniciando aplicação...
python main.py

REM Manter janela aberta em caso de erro
if errorlevel 1 (
    echo.
    echo Erro ao executar a aplicação!
    pause
)

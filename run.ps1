# Script para executar a aplicação de Informações de Hardware
# Este script ativa o ambiente virtual e executa o programa

# Verificar se o ambiente virtual existe
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host ""
    Write-Host "============================================================"
    Write-Host "PRIMEIRO USO - Criando ambiente virtual..." -ForegroundColor Green
    Write-Host "============================================================"
    Write-Host ""
    
    python -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erro ao criar ambiente virtual!" -ForegroundColor Red
        Write-Host "Certifique-se de que Python 3.7+ está instalado"
        Read-Host "Pressione Enter para sair"
        exit 1
    }
}

# Ativar ambiente virtual
& "venv\Scripts\Activate.ps1"

# Instalar dependências
Write-Host ""
Write-Host "Verificando dependências..."
pip install -r requirements.txt -q

# Executar a aplicação
Write-Host ""
Write-Host "Iniciando aplicação..." -ForegroundColor Green
python main.py

# Verificar se houve erro
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Erro ao executar a aplicação!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
}

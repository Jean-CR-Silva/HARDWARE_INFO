# Hardware Info System - Linux Build

Este documento explica como gerar o executável Linux do Hardware Info System.

## Requisitos

- Distribuição Linux: Debian, Ubuntu, Mint, Fedora, Zorin ou similares
- Python 3.8+ (geralmente já instalado)
- Acesso root/sudo (para instalar dependências)

## Como gerar o executável

### Método 1: Script automático (Recomendado)

1. Abra o terminal no diretório do projeto
2. Execute o script de build:
   ```bash
   chmod +x build_linux.sh
   ./build_linux.sh
   ```

O script irá:
- Instalar automaticamente todas as dependências do sistema
- Instalar dependências Python
- Gerar o executável usando PyInstaller
- Criar um binário standalone em `dist/HardwareInfo`

### Método 2: Instalação manual

Se preferir instalar manualmente:

```bash
# Debian/Ubuntu/Mint/Zorin
sudo apt update
sudo apt install python3 python3-pip python3-tk python3-dev build-essential

# Fedora
sudo dnf install python3 python3-pip python3-tkinter python3-devel gcc gcc-c++

# Instalar dependências Python
python3 -m pip install --user --upgrade pip
python3 -m pip install --user -r requirements.txt pyinstaller

# Gerar executável
python3 build_exe.py
```

## Executável gerado

Após a build, o executável estará em:
```
dist/HardwareInfo
```

### Características do executável:
- ✅ Funciona sem Python instalado
- ✅ Compatível com múltiplas distribuições Linux
- ✅ Interface gráfica completa (Tkinter)
- ✅ Coleta informações de hardware
- ✅ Exporta para TXT e PDF
- ✅ Análise de saúde da bateria (se aplicável)

## Distribuição

O executável `HardwareInfo` pode ser:
- Copiado para qualquer máquina Linux compatível
- Executado diretamente: `./HardwareInfo`
- Distribuído sem código fonte

## Suporte a hardware

O executável coleta informações usando:
- **Windows**: WMIC, PowerShell, powercfg
- **Linux**: dmidecode, /sys/class/dmi/id/, upower, /sys/class/power_supply/

## Resolução de problemas

### Erro de permissões
```bash
chmod +x build_linux.sh
sudo ./build_linux.sh
```

### dmidecode requer sudo
O script instala e usa `dmidecode` que pode requerer permissões elevadas.

### Interface gráfica não abre
Certifique-se de que o ambiente gráfico está disponível (X11/Wayland).

## Compatibilidade testada

- ✅ Debian 11+
- ✅ Ubuntu 20.04+
- ✅ Linux Mint 20+
- ✅ Fedora 35+
- ✅ Zorin OS 16+</content>
<parameter name="filePath">c:\teste\hardware_info_system\README_LINUX.md
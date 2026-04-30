#!/bin/bash
set -e

# Script para gerar o binário Linux com PyInstaller.
# Execute em uma máquina Linux (Debian/Ubuntu/Mint/Fedora/Zorin).
# O executável gerado funcionará sem Python instalado.

if [ "$(uname -s)" != "Linux" ]; then
  echo "Este script deve ser executado em Linux."
  exit 1
fi

echo "============================================================="
echo "GERADOR DE EXECUTÁVEL LINUX - Hardware Info System"
echo "============================================================="
echo

# Instalar dependências do sistema
echo "1. Instalando dependências do sistema..."
if command -v apt >/dev/null 2>&1; then
  # Debian/Ubuntu/Mint/Zorin
  echo "   Detectado sistema baseado em Debian/Ubuntu"
  sudo apt update
  sudo apt install -y python3 python3-pip python3-tk python3-dev build-essential
elif command -v dnf >/dev/null 2>&1; then
  # Fedora
  echo "   Detectado sistema baseado em Fedora"
  sudo dnf install -y python3 python3-pip python3-tkinter python3-devel gcc gcc-c++
elif command -v pacman >/dev/null 2>&1; then
  # Arch Linux
  echo "   Detectado sistema baseado em Arch Linux"
  sudo pacman -Syu --noconfirm python python-pip tk python-setuptools
else
  echo "   Sistema não reconhecido. Instale manualmente: python3, pip, tkinter"
  exit 1
fi

echo "   Dependências do sistema instaladas"
echo

# Instalar dependências Python
echo "2. Instalando dependências Python..."
python3 -m pip install --user --upgrade pip
python3 -m pip install --user -r requirements.txt pyinstaller

echo "   Dependências Python instaladas"
echo

# Gerar executável
echo "3. Gerando executável Linux..."
python3 build_exe.py

echo
echo "============================================================="
echo "SUCESSO! Executável Linux gerado!"
echo "============================================================="
echo
echo "Localização: $(pwd)/dist/HardwareInfo"
echo
echo "Este executável:"
echo "  - Funciona sem Python instalado"
echo "  - Compatível com Debian, Ubuntu, Mint, Fedora, Zorin"
echo "  - Pode ser copiado para qualquer máquina Linux compatível"
echo
echo "Para executar: ./dist/HardwareInfo"
echo "Para exportar: copie o arquivo dist/HardwareInfo"

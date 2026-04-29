"""
Script para gerar o executável (.exe) usando PyInstaller
Execute: python build_exe.py
"""

import subprocess
import os
import sys
from pathlib import Path

def main():
    """Gera o executável da aplicação."""
    
    print("=" * 60)
    print("GERADOR DE EXECUTÁVEL - Hardware Info System")
    print("=" * 60)
    print()
    
    # Verificar se PyInstaller está instalado
    print("1. Verificando se PyInstaller está instalado...")
    try:
        import PyInstaller
        print("   ✓ PyInstaller encontrado")
    except ImportError:
        print("   ✗ PyInstaller não está instalado")
        print("   Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    print()
    print("2. Preparando arquivos...")
    
    # Diretório do projeto
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Comando PyInstaller
    command = [
        sys.executable,
        "-m",
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=HardwareInfo",
        "--distpath=dist",
        "--buildpath=build",
        "--specpath=.",
        "--add-data=services:services",
        "--add-data=ui:ui",
        "--add-data=utils:utils",
        "--hidden-import=psutil",
        "main.py"
    ]
    
    print()
    print("3. Gerando executável (isto pode levar alguns minutos)...")
    print()
    
    try:
        result = subprocess.run(command, check=True)
        
        print()
        print("=" * 60)
        print("✓ SUCESSO! Executável gerado com sucesso!")
        print("=" * 60)
        print()
        print(f"Localização: {project_dir / 'dist' / 'HardwareInfo.exe'}")
        print()
        print("O arquivo pode ser executado independentemente:")
        print(f"  - Copie para qualquer computador")
        print(f"  - Não requer Python ou dependências instaladas")
        print()
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("✗ ERRO ao gerar executável!")
        print("=" * 60)
        print()
        print(f"Erro: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

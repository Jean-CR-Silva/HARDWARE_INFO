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
        print("   PyInstaller encontrado")
    except ImportError:
        print("   PyInstaller não está instalado")
        print("   Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    print()
    print("2. Preparando arquivos...")
    
    # Diretório do projeto
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Separador de caminhos para o Windows/Unix no PyInstaller
    data_sep = ';' if os.name == 'nt' else ':'
    
    # Nome do executável final
    exe_name = "HardwareInfo.exe" if os.name == 'nt' else "HardwareInfo"
    
    # Comando PyInstaller
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=HardwareInfo",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=.",
        f"--add-data=services{data_sep}services",
        f"--add-data=ui{data_sep}ui",
        f"--add-data=utils{data_sep}utils",
        "--hidden-import=psutil",
        "--hidden-import=reportlab",
        "main.py"
    ]
    
    print()
    print("3. Gerando executável (isto pode levar alguns minutos)...")
    print()
    
    try:
        result = subprocess.run(command, check=True)
        
        print()
        print("=" * 60)
        print("SUCESSO! Executável gerado com sucesso!")
        print("=" * 60)
        print()
        print(f"Localização: {project_dir / 'dist' / exe_name}")
        print()
        print("O arquivo pode ser executado independentemente:")
        print(f"  - Copie para qualquer computador com o mesmo sistema operacional")
        print(f"  - Não requer Python ou dependências instaladas")
        print()
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("ERRO ao gerar executável!")
        print("=" * 60)
        print()
        print(f"Erro: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

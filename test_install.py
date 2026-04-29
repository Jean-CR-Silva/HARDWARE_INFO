"""
Script de teste para validar a instalação do Hardware Info System

Execute: python test_install.py
"""

import sys
import subprocess
from pathlib import Path


def test_python_version():
    """Testa versão do Python."""
    print("🔍 Testando versão do Python...", end=" ")
    
    version_info = sys.version_info
    if version_info.major == 3 and version_info.minor >= 7:
        print(f"✓ OK (Python {version_info.major}.{version_info.minor}.{version_info.micro})")
        return True
    else:
        print(f"✗ FALHOU (Python {version_info.major}.{version_info.minor} é muito antigo)")
        return False


def test_required_modules():
    """Testa módulos obrigatórios."""
    print("🔍 Testando módulos obrigatórios...", end=" ")
    
    modules = {
        'tkinter': 'Tkinter (GUI)',
        'psutil': 'psutil (Hardware info)'
    }
    
    missing = []
    for module_name, module_label in modules.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append(f"{module_label} (pip install {module_name})")
    
    if not missing:
        print("✓ OK")
        return True
    else:
        print("✗ FALHOU")
        print("   Módulos faltantes:")
        for module in missing:
            print(f"     - {module}")
        return False


def test_optional_modules():
    """Testa módulos opcionais."""
    print("🔍 Testando módulos opcionais...", end=" ")
    
    try:
        import reportlab
        print("✓ OK (reportlab disponível para PDF)")
        return True
    except ImportError:
        print("⚠ AVISO (reportlab não instalado - PDF não funcionará)")
        print("   Para instalar: pip install reportlab")
        return False


def test_imports():
    """Testa imports do projeto."""
    print("🔍 Testando imports do projeto...", end=" ")
    
    try:
        from services.hardware_info import HardwareCollector
        from ui.interface import HardwareInfoApp
        from utils.helpers import export_to_txt, export_to_pdf
        print("✓ OK")
        return True
    except ImportError as e:
        print(f"✗ FALHOU: {str(e)}")
        return False


def test_hardware_collector():
    """Testa coleta de dados."""
    print("🔍 Testando coleta de dados...", end=" ")
    
    try:
        from services.hardware_info import HardwareCollector
        
        collector = HardwareCollector()
        data = collector.collect_all()
        
        # Verificar se conseguiu coletar alguns dados
        valid_data = [v for v in data.values() if v and v != "Não disponível"]
        
        if len(valid_data) >= 3:
            print(f"✓ OK ({len(valid_data)}/7 dados coletados)")
            return True
        else:
            print(f"⚠ AVISO (Apenas {len(valid_data)}/7 dados disponíveis)")
            print("   Alguns dados de hardware podem não estar disponíveis neste sistema")
            return False
            
    except Exception as e:
        print(f"✗ FALHOU: {str(e)}")
        return False


def test_file_structure():
    """Testa estrutura de arquivos."""
    print("🔍 Testando estrutura de arquivos...", end=" ")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'services/hardware_info.py',
        'ui/interface.py',
        'utils/helpers.py',
        'README.md'
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if not missing:
        print("✓ OK")
        return True
    else:
        print("✗ FALHOU")
        print("   Arquivos faltantes:")
        for file_path in missing:
            print(f"     - {file_path}")
        return False


def test_gui_creation():
    """Testa criação da GUI (sem mostrar janela)."""
    print("🔍 Testando criação da interface gráfica...", end=" ")
    
    try:
        import tkinter as tk
        from ui.interface import HardwareInfoApp
        
        # Criar janela de teste
        root = tk.Tk()
        root.withdraw()  # Esconder janela
        
        app = HardwareInfoApp(root)
        
        # Verificar se foi criada
        if app and app.info_labels:
            print(f"✓ OK ({len(app.info_labels)} campos criados)")
            root.destroy()
            return True
        else:
            print("✗ FALHOU")
            root.destroy()
            return False
            
    except Exception as e:
        print(f"✗ FALHOU: {str(e)}")
        return False


def main():
    """Executa todos os testes."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  TESTE DE INSTALAÇÃO - HARDWARE INFO SYSTEM".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    tests = [
        ("Versão do Python", test_python_version),
        ("Módulos obrigatórios", test_required_modules),
        ("Módulos opcionais", test_optional_modules),
        ("Imports do projeto", test_imports),
        ("Estrutura de arquivos", test_file_structure),
        ("Coleta de dados", test_hardware_collector),
        ("Interface gráfica", test_gui_creation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ EXCEÇÃO: {str(e)}")
            results.append((test_name, False))
    
    # Resumo
    print("\n")
    print("=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSOU" if result else "✗ FALHOU"
        print(f"{status:10} - {test_name}")
    
    print("=" * 60)
    print(f"Total: {passed}/{total} testes passaram")
    print("=" * 60)
    print()
    
    if passed == total:
        print("✓ TUDO OK! Sistema pronto para usar.")
        print()
        print("Para iniciar a aplicação, execute:")
        print("  python main.py")
        print()
        return 0
    elif passed >= total - 1:
        print("⚠ AVISO: Alguns testes falharam, mas o sistema pode funcionar.")
        print()
        print("Se tiver problemas, execute:")
        print("  pip install -r requirements.txt")
        print()
        return 1
    else:
        print("✗ ERRO: Sistema não está pronto.")
        print()
        print("Por favor, corrija os problemas acima e tente novamente.")
        print()
        return 2


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

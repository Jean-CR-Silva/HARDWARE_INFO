"""
Script de teste para validar coleta de dados com múltiplas estratégias
Execute: python test_hardware_collection.py
"""

import subprocess
import logging
from pathlib import Path
import sys

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)-10s | %(message)s'
)
logger = logging.getLogger(__name__)


def print_section(title):
    """Imprime um separador visual."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def test_cpu_commands():
    """Testa todos os comandos para CPU."""
    print_section("TESTANDO COMANDOS PARA PROCESSADOR (CPU)")
    
    commands = {
        "WMIC cpu get name": "wmic cpu get name",
        "WMIC processor get name": "wmic processor get name",
        "PowerShell Win32_Processor": 'powershell -Command "Get-WmiObject Win32_Processor | Select-Object -ExpandProperty Name | Select-Object -First 1"',
        "Python platform.processor()": "python -c \"import platform; print(platform.processor())\"",
    }
    
    for description, command in commands.items():
        print(f"🔍 {description}")
        print(f"   Comando: {command[:60]}...")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    print(f"   ✅ SUCESSO: {output}")
                else:
                    print(f"   ⚠️  Vazio ou não encontrado")
            else:
                error = result.stderr.strip()
                if error:
                    print(f"   ❌ ERRO: {error[:60]}...")
                else:
                    print(f"   ⚠️  Comando retornou erro")
                    
        except Exception as e:
            print(f"   ❌ EXCEÇÃO: {str(e)}")
        
        print()



    """Testa todos os comandos para MAC address."""
    print_section("TESTANDO COMANDOS PARA ENDEREÇO MAC")
    
    commands = {
        "getmac (Comando Windows)": "getmac",
        "ipconfig /all (Parse)": "ipconfig /all",
        "PowerShell Get-NetAdapter": 'powershell -Command "Get-NetAdapter -Physical | Where-Object {$_.Status -eq \'Up\'} | Select-Object -ExpandProperty MacAddress | Select-Object -First 1"',
        "PowerShell Win32_NetworkAdapterConfiguration": 'powershell -Command "Get-WmiObject Win32_NetworkAdapterConfiguration -Filter \'IPEnabled=True\' | Select-Object -ExpandProperty MACAddress | Select-Object -First 1"',
    }
    
    for description, command in commands.items():
        print(f"🔍 {description}")
        print(f"   Comando: {command[:60]}...")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    print(f"   ✅ SUCESSO: {output}")
                else:
                    print(f"   ⚠️  Vazio ou não encontrado")
            else:
                error = result.stderr.strip()
                if error:
                    print(f"   ❌ ERRO: {error[:60]}...")
                else:
                    print(f"   ⚠️  Comando retornou erro")
                    
        except Exception as e:
            print(f"   ❌ EXCEÇÃO: {str(e)}")
        
        print()



    """Testa todos os comandos WMIC disponíveis."""
    print_section("TESTANDO COMANDOS WMIC")
    
    commands = {
        "Serial (WMIC BIOS)": "wmic bios get serialnumber",
        "Serial (WMIC CSProduct)": "wmic csproduct get identifyingnumber",
        "Modelo (WMIC CSProduct)": "wmic csproduct get name",
        "Modelo (WMIC ComputerSystem)": "wmic computersystem get model",
        "Fabricante (WMIC CSProduct)": "wmic csproduct get vendor",
        "Fabricante (WMIC ComputerSystem)": "wmic computersystem get manufacturer",
    }
    
    for description, command in commands.items():
        print(f"🔍 {description}")
        print(f"   Comando: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                lines = output.split('\n')
                
                if len(lines) > 1:
                    value = lines[1].strip()
                    if value:
                        print(f"   ✅ SUCESSO: {value}")
                    else:
                        print(f"   ⚠️  Vazio ou não encontrado")
                else:
                    print(f"   ⚠️  Saída inválida: {output}")
            else:
                print(f"   ❌ ERRO: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ EXCEÇÃO: {str(e)}")
        
        print()


def test_powershell_commands():
    """Testa todos os comandos PowerShell disponíveis."""
    print_section("TESTANDO COMANDOS POWERSHELL")
    
    commands = {
        "Serial (Win32_BIOS)": 'powershell -Command "Get-WmiObject Win32_BIOS | Select-Object -ExpandProperty SerialNumber"',
        "Serial (Win32_ComputerSystemProduct)": 'powershell -Command "Get-WmiObject Win32_ComputerSystemProduct | Select-Object -ExpandProperty IdentifyingNumber"',
        "Modelo (Win32_ComputerSystemProduct)": 'powershell -Command "Get-WmiObject Win32_ComputerSystemProduct | Select-Object -ExpandProperty Name"',
        "Modelo (Win32_ComputerSystem)": 'powershell -Command "Get-WmiObject Win32_ComputerSystem | Select-Object -ExpandProperty Model"',
        "Fabricante (Win32_ComputerSystemProduct)": 'powershell -Command "Get-WmiObject Win32_ComputerSystemProduct | Select-Object -ExpandProperty Vendor"',
        "Fabricante (Win32_ComputerSystem)": 'powershell -Command "Get-WmiObject Win32_ComputerSystem | Select-Object -ExpandProperty Manufacturer"',
    }
    
    for description, command in commands.items():
        print(f"🔍 {description}")
        print(f"   Comando: {command[:60]}...")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    print(f"   ✅ SUCESSO: {output}")
                else:
                    print(f"   ⚠️  Vazio ou não encontrado")
            else:
                error = result.stderr.strip()
                if error:
                    print(f"   ❌ ERRO: {error[:60]}...")
                else:
                    print(f"   ⚠️  Comando retornou erro")
                    
        except Exception as e:
            print(f"   ❌ EXCEÇÃO: {str(e)}")
        
        print()


def test_python_module():
    """Testa o módulo Python de coleta."""
    print_section("TESTANDO MÓDULO PYTHON")
    
    try:
        from services.hardware_info import HardwareCollector
        
        print("✅ Módulo importado com sucesso\n")
        
        collector = HardwareCollector()
        
        print("Coletando dados...\n")
        
        data_tests = [
            ("Número de Série", collector.get_serial),
            ("Modelo", collector.get_model),
            ("Fabricante", collector.get_manufacturer),
            ("Endereço MAC", collector.get_mac),
        ]
        
        for name, method in data_tests:
            print(f"🔍 {name}")
            try:
                result = method()
                if result:
                    print(f"   ✅ OBTIDO: {result}\n")
                else:
                    print(f"   ⚠️  Não encontrado\n")
            except Exception as e:
                print(f"   ❌ ERRO: {str(e)}\n")
        
        # Coleta total
        print("Coletando TODAS as informações...")
        all_data = collector.collect_all()
        
        print("\n📊 RESULTADO FINAL:\n")
        for key, value in all_data.items():
            print(f"  {key.ljust(15)} : {value}")
            
    except ImportError as e:
        print(f"❌ Erro ao importar módulo: {str(e)}")
    except Exception as e:
        print(f"❌ Erro ao executar: {str(e)}")


def main():
    """Função principal."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  TESTE DE COLETA DE HARDWARE - MÚLTIPLAS ESTRATÉGIAS".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    test_wmic_commands()
    test_powershell_commands()
    test_cpu_commands()
    test_mac_commands()
    test_python_module()
    
    print_section("TESTE CONCLUÍDO")
    print("✅ Se você viu valores em ✅ SUCESSO, significa que funcionam!")
    print("⚠️  Se tudo está ⚠️, o dados podem não estar disponíveis no seu hardware.")
    print("❌ Se há ❌ erros, pode ser problema de permissões.")
    print("💡 Dica: Execute como Administrador para melhor resultado!\n")


if __name__ == "__main__":
    main()

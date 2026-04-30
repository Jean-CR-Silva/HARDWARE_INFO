"""
Módulo para coleta de informações de hardware do computador.
Utiliza WMI, PowerShell e bibliotecas padrão do Python.
"""

import subprocess
import platform
import uuid
import psutil
import logging
import re
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Optional, Tuple

# Configuração de logging
logger = logging.getLogger(__name__)


class HardwareCollector:
    """Responsável por coletar informações de hardware do sistema."""

    def __init__(self):
        """Inicializa o coletor de hardware."""
        self.data = {}

    def get_serial(self) -> Optional[str]:
        """
        Coleta o número de série do computador (BIOS).
        Tenta múltiplas estratégias para garantir sucesso.
        
        Returns:
            str: Número de série da máquina
            None: Caso não consiga obter a informação
        """
        # Estratégia 1: WMIC - wmic bios get serialnumber (Windows)
        try:
            command = 'wmic bios get serialnumber'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    serial = lines[1].strip()
                    if serial and serial.lower() != "serialnumber":
                        logger.info(f"Série obtida via WMIC: {serial}")
                        return serial
        except Exception as e:
            logger.debug(f"Estratégia 1 (WMIC bios) falhou: {str(e)}")
        
        # Estratégia 2: WMIC - wmic csproduct get identifyingnumber (Windows)
        try:
            command = 'wmic csproduct get identifyingnumber'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    serial = lines[1].strip()
                    if serial and serial.lower() != "identifyingnumber":
                        logger.info(f"Série obtida via WMIC csproduct: {serial}")
                        return serial
        except Exception as e:
            logger.debug(f"Estratégia 2 (WMIC csproduct) falhou: {str(e)}")
        
        # Estratégia 3: PowerShell - Get-WmiObject Win32_BIOS (Windows)
        try:
            command = 'powershell -Command "Get-WmiObject Win32_BIOS | Select-Object -ExpandProperty SerialNumber"'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                serial = result.stdout.strip()
                if serial and serial.lower() != "serialnumber":
                    logger.info(f"Série obtida via PowerShell Win32_BIOS: {serial}")
                    return serial
        except Exception as e:
            logger.debug(f"Estratégia 3 (PowerShell Win32_BIOS) falhou: {str(e)}")
        
        # Estratégia 4: PowerShell - Get-WmiObject Win32_ComputerSystemProduct (Windows)
        try:
            command = 'powershell -Command "Get-WmiObject Win32_ComputerSystemProduct | Select-Object -ExpandProperty IdentifyingNumber"'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                serial = result.stdout.strip()
                if serial and serial.lower() != "identifyingnumber":
                    logger.info(f"Série obtida via PowerShell Win32_ComputerSystemProduct: {serial}")
                    return serial
        except Exception as e:
            logger.debug(f"Estratégia 4 (PowerShell Win32_ComputerSystemProduct) falhou: {str(e)}")
        
        # Estratégia 5: dmidecode (Linux)
        try:
            command = 'sudo dmidecode -s system-serial-number'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                serial = result.stdout.strip()
                if serial and serial.lower() not in ["", "not specified", "to be filled by o.e.m."]:
                    logger.info(f"Série obtida via dmidecode: {serial}")
                    return serial
        except Exception as e:
            logger.debug(f"Estratégia 5 (dmidecode) falhou: {str(e)}")
        
        # Estratégia 6: Arquivo do sistema /sys/class/dmi/id/product_serial (Linux)
        try:
            with open('/sys/class/dmi/id/product_serial', 'r') as f:
                serial = f.read().strip()
                if serial and serial.lower() not in ["", "not specified", "to be filled by o.e.m."]:
                    logger.info(f"Série obtida via /sys/class/dmi/id/product_serial: {serial}")
                    return serial
        except Exception as e:
            logger.debug(f"Estratégia 6 (/sys/class/dmi/id/product_serial) falhou: {str(e)}")
        
        logger.warning("Não foi possível obter número de série")
        return None

    def get_model(self) -> Optional[str]:
        """
        Coleta o modelo do computador.
        Tenta múltiplas estratégias para garantir sucesso.
        
        Returns:
            str: Modelo do computador
            None: Caso não consiga obter a informação
        """
        # Estratégia 1: WMIC - wmic csproduct get name (Windows)
        try:
            command = 'wmic csproduct get name'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    model = lines[1].strip()
                    if model and model.lower() != "name":
                        logger.info(f"Modelo obtido via WMIC csproduct: {model}")
                        return model
        except Exception as e:
            logger.debug(f"Estratégia 1 (WMIC csproduct) falhou: {str(e)}")
        
        # Estratégia 2: WMIC - wmic computersystem get model (Windows)
        try:
            command = 'wmic computersystem get model'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    model = lines[1].strip()
                    if model and model.lower() != "model":
                        logger.info(f"Modelo obtido via WMIC computersystem: {model}")
                        return model
        except Exception as e:
            logger.debug(f"Estratégia 2 (WMIC computersystem) falhou: {str(e)}")
        
        # Estratégia 3: PowerShell - Get-WmiObject Win32_ComputerSystemProduct (Windows)
        try:
            command = 'powershell -Command "Get-WmiObject Win32_ComputerSystemProduct | Select-Object -ExpandProperty Name"'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                model = result.stdout.strip()
                if model and model.lower() != "name":
                    logger.info(f"Modelo obtido via PowerShell Win32_ComputerSystemProduct: {model}")
                    return model
        except Exception as e:
            logger.debug(f"Estratégia 3 (PowerShell Win32_ComputerSystemProduct) falhou: {str(e)}")
        
        # Estratégia 4: PowerShell - Get-WmiObject Win32_ComputerSystem (Windows)
        try:
            command = 'powershell -Command "Get-WmiObject Win32_ComputerSystem | Select-Object -ExpandProperty Model"'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                model = result.stdout.strip()
                if model and model.lower() != "model":
                    logger.info(f"Modelo obtido via PowerShell Win32_ComputerSystem: {model}")
                    return model
        except Exception as e:
            logger.debug(f"Estratégia 4 (PowerShell Win32_ComputerSystem) falhou: {str(e)}")
        
        # Estratégia 5: dmidecode (Linux)
        try:
            command = 'sudo dmidecode -s system-product-name'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                model = result.stdout.strip()
                if model and model.lower() not in ["", "not specified", "to be filled by o.e.m."]:
                    logger.info(f"Modelo obtido via dmidecode: {model}")
                    return model
        except Exception as e:
            logger.debug(f"Estratégia 5 (dmidecode) falhou: {str(e)}")
        
        # Estratégia 6: Arquivo do sistema /sys/class/dmi/id/product_name (Linux)
        try:
            with open('/sys/class/dmi/id/product_name', 'r') as f:
                model = f.read().strip()
                if model and model.lower() not in ["", "not specified", "to be filled by o.e.m."]:
                    logger.info(f"Modelo obtido via /sys/class/dmi/id/product_name: {model}")
                    return model
        except Exception as e:
            logger.debug(f"Estratégia 6 (/sys/class/dmi/id/product_name) falhou: {str(e)}")
        
        logger.warning("Não foi possível obter modelo do computador")
        return None

    def get_manufacturer(self) -> Optional[str]:
        """
        Coleta o fabricante do computador.
        Tenta múltiplas estratégias para garantir sucesso.
        
        Returns:
            str: Fabricante do computador
            None: Caso não consiga obter a informação
        """
        # Estratégia 1: WMIC - wmic csproduct get vendor
        try:
            command = 'wmic csproduct get vendor'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    manufacturer = lines[1].strip()
                    if manufacturer and manufacturer.lower() != "vendor":
                        logger.info(f"Fabricante obtido via WMIC csproduct: {manufacturer}")
                        return manufacturer
        except Exception as e:
            logger.debug(f"Estratégia 1 (WMIC csproduct vendor) falhou: {str(e)}")
        
        # Estratégia 2: WMIC - wmic computersystem get manufacturer
        try:
            command = 'wmic computersystem get manufacturer'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    manufacturer = lines[1].strip()
                    if manufacturer and manufacturer.lower() != "manufacturer":
                        logger.info(f"Fabricante obtido via WMIC computersystem: {manufacturer}")
                        return manufacturer
        except Exception as e:
            logger.debug(f"Estratégia 2 (WMIC computersystem) falhou: {str(e)}")
        
        # Estratégia 3: PowerShell - Get-WmiObject Win32_ComputerSystemProduct
        try:
            command = 'powershell -Command "Get-WmiObject Win32_ComputerSystemProduct | Select-Object -ExpandProperty Vendor"'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                manufacturer = result.stdout.strip()
                if manufacturer and manufacturer.lower() != "vendor":
                    logger.info(f"Fabricante obtido via PowerShell Win32_ComputerSystemProduct: {manufacturer}")
                    return manufacturer
        except Exception as e:
            logger.debug(f"Estratégia 3 (PowerShell Win32_ComputerSystemProduct) falhou: {str(e)}")
        
        # Estratégia 4: PowerShell - Get-WmiObject Win32_ComputerSystem
        try:
            command = 'powershell -Command "Get-WmiObject Win32_ComputerSystem | Select-Object -ExpandProperty Manufacturer"'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                manufacturer = result.stdout.strip()
                if manufacturer and manufacturer.lower() != "manufacturer":
                    logger.info(f"Fabricante obtido via PowerShell Win32_ComputerSystem: {manufacturer}")
                    return manufacturer
        except Exception as e:
            logger.debug(f"Estratégia 4 (PowerShell Win32_ComputerSystem) falhou: {str(e)}")
        
        # Estratégia 5: dmidecode (Linux)
        try:
            command = 'sudo dmidecode -s system-manufacturer'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                manufacturer = result.stdout.strip()
                if manufacturer and manufacturer.lower() not in ["", "not specified", "to be filled by o.e.m."]:
                    logger.info(f"Fabricante obtido via dmidecode: {manufacturer}")
                    return manufacturer
        except Exception as e:
            logger.debug(f"Estratégia 5 (dmidecode) falhou: {str(e)}")
        
        # Estratégia 6: Arquivo do sistema /sys/class/dmi/id/sys_vendor (Linux)
        try:
            with open('/sys/class/dmi/id/sys_vendor', 'r') as f:
                manufacturer = f.read().strip()
                if manufacturer and manufacturer.lower() not in ["", "not specified", "to be filled by o.e.m."]:
                    logger.info(f"Fabricante obtido via /sys/class/dmi/id/sys_vendor: {manufacturer}")
                    return manufacturer
        except Exception as e:
            logger.debug(f"Estratégia 6 (/sys/class/dmi/id/sys_vendor) falhou: {str(e)}")
        
        logger.warning("Não foi possível obter fabricante do computador")
        return None

    def get_cpu(self) -> Optional[str]:
        """
        Coleta informações do processador (CPU) com núcleos e threads.
        Tenta múltiplas estratégias para obter o nome e especificações.
        
        Returns:
            str: Modelo do processador com núcleos e threads
            None: Caso não consiga obter a informação
        """
        cpu_name = None
        
        # Estratégia 1: WMIC - wmic cpu get name
        try:
            command = 'wmic cpu get name'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    name = lines[1].strip()
                    if name and name.lower() != "name":
                        cpu_name = name
                        logger.info(f"CPU obtida via WMIC: {cpu_name}")
        except Exception as e:
            logger.debug(f"Estratégia 1 (WMIC cpu name) falhou: {str(e)}")
        
        # Estratégia 2: WMIC - wmic processor get name
        if not cpu_name:
            try:
                command = 'wmic processor get name'
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        name = lines[1].strip()
                        if name and name.lower() != "name":
                            cpu_name = name
                            logger.info(f"CPU obtida via WMIC processor: {cpu_name}")
            except Exception as e:
                logger.debug(f"Estratégia 2 (WMIC processor name) falhou: {str(e)}")
        
        # Estratégia 3: PowerShell Win32_Processor
        if not cpu_name:
            try:
                command = 'powershell -Command "Get-WmiObject Win32_Processor | Select-Object -ExpandProperty Name | Select-Object -First 1"'
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    name = result.stdout.strip()
                    if name and name.lower() != "name":
                        cpu_name = name
                        logger.info(f"CPU obtida via PowerShell Win32_Processor: {cpu_name}")
            except Exception as e:
                logger.debug(f"Estratégia 3 (PowerShell Win32_Processor) falhou: {str(e)}")
        
        # Estratégia 4: Python platform.processor()
        if not cpu_name:
            try:
                name = platform.processor()
                if name and name.strip():
                    cpu_name = name
                    logger.info(f"CPU obtida via platform.processor(): {cpu_name}")
            except Exception as e:
                logger.debug(f"Estratégia 4 (platform.processor) falhou: {str(e)}")
        
        # Se nenhuma estratégia funcionou, usar valor padrão
        if not cpu_name:
            cpu_name = "Processador Desconhecido"
            logger.warning("Não foi possível obter nome da CPU")
        
        # Sempre obter núcleos e threads
        try:
            cpu_count = psutil.cpu_count(logical=False) or 1
            logical_count = psutil.cpu_count(logical=True) or 1
            
            # Formatar saída clara e legível
            return f"{cpu_name} | {cpu_count} núcleo(s) | {logical_count} thread(s)"
        except Exception as e:
            logger.error(f"Erro ao obter contagem de núcleos: {str(e)}")
            return cpu_name

    def get_ram(self) -> Optional[str]:
        """
        Coleta informações de memória RAM.
        
        Returns:
            str: Quantidade de RAM em GB
            None: Caso não consiga obter a informação
        """
        try:
            # Obtém a memória total usando psutil
            ram_bytes = psutil.virtual_memory().total
            ram_gb = ram_bytes / (1024 ** 3)  # Converte para GB
            
            return f"{ram_gb:.2f} GB"
        except Exception as e:
            logger.error(f"Erro ao obter RAM: {str(e)}")
            return None

    def get_mac(self) -> Optional[str]:
        """
        Coleta o endereço MAC (Media Access Control) da máquina.
        Tenta múltiplas estratégias para garantir sucesso.
        
        Returns:
            str: Endereço MAC formatado (XX-XX-XX-XX-XX-XX)
            None: Caso não consiga obter a informação
        """
        # Estratégia 1: getmac - Comando Windows nativo
        try:
            command = 'getmac'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 0:
                    # Extrai o primeiro MAC address encontrado (que não seja header)
                    for line in lines:
                        line = line.strip()
                        if line and line != "Physical Address" and line != "Physical":
                            # Tira espaços e busca o padrão XX-XX-XX-XX-XX-XX
                            parts = line.split()
                            if parts:
                                mac = parts[0]
                                if self._is_valid_mac(mac):
                                    logger.info(f"MAC obtido via getmac: {mac}")
                                    return mac
        except Exception as e:
            logger.debug(f"Estratégia 1 (getmac) falhou: {str(e)}")
        
        # Estratégia 2: ipconfig /all - Parse de saída
        try:
            command = 'ipconfig /all'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    # Procura por "Physical Address" ou "Endereço Físico"
                    if 'Physical Address' in line or 'Endereço Físico' in line:
                        # Extrai o MAC (após o ":")
                        parts = line.split(':')
                        if len(parts) > 1:
                            mac = parts[-1].strip()
                            if self._is_valid_mac(mac):
                                logger.info(f"MAC obtido via ipconfig /all: {mac}")
                                return mac
        except Exception as e:
            logger.debug(f"Estratégia 2 (ipconfig /all) falhou: {str(e)}")
        
        # Estratégia 3: PowerShell Get-NetAdapter
        try:
            command = 'powershell -Command "Get-NetAdapter -Physical | Where-Object {$_.Status -eq \'Up\'} | Select-Object -ExpandProperty MacAddress | Select-Object -First 1"'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                mac = result.stdout.strip()
                if mac and self._is_valid_mac(mac):
                    logger.info(f"MAC obtido via PowerShell Get-NetAdapter: {mac}")
                    return mac
        except Exception as e:
            logger.debug(f"Estratégia 3 (PowerShell Get-NetAdapter) falhou: {str(e)}")
        
        # Estratégia 4: PowerShell Win32_NetworkAdapterConfiguration
        try:
            command = 'powershell -Command "Get-WmiObject Win32_NetworkAdapterConfiguration -Filter \'IPEnabled=True\' | Select-Object -ExpandProperty MACAddress | Select-Object -First 1"'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                mac = result.stdout.strip()
                if mac and self._is_valid_mac(mac):
                    logger.info(f"MAC obtido via PowerShell Win32_NetworkAdapterConfiguration: {mac}")
                    return mac
        except Exception as e:
            logger.debug(f"Estratégia 4 (PowerShell Win32_NetworkAdapterConfiguration) falhou: {str(e)}")
        
        # Estratégia 5: ip link show (Linux)
        try:
            command = 'ip link show'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    # Procura por link/ether
                    if 'link/ether' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            mac = parts[1]
                            if self._is_valid_mac(mac):
                                # Converte para formato Windows (XX-XX-XX-XX-XX-XX)
                                mac = mac.replace(':', '-').upper()
                                logger.info(f"MAC obtido via ip link show: {mac}")
                                return mac
        except Exception as e:
            logger.debug(f"Estratégia 5 (ip link show) falhou: {str(e)}")
        
        # Estratégia 6: ifconfig (Linux - alternativa)
        try:
            command = 'ifconfig'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    # Procura por HWaddr ou ether
                    if 'HWaddr' in line or 'ether' in line:
                        parts = line.split()
                        for part in parts:
                            if self._is_valid_mac(part):
                                # Converte para formato Windows (XX-XX-XX-XX-XX-XX)
                                mac = part.replace(':', '-').upper()
                                logger.info(f"MAC obtido via ifconfig: {mac}")
                                return mac
        except Exception as e:
            logger.debug(f"Estratégia 6 (ifconfig) falhou: {str(e)}")
        
        # Estratégia 7: Python uuid.getnode()
        try:
            mac_int = uuid.getnode()
            # Verifica se é um MAC real (não gerado)
            if mac_int != 0 and mac_int != -1 and mac_int != (1 << 40) - 1:
                # Converte para formato XX-XX-XX-XX-XX-XX
                mac = ':'.join(['{:02x}'.format((mac_int >> (i * 8)) & 0xff) for i in reversed(range(6))])
                # Converte para XX-XX-XX-XX-XX-XX (Windows format)
                mac = mac.replace(':', '-').upper()
                logger.info(f"MAC obtido via uuid.getnode(): {mac}")
                return mac
        except Exception as e:
            logger.debug(f"Estratégia 5 (uuid.getnode()) falhou: {str(e)}")
        
        logger.warning("Não foi possível obter endereço MAC")
        return None
    
    def _is_valid_mac(self, mac: str) -> bool:
        """
        Valida se uma string é um endereço MAC válido.
        
        Args:
            mac (str): String a validar
            
        Returns:
            bool: True se é MAC válido, False caso contrário
        """
        # Padrão: XX-XX-XX-XX-XX-XX ou XX:XX:XX:XX:XX:XX
        pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        return bool(re.match(pattern, mac))

    def get_os_info(self) -> Optional[str]:
        """
        Coleta informações do sistema operacional.
        
        Returns:
            str: Nome e versão do SO
            None: Caso não consiga obter a informação
        """
        try:
            system = platform.system()
            release = platform.release()
            version = platform.version()
            
            return f"{system} {release} ({version})"
        except Exception as e:
            logger.error(f"Erro ao obter SO: {str(e)}")
            return None
    def get_host_name(self) -> Optional[str]:
        """
        Coleta o nome do host / nome do computador.
        
        Returns:
            str: Nome do host
            None: Caso não consiga obter a informação
        """
        try:
            host_name = platform.node() or None
            if host_name:
                logger.info(f"Host obtido: {host_name}")
                return host_name
            logger.warning("Nome do host não disponível")
            return None
        except Exception as e:
            logger.error(f"Erro ao obter nome do host: {str(e)}")
            return None
    def _parse_battery_report(self, xml_file: str) -> Tuple[Optional[float], Optional[str]]:
        """
        Faz o parsing do arquivo HTML/XML gerado pelo powercfg /batteryreport.
        
        Args:
            xml_file (str): Caminho do arquivo
            
        Returns:
            Tuple: (health_percentage, status) ou (None, None) em caso de erro
        """
        try:
            # Ler o arquivo com tratamento de encoding
            with open(xml_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Usar regex para extrair Design Capacity e Full Charge Capacity
            # O arquivo é HTML/XHTML e contém valores como:
            # <span class="label">DESIGN CAPACITY</span></td><td>40.466 mWh
            # <span class="label">FULL CHARGE CAPACITY</span></td><td>28.204 mWh
            
            # Padrão 1: Procurar por "DESIGN CAPACITY" seguido de números
            design_pattern = r'DESIGN\s+CAPACITY</span>\s*</td>\s*<td[^>]*>([0-9.]+)\s*mWh'
            design_match = re.search(design_pattern, content, re.IGNORECASE)
            
            # Padrão 2: Procurar por "FULL CHARGE CAPACITY" seguido de números
            full_charge_pattern = r'FULL\s+CHARGE\s+CAPACITY</span>\s*</td>\s*<td[^>]*>([0-9.]+)\s*mWh'
            full_charge_match = re.search(full_charge_pattern, content, re.IGNORECASE)
            
            if not design_match or not full_charge_match:
                logger.warning("Não foi possível encontrar Design ou Full Charge Capacity no arquivo")
                logger.debug(f"Design match: {design_match}, Full charge match: {full_charge_match}")
                return None, None
            
            try:
                design_capacity = float(design_match.group(1))
                full_charge_capacity = float(full_charge_match.group(1))
            except (ValueError, IndexError) as e:
                logger.warning(f"Erro ao converter capacidades para float: {e}")
                return None, None
            
            if design_capacity <= 0:
                logger.warning("Design capacity é zero ou negativo")
                return None, None
            
            # Calcular porcentagem de saúde
            health_percentage = (full_charge_capacity / design_capacity) * 100
            
            # Determinar status
            if health_percentage >= 80:
                status = "✅ Boa"
            elif health_percentage >= 60:
                status = "⚠️ Regular"
            else:
                status = "❌ Necessária Troca"
            
            logger.info(f"Saúde da bateria: {health_percentage:.1f}% - {status}")
            return health_percentage, status
        
        except Exception as e:
            logger.error(f"Erro ao processar arquivo de bateria: {str(e)}")
            return None, None

    def get_battery_health(self) -> Optional[str]:
        """
        Coleta informações de saúde da bateria.
        Tenta múltiplas estratégias para Windows e Linux.
        
        Returns:
            str: Informações de saúde da bateria com porcentagem e status
            None: Caso não consiga obter a informação ou não haja bateria
        """
        # Estratégia 1: Windows - powercfg /batteryreport
        try:
            # Criar arquivo temporário para armazenar o relatório
            with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as temp_file:
                temp_xml_path = temp_file.name
            
            try:
                # Executar comando powercfg /batteryreport
                command = f'powercfg /batteryreport /output "{temp_xml_path}"'
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    logger.warning(f"Powercfg retornou código {result.returncode}: {result.stderr}")
                    # Em alguns casos (desktop sem bateria), o comando pode falhar
                    return "Sem bateria (Desktop)"
                
                # Fazer parsing do arquivo XML
                health_percentage, status = self._parse_battery_report(temp_xml_path)
                
                if health_percentage is None:
                    return "Informação não disponível"
                
                # Formatar saída
                return f"{health_percentage:.1f}% - {status}"
            
            finally:
                # Limpar arquivo temporário
                try:
                    Path(temp_xml_path).unlink()
                except Exception as e:
                    logger.debug(f"Erro ao deletar arquivo temporário: {str(e)}")
        
        except Exception as e:
            logger.debug(f"Estratégia 1 (powercfg) falhou: {str(e)}")
        
        # Estratégia 2: Linux - upower
        try:
            command = 'upower -e'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                battery_path = None
                for line in lines:
                    if 'battery' in line:
                        battery_path = line.strip()
                        break
                
                if battery_path:
                    # Obter informações detalhadas da bateria
                    command = f'upower -i {battery_path}'
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.returncode == 0:
                        output = result.stdout
                        # Procurar por capacity ou energy-full-design
                        capacity_match = re.search(r'capacity:\s*([0-9.]+)%', output, re.IGNORECASE)
                        if capacity_match:
                            capacity = float(capacity_match.group(1))
                            if capacity >= 80:
                                status = "✅ Boa"
                            elif capacity >= 60:
                                status = "⚠️ Regular"
                            else:
                                status = "❌ Necessária Troca"
                            
                            logger.info(f"Saúde da bateria via upower: {capacity:.1f}% - {status}")
                            return f"{capacity:.1f}% - {status}"
        
        except Exception as e:
            logger.debug(f"Estratégia 2 (upower) falhou: {str(e)}")
        
        # Estratégia 3: Linux - Arquivos do sistema /sys/class/power_supply/
        try:
            battery_dirs = list(Path('/sys/class/power_supply').glob('BAT*'))
            if battery_dirs:
                battery_dir = battery_dirs[0]  # Usar primeira bateria encontrada
                
                # Ler capacidade de design
                design_file = battery_dir / 'energy_full_design'
                if not design_file.exists():
                    design_file = battery_dir / 'charge_full_design'
                
                # Ler capacidade atual
                full_file = battery_dir / 'energy_full'
                if not full_file.exists():
                    full_file = battery_dir / 'charge_full'
                
                if design_file.exists() and full_file.exists():
                    with open(design_file, 'r') as f:
                        design_capacity = int(f.read().strip())
                    
                    with open(full_file, 'r') as f:
                        full_capacity = int(f.read().strip())
                    
                    if design_capacity > 0:
                        health_percentage = (full_capacity / design_capacity) * 100
                        
                        if health_percentage >= 80:
                            status = "✅ Boa"
                        elif health_percentage >= 60:
                            status = "⚠️ Regular"
                        else:
                            status = "❌ Necessária Troca"
                        
                        logger.info(f"Saúde da bateria via /sys/class/power_supply: {health_percentage:.1f}% - {status}")
                        return f"{health_percentage:.1f}% - {status}"
        
        except Exception as e:
            logger.debug(f"Estratégia 3 (/sys/class/power_supply) falhou: {str(e)}")
        
        # Estratégia 4: Verificar se há bateria usando psutil
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return "Sem bateria (Desktop)"
            else:
                # Se chegou aqui, há bateria mas não conseguimos obter saúde
                return "Informação não disponível"
        except Exception as e:
            logger.debug(f"Estratégia 4 (psutil) falhou: {str(e)}")
        
        logger.warning("Não foi possível obter saúde da bateria")
        return None

    def collect_all(self) -> Dict[str, Optional[str]]:
        """
        Coleta todas as informações de hardware.
        
        Returns:
            dict: Dicionário com todas as informações coletadas
        """
        self.data = {
            "serial": self.get_serial() or "Não disponível",
            "model": self.get_model() or "Não disponível",
            "manufacturer": self.get_manufacturer() or "Não disponível",
            "host": self.get_host_name() or "Não disponível",
            "cpu": self.get_cpu() or "Não disponível",
            "ram": self.get_ram() or "Não disponível",
            "mac": self.get_mac() or "Não disponível",
            "os": self.get_os_info() or "Não disponível",
            "battery": self.get_battery_health() or "Não disponível"
        }
        
        return self.data

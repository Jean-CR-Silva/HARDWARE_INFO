"""
Arquivo principal da aplicação.
Inicializa e executa o sistema de informações de hardware.
"""

import tkinter as tk
import logging
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from ui.interface import HardwareInfoApp

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Função principal da aplicação."""
    try:
        logger.info("Iniciando aplicação de Informações de Hardware...")
        
        # Criar janela raiz
        root = tk.Tk()
        
        # Criar e executar aplicação
        app = HardwareInfoApp(root)
        app.run()
        
    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {str(e)}")
        raise


if __name__ == "__main__":
    main()

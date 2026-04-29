"""
Módulo com funções auxiliares para o sistema.
"""

import os
from datetime import datetime
from typing import Optional


def ensure_dir_exists(directory: str) -> None:
    """
    Garante que um diretório existe, criando-o se necessário.
    
    Args:
        directory (str): Caminho do diretório
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def export_to_txt(data: dict, filename: str = "hardware_info.txt") -> bool:
    """
    Exporta as informações de hardware para um arquivo TXT.
    
    Args:
        data (dict): Dicionário com as informações
        filename (str): Nome do arquivo de saída
        
    Returns:
        bool: True se exportado com sucesso, False caso contrário
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("RELATÓRIO DE INFORMAÇÕES DE HARDWARE\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            f.write("INFORMAÇÕES DO SISTEMA:\n")
            f.write("-" * 60 + "\n")
            
            for key, value in data.items():
                label = get_label_for_key(key)
                f.write(f"{label}: {value}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("Fim do Relatório\n")
            f.write("=" * 60 + "\n")
        
        return True
    except Exception as e:
        print(f"Erro ao exportar para TXT: {str(e)}")
        return False


def export_to_pdf(data: dict, filename: str = "hardware_info.pdf") -> bool:
    """
    Exporta as informações de hardware para um arquivo PDF.
    Requer a biblioteca reportlab.
    
    Args:
        data (dict): Dicionário com as informações
        filename (str): Nome do arquivo de saída
        
    Returns:
        bool: True se exportado com sucesso, False caso contrário
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        # Criar PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=20
        )
        
        # Título
        title = Paragraph("RELATÓRIO DE INFORMAÇÕES DE HARDWARE", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Data
        date_text = Paragraph(
            f"<b>Data/Hora:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            styles['Normal']
        )
        elements.append(date_text)
        elements.append(Spacer(1, 12))
        
        # Tabela com dados
        table_data = [['Informação', 'Valor']]
        for key, value in data.items():
            label = get_label_for_key(key)
            table_data.append([label, value])
        
        table = Table(table_data, colWidths=[200, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        
        elements.append(table)
        
        # Gerar PDF
        doc.build(elements)
        return True
        
    except ImportError:
        print("Erro: A biblioteca 'reportlab' não está instalada. Use 'pip install reportlab'")
        return False
    except Exception as e:
        print(f"Erro ao exportar para PDF: {str(e)}")
        return False


def get_label_for_key(key: str) -> str:
    """
    Retorna um rótulo amigável para cada chave de dados.
    
    Args:
        key (str): Chave do dicionário
        
    Returns:
        str: Rótulo formatado
    """
    labels = {
        "serial": "Número de Série (BIOS)",
        "model": "Modelo do Computador",
        "manufacturer": "Fabricante",
        "cpu": "Processador (CPU)",
        "ram": "Memória RAM",
        "mac": "Endereço MAC",
        "os": "Sistema Operacional"
    }
    
    return labels.get(key, key.replace("_", " ").title())


def format_info_for_display(key: str, value: str) -> tuple:
    """
    Formata informações para exibição na interface.
    
    Args:
        key (str): Chave da informação
        value (str): Valor da informação
        
    Returns:
        tuple: (label, value) formatados
    """
    label = get_label_for_key(key)
    return (label, value)

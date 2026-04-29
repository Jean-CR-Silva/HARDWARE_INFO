"""
EXEMPLOS DE USO - Hardware Info System

Este arquivo demonstra como usar a biblioteca programaticamente.
Você pode usar os módulos de forma independente sem precisar da interface gráfica.
"""

# ============================================================================
# EXEMPLO 1: Uso Básico - Coletar Todas as Informações
# ============================================================================

from services.hardware_info import HardwareCollector

def exemplo_basico():
    """Exemplo básico de coleta de dados."""
    print("=" * 60)
    print("EXEMPLO 1: Uso Básico")
    print("=" * 60)
    print()
    
    # Criar coletor
    collector = HardwareCollector()
    
    # Coletar todas as informações
    dados = collector.collect_all()
    
    # Exibir dados
    for chave, valor in dados.items():
        print(f"{chave:20} : {valor}")
    
    print()


# ============================================================================
# EXEMPLO 2: Coletar Dados Específicos
# ============================================================================

def exemplo_especifico():
    """Exemplo coletando apenas dados específicos."""
    print("=" * 60)
    print("EXEMPLO 2: Dados Específicos")
    print("=" * 60)
    print()
    
    collector = HardwareCollector()
    
    # Coletar apenas o que você precisa
    print(f"Processador: {collector.get_cpu()}")
    print(f"RAM: {collector.get_ram()}")
    print(f"Modelo: {collector.get_model()}")
    
    print()


# ============================================================================
# EXEMPLO 3: Exportar para Arquivo TXT
# ============================================================================

def exemplo_export_txt():
    """Exemplo exportando dados para arquivo TXT."""
    print("=" * 60)
    print("EXEMPLO 3: Exportar para TXT")
    print("=" * 60)
    print()
    
    from utils.helpers import export_to_txt
    
    collector = HardwareCollector()
    dados = collector.collect_all()
    
    # Exportar
    sucesso = export_to_txt(dados, "meu_hardware.txt")
    
    if sucesso:
        print("✓ Arquivo 'meu_hardware.txt' criado com sucesso!")
    else:
        print("✗ Erro ao criar arquivo")
    
    print()


# ============================================================================
# EXEMPLO 4: Exportar para Arquivo PDF
# ============================================================================

def exemplo_export_pdf():
    """Exemplo exportando dados para arquivo PDF."""
    print("=" * 60)
    print("EXEMPLO 4: Exportar para PDF")
    print("=" * 60)
    print()
    
    from utils.helpers import export_to_pdf
    
    collector = HardwareCollector()
    dados = collector.collect_all()
    
    # Exportar
    sucesso = export_to_pdf(dados, "meu_hardware.pdf")
    
    if sucesso:
        print("✓ Arquivo 'meu_hardware.pdf' criado com sucesso!")
    else:
        print("✗ Erro ao criar arquivo (reportlab não instalado?)")
    
    print()


# ============================================================================
# EXEMPLO 5: Capturar Erros e Valores Padrão
# ============================================================================

def exemplo_tratamento_erros():
    """Exemplo mostrando tratamento de erros."""
    print("=" * 60)
    print("EXEMPLO 5: Tratamento de Erros")
    print("=" * 60)
    print()
    
    collector = HardwareCollector()
    
    # Se algum dado não está disponível, será retornado None
    cpu = collector.get_cpu()
    
    if cpu:
        print(f"✓ CPU encontrada: {cpu}")
    else:
        print("✗ CPU não disponível")
    
    # Na coleta total, valores não disponíveis são substituídos por "Não disponível"
    dados = collector.collect_all()
    print(f"Endereço MAC: {dados['mac']}")
    
    print()


# ============================================================================
# EXEMPLO 6: Reutilizar Dados Coletados
# ============================================================================

def exemplo_reutilizar():
    """Exemplo reutilizando dados coletados."""
    print("=" * 60)
    print("EXEMPLO 6: Reutilizar Dados")
    print("=" * 60)
    print()
    
    from utils.helpers import get_label_for_key
    
    collector = HardwareCollector()
    dados = collector.collect_all()
    
    # Acessar dados armazenados
    print("Dados armazenados no coletor:")
    for chave in ["serial", "model", "cpu", "ram", "mac"]:
        if chave in collector.data:
            label = get_label_for_key(chave)
            valor = collector.data[chave]
            print(f"  {label}: {valor}")
    
    print()


# ============================================================================
# EXEMPLO 7: Loop - Atualizar Dados Periodicamente
# ============================================================================

def exemplo_loop():
    """Exemplo coletando dados em loop."""
    print("=" * 60)
    print("EXEMPLO 7: Loop de Atualização")
    print("=" * 60)
    print()
    
    import time
    
    collector = HardwareCollector()
    
    # Coletar 3 vezes com intervalo
    for i in range(3):
        print(f"Coleta #{i+1}")
        dados = collector.collect_all()
        print(f"  RAM: {dados['ram']}")
        
        if i < 2:
            time.sleep(2)  # Aguardar 2 segundos
    
    print()


# ============================================================================
# EXEMPLO 8: Criar Relatório Customizado
# ============================================================================

def exemplo_relatorio_customizado():
    """Exemplo criando relatório customizado."""
    print("=" * 60)
    print("EXEMPLO 8: Relatório Customizado")
    print("=" * 60)
    print()
    
    from datetime import datetime
    
    collector = HardwareCollector()
    dados = collector.collect_all()
    
    # Criar relatório customizado
    with open("relatorio_customizado.txt", "w", encoding="utf-8") as f:
        f.write("RELATÓRIO CUSTOMIZADO DE HARDWARE\n")
        f.write("=" * 50 + "\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("IDENTIFICAÇÃO DA MÁQUINA:\n")
        f.write(f"  • Serial: {dados['serial']}\n")
        f.write(f"  • Modelo: {dados['model']}\n")
        f.write(f"  • Fabricante: {dados['manufacturer']}\n\n")
        
        f.write("ESPECIFICAÇÕES:\n")
        f.write(f"  • CPU: {dados['cpu']}\n")
        f.write(f"  • RAM: {dados['ram']}\n")
        f.write(f"  • MAC: {dados['mac']}\n")
        f.write(f"  • SO: {dados['os']}\n")
    
    print("✓ Relatório 'relatorio_customizado.txt' criado!")
    print()


# ============================================================================
# MAIN - Executar exemplos
# ============================================================================

if __name__ == "__main__":
    """Executa todos os exemplos."""
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  EXEMPLOS DE USO - HARDWARE INFO SYSTEM".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    try:
        # Executar exemplos
        exemplo_basico()
        exemplo_especifico()
        exemplo_export_txt()
        exemplo_export_pdf()
        exemplo_tratamento_erros()
        exemplo_reutilizar()
        exemplo_loop()
        exemplo_relatorio_customizado()
        
        print("=" * 60)
        print("✓ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print("=" * 60)
        print()
        print("Para mais informações, consulte:")
        print("  - README.md (documentação completa)")
        print("  - DEVELOPMENT.md (detalhes técnicos)")
        print("  - Código-fonte comentado")
        print()
        
    except Exception as e:
        print(f"\n✗ ERRO: {str(e)}\n")
        import traceback
        traceback.print_exc()

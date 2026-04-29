# Configuração de Desenvolvimento

## Estrutura do Projeto

```
hardware_info_system/
│
├── main.py                      # Arquivo principal - ponto de entrada
├── build_exe.py                 # Script para gerar executável
├── run.bat                      # Script para executar (Windows - Batch)
├── run.ps1                      # Script para executar (Windows - PowerShell)
├── requirements.txt             # Dependências do projeto
│
├── README.md                    # Documentação completa
├── QUICK_START.md              # Guia de início rápido
├── DEVELOPMENT.md              # Este arquivo
│
├── services/
│   ├── __init__.py             # Pacote Python
│   └── hardware_info.py        # Coleta de dados via WMI e subprocess
│
├── ui/
│   ├── __init__.py             # Pacote Python
│   └── interface.py            # Interface Tkinter
│
└── utils/
    ├── __init__.py             # Pacote Python
    └── helpers.py              # Funções auxiliares (export TXT/PDF)
```

---

## Descrição dos Módulos

### `services/hardware_info.py`
**Responsabilidade:** Coleta de informações de hardware

**Classe Principal:**
- `HardwareCollector`: Coleta dados usando WMI (Windows Management Instrumentation)

**Métodos Públicos:**
```python
get_serial()          # Número de série (BIOS)
get_model()           # Modelo do computador
get_manufacturer()    # Fabricante
get_cpu()            # Processador com núcleos/threads
get_ram()            # Memória RAM em GB
get_mac()            # Endereço MAC
get_os_info()        # Sistema Operacional
collect_all()        # Coleta TODAS as informações
```

**Dependências:**
- `subprocess`: Execução de comandos WMI
- `psutil`: Informações de CPU e RAM
- `platform`: Informações do SO
- `logging`: Registra erros

---

### `ui/interface.py`
**Responsabilidade:** Interface gráfica

**Classe Principal:**
- `HardwareInfoApp`: Aplicação Tkinter

**Recursos:**
- Layout responsivo com frames
- 7 campos de informação com auto-atualização
- 3 botões de ação (Coletar, Exportar TXT, Exportar PDF)
- Threading para não travar a UI durante coleta
- Dialogs para feedback do usuário
- Hover effects nos botões

**Métodos Principais:**
```python
create_widgets()            # Cria interface
on_collect_clicked()        # Clique no botão "Coletar"
collect_hardware_info()     # Coleta dados (thread)
update_ui()                 # Atualiza labels
on_export_txt_clicked()     # Exporta TXT
on_export_pdf_clicked()     # Exporta PDF
```

---

### `utils/helpers.py`
**Responsabilidade:** Funções auxiliares

**Funções:**
```python
ensure_dir_exists()         # Cria diretório se não existe
export_to_txt()            # Exporta para arquivo TXT
export_to_pdf()            # Exporta para arquivo PDF (requer reportlab)
get_label_for_key()        # Retorna rótulo formatado
format_info_for_display()   # Formata informação para UI
```

---

## Fluxo de Execução

```
main.py
  └─> HardwareInfoApp(root)
      └─> create_widgets()
          ├─> Header (título)
          ├─> Campos de informação (labels)
          └─> Botões de ação
      
      └─> on_collect_clicked()
          └─> threading.Thread(collect_hardware_info())
              └─> HardwareCollector.collect_all()
                  ├─> get_serial()
                  ├─> get_model()
                  ├─> get_cpu()
                  ├─> get_ram()
                  ├─> get_mac()
                  └─> ... etc
              
              └─> update_ui()
                  └─> Atualiza labels com dados
```

---

## Detalhes de Implementação

### Coleta de Dados (Windows)

**WMI (Windows Management Instrumentation):**
```
wmic bios get serialnumber         -> Serial
wmic csproduct get vendor          -> Fabricante
wmic csproduct get name            -> Modelo
wmic cpu get name                  -> CPU
getmac                             -> MAC Address
```

**Bibliotecas Python:**
```
psutil.cpu_count()                 -> Núcleos e threads
psutil.virtual_memory().total      -> RAM em bytes
platform.system()                  -> Nome do SO
```

---

### Threading

A coleta de informações é executada em thread separada para não congelar a UI:

```python
def on_collect_clicked(self):
    thread = threading.Thread(target=self.collect_hardware_info)
    thread.daemon = True
    thread.start()
```

Os updates da UI são feitos na thread principal usando `root.after()`:
```python
self.root.after(0, self.update_ui)
```

---

### Exportação

**TXT:**
- Arquivo de texto simples com formatação
- Inclui data/hora
- Separadores visuais

**PDF:**
- Requer biblioteca `reportlab`
- Tabela formatada com cores
- Cabeçalho profissional
- Alternância de cores nas linhas

---

## Dependências Explicadas

### Obrigatórias:
- **psutil**: Acesso a informações de hardware
  - CPU (núcleos, threads)
  - Memória RAM
  - Outros dados do sistema

### Opcionais:
- **reportlab**: Geração de PDFs
  - Sem isso, apenas TXT funciona
  - Instalar: `pip install reportlab`

### Padrão Python:
- **tkinter**: Interface gráfica (incluído)
- **subprocess**: Execução de comandos (incluído)
- **threading**: Multi-threading (incluído)
- **platform**: Informações de SO (incluído)
- **logging**: Logs de erros (incluído)

---

## Modificações e Extensões

### Adicionar Novo Dado

1. **Criar método em `HardwareCollector`:**
```python
def get_gpu(self) -> Optional[str]:
    """Coleta informações da GPU."""
    try:
        command = 'wmic path win32_videocontroller get name'
        # ... implementação
    except Exception as e:
        logger.error(f"Erro ao obter GPU: {str(e)}")
        return None
```

2. **Adicionar em `collect_all()`:**
```python
self.data["gpu"] = self.get_gpu() or "Não disponível"
```

3. **Adicionar campo na UI em `create_widgets()`:**
```python
info_fields = [
    # ... campos existentes
    ("gpu", "Placa de Vídeo (GPU)"),
]
```

### Mudar Tema de Cores

Em `HardwareInfoApp.__init__()`:
```python
self.bg_color = "#f0f0f0"          # Fundo
self.header_color = "#1f4788"       # Cabeçalho
self.button_color = "#28a745"       # Botões
self.button_hover = "#218838"       # Hover dos botões
```

---

## Boas Práticas Implementadas

✅ **Separação de Responsabilidades:**
- Coleta (services)
- UI (ui)
- Utilidades (utils)

✅ **Tratamento de Erros:**
- Try-except em todas as operações
- Logging de erros
- Valores padrão ("Não disponível")

✅ **Threading:**
- UI não congela durante coleta
- Operações longas em thread separada

✅ **Documentação:**
- Docstrings em todas as funções
- Comentários em trechos complexos
- Type hints em assinaturas

✅ **Código Limpo:**
- Nomes descritivos
- Funções com responsabilidade única
- Sem código duplicado

---

## Performance

- **Coleta de dados:** ~2-5 segundos (depende do hardware)
- **Startup:** ~1 segundo
- **Uso de memória:** ~50-80 MB
- **Execução standalone (.exe):** ~15-20 segundos (primeira vez)

---

## Compatibilidade

- **Python:** 3.7, 3.8, 3.9, 3.10, 3.11+
- **Windows:** 7, 8, 10, 11
- **Tkinter:** Incluído no Python (exceto Linux minimal)

---

## Debugging

### Ativar Logs Detalhados

Em `main.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Alterado de INFO para DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Testar Coleta Manualmente

```python
from services.hardware_info import HardwareCollector

collector = HardwareCollector()
data = collector.collect_all()
for key, value in data.items():
    print(f"{key}: {value}")
```

---

## Roadmap Futuro

- [ ] Suporte para Linux e macOS
- [ ] Histórico de coletas
- [ ] Gráficos de performance
- [ ] Integração com banco de dados local
- [ ] Tema escuro
- [ ] Multi-idioma

---

**Versão:** 1.0.0
**Última Atualização:** 2026
**Autor:** Sistema de Desenvolvimento

# 🖥️ Sistema de Informações de Hardware

Um aplicativo desktop completo que coleta e exibe informações de hardware do computador em uma interface gráfica intuitiva. **100% local, sem dependências de rede ou servidor externo.**

---

## 📋 Funcionalidades

✅ **Coleta Automática de Dados:**
- Número de série da máquina (BIOS)
- Fabricante do computador
- Modelo do computador
- Processador (CPU) com número de núcleos e threads
- Quantidade de memória RAM
- Endereço MAC
- Sistema Operacional

✅ **Interface Gráfica Intuitiva:**
- Design limpo e profissional
- Exibição organizada de informações
- Botão "Coletar Informações" para atualizar dados
- Feedback visual durante operações

✅ **Exportação de Dados:**
- Exportar para arquivo TXT (relatório formatado)
- Exportar para arquivo PDF (relatório profissional com tabelas)

---

## 🛠️ Requisitos

- **Python 3.7+**
- **Windows** (usa WMI e comandos específicos do Windows)
- Bibliotecas Python: `psutil`, `reportlab` (opcional para PDF)

---

## 📦 Instalação

### 1. Clonar ou Extrair o Projeto

```bash
# Navegue até o diretório do projeto
cd hardware_info_system
```

### 2. Criar um Ambiente Virtual (Recomendado)

```bash
# Windows - usando venv
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
# Instalar as bibliotecas necessárias
pip install -r requirements.txt
```

---

## 🚀 Como Executar

### Opção 1: Executar como Script Python

```bash
# Certifique-se de que o ambiente virtual está ativado
python main.py
```

### Opção 2: Executar Diretamente (Windows)

Dê um duplo clique no arquivo `main.py` ou crie um atalho para facilitar.

---

## 🔨 Gerar Executável (.exe)

### Passo 1: Instalar PyInstaller

```bash
pip install pyinstaller
```

### Passo 2: Gerar o Executável

Execute o comando abaixo no diretório raiz do projeto:

```bash
pyinstaller --onefile --windowed --icon=app_icon.ico --add-data="services:services" --add-data="ui:ui" --add-data="utils:utils" main.py
```

**Ou, se não tiver ícone:**

```bash
pyinstaller --onefile --windowed --add-data="services:services" --add-data="ui:ui" --add-data="utils:utils" main.py
```

### Passo 3: Localizar o Executável

O arquivo `.exe` será gerado em:
```
./dist/main.exe
```

### Passo 4: Distribuir (Opcional)

Copie apenas o arquivo `main.exe` da pasta `dist/` para distribuir. Ele é independente e pode ser executado em qualquer computador Windows com Python instalado... 

⚠️ **Nota:** Para criar um executável verdadeiramente portável, use a opção `--onefile`, que incorpora todas as dependências em um único arquivo.

---

## 📂 Estrutura do Projeto

```
hardware_info_system/
├── main.py                          # Arquivo principal
├── requirements.txt                 # Dependências do projeto
├── README.md                        # Este arquivo
│
├── services/
│   └── hardware_info.py            # Coleta de dados de hardware
│
├── ui/
│   └── interface.py                # Interface gráfica (Tkinter)
│
└── utils/
    └── helpers.py                  # Funções auxiliares e exportação
```

---

## 🔍 Detalhes Técnicos

### Métodos de Coleta de Dados

| Informação | Método |
|-----------|--------|
| Número de Série | WMI - `wmic bios get serialnumber` |
| Fabricante | WMI - `wmic csproduct get vendor` |
| Modelo | WMI - `wmic csproduct get name` |
| CPU | WMI - `wmic cpu get name` + psutil |
| RAM | psutil - `virtual_memory().total` |
| MAC | Windows - `getmac` |
| SO | Python - `platform` |

### Tecnologias Utilizadas

- **Tkinter**: Interface gráfica (incluído no Python)
- **psutil**: Informações de sistema e hardware
- **reportlab**: Geração de PDFs (opcional)
- **subprocess**: Execução de comandos WMI
- **threading**: Execução não-bloqueante

---

## ⚙️ Configuração e Troubleshooting

### Problema: "Permissão Negada" ao Executar

**Solução:** Execute o Command Prompt como Administrador:
```bash
# Windows - abra como Admin
python main.py
```

### Problema: "Módulo psutil não encontrado"

**Solução:** Instale as dependências novamente:
```bash
pip install -r requirements.txt
```

### Problema: Dados aparecem como "Não disponível"

**Razão:** Algumas máquinas não retornam certos dados via WMI. Isto é normal e variam conforme o hardware/SO.

### Problema: PyInstaller não encontra módulos

**Solução:** Use o comando completo com `--add-data`:
```bash
pyinstaller --onefile --windowed --add-data="services:services" --add-data="ui:ui" --add-data="utils:utils" main.py
```

---

## 📝 Exemplos de Uso

### Coletar Informações
1. Execute `python main.py` ou `main.exe`
2. Clique em **"🔄 Coletar Informações"**
3. Aguarde alguns segundos enquanto os dados são coletados
4. As informações aparecerão na tela

### Exportar como TXT
1. Após coletar os dados, clique em **"📄 Exportar TXT"**
2. Escolha o local e nome do arquivo
3. O arquivo será salvo com a data e hora da coleta

### Exportar como PDF
1. Após coletar os dados, clique em **"📊 Exportar PDF"**
2. Escolha o local e nome do arquivo
3. Um PDF formatado será gerado com todas as informações

---

## 🔒 Segurança e Privacidade

- ✅ **100% Local**: Nenhum dado é enviado pela rede
- ✅ **Sem Servidor**: Não há componente servidor
- ✅ **Sem Conexão Externa**: Não faz requisições HTTP
- ✅ **Sem Rastreamento**: Não coleta dados do usuário
- ✅ **Código Aberto**: Você pode revisar todo o código-fonte

---

## 📄 Licença

Este projeto é fornecido como está. Sinta-se livre para modificar e distribuir conforme necessário.

---

## 🤝 Contribuições

Melhorias e correções são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests com melhorias

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a seção **Troubleshooting** acima
2. Consulte o código-fonte comentado
3. Verifique se o Python e as dependências estão corretamente instalados

---

## 📚 Referências

- [Documentação Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Documentação psutil](https://psutil.readthedocs.io/)
- [Documentação PyInstaller](https://pyinstaller.readthedocs.io/)
- [WMI no Windows](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmi-start-page)

---

**Versão**: 1.0.0  
**Última Atualização**: 2026  
**Status**: ✅ Completo e Funcional

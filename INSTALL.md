# 📚 INSTRUÇÕES DETALHADAS DE INSTALAÇÃO

## Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Instalação do Python](#instalação-do-python)
3. [Instalação das Dependências](#instalação-das-dependências)
4. [Executar o Programa](#executar-o-programa)
5. [Gerar Executável (.exe)](#gerar-executável-exe)
6. [Troubleshooting](#troubleshooting)

---

## Pré-requisitos

Antes de começar, você precisa ter:
- [ ] Windows 7, 8, 10 ou 11
- [ ] Acesso à internet (para instalar dependências)
- [ ] Permissões de administrador (recomendado)

---

## Instalação do Python

### Passo 1: Baixar Python

1. Abra o navegador e acesse: https://www.python.org/downloads/
2. Clique em **"Download Python 3.11"** (ou versão mais recente)
3. Execute o instalador baixado

### Passo 2: Instalar Python

**IMPORTANTE:** Durante a instalação:

1. ✅ **MARQUE** "Add Python to PATH"
2. Clique em "Install Now"
3. Aguarde a instalação completar

![Python Installer](https://www.python.org/static/img/python-icon.png)

### Passo 3: Verificar Instalação

Abra o Command Prompt (CMD) ou PowerShell e execute:

```bash
python --version
```

Você deve ver algo como: `Python 3.11.0`

Se receber erro "Python não encontrado", reinstale marcando "Add Python to PATH".

---

## Instalação das Dependências

### Opção 1: Automática (Recomendado)

1. Navegue até a pasta do projeto
2. Abra o **Command Prompt** ou **PowerShell** nesta pasta
3. Execute:

```bash
# Windows - Batch (mais simples)
run.bat

# OU Windows - PowerShell
powershell -ExecutionPolicy Bypass -File run.ps1
```

O script irá:
- ✅ Criar ambiente virtual
- ✅ Instalar dependências
- ✅ Executar o programa

### Opção 2: Manual

#### Abrir Command Prompt ou PowerShell

1. Pressione `Win + R`
2. Digite `cmd` ou `powershell`
3. Pressione Enter

#### Navegar até o projeto

```bash
cd "C:\Caminho\Para\hardware_info_system"
```

#### Criar Ambiente Virtual

```bash
python -m venv venv
```

#### Ativar Ambiente Virtual

**Windows - CMD:**
```bash
venv\Scripts\activate
```

**Windows - PowerShell:**
```bash
venv\Scripts\Activate.ps1
```

Você saberá que está ativo quando ver `(venv)` no início da linha.

#### Instalar Dependências

```bash
pip install -r requirements.txt
```

A instalação deve levar alguns minutos.

---

## Executar o Programa

### Opção 1: Usar Script (Mais fácil)

```bash
# Windows
run.bat

# OU PowerShell
powershell -ExecutionPolicy Bypass -File run.ps1
```

### Opção 2: Manual (Terminal)

```bash
# 1. Ativar ambiente virtual (se não estiver ativo)
venv\Scripts\activate

# 2. Executar
python main.py
```

### Opção 3: Duplo clique em main.py

Clique duas vezes em `main.py` para executar diretamente.

---

## Interface da Aplicação

Quando a aplicação abrir, você verá:

```
┌─────────────────────────────────────────┐
│  📊 INFORMAÇÕES DE HARDWARE             │
│                                         │
│  [Coletar informações para começar]     │
└─────────────────────────────────────────┘
│ Número de Série: Carregando...          │
│ Fabricante: Carregando...               │
│ Modelo: Carregando...                   │
│ Processador: Carregando...              │
│ RAM: Carregando...                      │
│ Endereço MAC: Carregando...             │
│ SO: Carregando...                       │
└─────────────────────────────────────────┘
[🔄 Coletar] [📄 Exportar TXT] [📊 Exportar PDF]
```

### Como Usar:

1. **Clicar em "🔄 Coletar Informações"**
   - Aguarde alguns segundos
   - Os dados aparecerão na tela

2. **Exportar dados (Opcional)**
   - Clique em "📄 Exportar TXT" para salvar em arquivo de texto
   - Clique em "📊 Exportar PDF" para gerar relatório PDF

---

## Gerar Executável (.exe)

### Passo 1: Instalar PyInstaller

```bash
pip install pyinstaller
```

### Passo 2: Opção A - Script Automático

Na pasta do projeto:

```bash
python build_exe.py
```

O script irá gerar o executável automaticamente.

### Passo 2: Opção B - Comando Manual

```bash
pyinstaller --onefile --windowed --add-data="services:services" --add-data="ui:ui" --add-data="utils:utils" main.py
```

### Passo 3: Localizar o .exe

O arquivo estará em:
```
dist\main.exe
```

### Passo 4: Distribuir

Copie apenas o arquivo `main.exe` para qualquer pessoa usar!

---

## Troubleshooting

### Problema 1: "Python não encontrado"

**Causa:** Python não está no PATH

**Solução:**
1. Desinstale Python
2. Reinstale marcando "Add Python to PATH" ✅
3. Reinicie o computador
4. Tente novamente

---

### Problema 2: "ModuleNotFoundError: No module named 'psutil'"

**Causa:** Dependências não instaladas

**Solução:**
```bash
pip install -r requirements.txt
```

---

### Problema 3: "Permissão Negada"

**Causa:** Falta de permissões

**Solução:**
1. Abra Command Prompt como **Administrador**
2. Execute novamente

---

### Problema 4: "Não consegue coletar dados"

**Causa:** Comando WMI não funcionando

**Solução:**
1. Tente abrir CMD como Administrador
2. Se ainda não funcionar, alguns dados podem não estar disponíveis no seu hardware

---

### Problema 5: "Erro ao exportar PDF"

**Causa:** reportlab não instalado

**Solução:**
```bash
pip install reportlab
```

---

## Dúvidas Frequentes

### P: Preciso de internet para usar o programa?
**R:** Não! Internet é necessária apenas para instalar as dependências. O programa funciona 100% offline.

### P: Posso usar em Mac ou Linux?
**R:** A versão atual é apenas para Windows (usa WMI). Versões futuras podem suportar outros sistemas.

### P: Quanto espaço em disco preciso?
**R:** Aproximadamente 100-150 MB para Python + dependências. O executável standalone é ~50-70 MB.

### P: É seguro? Envia dados para a internet?
**R:** Sim, é 100% seguro. Não envia dados a lugar nenhum. Tudo é local.

### P: Posso modificar o código?
**R:** Sim! O código é aberto. Você pode personalizar conforme necessário.

---

## Próximos Passos

Após instalar com sucesso:

1. ✅ Explore a interface
2. ✅ Colete informações de hardware
3. ✅ Experimente exportar para TXT/PDF
4. ✅ (Opcional) Gere o executável para distribuir
5. ✅ Leia DEVELOPMENT.md para entender o código
6. ✅ Consulte examples.py para uso programático

---

## Suporte

Se encontrar problemas:

1. Verifique a seção "Troubleshooting"
2. Consulte README.md para documentação completa
3. Revise DEVELOPMENT.md para detalhes técnicos
4. Verifique o código-fonte (bem comentado)

---

## Checklist de Conclusão

- [ ] Python instalado e funcional
- [ ] Dependências instaladas
- [ ] Programa executa sem erros
- [ ] Consegue coletar informações
- [ ] Consegue exportar dados
- [ ] (Opcional) Gerou o .exe

**Parabéns! Você está pronto para usar o sistema! 🎉**

---

**Versão:** 1.0.0  
**Última Atualização:** 2026  
**Compatibilidade:** Windows 7/8/10/11

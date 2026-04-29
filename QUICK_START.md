# 🚀 GUIA RÁPIDO - Executar o Sistema

## Opção 1: Mais Rápida (Recomendado para primeira execução)

### Windows (Batch):
```bash
run.bat
```

### Windows (PowerShell):
```bash
powershell -ExecutionPolicy Bypass -File run.ps1
```

O script irá:
1. ✅ Criar ambiente virtual automaticamente
2. ✅ Instalar dependências
3. ✅ Executar a aplicação

---

## Opção 2: Manual (Para Desenvolvedores)

### 1. Criar ambiente virtual:
```bash
python -m venv venv
```

### 2. Ativar ambiente:

**Windows (CMD):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

### 3. Instalar dependências:
```bash
pip install -r requirements.txt
```

### 4. Executar:
```bash
python main.py
```

---

## Opção 3: Gerar Executável (.exe)

### Passo 1: Instalar PyInstaller
```bash
pip install pyinstaller
```

### Passo 2: Usar script de build (Automático)
```bash
python build_exe.py
```

### OU Passo 2: Comando Manual
```bash
pyinstaller --onefile --windowed --add-data="services:services" --add-data="ui:ui" --add-data="utils:utils" main.py
```

### Passo 3: Executável gerado em:
```
dist/main.exe  (ou dist/HardwareInfo.exe)
```

---

## Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Python não encontrado | Reinstale Python com "Add to PATH" ✓ |
| Permissão negada | Execute CMD como Administrador |
| Módulo não encontrado | Execute `pip install -r requirements.txt` |
| PyInstaller não funciona | Execute `pip install --upgrade pyinstaller` |

---

## 📋 Checklist Antes de Iniciar

- [ ] Python 3.7+ instalado
- [ ] Acesso à pasta do projeto
- [ ] Conexão com internet (apenas para instalar dependências)
- [ ] Permissões de escrita na pasta (para criar venv)

---

**Pronto? Execute `run.bat` ou `python main.py` e aproveite! 🎉**

# 🛠 Py-Doctor

**Py-Doctor** é uma ferramenta CLI para diagnosticar, limpar e manter projetos Python organizados dentro de um workspace.

---

## 📦 Funcionalidades

- Detecta projetos Python automaticamente na subpasta `python/` do seu workspace
- Diagnostica dependências a partir de `requirements.txt`
- Exibe pacotes faltando com visual interativo
- Modo de teste (nenhuma ação é executada, apenas simulada)
- Limpa arquivos temporários: `__pycache__`, `.pyc`, `.pyo`, `.log`
- Gera logs completos de tudo que foi feito em `logs/`

---

## 🚀 Como usar

1. Crie um ambiente Conda:

```bash
conda create -n pydoctor_env python=3.10 rich
conda activate pydoctor_env
```

2. Clone ou copie o projeto Py-Doctor

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.pydoctor_config` na raiz do repositório contendo o caminho do workspace e se deseja rodar em modo de teste:

```ini
workspace=/caminho/para/seu/workspace
modo_teste=true
```

5. Execute a CLI:

```bash
python -m py_doctor
```

---

## 📁 Estrutura esperada

```
/workspace/
  ├── python/
  │   ├── ProjetoA/
  │   ├── ProjetoB/
  │   └── ProjetoC/
  └── .pydoctor_config
```

Cada pasta em `python/` é considerada um projeto Python válido se contiver pelo menos um arquivo `.py` ou `requirements.txt`.

---

## 🧪 Modo de Teste

Para evitar mudanças reais, ative o modo de teste:

```ini
modo_teste=true
```

Isso impede a instalação de pacotes e remoção de arquivos, apenas exibindo a simulação.

---

## 📑 Logs

- Todos os logs são salvos automaticamente em `logs/`
- Cada execução principal cria `exec_log_YYYY-MM-DD_HH-MM-SS.txt`
- Logs individuais de diagnóstico e limpeza também são salvos

---

## 📋 Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

Instalação:

```bash
pip install -r requirements.txt
```

---

## ✨ Em breve

- Exportação de relatórios em Markdown/HTML
- Modo auditoria em lote
- Suporte a ambientes Conda por projeto

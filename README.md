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

3. Crie um arquivo `.pydoctor_config` na raiz do repositório:

```ini
workspace=/caminho/para/seu/workspace
modo_teste=true
```

4. Execute:

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
- `rich`

Instalação:

```bash
pip install rich
```

---

## ✨ Em breve

- Exportação de relatórios em Markdown/HTML
- Modo auditoria em lote
- Suporte a ambientes Conda por projeto

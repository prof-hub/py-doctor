# 🔧 Instruções para a IA

Este projeto contém um plano de ação completo a ser seguido pela IA assistente.
**Leia todas as partes a partir da seção `## 5. Plano de Ação para Finalização` e execute cada passo em ordem**, usando os arquivos `manual_parte_01.md` até `manual_parte_05.md`, disponíveis na pasta de partes.
Após executar, volte a este README, leia novamente a partir de `# Plano de Ação e Arquitetura do Py-Doctor para IA`,
e gere um relatório comparando o que foi executado com o que está descrito.
**Nesta etapa final, não modifique nada — apenas gere o relatório.**

---

# Plano de Ação e Arquitetura do Py-Doctor para IA

## 0. Instruções para a IA Assistente

**Objetivo:** Refatorar e finalizar a ferramenta Py-Doctor, tornando-a robusta, funcional e livre de dependências desnecessárias.

**Pré-requisitos:** Acesso completo ao código-fonte do projeto no repositório.

**Instrução Principal:** Siga o **Plano de Ação para Finalização** descrito na Seção 5 deste documento, passo a passo. Execute as modificações de código exatamente como especificado. Não prossiga para um passo sem completar o anterior.

---

## 1. Visão Geral

**Py-Doctor** é uma ferramenta de linha de comando (CLI) em Python, projetada para diagnosticar e manter projetos Python organizados. Seu propósito é automatizar tarefas de verificação de dependências, análise de consistência de código e limpeza de arquivos temporários. A ferramenta pode ser executada de forma interativa (com menus) ou não interativa (via argumentos de linha de comando).

## 2. Estrutura do Projeto

A arquitetura do projeto é modular e está contida dentro de um pacote Python (`py_doctor`). A estrutura de arquivos é a seguinte:

```
py-doctor/
├── .pydoctor_config      # Arquivo de configuração (criado interativamente se ausente)
├── README.md             # Documentação principal
├── requirements.txt      # Dependências do próprio Py-Doctor
├── IA_PLANO_DE_ACAO.md   # Este arquivo
├── py_doctor/
│   ├── __init__.py       # Define o pacote e seus metadados
│   ├── __main__.py       # Ponto de entrada da aplicação (CLI)
│   ├── utils.py          # Funções utilitárias (config, logs, etc.)
│   ├── checker.py        # Módulo de diagnóstico de dependências
│   ├── cleaner.py        # Módulo de limpeza de arquivos
│   └── filesystem.py     # (A SER REMOVIDO) Wrapper para operações de arquivo
└── logs/
    └── (Logs de execução são salvos aqui)
```

## 3. Componentes Principais

| Arquivo             | Responsabilidade                                                                                                                                                                                                                                                                                       |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`__main__.py`**   | **Orquestrador Central (CLI):** Ponto de entrada da aplicação. Responsável por: 1. Analisar argumentos de linha de comando (`argparse`). 2. Iniciar o menu interativo (`rich`) se nenhum argumento for passado. 3. Chamar as funções dos módulos `checker` e `cleaner` com base na escolha do usuário. |
| **`utils.py`**      | **Caixa de Ferramentas:** Módulo central de utilidades. Contém a lógica para: 1. Obter o caminho do workspace, com um fallback interativo (`obter_workspace`). 2. Criar e gerenciar o arquivo `.pydoctor_config`. 3. Centralizar a função de log (`logar`) e outras funções de apoio.                  |
| **`checker.py`**    | **O Doutor:** Contém toda a lógica de diagnóstico. Suas funções incluem: 1. Comparar `requirements.txt` com pacotes `pip` instalados. 2. Analisar o código-fonte (`ast`) para encontrar imports e verificar a consistência com `requirements.txt`. 3. Atualizar `requirements.txt` automaticamente.    |
| **`cleaner.py`**    | **O Faxineiro:** Responsável pela limpeza de arquivos. Suas funções incluem: 1. Remover pastas `__pycache__` e arquivos `.pyc`, `.pyo`. 2. Arquivar logs antigos (`arquivar_logs_antigos`).                                                                                                            |
| **`filesystem.py`** | **(Legado)** Um wrapper para funções dos módulos `os` e `shutil`. **Este módulo é redundante**, pois a biblioteca `pathlib` (já em uso) e `shutil` podem substituir suas funções de forma mais limpa e moderna.                                                                                        |

## 4. Fluxo de Execução

1.  **Inicialização:** O usuário executa `python -m py_doctor` ou `python __main__.py`.
2.  **Análise de Argumentos:** `__main__.py` verifica se foram passados argumentos (`diagnosticar`, `limpar`).
    * **Se sim (Modo Não Interativo):** Executa a função correspondente (`diagnosticar_projeto` ou `limpar_pycache`) e encerra.
    * **Se não (Modo Interativo):** Inicia a função `menu()`.
3.  **Carregamento da Configuração:** A função `obter_workspace` de `utils.py` é chamada.
    * Ela procura por `.pydoctor_config`.
    * Se não encontra ou o arquivo é inválido, entra em modo interativo e solicita ao usuário um caminho válido, salvando-o em um novo `.pydoctor_config`.
4.  **Menu Principal:** `menu()` lista os projetos encontrados no workspace.
5.  **Seleção de Ação:** O usuário escolhe um projeto, e `menu_acao()` é chamado, exibindo as opções: "Diagnosticar" ou "Limpar".
6.  **Execução da Tarefa:** A função correspondente de `checker.py` or `cleaner.py` é executada.
7.  **Registro de Log:** Todas as ações importantes são registradas em um arquivo na pasta `logs/`.

## 5. Plano de Ação para Finalização

O código está 90% completo. Para finalizar, siga estes passos em ordem.

### **Passo 1: Centralizar e Implementar as Funções Utilitárias Faltantes em `utils.py`**

O arquivo `py_doctor/utils.py` precisa conter todas as funções de suporte que são importadas por `checker.py` e `cleaner.py`. Substitua o conteúdo de `py_doctor/utils.py` pelo código abaixo, que inclui as funções `logar`, `mostrar_ultimo_log`, `esta_em_modo_teste` e `load_requirements`.

```python
# CONTEÚDO COMPLETO PARA O ARQUIVO py_doctor/utils.py

import configparser
import time
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

# --- Constantes ---
CONFIG_FILE = ".pydoctor_config"
LOG_DIR = Path("logs")
DEFAULT_CONFIG_CREATED = False

console = Console()

# --- Funções de Configuração ---

def _criar_config_padrao(workspace_path: Path):
    """Cria um arquivo .pydoctor_config com o caminho do workspace fornecido."""
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"workspace": str(workspace_path), "modo_teste": "false"}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        config.write(f)
    console.print(
        f"✅ [green]Arquivo de configuração '{CONFIG_FILE}' salvo para uso futuro.[/green]"
    )

def obter_workspace() -> Path:
    """Obtém o caminho do workspace, com fallback interativo."""
    config = configparser.ConfigParser()
    config_path = Path(CONFIG_FILE)
    global DEFAULT_CONFIG_CREATED

    if config_path.exists():
        try:
            config.read(config_path)
            workspace_str = config.get("DEFAULT", "workspace")
            workspace = Path(workspace_str).resolve()
            if workspace.is_dir():
                return workspace
        except (configparser.Error, KeyError):
            console.print(f"[yellow]⚠️  Aviso: O arquivo '{CONFIG_FILE}' está corrompido ou mal formatado.[/yellow]")

    console.print(Panel(
        f"[bold yellow]Arquivo '{CONFIG_FILE}' não encontrado ou inválido.[/bold yellow]\n\nPor favor, forneça o caminho para a sua pasta de projetos (workspace).",
        title="[cyan]Configuração Necessária[/cyan]",
        border_style="yellow",
    ))

    while True:
        path_str = Prompt.ask("[bold]📂 Digite o caminho do workspace[/bold]")
        if not path_str:
            console.print("[red]❌ O caminho não pode ser vazio. Tente novamente.[/red]")
            continue
        
        workspace = Path(path_str).expanduser().resolve()
        if workspace.is_dir():
            console.print(f"✅ [green]Workspace definido como:[/green] {workspace}")
            _criar_config_padrao(workspace)
            DEFAULT_CONFIG_CREATED = True
            return workspace
        else:
            console.print(f"[red]❌ Erro: O caminho '{workspace}' não existe ou não é um diretório.[/red]")

def esta_em_modo_teste() -> bool:
    """Verifica se o modo de teste está ativo no arquivo de configuração."""
    config = configparser.ConfigParser()
    if not Path(CONFIG_FILE).exists():
        return False
    config.read(CONFIG_FILE)
    return config.getboolean("DEFAULT", "modo_teste", fallback=False)

# --- Funções de Log ---

def garantir_logs():
    """Cria o diretório de logs se ele não existir."""
    LOG_DIR.mkdir(exist_ok=True)

def logar(conteudo: str, caminho_projeto: Path, tipo: str, nivel: str = "INFO"):
    """Salva uma string de log em um arquivo de log geral e em um log local do projeto."""
    garantir_logs()
    log_geral_path = LOG_DIR / f"pydoctor_main_{time.strftime('%Y%m%d')}.log"
    log_local_path = caminho_projeto / f".pydoctor_{tipo}.log"

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} [{nivel}] - {conteudo}"

    with log_geral_path.open("a", encoding="utf-8") as f:
        f.write(f"{log_entry}\n")

    with log_local_path.open("w", encoding="utf-8") as f:
        f.write(conteudo)

def mostrar_ultimo_log(caminho_projeto: Path, tipo: str = "diagnostico"):
    """Exibe o último log de um tipo específico salvo no diretório do projeto."""
    log_path = caminho_projeto / f".pydoctor_{tipo}.log"
    if not log_path.exists():
        console.print(f"[red]Nenhum log do tipo '{tipo}' encontrado em {caminho_projeto.name}[/red]")
        return
    with log_path.open("r", encoding="utf-8") as f:
        conteudo = f.read()
    console.print(Panel(conteudo, title=f"Último log de {tipo}"))

# --- Funções de Arquivo ---

def load_requirements(caminho_projeto: Path) -> list[str]:
    """Lê o arquivo requirements.txt e retorna uma lista de dependências."""
    req_path = caminho_projeto / "requirements.txt"
    if not req_path.exists():
        return []
    with req_path.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
```

### **Passo 2: Refatorar `checker.py` para Remover a Dependência de `filesystem`**

Modifique o arquivo `py_doctor/checker.py` para usar `pathlib` diretamente, eliminando a necessidade de `import py_doctor.filesystem as fs`.

* **Remova a linha:** `import py_doctor.filesystem as fs`.
* Nas funções `verificar_consistencia_requirements` e `atualizar_requirements`, **substitua** `codigo = fs.read_text(caminho, default="")` por `codigo = caminho.read_text(encoding="utf-8")`.
* Na função `atualizar_requirements`, **substitua** `fs.write_text(req_path, ...)` por `req_path.write_text("\n".join(novo_req) + "\n", encoding="utf-8")`.

### **Passo 3: Refatorar `cleaner.py` para Remover a Dependência de `filesystem`**

Modifique o arquivo `py_doctor/cleaner.py` de forma similar.

* **Adicione o import:** `import shutil` no topo do arquivo.
* **Remova a linha:** `import py_doctor.filesystem as fs`.
* Na função `_remover_caminho`, **substitua** a chamada `fs.remove_path(caminho)` pela seguinte lógica:
    ```python
    if caminho.is_dir():
        shutil.rmtree(caminho)
    else:
        caminho.unlink()
    ```

### **Passo 4: Deletar o Arquivo Redundante**

**Exclua** o arquivo `py_doctor/filesystem.py` do projeto. Ele não é mais necessário.

### **Passo 5: Adicionar Comando para Arquivar Logs**

A função `arquivar_logs_antigos` em `cleaner.py` nunca é chamada. Adicione um novo comando na CLI para executá-la.

* Em `__main__.py`, localize o bloco de `argparse` e **adicione um novo parser**:
    ```python
    # Adicionar junto aos outros parsers em __main__.py
    p_arquivar = sub.add_parser("arquivar-logs", help="Arquivar logs antigos")
    p_arquivar.add_argument("dias", type=int, help="Idade mínima em dias para arquivar os logs")
    ```
* No bloco `try...finally` de `__main__.py`, **adicione a chamada** para a nova funcionalidade:
    ```python
    # Adicionar no bloco de condicionais em __main__.py
    from cleaner import arquivar_logs_antigos
    ...
    elif args.comando == "arquivar-logs":
        arquivar_logs_antigos(args.dias)
    ```

## 6. Conclusão e Validação Final

Após executar todos os passos acima, o projeto Py-Doctor estará funcional, coeso e livre de dependências internas desnecessárias. O código estará pronto para ser empacotado, distribuído ou expandido com novas funcionalidades, como testes unitários (`pytest`) e geração de relatórios. Valide a execução de todos os comandos interativos e não interativos para garantir que a refatoração foi bem-sucedida.

## 7. Referências e Documentação
Apos a conclusão do projeto, é recomendado que você crie uma documentação detalhada sobre a arquitetura, a estrutura de diretórios e os passos realizados para refatorar o projeto. Isso ajudará outros desenvolvedores a entender o projeto e a colaborar de forma eficiente. A parir da completa confirmação do sucesso do projeto, você pode compartilhar a documentação com a comunidade para que possam ajudar a melhorar ainda mais o projeto. Para fins de documentação, você pode usar formatos como Markdown ou mesmo a própria documentação do Python. A partir daqui é recomendado que você faça um commit completo do projeto, incluindo as modificações realizadas. E reescreva o README.md com uma descrição completa do projeto, incluindo como ele pode ser utilizado, como ele foi refatorado e qual sua estrutura. Nao modifique nada ate aqui, pois é importante que o README seja a soma destas atualizacoes do projeto.

## 8. Testes Unitários 
Para garantir que a refatoração não tenha causado erros, é recomendado que você escreva testes unitários para cada função e módulo do projeto. Você pode usar frameworks de testes como `unittest` ou `pytest`. Os testes unitários garantirão que as modificações não tenham afetado a funcionalidade principal do projeto.

## 9. Documentação
Para documentar o projeto, você pode usar formatos como Markdown ou mesmo a própria documentação do Python. Isso ajudará outros desenvolvedores a entender o projeto e a colaborar de forma eficiente.

## 10. Contrua o readme.md
Agora é hora de escrever o README.md. Aqui está um exemplo de como você pode escrever o README.md:
```markdown

# 🛠 Py-Doctor - A Ferramenta de Diagnóstico e Manutenção de Projeto Python

## 📚 Descrição
Py-Doctor é uma ferramenta de linha de comando (CLI) em 
Python projetada para diagnosticar e manter projetos Python 
organizados. Ele automatiza tarefas de verificação de dependências, 
análise de consistência de código e limpeza de arquivos temporários. 
A ferramenta pode ser executada de forma interativa (com menus) ou 
não interativa (via argumentos de linha de comando).

Continue o README.md com uma descrição completa do projeto, 
incluindo como ele pode ser utilizado, como ele foi refatorado e 
qual sua estrutura. Nao modifique nada até aqui, pois é importante 
que o README seja a soma destas atualizações do projeto.
```

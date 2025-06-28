# Utilidades de configuracao e log para Py-Doctor

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



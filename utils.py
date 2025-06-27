"""Utilitários de configuração e registro de logs."""

import os
import datetime
import configparser
from functools import lru_cache
from glob import glob
from pathlib import Path
from rich.console import Console

try:  # pragma: no cover - optional dependency
    from rich.markdown import Markdown
except ImportError:  # pragma: no cover - optional dependency
    Markdown = None

console = Console()


LOG_DIR = Path("logs")
CONFIG_FILE = Path(".pydoctor_config")
_CONFIG_CACHE = None
# Marcado como ``True`` quando um arquivo de configuração padrão é gerado
DEFAULT_CONFIG_CREATED = False


def garantir_logs():
    """Garante que o diretório de logs existe.

    Returns:
        None
    """

    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)


def timestamp():
    """Retorna o timestamp atual formatado para nomes de arquivo.

    Returns:
        str: Timestamp no formato ``YYYY-MM-DD_HH-MM-SS``.
    """

    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def logar(texto, projeto, tipo="geral", nivel="INFO"):
    """Grava mensagens de log em ``LOG_DIR``.

    Args:
        texto (str): Mensagem a ser registrada.
        projeto (str): Identificação do projeto relacionado.
        tipo (str, optional): Prefixo do nome do arquivo de log. Defaults to
            ``"geral"``.
        nivel (str, optional): Severidade da mensagem. Defaults to ``"INFO"``.

    Returns:
        Path: Caminho completo do arquivo de log criado.
    """

    nome_log = f"{tipo}_log_{str(projeto).replace(os.sep, '_')}_{timestamp()}.txt"
    caminho = Path(LOG_DIR) / nome_log

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"[{nivel}] {texto}\n")

    print(f"📝 Log salvo em: {caminho}")
    return Path(caminho)


def esta_em_modo_teste():
    """Verifica se o modo de teste está habilitado.

    Returns:
        bool: ``True`` se a configuração indicar modo de teste.
    """

    config = carregar_configuracao()
    return config.get("modo_teste", "false").lower() == "true"


def criar_config_padrao(workspace: Path | None = None):
    """Gera um arquivo de configuração padrão.

    Args:
        workspace (Path | None): Caminho do workspace a ser usado. Se ``None``,
            :func:`Path.cwd` é utilizado.

    Returns:
        None
    """

    workspace = Path.cwd() if workspace is None else Path(workspace)
    conteudo = (
        "# Arquivo gerado automaticamente pelo Py-Doctor\n"
        "# Ajuste o caminho do workspace conforme necessário.\n"
        "[DEFAULT]\n"
        f"workspace={workspace}\n"
        "modo_teste=false\n"
    )
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(conteudo)


def carregar_configuracao():
    """Lê o arquivo ``.pydoctor_config`` com cache."""

    global _CONFIG_CACHE, DEFAULT_CONFIG_CREATED
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE

    parser = configparser.ConfigParser()
        try:
            with CONFIG_FILE.open("r", encoding="utf-8") as f:
                conteudo = f.read()

            # Detecta se o arquivo possui cabeçalho de seção
            linhas = [
                linha.strip()
                for linha in conteudo.splitlines()
                if linha.strip() and not linha.strip().startswith(("#", ";"))
            ]
            tem_header = linhas and linhas[0].startswith("[")

            if not tem_header:
                conteudo = "[DEFAULT]\n" + conteudo

            parser.read_string(conteudo)
            _CONFIG_CACHE = dict(parser["DEFAULT"]) if "DEFAULT" in parser else {}
        except Exception as e:  # pragma: no cover - safe guard for parse issues
            console.print(f"[red]Erro ao ler {CONFIG_FILE}: {e}[/]")
            _CONFIG_CACHE = {}
    else:
        _CONFIG_CACHE = {}

    return _CONFIG_CACHE


def reload_config():
    """Força a releitura do arquivo de configuração."""
    global _CONFIG_CACHE
    _CONFIG_CACHE = None
    return carregar_configuracao()


def obter_workspace():
    """Obtém o caminho configurado para o workspace.

    Returns:
        str: Caminho absoluto do diretório configurado.
    """

    config = carregar_configuracao()


def load_requirements(projeto_path):
    """Carrega as dependências de ``requirements.txt`` com cache.

    Args:
        projeto_path (str): Caminho do projeto.

    Returns:
        list[str]: Lista de dependências declaradas.
    """

    req_path = Path(projeto_path) / "requirements.txt"
    if not req_path.exists():
        return []
    mtime = req_path.stat().st_mtime
    return _load_requirements_cached(req_path, mtime)


@lru_cache(maxsize=None)
def _load_requirements_cached(req_path, _mtime):
    with open(req_path, "r", encoding="utf-8") as f:
        return [
            linha.strip()
            for linha in f
            if linha.strip() and not linha.startswith("#")
        ]


def mostrar_ultimo_log(caminho_projeto, tipo="diagnostico"):
    """Exibe o conteúdo do log mais recente do ``tipo`` para ``caminho_projeto``.

    Args:
        caminho_projeto (str): Caminho do projeto.
        tipo (str): Prefixo do log (``diagnostico`` ou ``limpeza``).

    Returns:
        None
    """

    path = Path(caminho_projeto)

    garantir_logs()
    safe_name = str(path).replace(os.sep, "_")
    padrao = str(LOG_DIR / f"{tipo}_log_{safe_name}_*.txt")
    arquivos = sorted(glob(padrao), reverse=True)
    if not arquivos:
        console.print(f"[red]Nenhum log encontrado para:[/] {path}")
        return

    ultimo = arquivos[0]
    console.rule(f"📜 Último log de {tipo}")
    with open(ultimo, "r", encoding="utf-8") as f:
        conteudo = f.read()
        if Markdown:
            console.print(Markdown(conteudo))
        else:
            console.print(
                "[yellow]⚠️ Módulo markdown_it não disponível — exibindo texto puro:"
            )
            console.print(conteudo)


__all__ = [
    "garantir_logs",
    "timestamp",
    "logar",
    "esta_em_modo_teste",
    "criar_config_padrao",
    "carregar_configuracao",
    "reload_config",
    "obter_workspace",
    "load_requirements",
    "mostrar_ultimo_log",
    "DEFAULT_CONFIG_CREATED",
    "CONFIG_FILE",
]


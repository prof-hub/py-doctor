"""Utilitários de configuração e registro de logs."""

import os
import datetime
import configparser
from functools import lru_cache
from glob import glob
from rich.console import Console

try:  # pragma: no cover - optional dependency
    from rich.markdown import Markdown
except ImportError:  # pragma: no cover - optional dependency
    Markdown = None

console = Console()


LOG_DIR = "logs"
CONFIG_FILE = ".pydoctor_config"
_CONFIG_CACHE = None


def garantir_logs():
    """Garante que o diretório de logs existe.

    Returns:
        None
    """

    os.makedirs(LOG_DIR, exist_ok=True)


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
        str: Caminho completo do arquivo de log criado.
    """

    nome_log = f"{tipo}_log_{projeto.replace('/', '_')}_{timestamp()}.txt"
    caminho = os.path.join(LOG_DIR, nome_log)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"[{nivel}] {texto}\n")

    print(f"📝 Log salvo em: {caminho}")
    return caminho


def esta_em_modo_teste():
    """Verifica se o modo de teste está habilitado.

    Returns:
        bool: ``True`` se a configuração indicar modo de teste.
    """

    config = carregar_configuracao()
    return config.get("modo_teste", "false").lower() == "true"


def carregar_configuracao():
    """Lê o arquivo ``.pydoctor_config`` com cache."""

    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE

    parser = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        try:
            parser.read(CONFIG_FILE)
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
    return os.path.expanduser(config.get("workspace", "~/workspace"))


def load_requirements(projeto_path):
    """Carrega as dependências de ``requirements.txt`` com cache.

    Args:
        projeto_path (str): Caminho do projeto.

    Returns:
        list[str]: Lista de dependências declaradas.
    """

    req_path = os.path.join(projeto_path, "requirements.txt")
    if not os.path.exists(req_path):
        return []
    mtime = os.path.getmtime(req_path)
    return _load_requirements_cached(req_path, mtime)


@lru_cache(maxsize=None)
def _load_requirements_cached(req_path, _mtime):
    with open(req_path, "r", encoding="utf-8") as f:
        return [
            linha.strip()
            for linha in f
            if linha.strip() and not linha.startswith("#")
        ]


def mostrar_ultimo_log(caminho_projeto=None, projeto_path=None, tipo="diagnostico"):
    """Exibe o conteúdo do log mais recente do ``tipo`` para ``caminho_projeto``.

    Args:
        caminho_projeto (str | None): Caminho do projeto.
        projeto_path (str | None): Alias para ``caminho_projeto``.
        tipo (str): Prefixo do log (``diagnostico`` ou ``limpeza``).

    Returns:
        None
    """

    path = caminho_projeto or projeto_path
    if not path:
        raise ValueError("caminho_projeto/projeto_path é obrigatório")

    garantir_logs()
    safe_name = path.replace(os.sep, "_")
    padrao = os.path.join(LOG_DIR, f"{tipo}_log_{safe_name}_*.txt")
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
    "carregar_configuracao",
    "reload_config",
    "obter_workspace",
    "load_requirements",
    "mostrar_ultimo_log",
]


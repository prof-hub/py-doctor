import os
import datetime
import configparser
from glob import glob
from rich.console import Console

try:
    from rich.markdown import Markdown
except ImportError:  # pragma: no cover - optional dependency
    Markdown = None

console = Console()

LOG_DIR = "logs"
CONFIG_FILE = ".pydoctor_config"


def garantir_logs():
    os.makedirs(LOG_DIR, exist_ok=True)


def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def logar(texto, projeto, tipo="geral", nivel="INFO"):
    """Grava mensagens de log em ``LOG_DIR`` com nivel de severidade."""

    garantir_logs()
    nome_log = f"{tipo}_log_{projeto.replace('/', '_')}_{timestamp()}.txt"
    caminho = os.path.join(LOG_DIR, nome_log)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"[{nivel}] {texto}\n")

    print(f"📝 Log salvo em: {caminho}")
    return caminho


def esta_em_modo_teste():
    config = carregar_configuracao()
    return config.get("modo_teste", "false").lower() == "true"


def carregar_configuracao():
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for linha in f:
                if "=" in linha:
                    chave, valor = linha.strip().split("=", 1)
                    config[chave.strip()] = valor.strip()
    return config


def obter_workspace():
    config = carregar_configuracao()
    return os.path.expanduser(config.get("workspace", "~/workspace"))


def mostrar_ultimo_log(caminho_projeto=None, projeto_path=None, tipo="diagnostico"):
    """Exibe o conteúdo do log mais recente do ``tipo`` para o projeto."""

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


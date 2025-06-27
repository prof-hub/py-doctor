"""Utilitários de configuração e registro de logs."""

import os
import datetime
import configparser


LOG_DIR = "logs"
CONFIG_FILE = ".pydoctor_config"


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

    garantir_logs()
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


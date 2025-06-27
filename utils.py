import os
import datetime
import configparser

# Cache para a configuração carregada
_CONFIG_CACHE = None

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
    """Lê o arquivo de configuração uma única vez e guarda em cache."""
    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE

    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for linha in f:
                if "=" in linha:
                    chave, valor = linha.strip().split("=", 1)
                    config[chave.strip()] = valor.strip()

    _CONFIG_CACHE = config
    return config


def reload_config():
    """Força a releitura do arquivo de configuração."""
    global _CONFIG_CACHE
    _CONFIG_CACHE = None
    return carregar_configuracao()


def obter_workspace():
    config = carregar_configuracao()
    return os.path.expanduser(config.get("workspace", "~/workspace"))

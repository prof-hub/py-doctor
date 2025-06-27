import os
import datetime
import configparser

LOG_DIR = "logs"
CONFIG_FILE = ".pydoctor_config"


def garantir_logs():
    os.makedirs(LOG_DIR, exist_ok=True)


def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def logar(texto, projeto, tipo="geral"):
    garantir_logs()
    nome_log = f"{tipo}_log_{projeto.replace('/', '_')}_{timestamp()}.txt"
    caminho = os.path.join(LOG_DIR, nome_log)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)
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

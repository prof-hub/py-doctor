import os
import datetime
import configparser

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
    parser = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = f.read()
        try:
            if data.lstrip().startswith("["):
                parser.read_string(data)
            else:
                parser.read_string("[DEFAULT]\n" + data)
        except configparser.Error as e:
            print(f"Erro ao ler {CONFIG_FILE}: {e}")
            return {}
    return dict(parser.defaults())


def obter_workspace():
    config = carregar_configuracao()
    return os.path.expanduser(config.get("workspace", "~/workspace"))

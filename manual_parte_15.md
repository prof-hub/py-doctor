    config.read(CONFIG_FILE)
    return config.getboolean("DEFAULT", "modo_teste", fallback=False)

# --- Funções de Log ---

def garantir_logs():
    """Cria o diretório de logs se ele não existir."""
    LOG_DIR.mkdir(exist_ok=True)

def logar(conteudo: str, caminho_projeto: Path, tipo: str, nivel: str = "INFO"):

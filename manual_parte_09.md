CONFIG_FILE = ".pydoctor_config"
LOG_DIR = Path("logs")
DEFAULT_CONFIG_CREATED = False

console = Console()

# --- Funções de Configuração ---

def _criar_config_padrao(workspace_path: Path):
    """Cria um arquivo .pydoctor_config com o caminho do workspace fornecido."""

    with log_path.open("r", encoding="utf-8") as f:
        conteudo = f.read()
    console.print(Panel(conteudo, title=f"Último log de {tipo}"))

# --- Funções de Arquivo ---

def load_requirements(caminho_projeto: Path) -> list[str]:
    """Lê o arquivo requirements.txt e retorna uma lista de dependências."""
    req_path = caminho_projeto / "requirements.txt"
    if not req_path.exists():

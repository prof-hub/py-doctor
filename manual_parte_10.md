    config = configparser.ConfigParser()
    config["DEFAULT"] = {"workspace": str(workspace_path), "modo_teste": "false"}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        config.write(f)
    console.print(
        f"✅ [green]Arquivo de configuração '{CONFIG_FILE}' salvo para uso futuro.[/green]"
    )

def obter_workspace() -> Path:
    """Obtém o caminho do workspace, com fallback interativo."""

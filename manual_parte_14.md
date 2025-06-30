            DEFAULT_CONFIG_CREATED = True
            return workspace
        else:
            console.print(f"[red]❌ Erro: O caminho '{workspace}' não existe ou não é um diretório.[/red]")

def esta_em_modo_teste() -> bool:
    """Verifica se o modo de teste está ativo no arquivo de configuração."""
    config = configparser.ConfigParser()
    if not Path(CONFIG_FILE).exists():
        return False

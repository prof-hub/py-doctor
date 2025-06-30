    """Salva uma string de log em um arquivo de log geral e em um log local do projeto."""
    garantir_logs()
    log_geral_path = LOG_DIR / f"pydoctor_main_{time.strftime('%Y%m%d')}.log"
    log_local_path = caminho_projeto / f".pydoctor_{tipo}.log"

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} [{nivel}] - {conteudo}"

    with log_geral_path.open("a", encoding="utf-8") as f:
        f.write(f"{log_entry}\n")

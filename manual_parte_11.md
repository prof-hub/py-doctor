    config = configparser.ConfigParser()
    config_path = Path(CONFIG_FILE)
    global DEFAULT_CONFIG_CREATED

    if config_path.exists():
        try:
            config.read(config_path)
            workspace_str = config.get("DEFAULT", "workspace")
            workspace = Path(workspace_str).resolve()
            if workspace.is_dir():
